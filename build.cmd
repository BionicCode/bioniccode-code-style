@echo off
REM Build script for creating the NuGet package

echo Building BionicCode.VisualStudio.CodeStyle NuGet package...
echo.

REM Check if nuget.exe is available
where nuget >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: nuget.exe not found in PATH
    echo Please download nuget.exe from https://www.nuget.org/downloads
    echo and add it to your PATH or place it in this directory.
    exit /b 1
)

REM Pack the NuGet package
nuget pack BionicCode.VisualStudio.CodeStyle.nuspec -OutputDirectory .\nupkg

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: NuGet package created successfully!
    echo Package location: .\nupkg\
    echo.
    echo To install locally, use:
    echo   nuget add .\nupkg\BionicCode.VisualStudio.CodeStyle.1.0.0.nupkg -Source C:\LocalNuGetFeed
) else (
    echo.
    echo ERROR: Failed to create NuGet package
    exit /b 1
)
