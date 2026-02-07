#!/usr/bin/env python3
"""
Validator for .editorconfig using a pattern-based JSON schema plus analyzer ID checks.
Produces GitHub Actions annotations (::error / ::warning) with line numbers.

Usage:
  python validate_editorconfig.py --schema .github/editorconfig-schema.json \
    --file BionicCode.CodeStyle/BionicCode.CodeStyle/.editorconfig \
    --known-rules-urls "URL1 URL2" \
    --fail-on-unknown-analysers false
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from typing import Dict, List, Tuple, Set, Optional


class EditorconfigValidator:
    """Validates .editorconfig files against a JSON schema and checks analyzer IDs."""

    def __init__(self, schema_path: str, editorconfig_path: str, 
                 known_rules_urls: List[str], fail_on_unknown: bool):
        self.schema_path = schema_path
        self.editorconfig_path = editorconfig_path
        self.known_rules_urls = known_rules_urls
        self.fail_on_unknown = fail_on_unknown
        
        self.schema: Dict = {}
        self.lines: List[str] = []
        self.parse_errors: List[Tuple[int, str]] = []
        self.errors: List[Tuple[int, str]] = []
        self.warnings: List[Tuple[int, str]] = []
        self.used_rules: Set[str] = set()
        self.known_rules: Set[str] = set()
    
    def load_schema(self) -> None:
        """Load the JSON schema from file."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        except FileNotFoundError:
            print(f"::error file={self.schema_path}::Schema file not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"::error file={self.schema_path}::Invalid JSON schema: {e}")
            sys.exit(1)
    
    def load_editorconfig(self) -> None:
        """Load the .editorconfig file."""
        try:
            with open(self.editorconfig_path, 'r', encoding='utf-8', errors='replace') as f:
                raw_lines = f.readlines()
            self.lines = [ln.rstrip('\n') for ln in raw_lines]
        except FileNotFoundError:
            print(f"::error file={self.editorconfig_path}::File not found")
            sys.exit(1)
    
    def parse_and_validate(self) -> None:
        """Parse the .editorconfig file and validate against schema."""
        section_re = re.compile(r'^\s*\[(.+?)\]\s*$')
        comment_re = re.compile(r'^\s*[#;]')
        keyval_re = re.compile(r'^\s*([^=]+?)\s*=\s*(.*?)\s*$')
        
        # Track current section
        current_section = None
        
        for idx, raw in enumerate(self.lines, start=1):
            stripped = raw.strip()
            
            # Skip empty lines and comments
            if not stripped or comment_re.match(stripped):
                continue
            
            # Check for section headers
            msec = section_re.match(raw)
            if msec:
                current_section = msec.group(1).strip()
                continue
            
            # Parse key=value pairs
            m = keyval_re.match(raw)
            if not m:
                self.parse_errors.append((idx, f"Unrecognized line format: {raw.strip()!r}"))
                continue
            
            key = m.group(1).strip()
            val = m.group(2).strip()
            
            # Validate the key-value pair against schema
            self.validate_key_value(key, val, idx)
    
    def validate_key_value(self, key: str, val: str, line_num: int) -> None:
        """Validate a single key-value pair against the schema."""
        # Special handling for analyzer severity keys
        diag_sev_re = re.compile(r'^dotnet_diagnostic\.([A-Za-z0-9_]+)\.severity$', re.IGNORECASE)
        md = diag_sev_re.match(key)
        
        if md:
            rule_id = md.group(1).upper()
            self.used_rules.add(rule_id)
            
            # Check if value is a valid severity
            severity_def = self.schema.get('definitions', {}).get('severity', {})
            allowed_severities = severity_def.get('enum', [])
            
            if allowed_severities and val.lower() not in [s.lower() for s in allowed_severities]:
                self.errors.append((
                    line_num,
                    f"Invalid severity '{val}' for '{key}'. Allowed: {', '.join(sorted(allowed_severities))}"
                ))
        else:
            # Check for malformed analyzer keys (but exclude naming rules which are valid)
            naming_rule_re = re.compile(r'^dotnet_naming_rule\.[A-Za-z0-9_]+\.severity$', re.IGNORECASE)
            if 'dotnet' in key.lower() and 'severity' in key.lower() and not naming_rule_re.match(key):
                self.warnings.append((
                    line_num,
                    f"Possibly malformed analyzer key: '{key}' (expected dotnet_diagnostic.<RULEID>.severity)"
                ))
        
        # Validate against pattern properties in schema
        self.validate_against_patterns(key, val, line_num)
    
    def validate_against_patterns(self, key: str, val: str, line_num: int) -> None:
        """Validate key-value pair against schema pattern properties."""
        pattern_props = self.schema.get('patternProperties', {})
        matched = False
        
        for pattern_str, pattern_schema in pattern_props.items():
            try:
                pattern = re.compile(pattern_str)
                if pattern.match(key):
                    matched = True
                    # Validate value against pattern schema
                    if not self.validate_value_against_schema(val, pattern_schema):
                        # Get more specific error message
                        error_msg = self.get_validation_error_message(key, val, pattern_schema)
                        self.errors.append((line_num, error_msg))
                    break
            except re.error:
                # Invalid regex pattern in schema - should not happen with valid schema
                continue
        
        if not matched:
            # Key doesn't match any pattern - this might be OK if there's a catch-all pattern
            pass
    
    def validate_value_against_schema(self, val: str, schema: Dict) -> bool:
        """Check if a value matches a schema definition."""
        if '$ref' in schema:
            # Resolve reference
            ref_path = schema['$ref']
            if ref_path.startswith('#/definitions/'):
                def_name = ref_path.split('/')[-1]
                schema = self.schema.get('definitions', {}).get(def_name, {})
        
        # Check enum
        if 'enum' in schema:
            return val in schema['enum']
        
        # Check pattern
        if 'pattern' in schema:
            try:
                pattern = re.compile(schema['pattern'])
                return bool(pattern.match(val))
            except re.error:
                return True  # Invalid pattern in schema, don't fail validation
        
        # If no specific validation rules, accept any string
        if schema.get('type') == 'string':
            return True
        
        return True
    
    def get_validation_error_message(self, key: str, val: str, schema: Dict) -> str:
        """Generate a descriptive error message for validation failures."""
        if '$ref' in schema:
            ref_path = schema['$ref']
            if ref_path.startswith('#/definitions/'):
                def_name = ref_path.split('/')[-1]
                schema = self.schema.get('definitions', {}).get(def_name, {})
        
        if 'enum' in schema:
            allowed = ', '.join(repr(v) for v in schema['enum'])
            return f"Invalid value '{val}' for key '{key}'. Allowed values: {allowed}"
        
        if 'pattern' in schema:
            return f"Value '{val}' for key '{key}' does not match expected pattern: {schema['pattern']}"
        
        return f"Invalid value '{val}' for key '{key}'"
    
    def fetch_known_analyzer_ids(self) -> None:
        """Fetch known analyzer IDs from upstream sources."""
        for url in self.known_rules_urls:
            if not url.strip():
                continue
            
            try:
                with urllib.request.urlopen(url, timeout=10) as resp:
                    if resp.status != 200:
                        continue
                    txt = resp.read().decode('utf-8', errors='ignore')
                    # Find tokens that look like analyzer IDs: CA1000, CS0168, IDE0090, etc.
                    found = set(re.findall(r'\b[A-Z]{1,4}\d{2,5}\b', txt))
                    if found:
                        self.known_rules.update(found)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
                # Best-effort, continue on failure
                continue
            except Exception:
                # Catch any other unexpected errors
                continue
    
    def check_analyzer_ids(self) -> None:
        """Check if used analyzer IDs are in the known list."""
        if not self.known_rules:
            print("::notice ::Could not fetch authoritative analyzer ID list; existence checks skipped. This is non-fatal.")
            return
        
        for rule in sorted(self.used_rules):
            if rule not in self.known_rules:
                # Find the line number for this rule
                line_num = self.find_line_for_text(f"dotnet_diagnostic.{rule}.severity")
                if line_num:
                    self.warnings.append((
                        line_num,
                        f"Referenced analyzer rule '{rule}' not found in fetched upstream lists; "
                        f"verify the rule ID is correct."
                    ))
    
    def find_line_for_text(self, text: str) -> Optional[int]:
        """Find the line number containing the given text (case-insensitive)."""
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        for i, line in enumerate(self.lines, start=1):
            if pattern.search(line):
                return i
        return None
    
    def emit_annotations(self) -> None:
        """Emit GitHub Actions annotations for errors and warnings."""
        fname = self.editorconfig_path
        
        # Emit parse errors
        for line_num, msg in self.parse_errors:
            print(f"::error file={fname},line={line_num},title=.editorconfig parse error::{msg}")
        
        # Emit validation errors
        for line_num, msg in self.errors:
            print(f"::error file={fname},line={line_num},title=.editorconfig error::{msg}")
        
        # Emit warnings
        for line_num, msg in self.warnings:
            print(f"::warning file={fname},line={line_num},title=.editorconfig warning::{msg}")
    
    def get_exit_code(self) -> int:
        """Determine the appropriate exit code based on validation results."""
        # Always fail on parse errors or schema validation errors
        if self.parse_errors or self.errors:
            return 1
        
        # Fail on warnings if configured to do so
        if self.fail_on_unknown and self.warnings:
            return 1
        
        return 0
    
    def run(self) -> int:
        """Run the complete validation process."""
        self.load_schema()
        self.load_editorconfig()
        self.parse_and_validate()
        
        # Only fetch known analyzer IDs if we found any rules to check
        if self.used_rules:
            self.fetch_known_analyzer_ids()
            self.check_analyzer_ids()
        
        self.emit_annotations()
        
        exit_code = self.get_exit_code()
        
        if exit_code == 0:
            print("Validator completed: no fatal issues found.")
        else:
            print("Validator completed with errors.")
        
        return exit_code


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate .editorconfig file against JSON schema and check analyzer IDs'
    )
    parser.add_argument('--schema', required=True, help='Path to JSON schema file')
    parser.add_argument('--file', required=True, help='Path to .editorconfig file')
    parser.add_argument('--known-rules-urls', default='', 
                        help='Space-separated URLs to fetch known analyzer IDs')
    parser.add_argument('--fail-on-unknown-analysers', default='false',
                        help='Fail validation if unknown analyzer IDs are found (true/false)')
    
    args = parser.parse_args()
    
    # Parse URLs
    urls = [u.strip() for u in args.known_rules_urls.split() if u.strip()]
    
    # Parse fail flag
    fail_on_unknown = args.fail_on_unknown_analysers.lower() in ('true', '1', 'yes')
    
    # Create and run validator
    validator = EditorconfigValidator(
        schema_path=args.schema,
        editorconfig_path=args.file,
        known_rules_urls=urls,
        fail_on_unknown=fail_on_unknown
    )
    
    exit_code = validator.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
