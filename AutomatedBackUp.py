# import directories
import os
import shutil
import datetime
from colorama import Fore, Style, init
import time
from CustLogger import CustLogger
import json
import traceback
import math

# Initialize Logger
# CurrentDir = os.getcwd()
# Location = os.path.join(CurrentDir,'log')
# logger = CustLogger(LogLocation=Location)
# logger.InitLogDir()
logger = CustLogger()

def get_last_modified_time(file_path: str, time_threshold: int) -> bool:
    # Get the last modified time of the file
    timestamp = os.path.getmtime(file_path)
    # Convert the timestamp to a readable format
    last_modified_time = datetime.datetime.fromtimestamp(timestamp)
    # return last_modified_time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.now()
    threshold_time = current_time - datetime.timedelta(minutes=time_threshold)

    return last_modified_time >= threshold_time

def CreateDirectory (NewDirectory: str,DestinationPath: str = None) -> None:
    try:
        if DestinationPath is not None:
            NewDirectoryPath = os.path.join(DestinationPath,NewDirectory)
            os.makedirs(NewDirectoryPath,exist_ok=True)
            print(f"{Fore.CYAN}Creating New Directory {NewDirectory} in {DestinationPath} - {Fore.LIGHTGREEN_EX}SUCCESS")

            InfoMessge = f"Creating New Directory {NewDirectory} in {DestinationPath} - SUCCESS"
            logger.log(type="info",Message=InfoMessge)
        else: #If no DestinationPath is given, we assume FullPath (including Destination) is provided
            os.makedirs(NewDirectory,exist_ok=True)
            print(f"{Fore.CYAN}Creating New Directory {NewDirectory} - {Fore.LIGHTGREEN_EX}SUCCESS")

            InfoMessge = f"Creating New Directory {NewDirectory} - SUCCESS"
            logger.log(type="info",Message=InfoMessge)
    except Exception as e:
        ErrorMessage = f"Error Creating Directory {NewDirectory}: {e}\n\t{traceback.format_exc().replace("\n","\n\t")}"
        logger.log(type="error",Message=ErrorMessage)
        raise RuntimeError(ErrorMessage)

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
    try:
        ObjectsToCreate = {
                            "files_list": [],
                            "directories_list": []
                        }
        
        # Iterate through all the files in the directory
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            
            DirPathBaseName = os.path.basename(directory_path)
            # print(DirPathBaseName)

            # ParentDirectory = None # May need to add this back in...
            if os.path.isfile(file_path) and ParentDir is None:
                if threshold_time is None or get_last_modified_time(file_path,threshold_time):
                    ObjectsToCreate["files_list"].append(file_name)

            elif os.path.isfile(file_path) and ParentDir is not None:
                if threshold_time is None or get_last_modified_time(file_path,threshold_time):
                    ObjectsToCreate["files_list"].append(os.path.join(ParentDir,file_name))

            # elif os.path.isdir(file_path) and ParentDir is None:
            #     ObjectsToCreate["directories_list"].append(file_name)

            #     RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=file_name)
            #     ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            #     ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])

            # elif os.path.isdir(file_path) and ParentDir is not None:
            #     ParentDirectory = os.path.join(ParentDir,file_name)

            #     ObjectsToCreate["directories_list"].append(os.path.join(ParentDir,file_name))

            #     RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=ParentDirectory)
            #     ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
            #     ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])

            elif os.path.isdir(file_path):
                if ParentDir is None:
                    ParentDirectory = file_name
                    ObjectsToCreate["directories_list"].append(file_name)
                else:
                    ParentDirectory = os.path.join(ParentDir,file_name)
                    ObjectsToCreate["directories_list"].append(os.path.join(ParentDir,file_name))
                
                RecursiveRun = list_files_in_directory(file_path,DestinationPath,threshold_time,ParentDir=ParentDirectory)
                ObjectsToCreate["files_list"].extend(RecursiveRun["files_list"])
                ObjectsToCreate["directories_list"].extend(RecursiveRun["directories_list"])

                
        return ObjectsToCreate
    
    except Exception as e:
        ErrorMessage = f"{e}\n\t{traceback.format_exc().replace("\n","\n\t")}"
        logger.log(type="error",Message=ErrorMessage)

