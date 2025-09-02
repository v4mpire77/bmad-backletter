<#!
  Windows setup wrapper.
  Usage:
    .\tools\windows\setup.ps1 [-RecreateVenv] [-SkipInstall]
#>
param(
  [switch]$RecreateVenv,
  [switch]$SkipInstall
)

$root = Resolve-Path (Join-Path $PSScriptRoot '..' '..')
$setup = Join-Path $root 'setup.ps1'

& $setup @PSBoundParameters
