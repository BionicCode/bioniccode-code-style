#!/bin/bash
# Build script for creating the NuGet package

echo "Building BionicCode.VisualStudio.CodeStyle NuGet package..."
echo ""

# Check if nuget or dotnet is available
if command -v nuget &> /dev/null; then
    echo "Using nuget to pack..."
    nuget pack BionicCode.VisualStudio.CodeStyle.nuspec -OutputDirectory ./nupkg
    exit_code=$?
elif command -v dotnet &> /dev/null; then
    echo "Using dotnet to pack..."
    # Note: dotnet pack works best with .csproj, but we can use nuget spec
    dotnet pack -p:NuspecFile=BionicCode.VisualStudio.CodeStyle.nuspec -o ./nupkg 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "dotnet pack with nuspec not supported, trying nuget..."
        if command -v mono &> /dev/null && [ -f nuget.exe ]; then
            mono nuget.exe pack BionicCode.VisualStudio.CodeStyle.nuspec -OutputDirectory ./nupkg
            exit_code=$?
        else
            echo "ERROR: Please install nuget or use Windows to build this package"
            echo "You can download nuget.exe from https://www.nuget.org/downloads"
            exit 1
        fi
    fi
    exit_code=$?
else
    echo "ERROR: Neither nuget nor dotnet found in PATH"
    echo "Please install .NET SDK or nuget.exe"
    exit 1
fi

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "SUCCESS: NuGet package created successfully!"
    echo "Package location: ./nupkg/"
    echo ""
    echo "To install locally, use:"
    echo "  nuget add ./nupkg/BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source ~/LocalNuGetFeed"
else
    echo ""
    echo "ERROR: Failed to create NuGet package"
    exit 1
fi
