# Begin AddAsSourcePath
$CurrentDir = (get-location).ToString()
$ParentDirectory = [System.IO.Directory]::GetParent($CurrentDir)
# Below must be global variable so we can use the value in function definition
$global:ConfigPath = join-path -path $ParentDirectory -ChildPath "config.json"

function AddAsSourcePath {
    param ([string[]]$DirToAdd)
    <#
    Two Options:
    1. No Parameter --> Adds Current Directory (thus all subdirectories and files) to source
    2. Specify Subdirectory --> Only adds subdirectory and ignores all other files or subdirectories in current dir
    #>

    # Specify .Path below or else we get dictionary returned
    $CurrentDirectory = (Get-Location).Path.ToString()

    #Set path to config.json
    $JsonPath = $global:ConfigPath

    # First, if no parameter passed, add current Directory to config.json
    if (-not $DirToAdd) {
        # Get current directories in Json file
        $JsonContent = get-content -Path $JsonPath -Raw
        # Convert JSON content to powershell object (so we can append to it)
        $JsonObject = $JsonContent | ConvertFrom-Json
        # Add current directory to source array
        $JsonObject.source += $CurrentDirectory
        # Convert Powershell object back to JSON
        $NewJsonContent = $JsonObject | ConvertTo-Json -depth 3
        # Write updated JSON Content back to the file
        set-content -path $JsonPath -value $NewJsonContent
        # Leave message that Path was successfully added
        write-host "$CurrentDirectory successfully added"
    } else {
        #Create array to hold new Path values
        $NewPaths = @()

        #Iterate through $DirectoriesToAdd to create full path
        foreach ($Dir in $DirToAdd) {
            $CleanDir = resolve-path $Dir.ToString()
            # NEED TO FIX BELOW
            $FullPath = join-path -path $CurrentDirectory -ChildPath $CleanDir.ToString()
            $NewPaths += $FullPath
        }

        #Read JSON File Content
        $JsonContent = get-content -Path $JsonPath -Raw

        #Convert JSON content to PowerShell Object
        $JsonObject = $JsonContent | ConvertFrom-Json

        #Add new file paths to the source array
        $JsonObject.source += $NewPaths

        #Convert PowerShell object back to JSON
        $NewJsonContent = $JsonObject | ConvertTo-Json -Depth 3

        #Write the updated JSON content back to the file
        set-content -path $JsonPath -value $NewJsonContent

        write-output "$DirToAdd successfully added"
    }
}
# End AddAsSourcePath