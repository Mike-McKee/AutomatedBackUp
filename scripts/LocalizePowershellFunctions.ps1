<#
This script creates the AddAsSourcePath function which you can run in any directory to add it to the source directory list
#>


# If function already exists, do not continue
$exists = (Select-String -Path $Profile -Pattern "AddAsSourcePath").count -gt 0
if ($exists) {
    return
}

$CurrentDir = (get-location).ToString()
$ParentDirectory = [System.IO.Directory]::GetParent($CurrentDir)
$ConfigPath = join-path -path $ParentDirectory -ChildPath "config.json"


$AddAsSourcePath = @"
# Begin AddAsSourcePath
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
    `$JsonPath = 'C:\Users\mike\Coding\AutomatedBackup\'

    # First, if no parameter passed, add current Directory to config.json
    if (-not `$DirToAdd) {
        # Get current directories in Json file
        `$JsonContent = get-content -Path `$JsonPath -Raw
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
        #Create array to hold new Path values
        `$NewPaths = @()

        #Iterate through `$DirectoriesToAdd to create full path
        foreach (`$Dir in `$DirToAdd) {
            `$CleanDir = resolve-path `$Dir.ToString()
            # NEED TO FIX BELOW
            `$FullPath = join-path -path `$CurrentDirectory -ChildPath `$CleanDir.ToString()
            `$NewPaths += `$FullPath
        }

        #Read JSON File Content
        `$JsonContent = get-content -Path `$JsonPath -Raw

        #Convert JSON content to PowerShell Object
        `$JsonObject = `$JsonContent | ConvertFrom-Json

        #Add new file paths to the source array
        `$JsonObject.source += `$NewPaths

        #Convert PowerShell object back to JSON
        `$NewJsonContent = `$JsonObject | ConvertTo-Json -Depth 3

        #Write the updated JSON content back to the file
        set-content -path `$JsonPath -value `$NewJsonContent

        write-output "`$DirToAdd successfully added"
    }
}
# End AddAsSourcePath
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

# Now add function to current session
Invoke-Expression $AddAsSourcePath

# Now add function to Powershell $Profile
# Get current $Profile content
$CurrentProfileContent = get-content -path $Profile -Raw
# Add function to $Profile (note: `n creates newline... similar to \n)
$CurrentProfileContent += "`n$AddAsSourcePath"
# Finally save new content...
set-content -path $Profile -value $CurrentProfileContent

# This adds function to current session so you don't have to restart PowerShell
. $Profile

write-host "AddAsSourcePath function created..." -foregroundcolor green