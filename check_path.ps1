# Run in PowerShell from project folder: .\check_path.ps1
# Shows how Git sees paths under OFAC DB
Write-Host "=== Files in current index ==="
git ls-files "OFAC DB/"
Write-Host ""
Write-Host "=== All files in latest commit (branch main) ==="
git ls-tree -r main --name-only | Select-String -Pattern "OFAC|sdn|cons"
Write-Host ""
Write-Host "=== File on disk? ==="
if (Test-Path "OFAC DB\sdn_advanced.xml") { Write-Host "OFAC DB\sdn_advanced.xml exists" } else { Write-Host "OFAC DB\sdn_advanced.xml NOT FOUND" }
