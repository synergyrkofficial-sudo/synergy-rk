Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $root "frontend"
$publicPath = Join-Path $frontendPath "public"
$robotsPath = Join-Path $publicPath "robots.txt"
$sitemapPath = Join-Path $publicPath "sitemap.xml"

if (-not (Test-Path $frontendPath)) {
  throw "frontend folder not found: $frontendPath"
}

if (-not (Test-Path $publicPath)) {
  throw "public folder not found (required for SEO files): $publicPath"
}

if (-not (Test-Path $robotsPath)) {
  throw "robots.txt not found (required): $robotsPath"
}

if (-not (Test-Path $sitemapPath)) {
  throw "sitemap.xml not found (required): $sitemapPath"
}

Push-Location "$frontendPath"
try {
  vercel --prod --force --yes
}
finally {
  Pop-Location
}

