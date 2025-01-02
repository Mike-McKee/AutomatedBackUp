function AutoBuAddSrcPath {
    param ([string[]]$DirToAdd)

    #Set path to config.json
    $JsonPath = "C:\Users\mike\Coding\AutomatedBackUp\Version5\config.json"

    #Find Current Directory
    $CurrentDirectory = Get-Location

    #Create array to hold new Path values
    $NewPaths = @()

    #Iterate through $DirectoriesToAdd to create full path
    foreach ($Dir in $DirToAdd) {
        $FullPath = join-path -path $CurrentDirectory -ChildPath $Dir
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

    write-output "Paths successfully added"
}
