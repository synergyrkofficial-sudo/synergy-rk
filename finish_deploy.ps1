Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $root "frontend"

if (-not (Test-Path $frontendPath)) {
  throw "frontend folder not found: $frontendPath"
}

Push-Location "$frontendPath"
try {
  vercel --prod --yes
}
finally {
  Pop-Location
}

