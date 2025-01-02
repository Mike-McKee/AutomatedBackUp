import directories
import os
import shutil
import datetime
from colorama import Fore, Style, init
import time
import wrappers

"""
TO DO:
------
Make script iterate detect subdirectories and create them in the new destination...
"""
init(autoreset=True)

def get_last_modified_time(file_path: str, time_threshold: int) -> bool:
    # Get the last modified time of the file
    timestamp = os.path.getmtime(file_path)
    # Convert the timestamp to a readable format
    last_modified_time = datetime.datetime.fromtimestamp(timestamp)
    # return last_modified_time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.now()
    threshold_time = current_time - datetime.timedelta(minutes=time_threshold)

    return last_modified_time >= threshold_time

def CreateDirectory (NewDirectory: str,DestinationPath: str) -> None:
    try:
        NewDirectoryPath = os.path.join(DestinationPath,NewDirectory)
        os.makedirs(NewDirectoryPath,exist_ok=True)
        print(f"{Fore.CYAN}Creating New Directory {NewDirectory} in {DestinationPath} - {Fore.LIGHTGREEN_EX}SUCCESS")
    except Exception as e:
        raise RuntimeError(f"Error Creating Directory {NewDirectory}: {e}")

def list_files_in_directory(directory_path: str
                           ,DestinationPath: str
                           ,threshold_time: int
                           ,ParentDir: str = None) -> dict:
    """
    Lists all files in the given directory.

    Parameters:
    -----------
    directory_path = the directory we begin our search in
    DestinationPath = location we need to create new directories
    threshold_time = how far back to look for items to copy (based on modified by date)
    ParentDir = for subdirectories so we can add their full path when creating directories
    
    Old Returns list like this: ['testfile.txt','testfile2.txt']
    Old Returns list like this: ['C:\\Users\\mike\\AutomatedBackUpTest\\Source_Files\\testfile.txt','C:\\Users\\mike\\AutomatedBackUpTest\\Source_Files\\testfile2.txt']
    """
    # files_list = []
    ObjectsToCreate = {
                        "files_list": [],
                        "directories_list": []
                       }
    
    # Iterate through all the files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        ParentDirectory = None
        if os.path.isfile(file_path) and ParentDir is None:
            if threshold_time is None:
                ObjectsToCreate["files_list"].append(file_name)
            elif get_last_modified_time(file_path,threshold_time):
                ObjectsToCreate["files_list"].append(file_name)

        elif os.path.isfile(file_path) and ParentDir is not None:
            if threshold_time is None or get_last_modified_time(file_path,threshold_time):
                ObjectsToCreate["files_list"].append(os.path.join(ParentDir,file_name))

        elif os.path.isdir(file_path) and ParentDir is None:
            CreateDirectory(NewDirectory=file_name,DestinationPath=DestinationPath)
            ObjectsToCreate["directories_list"].append(file_path)

            RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=file_name)
            ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])

        elif os.path.isdir(file_path) and ParentDir is not None:
            ParentDirectory = os.path.join(ParentDir,file_name)
            CreateDirectory(NewDirectory=ParentDirectory,DestinationPath=DestinationPath)
            ObjectsToCreate["directories_list"].append(file_path)

            RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=ParentDirectory)
            ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])
            
    return ObjectsToCreate

def main():
    src_directory = directories.SOURCE
    dest_directory = directories.DESTINATION
    search_time_threshold = None #This allows us to test without placing time constraint on search

    FilesToTransfer = []
    DirectoriesToAdd = []
    for file in src_directory:
        ObjectsToAdd = list_files_in_directory(file,dest_directory,search_time_threshold)
        # print(ObjectsToAdd)
        FilesToTransfer.extend(ObjectsToAdd["files_list"])
        DirectoriesToAdd.extend(ObjectsToAdd["directories_list"])

    print("Files To Transfer")
    print("-----------------")
    print(FilesToTransfer)
    print("\n")
    print("Directories To Add")
    print("------------------")
    print(DirectoriesToAdd)
    

if __name__ == "__main__":
    main()