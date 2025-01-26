# AutomatedBackUp
Custom Python Tool to Automate File Backup.

This repo allows me to automtaically backup files from my local computer to a specified cloud location.

I built it because I have hundreds of files saved on my work laptop, within multiple directories. My company gives each employee a personal ShareFile drive to save files in the cloud.

This is a perfect location to backup files in case of a disaster or malfunction.

The problem, however, is that I currently do not save anything to my personal ShareFile.

Why? Well, it's a mix of me being lazy and manually moving multiple files at once is a hassle. So, I don't do it.

But this tool will automate the backup process and allow me to sleep better knowing my files (and hard work over the last 15 months) is safe.

# How to use it...

## config-example.json file

A few things for you to do here:

1. Rename the file to config.json. If you do not do this, AutomatedBackup.py will not be able to determine which files to move and where to move them.
2. Add your destination path (aka where you want to backup your files to)

## Powershell functions

Powershell functions you need to know:
1. `AddAsSourcePath` - this adds a directory to your config.json source list. The function requires a string parameter that must be a subdirectory of your cwd. Here is an example of how to execute the function: `AddAsSourcePath .\scripts\`

2. `ExecuteAutomatedBackup` - this function executes the AutomatedBackUp.py script. The function automatically cd's into the scripts directory, hence why you can execute it from anywhere. There are no parameters. Here is an example of how to execute the function: `ExecuteAutomatedBackup`

I suggest making the two functions built-in to Powershell, this way you can execute them from any directory. Here's how to do it:
- Open Powershell
- Go to your directory containing this repo and cd into the scripts folder
- Run this: `.\LocalizePowershellFunctions.ps1`
- Then run this: `. $PROFILE`

To verify the process worked, you can execute the below. Note: if nothing appears, then `LocalizePowershellFunctions.ps1` failed. You can debug on your own or reach out to me for help.
- `get-command -commandtype function | where-object { $_.Name -like "AddAsSourcePath" -or $_.Name -like "ExecuteAutomatedBackup" }`

If you ever need to remove the functions from your built-in list, execute the following:
- `Remove-Item Function:\AddAsSourcePath`
- `Remove-Item Function:\ExecuteAutomatedBackup`