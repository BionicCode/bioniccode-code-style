# BionicCode Visual Studio Code Style

A NuGet package that automatically deploys a comprehensive `.editorconfig` file to your solution root, enforcing consistent C# and .NET coding standards across your entire development team.

## Overview

This package provides a solution-wide `.editorconfig` file that can be easily installed and updated via NuGet. The `.editorconfig` file is automatically copied to your solution root on build, ensuring that all projects in your solution adhere to the same coding standards.

## Features

- ✅ Comprehensive .NET and C# coding standards
- ✅ Automatic deployment to solution root
- ✅ Easy installation via NuGet Package Manager
- ✅ Simple updates through package version upgrades
- ✅ Supports all modern .NET projects using PackageReference
- ✅ Includes formatting rules, naming conventions, and code style preferences
- ✅ Works with Visual Studio, Visual Studio Code, and JetBrains Rider

## Installation

### Via Package Manager Console

```powershell
Install-Package BionicCode.VisualStudio.CodeStyle
```

### Via .NET CLI

```bash
dotnet add package BionicCode.VisualStudio.CodeStyle
```

### Via Visual Studio

1. Right-click on your project in Solution Explorer
2. Select "Manage NuGet Packages..."
3. Search for "BionicCode.VisualStudio.CodeStyle"
4. Click "Install"

## How It Works

When you install this package into any project in your solution:

1. The package includes a `.editorconfig` file in its `contentFiles` directory
2. An MSBuild `.props` file is automatically imported into your project
3. On the first build after installation, the `.editorconfig` is copied to your solution root
4. The `.editorconfig` file is automatically detected by Visual Studio, VS Code (with EditorConfig extension), and other compatible editors

## Usage

### First-Time Setup

1. Install the package in **any one project** in your solution (preferably a startup project or main library)
2. Build the project
3. The `.editorconfig` will be automatically copied to your solution root
4. All projects in your solution will now use these coding standards

### Updating the Code Style

To update to a newer version of the coding standards:

1. Update the NuGet package to the latest version
2. Delete the existing `.editorconfig` file from your solution root (or let it be overwritten)
3. Build the project
4. The new `.editorconfig` will be deployed

### Customization

If you need to customize the `.editorconfig` for your specific needs:

1. After the initial deployment, the `.editorconfig` file will be in your solution root
2. Edit it directly to match your team's preferences
3. Commit the customized `.editorconfig` to your version control
4. **Note**: The package will not overwrite the file if it already exists and hasn't changed

## What's Included

The `.editorconfig` file includes comprehensive settings for:

- **Core EditorConfig Options**: Character encoding, indentation, line endings
- **C# Formatting Rules**: Brace placement, spacing, indentation preferences
- **Code Style Preferences**: `var` usage, expression-bodied members, pattern matching
- **Naming Conventions**: PascalCase for types, camelCase with underscore for private fields, etc.
- **Language Features**: Modern C# features like null-coalescing, null-propagation, object initializers
- **File-Type Specific Rules**: Different indentation for XML, JSON, YAML files

## Editor Support

### Visual Studio

Visual Studio (2017 and later) natively supports `.editorconfig` files. No additional setup required.

### Visual Studio Code

Install the [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) extension:

```bash
code --install-extension EditorConfig.EditorConfig
```

### JetBrains Rider

Rider has built-in support for `.editorconfig` files. No additional setup required.

## Package Details

- **Development Dependency**: This package is marked as a development dependency and will not be included in your application's runtime dependencies
- **Transitive Support**: The package uses `buildTransitive` to ensure it works correctly with transitive package references
- **Multi-Targeting**: Compatible with all .NET project types using PackageReference

## Building the Package

To build the NuGet package from source:

```bash
nuget pack BionicCode.VisualStudio.CodeStyle.nuspec
```

Or if you have the .NET SDK installed:

```bash
dotnet pack
```

## Contributing

Contributions are welcome! If you have suggestions for improving the default code style settings, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Version History

### 1.0.0
- Initial release
- Comprehensive .editorconfig with .NET and C# coding standards
- Automatic deployment to solution root on build
- Support for all modern .NET projects using PackageReference