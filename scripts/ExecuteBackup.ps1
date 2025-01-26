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