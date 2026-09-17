$ErrorActionPreference = 'Stop'
$framework = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319'
$wpf = Join-Path $framework 'WPF'
Push-Location $PSScriptRoot
try {
    & (Join-Path $framework 'csc.exe') /nologo /target:winexe /platform:anycpu /optimize+ /out:SilverBasketballPet.exe /win32manifest:app.manifest /resource:sprites.png,sprites.png "/reference:$wpf\PresentationCore.dll" "/reference:$wpf\PresentationFramework.dll" "/reference:$wpf\WindowsBase.dll" /reference:System.Xaml.dll Pet.cs
    if ($LASTEXITCODE -ne 0) { throw 'Compilation failed' }
} finally { Pop-Location }
