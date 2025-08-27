# tools\bus.psm1
# Minimal file-bus with helpers: Send-Task, Receive-Task, Complete-Task, Send-Event

param()

$script:Roles = "orchestrator","po","architect","backend","frontend","qa","compliance"
$script:BusRoot = Join-Path $PSScriptRoot "..\bus"

function Initialize-Bus {
  param([string]$Root = $script:BusRoot)
  $script:BusRoot = $Root
  $dirs = "inbox","processing","outbox","archive"
  foreach ($d in $dirs) {
    foreach ($r in $script:Roles) {
      New-Item -ItemType Directory -Force -Path (Join-Path $Root "$d\$r") | Out-Null
    }
  }
  Write-Verbose "Bus ready at $Root"
  return $Root
}

function Send-Message {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]$To,
    [Parameter(Mandatory)][string]$From,
    [Parameter(Mandatory)][string]$Type,
    [Parameter(Mandatory)][hashtable]$Payload
  )
  $id = [guid]::NewGuid().ToString()
  $msg = [pscustomobject]@{
    id=$id; ts=(Get-Date).ToString("o"); to=$To; from=$From; type=$Type; payload=$Payload
  } | ConvertTo-Json -Depth 20
  $dir = Join-Path $script:BusRoot "inbox\$To"
  $tmp = Join-Path $dir "$id.tmp"
  $fin = Join-Path $dir "$id.json"
  $msg | Out-File -Encoding utf8 $tmp
  Rename-Item $tmp $fin
  return $id
}

function Receive-Next {
  [CmdletBinding()]
  param([Parameter(Mandatory)][ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]$Role)
  $dir = Join-Path $script:BusRoot "inbox\$Role"
  $file = Get-ChildItem $dir -Filter *.json -ErrorAction SilentlyContinue | Sort-Object LastWriteTime | Select-Object -First 1
  if (-not $file) { return $null }
  $procDir = Join-Path $script:BusRoot "processing\$Role"
  New-Item -ItemType Directory -Force -Path $procDir | Out-Null
  $claimed = Join-Path $procDir $file.Name
  try {
    Move-Item $file.FullName $claimed
    $obj = Get-Content $claimed -Raw | ConvertFrom-Json
    $obj | Add-Member NoteProperty _path $claimed
    $obj | Add-Member NoteProperty _role $Role
    return $obj
  } catch { return $null }
}

function Complete-Message {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][pscustomobject]$Msg,
    [Parameter(Mandatory)][ValidateSet("ok","fail")]$Status,
    [string]$ResultText = "",
    [string]$NotifyTo   # optional: also send a summary event to another role (e.g., "orchestrator")
  )
  $role = $Msg.to
  $name = [IO.Path]::GetFileNameWithoutExtension($Msg._path)
  $outDir = Join-Path $script:BusRoot "outbox\$role"
  $arcDir = Join-Path $script:BusRoot "archive\$role"
  New-Item -ItemType Directory -Force -Path $outDir,$arcDir | Out-Null
  $resFile = Join-Path $outDir "$name.$Status.txt"
  "[$((Get-Date).ToString('o'))] $Status`n$ResultText" | Out-File -Encoding utf8 $resFile
  Move-Item $Msg._path (Join-Path $arcDir "$name.json")

  if ($NotifyTo) {
    Send-Event -To $NotifyTo -From $role -Name "completed" -Data @{ id = $Msg.id; status = $Status; note = $ResultText }
  }
}

# ---------- Friendly helpers (what I was offering) ----------

function Send-Task {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]$To,
    [Parameter(Mandatory)][string]$From,
    [Parameter(Mandatory)][string]$Title,
    [Parameter()][string]$Description = "",
    [Parameter()][hashtable]$Data = @{}
  )
  $payload = @{
    title = $Title; description = $Description; data = $Data
  }
  return Send-Message -To $To -From $From -Type "task" -Payload $payload
}

function Receive-Task {
  [CmdletBinding()]
  param([Parameter(Mandatory)][ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]$Role)
  $m = Receive-Next -Role $Role
  if (-not $m) { return $null }
  # expose convenience props
  $m | Add-Member NoteProperty title       $m.payload.title     -Force
  $m | Add-Member NoteProperty description $m.payload.description -Force
  $m | Add-Member NoteProperty data        $m.payload.data      -Force
  return $m
}

function Complete-Task {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][pscustomobject]$Task,
    [Parameter(Mandatory)][ValidateSet("ok","fail")]$Status,
    [string]$Note = "",
    [string]$NotifyTo = "orchestrator"
  )
  Complete-Message -Msg $Task -Status $Status -ResultText $Note -NotifyTo $NotifyTo
}

function Send-Event {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][ValidateSet("orchestrator","po","architect","backend","frontend","qa","compliance")]$To,
    [Parameter(Mandatory)][string]$From,
    [Parameter(Mandatory)][string]$Name,
    [Parameter()][hashtable]$Data = @{}
  )
  return Send-Message -To $To -From $From -Type "event" -Payload (@{ name=$Name; data=$Data })
}

Export-ModuleMember -Function Initialize-Bus, Send-Message, Receive-Next, Complete-Message, Send-Task, Receive-Task, Complete-Task, Send-Event
