# scripts\Start-Notifier.ps1
param(
  [ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]
  [string]$Role = "orchestrator",
  [string]$BusRoot = (Join-Path $PSScriptRoot "..\bus")
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$watchPath = Join-Path $BusRoot "outbox\$Role"
New-Item -ItemType Directory -Force -Path $watchPath | Out-Null

$icon = New-Object System.Windows.Forms.NotifyIcon
$icon.Icon = [System.Drawing.SystemIcons]::Information
$icon.Text = "BMad $Role notifier"
$icon.Visible = $true

$menu = New-Object System.Windows.Forms.ContextMenuStrip
$open = $menu.Items.Add("Open outbox")
$exit = $menu.Items.Add("Exit")
$icon.ContextMenuStrip = $menu

$open.Add_Click({ ii $watchPath })
$exit.Add_Click({
  $icon.Visible = $false
  $fsw.EnableRaisingEvents = $false
  $fsw.Dispose()
  [System.Windows.Forms.Application]::Exit()
})

$fsw = New-Object System.IO.FileSystemWatcher $watchPath, "*.txt"
$fsw.IncludeSubdirectories = $false
$fsw.EnableRaisingEvents = $true
$fsw.NotifyFilter = [IO.NotifyFilters]'FileName, LastWrite'

$handler = Register-ObjectEvent $fsw Created -Action {
  Start-Sleep -Milliseconds 120   # allow writer to finish
  $path = $Event.SourceEventArgs.FullPath
  try {
    $first = (Get-Content $path -TotalCount 1)
    $msg = (Split-Path $path -Leaf)
    $icon.ShowBalloonTip(3000, "[$Role] $msg", $first, [System.Windows.Forms.ToolTipIcon]::Info)
  } catch {}
}

[System.Windows.Forms.Application]::Run()
Unregister-Event -SourceIdentifier $handler.Name -ErrorAction SilentlyContinue
$icon.Visible = $false
