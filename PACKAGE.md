# BionicCode.VisualStudio.CodeStyle

Automatically deploy a comprehensive `.editorconfig` file to your solution root via NuGet!

## 🎯 What is this?

This NuGet package provides a **solution-wide .editorconfig** that enforces consistent C# and .NET coding standards across your entire development team. Simply install the package, build your project, and the `.editorconfig` is automatically deployed to your solution root.

## ✨ Features

- ✅ **Zero Configuration** - Works out of the box
- ✅ **Automatic Deployment** - Copies `.editorconfig` to solution root on build
- ✅ **Comprehensive Rules** - 200+ formatting and style rules included
- ✅ **Easy Updates** - Update coding standards by upgrading the package
- ✅ **Multi-Editor Support** - Works with Visual Studio, VS Code, and Rider
- ✅ **Solution-Wide** - Install once, applies to all projects

## 🚀 Quick Start

### Installation

```bash
# Via .NET CLI
dotnet add package BionicCode.VisualStudio.CodeStyle

# Via Package Manager Console
Install-Package BionicCode.VisualStudio.CodeStyle
```

### Usage

1. Install the package in any project in your solution
2. Build your project
3. The `.editorconfig` appears in your solution root
4. Done! All projects now follow the same coding standards

## 📋 What's Included

The `.editorconfig` includes:

### Core Settings
- UTF-8 encoding
- 4-space indentation (C#)
- CRLF line endings
- Trim trailing whitespace

### C# Conventions
- `var` preferences
- Expression-bodied members
- Pattern matching
- Null-checking preferences
- Modern C# features

### Formatting Rules
- Brace placement (all on new lines)
- Spacing around operators
- Indentation in switch statements
- New line preferences

### Naming Conventions
- Interfaces: `IPascalCase`
- Types: `PascalCase`
- Methods: `PascalCase`
- Private fields: `_camelCase`
- Constants: `PascalCase`

### File-Specific Rules
- XML files: 2-space indent
- JSON files: 2-space indent
- YAML files: 2-space indent
- Markdown: Keep trailing whitespace

## 🛠️ Compatibility

- **Frameworks**: .NET Framework 4.5+, .NET Core 1.0+, .NET 5+
- **Project Types**: All projects using PackageReference
- **Editors**: 
  - Visual Studio 2017+
  - Visual Studio Code (with EditorConfig extension)
  - JetBrains Rider
  - Any EditorConfig-compatible editor

## 🎨 Customization

After deployment, you can customize the `.editorconfig` for your needs:

1. Edit the file in your solution root
2. Commit it to version control
3. Your customizations are preserved (won't be overwritten)

## 📖 Documentation

- [README](https://github.com/BionicCode/visual-studio-code-style/blob/main/README.md) - Full documentation
- [Quick Start Guide](https://github.com/BionicCode/visual-studio-code-style/blob/main/QUICKSTART.md) - Get started quickly
- [Architecture](https://github.com/BionicCode/visual-studio-code-style/blob/main/ARCHITECTURE.md) - How it works internally
- [Examples](https://github.com/BionicCode/visual-studio-code-style/tree/main/example) - See it in action

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](https://github.com/BionicCode/visual-studio-code-style/blob/main/CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](https://github.com/BionicCode/visual-studio-code-style/blob/main/LICENSE) for details.

## 🔗 Links

- [GitHub Repository](https://github.com/BionicCode/visual-studio-code-style)
- [Report Issues](https://github.com/BionicCode/visual-studio-code-style/issues)
- [EditorConfig Specification](https://editorconfig.org/)

## 💡 Tips

### For Team Leads
- Install in one shared library project
- Commit the deployed `.editorconfig` to version control
- Team members get consistent formatting automatically

### For Library Authors
- This is a development dependency only
- Won't be included in your library's dependencies
- Won't affect consumers of your package

### For CI/CD
- The package works in build pipelines
- No special configuration needed
- `.editorconfig` is copied during restore + build

## 🎯 Why Use This Package?

### Before
- Manual `.editorconfig` creation and distribution
- Inconsistent formatting across projects
- Hard to update standards across multiple repositories
- New team members need manual setup

### After
- One command: `dotnet add package`
- Automatic deployment on build
- Easy updates via package manager
- Zero manual configuration

## 📊 Stats

- **200+ rules** configured
- **10+ file types** supported
- **3 major editors** compatible
- **All .NET versions** supported

---

**Made with ❤️ by BionicCode**
