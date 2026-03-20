param(
    [string]$OutputPath = ".github\social-preview.png"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$resolvedOutput = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
} else {
    Join-Path $repoRoot $OutputPath
}
$outputDir = Split-Path -Parent $resolvedOutput
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$width = 1280
$height = 640
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

try {
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

    $backgroundRect = New-Object System.Drawing.Rectangle 0, 0, $width, $height
    $backgroundBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $backgroundRect,
        [System.Drawing.Color]::FromArgb(255, 14, 20, 36),
        [System.Drawing.Color]::FromArgb(255, 23, 53, 81),
        20
    )
    $graphics.FillRectangle($backgroundBrush, $backgroundRect)

    $accentBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 66, 211, 146))
    $mutedAccentBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 29, 135, 116))
    $panelBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(230, 10, 16, 28))
    $panelBorderPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 59, 93, 123)), 2
    $whiteBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 245, 248, 252))
    $softBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 180, 194, 214))
    $darkBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 15, 21, 31))

    $graphics.FillRectangle($accentBrush, 68, 64, 120, 12)
    $graphics.FillRectangle($mutedAccentBrush, 196, 64, 76, 12)

    $titleFont = New-Object System.Drawing.Font("Bahnschrift", 38, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $subtitleFont = New-Object System.Drawing.Font("Segoe UI", 22, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $labelFont = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $bulletFont = New-Object System.Drawing.Font("Segoe UI", 19, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
    $footerFont = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)

    $graphics.DrawString("Windows-native BitNet inference", $titleFont, $whiteBrush, 72, 98)
    $graphics.DrawString("CPU GGUF + GPU runtime for ternary LLMs", $subtitleFont, $softBrush, 74, 154)

    $panelRect = New-Object System.Drawing.Rectangle 70, 236, 1140, 276
    $graphics.FillRectangle($panelBrush, $panelRect)
    $graphics.DrawRectangle($panelBorderPen, $panelRect)

    $graphics.DrawString("What this repo gives you", $labelFont, $accentBrush, 102, 270)

    $bullets = @(
        "Windows release zips and smoke-tested packaging",
        "CPU path built around llama.cpp and GGUF",
        "Separate GPU runtime with packed int2 decode",
        "Terminal chat and browser chat entrypoints"
    )

    $bulletY = 322
    foreach ($bullet in $bullets) {
        $graphics.FillEllipse($accentBrush, 108, $bulletY + 10, 10, 10)
        $graphics.DrawString($bullet, $bulletFont, $whiteBrush, 132, $bulletY)
        $bulletY += 48
    }

    $badgeRect = New-Object System.Drawing.Rectangle 820, 98, 330, 92
    $badgeBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 230, 244, 238))
    $graphics.FillRectangle($badgeBrush, $badgeRect)
    $graphics.DrawRectangle((New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 66, 211, 146)), 2), $badgeRect)
    $graphics.DrawString("BitNet + ternary", $labelFont, $darkBrush, 848, 118)
    $graphics.DrawString("Windows-focused tooling", $subtitleFont, $darkBrush, 848, 148)

    $graphics.DrawString("github.com/syn-999/core58-w2a8-msvc", $footerFont, $softBrush, 74, 566)

    $bitmap.Save($resolvedOutput, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host $resolvedOutput
}
finally {
    foreach ($obj in @(
        $titleFont,
        $subtitleFont,
        $labelFont,
        $bulletFont,
        $footerFont,
        $accentBrush,
        $mutedAccentBrush,
        $panelBrush,
        $panelBorderPen,
        $whiteBrush,
        $softBrush,
        $darkBrush,
        $backgroundBrush,
        $graphics,
        $bitmap
    )) {
        if ($null -ne $obj) {
            $obj.Dispose()
        }
    }
}
