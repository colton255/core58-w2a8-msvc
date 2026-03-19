@echo off
setlocal

set "VCVARS="
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

if exist "%VSWHERE%" (
    for /f "usebackq delims=" %%I in (`"%VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
        if exist "%%I\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%%I\VC\Auxiliary\Build\vcvars64.bat"
    )
)

if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\17\Community\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\17\Community\VC\Auxiliary\Build\vcvars64.bat"
if not defined VCVARS if exist "%ProgramFiles%\Microsoft Visual Studio\17\BuildTools\VC\Auxiliary\Build\vcvars64.bat" set "VCVARS=%ProgramFiles%\Microsoft Visual Studio\17\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if not defined VCVARS (
    echo Unable to locate vcvars64.bat. Install Visual Studio Build Tools with C++ support.
    exit /b 1
)

call "%VCVARS%"
if errorlevel 1 exit /b %errorlevel%

where nvcc >nul 2>&1
if errorlevel 1 (
    echo nvcc was not found on PATH. Install the CUDA toolkit and reopen the shell.
    exit /b 1
)

pushd "%~dp0"

:: Keep the Windows build as close as possible to Microsoft's upstream kernel flags.
:: We still emit a Windows DLL and keep a multi-arch fatbin for consumer GPUs.
nvcc -std=c++17 -Xcudafe --diag_suppress=177 -lineinfo -O3 -allow-unsupported-compiler -shared -o libbitnet.dll bitnet_kernels.cu -gencode=arch=compute_80,code=sm_80 -gencode=arch=compute_86,code=sm_86 -gencode=arch=compute_89,code=sm_89 -gencode=arch=compute_90,code=sm_90 -Xcompiler "/wd4819"
set "BUILD_RC=%errorlevel%"
popd

if not "%BUILD_RC%"=="0" exit /b %BUILD_RC%

echo Compilation Complete!
endlocal
