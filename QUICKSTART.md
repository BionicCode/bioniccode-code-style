# Quick Start Guide

## For Package Consumers

### Installing the Package

1. **Via Package Manager Console (Visual Studio)**
   ```powershell
   Install-Package BionicCode.VisualStudio.CodeStyle
   ```

2. **Via .NET CLI**
   ```bash
   dotnet add package BionicCode.VisualStudio.CodeStyle
   ```

3. **Via PackageReference in .csproj**
   ```xml
   <ItemGroup>
     <PackageReference Include="BionicCode.VisualStudio.CodeStyle" Version="1.0.0">
       <PrivateAssets>all</PrivateAssets>
       <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
     </PackageReference>
   </ItemGroup>
   ```

### After Installation

1. Build your project
2. Check your solution root - you should see a new `.editorconfig` file
3. Open any C# file - the coding standards are now active

## For Package Developers/Contributors

### Building the Package

#### On Windows
```cmd
build.cmd
```

#### On Linux/Mac
```bash
./build.sh
```

The package will be created in the `./nupkg/` directory.

### Testing Locally

1. **Create a local NuGet source**
   ```bash
   # Create a directory for your local feed
   mkdir C:\LocalNuGetFeed  # Windows
   mkdir ~/LocalNuGetFeed   # Linux/Mac
   ```

2. **Add the package to your local source**
   ```bash
   # Windows
   nuget add .\nupkg\BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source C:\LocalNuGetFeed
   
   # Linux/Mac
   nuget add ./nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source ~/LocalNuGetFeed
   ```

3. **Configure NuGet to use your local source**
   ```bash
   # Add local source (do this once)
   dotnet nuget add source C:\LocalNuGetFeed --name Local  # Windows
   dotnet nuget add source ~/LocalNuGetFeed --name Local   # Linux/Mac
   ```

4. **Create a test solution/project**
   ```bash
   mkdir TestSolution
   cd TestSolution
   dotnet new sln -n TestSolution
   dotnet new console -n TestProject
   dotnet sln add TestProject/TestProject.csproj
   ```

5. **Install the package from your local source**
   ```bash
   cd TestProject
   dotnet add package BionicCode.VisualStudio.CodeStyle --source Local
   ```

6. **Build and verify**
   ```bash
   dotnet build
   # Check if .editorconfig was created in TestSolution directory
   ls ../.editorconfig  # Linux/Mac
   dir ..\.editorconfig  # Windows
   ```

### Updating the Package

1. Update the version in `BionicCode.VisualStudio.CodeStyle.nuspec`
2. Make your changes to `.editorconfig` or other files
3. Run the build script
4. Test with a new version number

### Publishing the Package

To publish to NuGet.org:

```bash
nuget push ./nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source https://api.nuget.org/v3/index.json -ApiKey YOUR_API_KEY
```

Or using dotnet:

```bash
dotnet nuget push ./nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg --api-key YOUR_API_KEY --source https://api.nuget.org/v3/index.json
```

## Troubleshooting

### The .editorconfig is not being copied

1. Clean and rebuild your solution
2. Check the build output for messages about copying .editorconfig
3. Verify the package is installed correctly: check packages.lock.json or obj/project.assets.json

### I want to customize the .editorconfig

After the first deployment:
1. Edit the `.editorconfig` in your solution root
2. Commit it to version control
3. The package will not overwrite it if it's unchanged

### Multiple projects installing the package

It's recommended to install the package in only one project per solution (preferably your main/startup project). The .editorconfig will be copied to the solution root and apply to all projects.

## Support

For issues, questions, or contributions, please visit:
https://github.com/BionicCode/visual-studio-code-style
