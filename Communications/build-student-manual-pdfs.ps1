[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'Student Manual PDFs'),
    [string]$BaseUrl = 'http://127.0.0.1:8766/Student/Labs/Web'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$edgeCandidates = @(
    (Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'),
    (Join-Path $env:ProgramFiles 'Microsoft\Edge\Application\msedge.exe')
)
$edgePath = $edgeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edgePath) {
    throw 'Microsoft Edge is required to generate the student manual PDFs.'
}

$manuals = @(
    @{ Source = 'index.html'; Output = '00 - Course Overview.pdf' },
    @{ Source = '01-connect.html'; Output = '01 - Connect to GitHub Data.pdf' },
    @{ Source = '02-transform-model.html'; Output = '02 - Transform and Model.pdf' },
    @{ Source = '03-build-report.html'; Output = '03 - Build the Power BI Report.pdf' },
    @{ Source = '04-publish-service.html'; Output = '04 - Publish to Power BI.pdf' },
    @{ Source = '05-manage-power-bi-service.html'; Output = '05 - Manage Power BI Service.pdf' },
    @{ Source = 'follow-up.html'; Output = '06 - Optional Follow Up.pdf' }
)

try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/index.html" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -ne 200) {
        throw "Unexpected HTTP status $($response.StatusCode)."
    }
} catch {
    throw "The manual source is unavailable at $BaseUrl. Start a local web server from the repository root, for example: python -m http.server 8766 --bind 127.0.0.1"
}

New-Item $OutputDirectory -ItemType Directory -Force | Out-Null
$expectedOutputs = $manuals.Output
Get-ChildItem $OutputDirectory -Filter '*.pdf' | Where-Object { $_.Name -notin $expectedOutputs } | Remove-Item -Force
$profileDirectory = Join-Path $env:TEMP "PBI-Manual-PDF-$([guid]::NewGuid())"

try {
    foreach ($manual in $manuals) {
        $outputPath = Join-Path $OutputDirectory $manual.Output
        Remove-Item $outputPath -Force -ErrorAction SilentlyContinue

        $arguments = @(
            '--headless=new',
            '--disable-gpu',
            '--no-pdf-header-footer',
            '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=5000',
            "--user-data-dir=`"$profileDirectory`"",
            "--print-to-pdf=`"$outputPath`"",
            "$BaseUrl/$($manual.Source)"
        )
        $process = Start-Process -FilePath $edgePath -ArgumentList $arguments -PassThru -Wait
        if ($process.ExitCode -ne 0 -or -not (Test-Path $outputPath)) {
            throw "PDF generation failed for $($manual.Source). Edge exit code: $($process.ExitCode)"
        }
    }
} finally {
    Remove-Item $profileDirectory -Recurse -Force -ErrorAction SilentlyContinue
}

Get-ChildItem $OutputDirectory -Filter '*.pdf' | Sort-Object Name | Select-Object Name, Length
