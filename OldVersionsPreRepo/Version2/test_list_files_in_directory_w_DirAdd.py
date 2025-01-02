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
    NewDirectoryPath = os.path.join(DestinationPath,NewDirectory)
    os.makedirs(NewDirectoryPath,exist_ok=True)
    print(f"{Fore.CYAN}Creating New Directory {NewDirectory} in {DestinationPath} - {Fore.LIGHTGREEN_EX}SUCCESS")

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
        ActionStep = None
        if os.path.isfile(file_path) and ParentDir is None:
            ActionStep = 1
            print(f"Action Step = {ActionStep}")
            if threshold_time is None:
                ObjectsToCreate["files_list"].append(file_name)
            elif get_last_modified_time(file_path,threshold_time):
                ObjectsToCreate["files_list"].append(file_name)

            #For testing purposes...
            print(f"Current file_name = {file_name}")
            print(f"Current file type = {'file' if os.path.isfile(file_path) else 'dir'}")
            print("Current ObjectsToCreate values...")
            print(ObjectsToCreate)
            print("\n")

        elif os.path.isfile(file_path) and ParentDir is not None:
            ActionStep = 2
            print(f"Action Step = {ActionStep}")
            if threshold_time is None or get_last_modified_time(file_path,threshold_time):
                ObjectsToCreate["files_list"].append(os.path.join(ParentDir,file_name))
            # elif get_last_modified_time(file_path,threshold_time):
            #     ObjectsToCreate["files_list"].append(os.path.join(ParentDir,file_name))

            #For testing purposes...
            print(f"Current file_name = {file_name}")
            print(f"Current file type = {'file' if os.path.isfile(file_path) else 'dir'}")
            print("Current ObjectsToCreate values...")
            print(ObjectsToCreate)
            print("\n")

        elif os.path.isdir(file_path) and ParentDir is None:
            ActionStep = 3
            print(f"Action Step = {ActionStep}")
            # CreateDirectory(NewDirectory=file_name,DestinationPath=DestinationPath)
            ObjectsToCreate["directories_list"].append(file_path)
            print(f"\tfile_path = {file_path}")

            #For testing purposes...
            print(f"Current file_name = {file_name}")
            print(f"Current file type = {'file' if os.path.isfile(file_path) else 'dir'}")
            print("Current ObjectsToCreate values...")
            print(ObjectsToCreate)
            print("\n")

            RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=file_name)
            ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])

        elif os.path.isdir(file_path) and ParentDir is not None:
            ActionStep = 4
            print(f"Action Step = {ActionStep}")
            # CreateDirectory(NewDirectory=file_name,DestinationPath=DestinationPath)
            # print("FOR loop Scenario 4")
            # print(f"\tfile_name = {file_name}")
            print(f"\tfile_path = {file_path}")
            # print(f"\tParentDir = {ParentDir}")
            # print(f"\tParentDirectory = {ParentDirectory}")
            # print(f"\tos.path.join(ParentDir,file_name) = {os.path.join(ParentDir,file_name)}")
            # print(f"\tos.path.join(directory_path,file_name) = {os.path.join(directory_path,file_name)}")
            
            # ObjectsToCreate["directories_list"].append(os.path.join(ParentDir,file_name))
            # print(f"\tBefore adding file_path to ObjectsToCreate...")
            # print(ObjectsToCreate["directories_list"])
            # print(f"\t\tfile_path = {file_path}")
            # print("\tAfter adding file_path ot ObjectsToCreate")
            # print(ObjectsToCreate["directories_list"])
            ParentDirectory = os.path.join(ParentDir,file_name)
            ObjectsToCreate["directories_list"].append(file_path)

            #For testing purposes...
            print(f"Current file_name = {file_name}")
            print(f"Current file type = {'file' if os.path.isfile(file_path) else 'dir'}")
            print("Current ObjectsToCreate values...")
            print(ObjectsToCreate)
            print("\n")

            RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=ParentDirectory)
            ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])
            
    return ObjectsToCreate

def main():
    src_directory = directories.SOURCE
    dest_directory = directories.DESTINATION
    search_time_threshold = None #This allows us to test without placing time constraint on search
    filelist = src_directory[0]
    for item in os.listdir(filelist):
        print(item)
    
    print("\n\n")
    for file in src_directory:
        print(f"file = {file}")
        ObjectsToAdd = list_files_in_directory(file,dest_directory,search_time_threshold)
        print(ObjectsToAdd)
    # print(FilesToTransfer)
    # print(DirectoriesToAdd)
    

if __name__ == "__main__":
    main()