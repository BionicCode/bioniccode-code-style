#!/usr/bin/env python3
"""
Validator for .editorconfig using a pattern-based JSON schema plus analyzer ID checks.
Produces GitHub Actions annotations (::error / ::warning) with line numbers.

Usage:
  python validate_editorconfig.py --schema .github/editorconfig-schema.json --file BionicCode.CodeStyle/.../.editorconfig \
    --known-rules-urls "<url1> <url2>" --fail-on-unknown-analysers false
"""

import argparse
import json
import re
import sys
import urllib.request
from jsonschema import Draft7Validator

def load_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_lines(path):
    with open(path, "r", encoding='utf-8', errors='replace') as f:
        return [ln.rstrip("\n") for ln in f.readlines()]

def parse_editorconfig_lines(lines):
    """
    Returns list of (lineno, section, key, value) tuples. section may be None for top-level.
    Non key=value lines (comments / blank) are skipped.
    Unrecognized lines cause a parse error entry.
    """
    section = None
    parsed = []
    parse_errors = []
    section_re = re.compile(r'^\s*\[(.+?)\]\s*$')
    comment_re = re.compile(r'^\s*[#;]')
    keyval_re = re.compile(r'^\s*([^=]+?)\s*=\s*(.*?)\s*$')

    for idx, raw in enumerate(lines, start=1):
        s = raw.strip()
        if s == "" or comment_re.match(s):
            continue
        msec = section_re.match(raw)
        if msec:
            section = msec.group(1).strip()
            continue
        m = keyval_re.match(raw)
        if not m:
            parse_errors.append((idx, raw))
            continue
        key = m.group(1).strip()
        val = m.group(2).strip()
        parsed.append((idx, section, key, val))
    return parsed, parse_errors

def load_known_analyzer_ids(urls):
    ids = set()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                if resp.status != 200:
                    continue
                txt = resp.read().decode('utf-8', errors='ignore')
                found = re.findall(r'\b[A-Z]{1,4}\d{2,5}\b', txt)
                ids.update(found)
        except Exception:
            continue
    return ids

def match_schema_patterns(schema, key):
    """
    Find an applicable patternProperty in the loaded JSON schema.
    Returns the schema fragment (dict) or None.
    """
    pps = schema.get("patternProperties", {})
    for patt, frag in pps.items():
        try:
            if re.match(patt, key):
                return frag
        except re.error:
            continue
    return None

def validate_value_against_fragment(value, frag):
    """
    Basic validation for the small fragment types we use in schema:
    - $ref to definitions/severity/bool/value_with_severity
    - type: string + enum/pattern
    - if frag is {"$ref":"#/definitions/any"} accept
    """
    # direct $ref
    if isinstance(frag, dict) and "$ref" in frag:
        ref = frag["$ref"]
        if ref.endswith("/severity") or ref.endswith("#/definitions/severity"):
            if value.lower() in {"none", "silent", "suggestion", "warning", "error", "default"}:
                return True, None
            return False, f"invalid severity '{value}'"
        if ref.endswith("/value_with_severity") or ref.endswith("#/definitions/value_with_severity"):
            # form "value" or "value:severity"
            if re.match(r"^[^:]+(:((none|silent|suggestion|warning|error|default)))?$", value, re.IGNORECASE):
                return True, None
            return False, f"value must be optionally suffixed with :severity where severity in [none,silent,suggestion,warning,error,default]"
        if ref.endswith("/bool"):
            if value.lower() in {"true", "false"}:
                return True, None
            return False, f"boolean expected (true/false), got '{value}'"
        if ref.endswith("/any"):
            return True, None

    # direct dict checks (type/pattern/enum)
    if isinstance(frag, dict):
        typ = frag.get("type")
        if typ == "string" or typ is None:
            enum = frag.get("enum")
            if enum:
                if value in enum:
                    return True, None
                return False, f"value must be one of {enum}, got '{value}'"
            pat = frag.get("pattern")
            if pat:
                if re.match(pat, value):
                    return True, None
                return False, f"value does not match pattern /{pat}/"
            # fallback accept
            return True, None

    return True, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--known-rules-urls", default="", help="space-separated urls")
    ap.add_argument("--fail-on-unknown-analysers", default="false")
    args = ap.parse_args()

    schema = load_schema(args.schema)
    lines = read_lines(args.file)
    parsed, parse_errors = parse_editorconfig_lines(lines)

    # Emit parse errors
    failed = False
    for ln, raw in parse_errors:
        print(f"::error file={args.file},line={ln},title=.editorconfig parse error::Unrecognized line: {raw}")
        failed = True
    if failed:
        sys.exit(1)

    # Validate each key
    known_analyzers = set()
    if args.known_rules_urls:
        known_analyzers = load_known_analyzer_ids(args.known_rules_urls.split())

    used_analyzers = set()
    warnings = []
    errors = []

    for (ln, section, key, val) in parsed:
        # If key contains section qualifiers (not in this schema), validate full key
        fullkey = key
        frag = match_schema_patterns(schema, fullkey)
        if frag is None:
            # Not matched by schema patternProperties; fallback: if key starts with dotnet_ allow but warn
            if fullkey.startswith("dotnet_") or fullkey.startswith("csharp_") or fullkey.startswith("csharp."):
                warnings.append((ln, f"Unrecognized dotnet/csharp key '{fullkey}'. Not in schema - consider adding it."))
                continue
            else:
                # Accept unknown non-dotnet keys (they can be other tools/editor settings)
                continue

        # Special case analyzer ID capture
        mdiag = re.match(r"^dotnet_diagnostic\.([A-Za-z0-9_]+)\.severity$", fullkey, re.IGNORECASE)
        if mdiag:
            rule = mdiag.group(1).upper()
            used_analyzers.add(rule)

        ok, msg = validate_value_against_fragment(val, frag)
        if not ok:
            errors.append((ln, f"Invalid value for '{fullkey}': {msg}"))
            continue

    # Unknown analyzer ID warnings
    if known_analyzers:
        for rule in sorted(used_analyzers):
            if rule not in known_analyzers:
                # find line
                pattern = f"dotnet_diagnostic.{rule}.severity"
                lineno = None
                for i, l in enumerate(lines, start=1):
                    if pattern.lower() in l.lower():
                        lineno = i
                        break
                warnings.append((lineno or 1, f"Referenced analyzer '{rule}' not found in upstream lists; verify rule ID."))

    # Emit warnings and errors
    for ln, msg in warnings:
        if ln:
            print(f"::warning file={args.file},line={ln},title=.editorconfig warning::{msg}")
        else:
            print(f"::warning file={args.file},title=.editorconfig warning::{msg}")

    for ln, msg in errors:
        if ln:
            print(f"::error file={args.file},line={ln},title=.editorconfig error::{msg}")
        else:
            print(f"::error file={args.file},title=.editorconfig error::{msg}")

    if errors:
        sys.exit(1)

    if args.fail_on_unknown_analysers.lower() in ("1","true","yes") and warnings:
        # escalate warnings to failure if requested (e.g. unknown analyzer IDs)
        sys.exit(1)

    print("Validation completed: no fatal schema violations.")
    sys.exit(0)

if __name__ == "__main__":
    main()
