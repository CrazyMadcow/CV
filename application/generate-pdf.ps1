param(
  [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir
$htmlPath = Join-Path $scriptDir 'ajou.html'

if (-not $OutputPath) {
  $OutputPath = Join-Path $projectDir 'dist\Kwangwoo_Jang_Ajou.pdf'
}

$outputFullPath = [IO.Path]::GetFullPath($OutputPath)
$outputDir = Split-Path -Parent $outputFullPath
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$chromeCandidates = @(
  'C:\Program Files\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
  (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
)
$chromePath = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chromePath) {
  throw 'Google Chrome was not found. Check the Chrome installation path.'
}

$tempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')
$profileDir = [IO.Path]::GetFullPath((Join-Path $tempRoot ("kwangwoo-ajou-pdf-" + [guid]::NewGuid().ToString('N'))))
$htmlUri = [Uri]::new($htmlPath).AbsoluteUri

try {
  $previousWriteTime = if (Test-Path -LiteralPath $outputFullPath) {
    (Get-Item -LiteralPath $outputFullPath).LastWriteTimeUtc
  } else {
    $null
  }

  & $chromePath `
    '--headless=new' `
    '--no-sandbox' `
    '--disable-gpu' `
    '--allow-file-access-from-files' `
    '--no-pdf-header-footer' `
    "--user-data-dir=$profileDir" `
    "--print-to-pdf=$outputFullPath" `
    $htmlUri

  $deadline = [DateTime]::UtcNow.AddSeconds(15)
  $isUpdated = $false
  while (-not $isUpdated -and [DateTime]::UtcNow -lt $deadline) {
    if (Test-Path -LiteralPath $outputFullPath) {
      $currentWriteTime = (Get-Item -LiteralPath $outputFullPath).LastWriteTimeUtc
      $isUpdated = ($null -eq $previousWriteTime) -or ($currentWriteTime -gt $previousWriteTime)
    }
    if ($isUpdated) { break }
    Start-Sleep -Milliseconds 250
  }

  if (-not $isUpdated) {
    throw 'The PDF file was not generated.'
  }

  Start-Sleep -Milliseconds 500

  $pdf = Get-Item -LiteralPath $outputFullPath
  Write-Host ("PDF generated: {0} ({1:N0} bytes)" -f $pdf.FullName, $pdf.Length)
}
finally {
  if (Test-Path -LiteralPath $profileDir) {
    if (-not $profileDir.StartsWith($tempRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        -not (Split-Path -Leaf $profileDir).StartsWith('kwangwoo-ajou-pdf-')) {
      throw "Unsafe temporary path: $profileDir"
    }
    Remove-Item -LiteralPath $profileDir -Recurse -Force
  }
}
