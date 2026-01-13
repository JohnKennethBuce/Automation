' ============================================================
' StartHmopiTunnel.vbs
' This VBS script runs the batch file as Administrator silently
' Location: C:\1jap\Automation\StartHmopiTunnel.vbs
' ============================================================

Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "cmd.exe", "/c ""C:\1jap\Automation\StartHmopiTunnel.bat""", "", "runas", 1
