<#
This script creates the AddAsSourcePath function which you can run in any directory to add it to the source directory list
#>


# If functions already exist, do not continue
$exists = (Select-String -Path $Profile -Pattern "AddAsSourcePath").count -gt 0
if ($exists) {
    return
}
$exists = (Select-String -Path $Profile -Pattern "ExecuteAutomatedBackup").count -gt 0
if ($exists) {
    return
}



$AddAsSourcePath = @"
function AddAsSourcePath {
    param ([string[]]`$DirToAdd)
    <#
    Two Options:
    1. No Parameter --> Adds Current Directory (thus all subdirectories and files) to source
    2. Specify Subdirectory --> Only adds subdirectory and ignores all other files or subdirectories in current dir
    #>

    # Specify .Path below or else we get dictionary returned
    `$CurrentDirectory = (Get-Location).Path.ToString()

    #Set path to config.json
    `$JsonPath = 'C:\Users\mike\Coding\AutomatedBackup\config.json'

    # First, if no parameter passed, add current Directory to config.json
    if (-not `$DirToAdd) {
        # Get current directories in Json file
        `$JsonContent = get-content -Path `$JsonPath
        # Convert JSON content to powershell object (so we can append to it)
        `$JsonObject = `$JsonContent | ConvertFrom-Json
        # Add current directory to source array
        `$JsonObject.source += `$CurrentDirectory
        # Convert Powershell object back to JSON
        `$NewJsonContent = `$JsonObject | ConvertTo-Json -depth 3
        # Write updated JSON Content back to the file
        set-content -path `$JsonPath -value `$NewJsonContent
        # Leave message that Path was successfully added
        write-host "`$CurrentDirectory successfully added"
    } else {
        # Changing function to require no paramter... If something is passed, raise Error
        write-host "-------- ERROR: AddAsSourcePath takes no paramter --------" -foregroundcolor Red
    }
}

"@

$ExecuteAutomatedBackup = @"
function ExecuteAutomatedBackup {
# First, let's go to the directory where our Python script exists
<# ---------------- INSERT THE REPO'S DIRECTORY BELOW ---------------- #>
cd 'C:\Users\mike\Coding\AutomatedBackup\'

if (-not (test-path ".\myenv\")) {
    <# Initialize Python virtual environment and install necessary libraries #>
    write-host "Creating Python Virtual Environment..."
    # Initialize virtual 
    py -m venv myenv
    write-host "Python Virtual Environment 'myenv' Created"

    # Activate virtual environment
    .\myenv\Scripts\Activate

    # install necessary pip libraries
    pip install -r requirements.txt
} else {
    & .\myenv\Scripts\Activate
}

# NOW WE EXECUTE THE PYTHON BACKUP SCRIPT
py .\AutomatedBackUp.py

write-host "YAY!!! FINISHED"
deactivate
}

"@

# Now add functions to current session
Invoke-Expression $AddAsSourcePath
Invoke-Expression $ExecuteAutomatedBackup

<# -------------- Now add functions to Powershell $Profile -------------- #>
# Get current $Profile content
$CurrentProfileContent = get-content -path $Profile -Raw

# Add functions to $Profile (note: `n creates newline... similar to \n)
$CurrentProfileContent += "`n$AddAsSourcePath`n$ExecuteAutomatedBackup"

# Finally save new content...
set-content -path $Profile -value $CurrentProfileContent

# This adds function to current session so you don't have to restart PowerShell
. $PROFILE

write-host "AddAsSourcePath function created..." -foregroundcolor green
write-host "ExecuteAutomatedBackup function created..." -foregroundcolor green