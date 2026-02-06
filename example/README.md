# Example Usage

This directory contains a simple example demonstrating how the `BionicCode.VisualStudio.CodeStyle` NuGet package works.

## Testing the Package Locally

### Step 1: Build the NuGet Package

From the repository root, run:

**Windows:**
```cmd
build.cmd
```

**Linux/Mac:**
```bash
./build.sh
```

This will create the package in `./nupkg/` directory.

### Step 2: Add Local NuGet Source

```bash
# Create a local NuGet feed directory
mkdir C:\LocalNuGetFeed  # Windows
mkdir ~/LocalNuGetFeed   # Linux/Mac

# Add the package to the local source
nuget add ../nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source C:\LocalNuGetFeed  # Windows
nuget add ../nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source ~/LocalNuGetFeed   # Linux/Mac

# Add the local source to NuGet configuration (one-time setup)
dotnet nuget add source C:\LocalNuGetFeed --name LocalFeed  # Windows
dotnet nuget add source ~/LocalNuGetFeed --name LocalFeed   # Linux/Mac
```

### Step 3: Install the Package

From the TestSolution directory:

```bash
cd TestProject
dotnet add package BionicCode.VisualStudio.CodeStyle --source LocalFeed
```

Or manually edit `TestProject/TestProject.csproj` and add:

```xml
<ItemGroup>
  <PackageReference Include="BionicCode.VisualStudio.CodeStyle" Version="1.0.0">
    <PrivateAssets>all</PrivateAssets>
    <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
  </PackageReference>
</ItemGroup>
```

### Step 4: Build and Verify

```bash
dotnet build
```

After building, check if the `.editorconfig` file was created in the TestSolution root directory:

```bash
ls ../.editorconfig  # Linux/Mac
dir ..\.editorconfig  # Windows
```

You should see the `.editorconfig` file has been automatically deployed to the solution root!

### Step 5: See It In Action

Open the solution in Visual Studio, Visual Studio Code (with EditorConfig extension), or Rider. The coding standards defined in `.editorconfig` will now be active for all projects in the solution.

## What Gets Deployed

- `.editorconfig` file with comprehensive C# and .NET coding standards
- Located at: `TestSolution/.editorconfig` (solution root)
- Applies to all projects in the solution

## Cleanup

To remove the example and start fresh:

```bash
# Remove the entire example directory
rm -rf example/  # Linux/Mac
rmdir /s example  # Windows

# Or just remove the deployed .editorconfig
rm example/TestSolution/.editorconfig  # Linux/Mac
del example\TestSolution\.editorconfig  # Windows
```
