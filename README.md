# AutomatedBackUp
Custom Python Tool to Automate File Backup.

This repo allows me to automtaically backup files from my local computer to a specified cloud location.

I built it because I have hundreds of files saved on my work laptop, within multiple directories. My company gives each employee a personal ShareFile drive to save files in the cloud.

This is a perfect location to backup files in case of a disaster or malfunction.

The problem, however, is that I currently do not save anything to my personal ShareFile.

Why? Well, it's a mix of me being lazy and manually moving multiple files at once is a hassle. So, I don't do it.

But this tool will automate the backup process and allow me to sleep better knowing my files (and hard work over the last 15 months) is safe.

# How to use it...

# AddAsSourcePath.ps1

## What does it do?

This script allows you to automatically add source directories to config.json.

Follow the steps in the next section to declare AddAsSourcePath as a built-in PowerShell function.

Once you do so, execute the following to add a directory to the source directories in config.json: `AddAsSourcePath .`

This command adds all directories and subdirectories within your current directory to the list of items to backup.

## How to add as buil-in PowerShell function 

If you want to add AddAsSourcePath.ps1 as a built-in function on your system, follow the below steps:

1. Open powershell
2. Go to your directory containing this repo and the AddAsSourcePath.ps1 file
3. Enter: `add-content -path $Profile -value (get-content -path .\AddAsSourcePath.ps1 -raw); . .\AddAsSourcePath.ps1`
4. Run this to verify the function exists in your current session: ``get-command -commandtype function | where-object { $_.Name -like "AddAsSourcePath*" }``

If you want to remove the function from your system's built-in list, follow the below steps:

1. Open powershell
2. Enter `(Get-Content -path $Profile -raw) -replace 'function AddAsSourcePath {.*?}','' | set-content -path $Profile; Remove-item Function:\AddAsSourcePath`
3. Restart PowerShell and run the following to validate it no longer exists: `get-command -commandtype function | where-object { $_.Name -like "AddAsSourcePath*" }`

Testing this one now... `(get-content -path $Profile -raw) -replace "# Begin AddAsSourcePath.*?# End AddAsSourcePath",""` Remove function not working yet...

