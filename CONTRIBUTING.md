# Contributing to BionicCode Visual Studio Code Style

Thank you for your interest in contributing to this project! This guide will help you get started.

## Ways to Contribute

1. **Improve the .editorconfig**: Suggest better default rules or fix issues
2. **Documentation**: Improve README, guides, or examples
3. **Bug fixes**: Fix issues with package deployment or build scripts
4. **Features**: Add new functionality like multiple style profiles

## Getting Started

### Prerequisites

- .NET SDK (6.0 or later)
- NuGet CLI or `dotnet` CLI
- Git

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/visual-studio-code-style.git
   cd visual-studio-code-style
   ```

3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

### Modifying the .editorconfig

The main `.editorconfig` file is in the repository root. When making changes:

1. Follow the EditorConfig specification: https://editorconfig.org/
2. Use comments to explain non-obvious rules
3. Test your changes with real C# projects
4. Ensure rules work across Visual Studio, VS Code, and Rider

### Modifying the Package

If you change the package structure:

1. Update `BionicCode.VisualStudio.CodeStyle.nuspec` if needed
2. Update `BionicCode.VisualStudio.CodeStyle.props` if changing deployment logic
3. Update version number following semantic versioning
4. Document breaking changes in the nuspec `releaseNotes`

### Testing Your Changes

1. Build the package:
   ```bash
   ./build.sh    # Linux/Mac
   build.cmd     # Windows
   ```

2. Test with the example project:
   ```bash
   cd example/TestSolution
   # Follow instructions in example/README.md
   ```

3. Verify the `.editorconfig` is deployed correctly

### Documentation

Update documentation when:
- Adding new features
- Changing behavior
- Fixing bugs that affect usage

Files to update:
- `README.md` - Main documentation
- `QUICKSTART.md` - If changing installation/usage
- `ARCHITECTURE.md` - If changing package internals
- `example/README.md` - If changing example

## Code Style

This project uses the `.editorconfig` it distributes! After installing the package locally:
- Follow the formatting rules defined in `.editorconfig`
- Use consistent indentation (4 spaces for C#, 2 for XML/JSON)
- Keep line endings as CRLF (Windows) or let EditorConfig handle it

## Submitting Changes

1. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add rule for async method naming conventions"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request with:
   - Clear title describing the change
   - Description of what changed and why
   - Any breaking changes highlighted
   - Test results or validation steps

## Pull Request Guidelines

### PR Title Format

Use clear, descriptive titles:
- ✅ "Add support for F# file formatting rules"
- ✅ "Fix solution directory resolution for standalone projects"
- ❌ "Update files"
- ❌ "Changes"

### PR Description

Include:
- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How did you test it?
- **Breaking Changes**: Any breaking changes?

### Checklist

- [ ] Code follows the project's style guidelines
- [ ] Documentation updated if needed
- [ ] Build scripts work (`build.cmd` / `build.sh`)
- [ ] Example project tested
- [ ] Commit messages are clear
- [ ] No unnecessary files included (use `.gitignore`)

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

Update version in:
- `BionicCode.VisualStudio.CodeStyle.nuspec`
- `README.md` version history
- `example/README.md` if paths reference version numbers

## Release Process

For maintainers:

1. Update version in `.nuspec`
2. Update release notes in `.nuspec`
3. Update `README.md` version history
4. Build package: `./build.sh` or `build.cmd`
5. Test package locally
6. Tag release: `git tag v1.0.0`
7. Push tag: `git push origin v1.0.0`
8. Publish to NuGet.org:
   ```bash
   nuget push ./nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source https://api.nuget.org/v3/index.json -ApiKey YOUR_API_KEY
   ```

## Questions?

- Open an issue for questions
- Check existing issues and PRs first
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
