$ErrorActionPreference = 'Stop'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
Push-Location $PSScriptRoot
try {
    & $compiler /nologo /target:winexe /optimize+ /out:SilverBasketballPet.exe /reference:System.Drawing.dll /reference:System.Windows.Forms.dll /resource:sprites.png,sprites.png Pet.cs
    if ($LASTEXITCODE -ne 0) { throw 'Compilation failed' }
} finally { Pop-Location }
