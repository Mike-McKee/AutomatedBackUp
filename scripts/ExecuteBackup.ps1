<# First, let's verify we are in the correct directory #>
$CurrentDirectory = (get-location).ToString()
$ParentDirectory = [System.IO.Directory]::GetParent($CurrentDirectory)
# write-host $CurrentDirectory
# write-host "Parent Directory: $ParentDirectory"

if ($CurrentDirectory -match ".*\\scripts$" -and $ParentDirectory -match ".*\\AutomatedBackUp$") {
    cd ..
} else {
    write-host "INCORRECT DIRECTORY --> PLEASE GO TO \AutomatedBackUp\scripts TO EXECUTE" -foregroundcolor red
    return #stops execution
}


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
py .\copy_function.py

write-host "YAY!!! FINISHED"
deactivate