# Render assets/social/*.svg to 1280x640 PNGs with headless Chrome.
# usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\render_png.ps1
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$tmp = Join-Path $env:TEMP 'paukennick-render'
New-Item -ItemType Directory -Force $tmp | Out-Null
Get-ChildItem (Join-Path $root 'assets\social') -Filter *.svg | ForEach-Object {
  $html = Join-Path $tmp ($_.BaseName + '.html')
  $uri = ([System.Uri]$_.FullName).AbsoluteUri
  "<html><body style='margin:0;overflow:hidden'><img src='$uri' width='1280' height='640' style='display:block'></body></html>" |
    Set-Content -Encoding utf8 $html
  $png = Join-Path $_.DirectoryName ($_.BaseName + '.png')
  & $chrome --headless=new --disable-gpu --user-data-dir="$tmp\profile" --no-first-run --disable-extensions --hide-scrollbars --force-device-scale-factor=1 `
    --window-size=1280,640 --screenshot="$png" ([System.Uri]$html).AbsoluteUri 2>&1 | Out-Null
  Start-Sleep -Milliseconds 300
  "rendered $png"
}