def copy_files(
                src_directory: str
               ,dest_directory: str
               ,files_to_transfer: list[str]
               ) -> None:
    
    init(autoreset=True) # Resets the font color after each print

    TotalObjects = len(files_to_transfer)

    for FileNum,src_file in enumerate(files_to_transfer,1):
        file_name = os.path.basename(src_file)

        if not os.path.isfile(os.path.join(src_directory,src_file)):
            print(f"{file_name} does not exist in the source directory.")
            continue

        try:
            # shutil.copy() parameters must be full path
            FileSourcePath = os.path.join(src_directory,src_file)
            FileDestinationPath = os.path.join(dest_directory,src_file)
            # print(FileSourcePath)
            # print(FileDestinationPath)
            shutil.copy(FileSourcePath,FileDestinationPath) #UNCOMMENT TO ACTUALLY COPY FILES
            print(f"{Fore.GREEN}Copying ({FileNum} of {TotalObjects}): {src_file} to {dest_directory}")

            # Log actions
            InfoMessage = f"Copying ({FileNum} of {TotalObjects}): {src_file} to {dest_directory}"
            logger.log(type="info",Message=InfoMessage)
        except Exception as e:
            ErrorMessage = f"Error copying {file_name}: {e}\n\t{traceback.format_exc().replace("\n","\n\t")}"
            logger.log(type="error",Message=ErrorMessage)
            print(f"{Fore.RED}Error copying {file_name}: {e}")

def main():
    try:
        with open("config.json","r") as DirFiles:
            directories = json.load(DirFiles)

        src_directory = directories["source"]
        dest_directory = directories["destination"]
        
        #If we select a time threshold, make sure it's in minutes
        if directories["LastExecution"]:
            LastExecutionDate = datetime.datetime.strptime(directories["LastExecution"],"%Y-%m-%d %H:%M:%S")
            TimeDifference = datetime.datetime.now() - LastExecutionDate
            search_time_threshold = math.ceil(TimeDifference.total_seconds() /60)
        else:
            search_time_threshold = None #This allows us to test without placing time constraint on search

        init(autoreset=True)
        print(f"Searching for files to copy to {Fore.LIGHTBLUE_EX}{dest_directory}")
        print(f"Found {Fore.LIGHTBLUE_EX}{len(src_directory)}{Style.RESET_ALL} directories to search...\n")
        
        SrcDirBaseNames = [os.path.basename(Dir) for Dir in src_directory]

        FilesToCopy = {}
        # print(src_directory)
        for directory in src_directory:
            # Printint Directory name for each we search
            print(f"\tSearching {directory} for files...")
            ObjectsToCreate = list_files_in_directory(directory_path=directory
                                                ,DestinationPath=dest_directory
                                                ,threshold_time=search_time_threshold
                                                ,ParentDir=None)
            FilesToCopy[directory] = ObjectsToCreate
        print("\n")
        
        # print(FilesToCopy)

        # ***Now we have to iterate through dictionary and copy files/create directionries
        for key in FilesToCopy:
            # print(FilesToCopy[key])
            ObjectsToCreate = FilesToCopy[key]
            FilesToTransfer = ObjectsToCreate["files_list"]
            DirectoriesToAdd = ObjectsToCreate["directories_list"]

            # # Print Messages for how many files we have to transfer and directories we have to add
            print(f"Found {len(FilesToTransfer)} files in {key} to copy to {Fore.LIGHTBLUE_EX}{dest_directory}")
            
            if len(DirectoriesToAdd) > 0:
                print(f"Found {len(DirectoriesToAdd)} directories in {key} to create in {Fore.LIGHTBLUE_EX}{dest_directory}")
            else:
                pass
        
            print(f"Executing - Creating {len(DirectoriesToAdd)} new directories from {key}...")

            # Here will need logic in future to initially check if the ParentDir already exists...
            # "key" is our source directory. So take the basename and create that directory in our destination
            ParentDirToCreate = os.path.join(dest_directory,os.path.basename(key))
            if not os.path.exists(ParentDirToCreate):
                CreateDirectory(NewDirectory=ParentDirToCreate,DestinationPath=None)

            # First, let's create the new directories
            for DirectoryToAdd in DirectoriesToAdd:
                if not os.path.exists(os.path.join(ParentDirToCreate,DirectoryToAdd)):
                    CreateDirectory(NewDirectory=DirectoryToAdd,DestinationPath=ParentDirToCreate)
            
            print(f"Executing - Copying {len(FilesToTransfer)} files from {key}...")

            # Now, let's copy the files to our destination directory
            copy_files(src_directory=key,dest_directory=ParentDirToCreate,files_to_transfer=FilesToTransfer)

        # Change the "LastExecution" value in config.json to represent the current date/time
        directories["LastExecution"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("config.json","w") as DirFiles:
            json.dump(directories,DirFiles,indent=4)

    except Exception as e:
        # Traceback library allows us to log the full error message. Similarily to the error message that normally shows up in the terminal
        # Replace() function allows us to indent every new line in traceback.formate_exc()
        ErrorMessage = f"{e}\n\t{traceback.format_exc().replace("\n","\n\t")}"
        logger.log(type="error",Message=ErrorMessage)

if __name__ == "__main__":
    init(autoreset=True)
    main()

