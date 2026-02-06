# Package Architecture

This document explains how the `BionicCode.VisualStudio.CodeStyle` NuGet package works internally.

## Overview

The package uses NuGet's `contentFiles` and MSBuild `props` integration to automatically deploy a `.editorconfig` file to the solution root when any project in the solution builds.

## Package Structure

```
BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg
├── contentFiles/
│   └── any/
│       └── any/
│           └── .editorconfig              # The actual .editorconfig file
├── build/
│   └── BionicCode.VisualStudio.CodeStyle.props    # MSBuild integration
├── buildTransitive/
│   └── BionicCode.VisualStudio.CodeStyle.props    # Transitive package support
└── README.md                              # Documentation
```

## How It Works

### 1. Package Installation

When a developer installs the package via:
```bash
dotnet add package BionicCode.VisualStudio.CodeStyle
```

NuGet adds a `PackageReference` to the project file:
```xml
<PackageReference Include="BionicCode.VisualStudio.CodeStyle" Version="1.0.0" />
```

### 2. MSBuild Integration

During NuGet restore, the package's `.props` file is automatically imported into the project. This happens because NuGet automatically imports any `.props` files from the `build/` and `buildTransitive/` directories of installed packages.

The import happens early in the build process, before most targets execute.

### 3. Build-Time Copy

The `.props` file defines a custom MSBuild target that executes before the build:

```xml
<Target Name="CopyEditorConfigToSolutionRoot" BeforeTargets="BeforeBuild">
  <!-- Copy .editorconfig from package to solution root -->
</Target>
```

This target:
1. Locates the `.editorconfig` file in the package's `contentFiles` directory
2. Determines the solution root directory using MSBuild properties
3. Copies the file to the solution root (only if it doesn't exist or is different)

### 4. EditorConfig Discovery

Once deployed, the `.editorconfig` file is automatically discovered by:
- Visual Studio (2017+)
- Visual Studio Code (with EditorConfig extension)
- JetBrains Rider
- Other EditorConfig-compatible editors

The editors apply these rules to all files in the solution that match the patterns defined in `.editorconfig`.

## Key Design Decisions

### Why contentFiles?

The `contentFiles` feature in NuGet PackageReference is designed for content that needs to be accessible during build but not included in the output. This is perfect for configuration files like `.editorconfig`.

### Why Copy Instead of Link?

Unlike some other configuration files (e.g., `.ruleset` for analyzers), `.editorconfig` files:
- Cannot be "linked" or referenced from another location
- Must physically exist at the root of the directory tree they apply to
- Are discovered by scanning upward from the current file's directory

Therefore, copying is the only viable approach.

### Why BeforeTargets="BeforeBuild"?

We copy the file before the build starts to ensure:
1. The file is in place before any analyzers or code generators run
2. It's available for any build-time code style checks
3. It doesn't interfere with the actual compilation process

### Why SkipUnchangedFiles="true"?

This prevents unnecessary file operations and preserves file timestamps. If a developer has customized the `.editorconfig`, it won't be overwritten unless the source file in the package has actually changed.

## Directory Resolution

The `.props` file uses MSBuild properties to find the solution root:

```xml
<SolutionRootDir Condition="'$(SolutionDir)' != '' And '$(SolutionDir)' != '*Undefined*'">
  $(SolutionDir)
</SolutionRootDir>
<SolutionRootDir Condition="'$(SolutionRootDir)' == ''">
  $(MSBuildProjectDirectory)\..\
</SolutionRootDir>
```

This handles two scenarios:
1. **Building from Visual Studio**: `$(SolutionDir)` is automatically set
2. **Building from command line**: Falls back to parent directory of the project

## Package Properties

### developmentDependency

```xml
<developmentDependency>true</developmentDependency>
```

This tells NuGet that this package:
- Is only needed during development
- Should not be included as a dependency when your package is consumed by others
- Won't be packed into packages that depend on your project

### buildTransitive

By including the `.props` file in both `build/` and `buildTransitive/`, the package works correctly even when:
- Project A references the package directly
- Project B references Project A
- Project B also gets the `.editorconfig` behavior transitively

## Customization

After deployment, developers can customize the `.editorconfig` file:

1. The deployed file can be freely edited
2. Changes are preserved because `SkipUnchangedFiles="true"` prevents overwriting
3. The file can be committed to version control
4. Future package updates will only overwrite if the source file changes

## Troubleshooting

### File Not Copied

Check:
- Build output for "Copying .editorconfig" messages
- Package is correctly installed in `packages.lock.json` or `obj/project.assets.json`
- MSBuild `/v:detailed` output for target execution

### Wrong Location

The file should be at:
- `$(SolutionDir)\.editorconfig` when building from Visual Studio
- `$(MSBuildProjectDirectory)\..\..editorconfig` when building standalone projects

### Multiple Projects

If multiple projects in the same solution install the package:
- Each will try to copy the file
- MSBuild's `SkipUnchangedFiles` prevents conflicts
- The last one to build wins (but they're all copying the same file)

## Version Updates

When updating the package version:

1. Update `version` in `.nuspec`
2. Rebuild the package
3. Users update via `dotnet add package` or Package Manager
4. On next build, if `.editorconfig` content changed, it will be updated
5. If users customized it, they need to manually merge changes

## Future Enhancements

Potential improvements for future versions:

- **Multiple .editorconfig profiles**: Offer different style presets
- **Configuration options**: Allow users to choose which rules to enable
- **Integration with analyzers**: Bundle with StyleCop or other analyzers
- **Custom MSBuild properties**: Let users configure deployment behavior
- **Merge tool**: Smart merging of user customizations with package updates
