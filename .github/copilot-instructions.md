# GitHub Copilot Instructions

## Project Overview

This repository contains **BionicCode.VisualStudio.CodeStyle**, a NuGet package that automatically deploys a comprehensive `.editorconfig` file to the solution root of any .NET project. The package uses MSBuild integration to copy the configuration file during build time.

## Project Architecture

- **Package Type**: NuGet development dependency package
- **Core Technology**: MSBuild `.props` files for build-time integration
- **Content Deployment**: Uses NuGet `contentFiles` feature to package `.editorconfig`
- **Deployment Mechanism**: MSBuild target that copies `.editorconfig` to solution root before build
- **Target Platform**: .NET projects using PackageReference (all modern .NET versions)

## Key Files and Their Purpose

- **`.editorconfig`**: The main configuration file with C# and .NET coding standards
- **`BionicCode.VisualStudio.CodeStyle.nuspec`**: NuGet package specification
- **`BionicCode.VisualStudio.CodeStyle.props`**: MSBuild integration that performs the file copy
- **`build.cmd` / `build.sh`**: Scripts for building the NuGet package
- **`ARCHITECTURE.md`**: Detailed explanation of package internals
- **`README.md`**: User-facing documentation
- **`PACKAGE.md`**: Package-specific documentation
- **`CONTRIBUTING.md`**: Contribution guidelines
- **`QUICKSTART.md`**: Quick start guide for users

## Coding Standards and Conventions

### Documentation
- Use clear, concise markdown for all documentation
- Include code examples for technical concepts
- Maintain consistent formatting across all markdown files
- Use proper heading hierarchy (H1 for titles, H2 for main sections, etc.)

### XML and MSBuild Files
- Use proper XML formatting with 2-space indentation
- Always include XML declarations in `.nuspec` files
- Use descriptive property names in MSBuild files
- Add comments to explain non-obvious MSBuild logic

### .editorconfig Files
- Follow standard EditorConfig syntax
- Group related settings together with comments
- Use clear section headers to separate different file types
- Test all rules to ensure they work in Visual Studio, VS Code, and Rider

### Version Management
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `.nuspec` file
- Document changes in `releaseNotes` section
- Update README.md version history

## Building and Testing

### Building the NuGet Package

**Windows:**
```bash
build.cmd
```

**Linux/macOS:**
```bash
chmod +x build.sh
./build.sh
```

**Manual build with NuGet CLI:**
```bash
nuget pack BionicCode.VisualStudio.CodeStyle.nuspec
```

### Testing the Package

1. Build the package locally
2. Create or use an example .NET project in `example/` directory
3. Install the package from local source:
   ```bash
   dotnet add package BionicCode.VisualStudio.CodeStyle --source ./
   ```
4. Build the example project and verify:
   - `.editorconfig` is copied to solution root
   - Build output shows the copy operation
   - File content is correct
5. Test with Visual Studio, VS Code, and Rider if possible

### Verification Checklist

- [ ] Package builds without errors
- [ ] `.nuspec` version matches intended release
- [ ] All files are included in the package (inspect with NuGet Package Explorer or extract `.nupkg` as `.zip`)
- [ ] `.editorconfig` is in `contentFiles/any/any/` directory
- [ ] `.props` file is in both `build/` and `buildTransitive/` directories
- [ ] README.md is included at package root
- [ ] Package installs correctly in test project
- [ ] `.editorconfig` deploys to solution root on build
- [ ] File is not overwritten if already exists with same content

## Common Tasks

### Updating Code Style Rules

1. Edit `.editorconfig` with new or modified rules
2. Test the changes in an example project
3. Update version in `.nuspec` if releasing
4. Update documentation to reflect changes
5. Add notes to `releaseNotes` in `.nuspec`

### Modifying Deployment Logic

1. Edit `BionicCode.VisualStudio.CodeStyle.props`
2. Test with various project structures (single project, multi-project solutions)
3. Verify behavior with and without `$(SolutionDir)` defined
4. Test transitive behavior (package installed in dependency of a project)
5. Update `ARCHITECTURE.md` with any changes to the mechanism

### Adding New Documentation

1. Create markdown file with descriptive name
2. Follow existing documentation style
3. Add to package if user-facing (update `.nuspec`)
4. Cross-reference from README.md or other relevant docs
5. Use relative links for internal references

## Important Constraints

- **Never remove or modify the MSBuild `SkipUnchangedFiles="true"` attribute** - this prevents overwriting user customizations
- **Always include `.props` in both `build/` and `buildTransitive/` directories** - required for transitive package support
- **Keep the package marked as `developmentDependency`** - ensures it's not included in consumers' dependencies
- **Maintain backward compatibility** in MSBuild property resolution - support both `$(SolutionDir)` and fallback scenarios
- **Do not add runtime dependencies** - this is a build-time only package
- **Preserve file structure** - NuGet requires specific directory layouts for contentFiles

## Dependencies and External Tools

### Required Tools
- **NuGet CLI** or **.NET SDK**: For building the package
- **MSBuild** (via .NET SDK): For testing deployment

### No Runtime Dependencies
This package has no runtime dependencies and should remain that way. All functionality is build-time only.

### EditorConfig Compatibility
Test compatibility with:
- Visual Studio 2017, 2019, 2022
- Visual Studio Code with EditorConfig extension
- JetBrains Rider
- Any other EditorConfig-compatible editors

## Security Considerations

- Do not include sensitive information in `.editorconfig`
- Ensure `.props` file does not execute arbitrary code
- Validate file paths to prevent directory traversal
- Keep package signing in mind for future releases

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Start with a verb ("Update", "Add", "Fix", "Remove")
- Keep first line under 72 characters
- Add detailed explanation in body if needed
- Reference issue numbers when applicable

## Release Process

1. Update version in `BionicCode.VisualStudio.CodeStyle.nuspec`
2. Update `releaseNotes` in `.nuspec`
3. Update `README.md` version history
4. Build and test the package thoroughly
5. Create git tag with version number
6. Push to NuGet.org (manual process, not automated)
7. Create GitHub release with release notes

## Additional Context

- This package is designed to be **zero-configuration** for users
- The `.editorconfig` should be **comprehensive but not overly prescriptive**
- Users should be able to **customize the deployed file** without package interference
- The package should **work in all build scenarios** (Visual Studio, CLI, CI/CD)
- Focus on **developer experience** - installation should be a single command
- **Documentation is critical** - users need to understand how the package works
