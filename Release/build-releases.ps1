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
    @{ Source = 'Student\Labs\Web\index.html'; Destination = 'Labs\Web\index.html' },
    @{ Source = 'Student\Labs\Web\01-connect.html'; Destination = 'Labs\Web\01-connect.html' },
    @{ Source = 'Student\Labs\Web\02-transform-model.html'; Destination = 'Labs\Web\02-transform-model.html' },
    @{ Source = 'Student\Labs\Web\03-build-report.html'; Destination = 'Labs\Web\03-build-report.html' },
    @{ Source = 'Student\Labs\Web\04-publish-service.html'; Destination = 'Labs\Web\04-publish-service.html' },
    @{ Source = 'Student\Labs\Web\follow-up.html'; Destination = 'Labs\Web\follow-up.html' },
    @{ Source = 'Student\Labs\Web\styles'; Destination = 'Labs\Web\styles' },
    @{ Source = 'Student\Labs\Web\scripts'; Destination = 'Labs\Web\scripts' },
    @{ Source = 'Student\Labs\Web\Branding'; Destination = 'Labs\Web\Branding' },
    @{ Source = 'Student\Labs\Images'; Destination = 'Labs\Images' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Data' }
)

$instructorMappings = @(
    @{ Source = 'Release\Instructor-README.md'; Destination = 'README.md' },
    @{ Source = 'Release\Student-README.md'; Destination = 'Student\README.md' },
    @{ Source = 'Student\Labs\Web\index.html'; Destination = 'Student\Labs\Web\index.html' },
    @{ Source = 'Student\Labs\Web\01-connect.html'; Destination = 'Student\Labs\Web\01-connect.html' },
    @{ Source = 'Student\Labs\Web\02-transform-model.html'; Destination = 'Student\Labs\Web\02-transform-model.html' },
    @{ Source = 'Student\Labs\Web\03-build-report.html'; Destination = 'Student\Labs\Web\03-build-report.html' },
    @{ Source = 'Student\Labs\Web\04-publish-service.html'; Destination = 'Student\Labs\Web\04-publish-service.html' },
    @{ Source = 'Student\Labs\Web\follow-up.html'; Destination = 'Student\Labs\Web\follow-up.html' },
    @{ Source = 'Student\Labs\Web\styles'; Destination = 'Student\Labs\Web\styles' },
    @{ Source = 'Student\Labs\Web\scripts'; Destination = 'Student\Labs\Web\scripts' },
    @{ Source = 'Student\Labs\Web\Branding'; Destination = 'Student\Labs\Web\Branding' },
    @{ Source = 'Student\Labs\Images'; Destination = 'Student\Labs\Images' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Student\Data' },
    @{ Source = 'Student\Labs\PDF\INSTRUCTIONS.pdf'; Destination = 'Instructor\Reference\INSTRUCTIONS.pdf' },
    @{ Source = 'Student\Labs\PDF\TRANSFORMATIONS.pdf'; Destination = 'Instructor\Reference\TRANSFORMATIONS.pdf' },
    @{ Source = 'Student\Labs\PDF\REPORT_BUILDING_GUIDE.pdf'; Destination = 'Instructor\Reference\REPORT_BUILDING_GUIDE.pdf' },
    @{ Source = 'Student\PowerQuery'; Destination = 'Instructor\Reference\PowerQuery' },
    @{ Source = 'Student\ReportBackgrounds'; Destination = 'Instructor\Reference\ReportBackgrounds' },
    @{ Source = 'Instructor\DeliveryGuide'; Destination = 'Instructor\DeliveryGuide' },
    @{ Source = 'Communications'; Destination = 'Instructor\Customer Communications' },
    @{ Source = 'Student\Labs\Completed\Completed_Report.pbix'; Destination = 'Instructor\Completed Reports\Completed_Report.pbix' },
    @{ Source = 'Coding-Forge_Data'; Destination = 'Instructor\Source Data' },
    @{ Source = 'Certificate'; Destination = 'Instructor\Certificates' },
    @{ Source = 'Sample Reports'; Destination = 'Instructor\Sample Reports' },
    @{ Source = 'Instructor\PPT\Lesson 1 - Power BI Overview.pptx'; Destination = 'Instructor\Slide Decks\Lesson 1 - Power BI Overview.pptx' },
    @{ Source = 'Instructor\PPT\Lesson 2 - Getting your Data into Power BI (2).pptx'; Destination = 'Instructor\Slide Decks\Lesson 2 - Getting your Data into Power BI.pptx' },
    @{ Source = 'Instructor\PPT\Lesson 3 - Building Reports.pptx'; Destination = 'Instructor\Slide Decks\Lesson 3 - Building Reports.pptx' },
    @{ Source = 'Instructor\PPT\Lesson 4 - Publish Collaborate and Sharing.pptx'; Destination = 'Instructor\Slide Decks\Lesson 4 - Publish Collaborate and Sharing.pptx' }
)

New-ReleaseArchive -ArchivePath $studentArchive -RootName $studentRootName -Mappings $studentMappings
New-ReleaseArchive -ArchivePath $instructorArchive -RootName $instructorRootName -Mappings $instructorMappings

Assert-Archive -ArchivePath $studentArchive `
    -RequiredPatterns @(
        "$studentRootName/README.md",
        "$studentRootName/Labs/Web/index.html",
        "$studentRootName/Labs/Web/styles/manual-print.css",
        "$studentRootName/Labs/Web/scripts/delivery-config.js",
        "$studentRootName/Labs/Web/Branding/*",
        "$studentRootName/Labs/Images/*.png",
        "$studentRootName/Data/*.csv"
    ) `
    -ForbiddenPatterns @(
        '*PBIP*',
        '*.pbix',
        '*.pptx',
        '*DeliveryGuide*',
        '*Customer Communications*',
        '*Customer Training Access and Readiness Email*',
        '*Student Manual PDFs*',
        '*Course Overview.pdf',
        '*Connect to GitHub Data.pdf',
        '*Transform and Model.pdf',
        '*Build the Power BI Report.pdf',
        '*Publish to Power BI.pdf',
        '*Optional Follow Up.pdf',
        '*.py'
    )

Assert-Archive -ArchivePath $instructorArchive `
    -RequiredPatterns @(
        "$instructorRootName/README.md",
        "$instructorRootName/Student/Labs/Web/index.html",
        "$instructorRootName/Instructor/DeliveryGuide/*",
        "$instructorRootName/Instructor/Customer Communications/Customer Training Access and Readiness Email.md",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/00 - Course Overview.pdf",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/01 - Connect to GitHub Data.pdf",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/02 - Transform and Model.pdf",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/03 - Build the Power BI Report.pdf",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/04 - Publish to Power BI.pdf",
        "$instructorRootName/Instructor/Customer Communications/Student Manual PDFs/05 - Optional Follow Up.pdf",
        "$instructorRootName/Instructor/Completed Reports/Completed_Report.pbix",
        "$instructorRootName/Instructor/Slide Decks/*.pptx",
        "$instructorRootName/Instructor/Source Data/*.csv"
    ) `
    -ForbiddenPatterns @(
        '*PBIP*',
        '*PPT/Archive*',
        '*Completed Reports/Legacy*',
        '*Completed_Report_2.pbix',
        '*__pycache__*',
        '*.pyc'
    )

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