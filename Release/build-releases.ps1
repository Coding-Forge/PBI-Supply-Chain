[CmdletBinding()]
param(
    [string]$Version = (Get-Date -Format 'yyyy.MM.dd'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'dist')
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repositoryRoot = Split-Path $PSScriptRoot -Parent
$studentRootName = "PBI-Factory-Student-$Version"
$instructorRootName = "PBI-Factory-Instructor-$Version"
$studentArchive = Join-Path $OutputDirectory "$studentRootName.zip"
$instructorArchive = Join-Path $OutputDirectory "$instructorRootName.zip"

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-RelativeFiles {
    param([Parameter(Mandatory)][string]$Path)

    $fullPath = Join-Path $repositoryRoot $Path
    if (-not (Test-Path $fullPath)) {
        throw "Release source does not exist: $Path"
    }

    if (Test-Path $fullPath -PathType Leaf) {
        return ,(Get-Item $fullPath)
    }

    return @(Get-ChildItem $fullPath -Recurse -File | Sort-Object FullName)
}

function Add-FileToArchive {
    param(
        [Parameter(Mandatory)]$Archive,
        [Parameter(Mandatory)]$EntryNames,
        [Parameter(Mandatory)][string]$SourcePath,
        [Parameter(Mandatory)][string]$EntryPath
    )

    $entryName = $EntryPath.Replace('\', '/')
    if (-not $EntryNames.Add($entryName)) {
        throw "Duplicate archive entry: $entryName"
    }

    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $Archive,
        $SourcePath,
        $entryName,
        [System.IO.Compression.CompressionLevel]::Optimal
    ) | Out-Null
}

function Add-MappedPath {
    param(
        [Parameter(Mandatory)]$Archive,
        [Parameter(Mandatory)]$EntryNames,
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][string]$Destination
    )

    $sourceFullPath = Join-Path $repositoryRoot $Source
    $sourceItem = Get-Item $sourceFullPath
    foreach ($file in Get-RelativeFiles $Source) {
        $relativePath = if ($sourceItem.PSIsContainer) {
            $file.FullName.Substring($sourceItem.FullName.Length).TrimStart('\', '/')
        } else {
            $file.Name
        }
        $entryPath = if ($sourceItem.PSIsContainer) {
            Join-Path $Destination $relativePath
        } else {
            $Destination
        }
        Add-FileToArchive `
            -Archive $Archive `
            -EntryNames $EntryNames `
            -SourcePath $file.FullName `
            -EntryPath $entryPath
    }
}

function New-ReleaseArchive {
    param(
        [Parameter(Mandatory)][string]$ArchivePath,
        [Parameter(Mandatory)][string]$RootName,
        [Parameter(Mandatory)][array]$Mappings
    )

    if (Test-Path $ArchivePath) {
        Remove-Item $ArchivePath -Force
    }

    $stream = [System.IO.File]::Open($ArchivePath, [System.IO.FileMode]::CreateNew)
    try {
        $entryNames = [System.Collections.Generic.HashSet[string]]::new(
            [System.StringComparer]::OrdinalIgnoreCase
        )
        $archive = [System.IO.Compression.ZipArchive]::new(
            $stream,
            [System.IO.Compression.ZipArchiveMode]::Create,
            $false
        )
        try {
            foreach ($mapping in $Mappings) {
                Add-MappedPath `
                    -Archive $archive `
                    -EntryNames $entryNames `
                    -Source $mapping.Source `
                    -Destination (Join-Path $RootName $mapping.Destination)
            }
        } finally {
            $archive.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
}

function Get-ArchiveEntries {
    param([Parameter(Mandatory)][string]$ArchivePath)

    $archive = [System.IO.Compression.ZipFile]::OpenRead($ArchivePath)
    try {
        return @($archive.Entries | ForEach-Object FullName)
    } finally {
        $archive.Dispose()
    }
}

function Assert-Archive {
    param(
        [Parameter(Mandatory)][string]$ArchivePath,
        [Parameter(Mandatory)][string[]]$RequiredPatterns,
        [Parameter(Mandatory)][string[]]$ForbiddenPatterns
    )

    $entries = Get-ArchiveEntries $ArchivePath
    foreach ($pattern in $RequiredPatterns) {
        if (-not ($entries -like $pattern)) {
            throw "Archive is missing required content '$pattern': $ArchivePath"
        }
    }
    foreach ($pattern in $ForbiddenPatterns) {
        if ($entries -like $pattern) {
            throw "Archive contains forbidden content '$pattern': $ArchivePath"
        }
    }
}

New-Item $OutputDirectory -ItemType Directory -Force | Out-Null

$studentMappings = @(
    @{ Source = 'Release\Student-README.md'; Destination = 'README.md' },
    @{ Source = 'Student\Lab\index.html'; Destination = 'Lab\index.html' },
    @{ Source = 'Student\Lab\01-connect.html'; Destination = 'Lab\01-connect.html' },
    @{ Source = 'Student\Lab\02-transform-model.html'; Destination = 'Lab\02-transform-model.html' },
    @{ Source = 'Student\Lab\03-build-report.html'; Destination = 'Lab\03-build-report.html' },
    @{ Source = 'Student\Lab\04-publish-service.html'; Destination = 'Lab\04-publish-service.html' },
    @{ Source = 'Student\Lab\follow-up.html'; Destination = 'Lab\follow-up.html' },
    @{ Source = 'Student\Lab\manual-print.css'; Destination = 'Lab\manual-print.css' },
    @{ Source = 'Student\Lab\delivery-brand.js'; Destination = 'Lab\delivery-brand.js' },
    @{ Source = 'Student\Lab\delivery-config.js'; Destination = 'Lab\delivery-config.js' },
    @{ Source = 'Student\Lab\Branding'; Destination = 'Lab\Branding' },
    @{ Source = 'Student\Images'; Destination = 'Images' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Data' }
)

$instructorMappings = @(
    @{ Source = 'Release\Instructor-README.md'; Destination = 'README.md' },
    @{ Source = 'Release\Student-README.md'; Destination = 'Student\README.md' },
    @{ Source = 'Student\Lab\index.html'; Destination = 'Student\Lab\index.html' },
    @{ Source = 'Student\Lab\01-connect.html'; Destination = 'Student\Lab\01-connect.html' },
    @{ Source = 'Student\Lab\02-transform-model.html'; Destination = 'Student\Lab\02-transform-model.html' },
    @{ Source = 'Student\Lab\03-build-report.html'; Destination = 'Student\Lab\03-build-report.html' },
    @{ Source = 'Student\Lab\04-publish-service.html'; Destination = 'Student\Lab\04-publish-service.html' },
    @{ Source = 'Student\Lab\follow-up.html'; Destination = 'Student\Lab\follow-up.html' },
    @{ Source = 'Student\Lab\manual-print.css'; Destination = 'Student\Lab\manual-print.css' },
    @{ Source = 'Student\Lab\delivery-brand.js'; Destination = 'Student\Lab\delivery-brand.js' },
    @{ Source = 'Student\Lab\delivery-config.js'; Destination = 'Student\Lab\delivery-config.js' },
    @{ Source = 'Student\Lab\Branding'; Destination = 'Student\Lab\Branding' },
    @{ Source = 'Student\Images'; Destination = 'Student\Images' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Student\Data' },
    @{ Source = 'Student\Lab\INSTRUCTIONS.pdf'; Destination = 'Instructor\Reference\INSTRUCTIONS.pdf' },
    @{ Source = 'Student\Lab\TRANSFORMATIONS.pdf'; Destination = 'Instructor\Reference\TRANSFORMATIONS.pdf' },
    @{ Source = 'Student\Lab\REPORT_BUILDING_GUIDE.pdf'; Destination = 'Instructor\Reference\REPORT_BUILDING_GUIDE.pdf' },
    @{ Source = 'Student\PowerQuery'; Destination = 'Instructor\Reference\PowerQuery' },
    @{ Source = 'Student\ReportBackgrounds'; Destination = 'Instructor\Reference\ReportBackgrounds' },
    @{ Source = 'Student\DeliveryGuide'; Destination = 'Instructor\DeliveryGuide' },
    @{ Source = 'Communications'; Destination = 'Instructor\Customer Communications' },
    @{ Source = 'Student\Lab\Completed_Report.pbix'; Destination = 'Instructor\Completed Reports\Completed_Report.pbix' },
    @{ Source = 'Student\Lab\Completed_Report_2.pbix'; Destination = 'Instructor\Completed Reports\Completed_Report_2.pbix' },
    @{ Source = 'Completed'; Destination = 'Instructor\Completed Reports\Legacy' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Instructor\Source Data' },
    @{ Source = 'Certificate'; Destination = 'Instructor\Certificates' },
    @{ Source = 'Sample Reports'; Destination = 'Instructor\Sample Reports' },
    @{ Source = 'PPT\Lesson 1 - Power BI Overview.pptx'; Destination = 'Instructor\Slide Decks\Lesson 1 - Power BI Overview.pptx' },
    @{ Source = 'PPT\Lesson 2 - Getting your Data into Power BI (2).pptx'; Destination = 'Instructor\Slide Decks\Lesson 2 - Getting your Data into Power BI.pptx' },
    @{ Source = 'PPT\Lesson 3 - Building Reports.pptx'; Destination = 'Instructor\Slide Decks\Lesson 3 - Building Reports.pptx' },
    @{ Source = 'PPT\Lesson 4 - Publish Collaborate and Sharing.pptx'; Destination = 'Instructor\Slide Decks\Lesson 4 - Publish Collaborate and Sharing.pptx' }
)

New-ReleaseArchive -ArchivePath $studentArchive -RootName $studentRootName -Mappings $studentMappings
New-ReleaseArchive -ArchivePath $instructorArchive -RootName $instructorRootName -Mappings $instructorMappings

Assert-Archive -ArchivePath $studentArchive `
    -RequiredPatterns @(
        "$studentRootName/README.md",
        "$studentRootName/Lab/index.html",
        "$studentRootName/Lab/delivery-config.js",
        "$studentRootName/Lab/Branding/*",
        "$studentRootName/Images/*.png",
        "$studentRootName/Data/*.csv"
    ) `
    -ForbiddenPatterns @(
        '*PBIP*',
        '*.pbix',
        '*.pptx',
        '*DeliveryGuide*',
        '*Customer Communications*',
        '*Customer Training Access and Readiness Email*',
        '*.py'
    )

Assert-Archive -ArchivePath $instructorArchive `
    -RequiredPatterns @(
        "$instructorRootName/README.md",
        "$instructorRootName/Student/Lab/index.html",
        "$instructorRootName/Instructor/DeliveryGuide/*",
        "$instructorRootName/Instructor/Customer Communications/Customer Training Access and Readiness Email.md",
        "$instructorRootName/Instructor/Completed Reports/*.pbix",
        "$instructorRootName/Instructor/Slide Decks/*.pptx",
        "$instructorRootName/Instructor/Source Data/*.csv"
    ) `
    -ForbiddenPatterns @('*PBIP*', '*PPT/Archive*', '*__pycache__*', '*.pyc')

$hashPath = Join-Path $OutputDirectory 'SHA256SUMS.txt'
$hashLines = @($studentArchive, $instructorArchive) | ForEach-Object {
    $hash = Get-FileHash $_ -Algorithm SHA256
    "$($hash.Hash.ToLowerInvariant())  $([System.IO.Path]::GetFileName($_))"
}
[System.IO.File]::WriteAllLines($hashPath, $hashLines, [System.Text.UTF8Encoding]::new($false))

@($studentArchive, $instructorArchive) | ForEach-Object {
    $entries = Get-ArchiveEntries $_
    $item = Get-Item $_
    [pscustomobject]@{
        Archive = $item.Name
        Files = $entries.Count
        SizeMB = [math]::Round($item.Length / 1MB, 2)
    }
} | Format-Table -AutoSize

Write-Host "Checksums: $hashPath"