param([string]$OutputPath)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir
$htmlPath = Join-Path $scriptDir 'kau-collaboration.html'
if (-not $OutputPath) { $OutputPath = Join-Path $projectDir 'dist\Kwangwoo_Jang_KAU_Collaboration_Plan.pdf' }
$outputFullPath = [IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Path (Split-Path -Parent $outputFullPath) -Force | Out-Null

$chromeCandidates = @(
  'C:\Program Files\Google\Chrome\Application\chrome.exe',
  'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
  (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
)
$chromePath = $chromeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $chromePath) { throw 'Google Chrome was not found.' }

$tempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')
$profileDir = [IO.Path]::GetFullPath((Join-Path $tempRoot ('kwangwoo-kau-pdf-' + [guid]::NewGuid().ToString('N'))))
$htmlUri = [Uri]::new($htmlPath).AbsoluteUri
try {
  $args = @(
    '--headless=new', '--no-sandbox', '--disable-gpu',
    '--allow-file-access-from-files', '--no-pdf-header-footer',
    "--user-data-dir=$profileDir", "--print-to-pdf=$outputFullPath", $htmlUri
  )
  $process = Start-Process -FilePath $chromePath -ArgumentList $args -WindowStyle Hidden -Wait -PassThru
  if ($process.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $outputFullPath)) {
    throw "PDF generation failed (exit code $($process.ExitCode))."
  }
  $pdf = Get-Item -LiteralPath $outputFullPath
  Write-Host ("PDF generated: {0} ({1:N0} bytes)" -f $pdf.FullName, $pdf.Length)
}
finally {
  if (Test-Path -LiteralPath $profileDir) {
    $resolvedProfile = (Resolve-Path -LiteralPath $profileDir).Path
    if (-not $resolvedProfile.StartsWith($tempRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or
        -not (Split-Path -Leaf $resolvedProfile).StartsWith('kwangwoo-kau-pdf-')) {
      throw "Unsafe temporary profile path: $resolvedProfile"
    }
    Remove-Item -LiteralPath $resolvedProfile -Recurse -Force
  }
}
