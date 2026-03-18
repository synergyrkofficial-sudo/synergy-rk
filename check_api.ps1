Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$url = "https://api.synergyrkofficial.com/api/stats"

try {
  $resp = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 10
  Write-Host "OK $($resp.StatusCode) $url"
  Write-Host $resp.Content
} catch {
  Write-Host "FAILED $url"
  Write-Host $_.Exception.Message
  if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
    Write-Host $_.ErrorDetails.Message
  }
  exit 1
}

