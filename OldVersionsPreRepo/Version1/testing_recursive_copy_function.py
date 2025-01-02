import directories
import os
import shutil
import datetime
from colorama import Fore, Style, init
import time

def get_last_modified_time(file_path: str, time_threshold: int) -> bool:
    # Get the last modified time of the file
    timestamp = os.path.getmtime(file_path)
    # Convert the timestamp to a readable format
    last_modified_time = datetime.datetime.fromtimestamp(timestamp)
    # return last_modified_time.strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.now()
    threshold_time = current_time - datetime.timedelta(minutes=time_threshold)

    return last_modified_time >= threshold_time

def list_files_in_directory(directory_path: str,threshold_time: int) -> list:
    """
    Lists all files in the given directory.
    
    Old Returns list like this: ['testfile.txt','testfile2.txt']
    New Returns list like this: ['C:\\Users\\mike\\AutomatedBackUpTest\\Source_Files\\testfile.txt','C:\\Users\\mike\\AutomatedBackUpTest\\Source_Files\\testfile2.txt']
    """
    files_list = []

    # Iterate through all the files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            if get_last_modified_time(file_path,threshold_time):
                # files_list.append(file_name)
                files_list.append(file_path)
        elif os.path.isdir(file_path):
            files_list.extend(list_files_in_directory(file_path,threshold_time))

    return files_list

def copy_files(
                src_directory: str
               ,dest_directory: str
               ,files_to_transfer: list[str]
               ) -> None:

    for src_file in files_to_transfer:
        file_name = os.path.basename(src_file)
        time.sleep(0.5)
    # for file_name in files_to_transfer:

        if not os.path.isfile(src_file):
            print(f"{file_name} does not exist in the source directory.")
            continue
        
        init(autoreset=True) # Resets the font color after each print

        try:
            #shutil.copy(src_file_path, dest_file_path)
            print(f"{Fore.GREEN}Copying: {src_file} to {dest_directory}")
        except Exception as e:
            print(f"{Fore.RED}Error copying {file_name}: {e}")

def main():
    src_directory = directories.SOURCE
    dest_directory = directories.DESTINATION
    init(autoreset=True)
    print(f"Searching {Fore.LIGHTBLUE_EX}{src_directory}{Style.RESET_ALL} for files to copy to {Fore.LIGHTBLUE_EX}{dest_directory}")
    files_to_transfer = list_files_in_directory(src_directory,threshold_time=500) #500 minutes
    print(f"Found {len(files_to_transfer)} files to copy to {Fore.LIGHTBLUE_EX}{dest_directory}")
    print(f"Beginning execution for {len(files_to_transfer)} files...")

    # print(files_to_transfer)
    # for file_name in files_to_transfer:
    #     src_file_path = os.path.join(src_directory, file_name)
    #     dest_file_path = os.path.join(dest_directory, file_name)
    #     print(f"{src_file_path} | {dest_file_path}\n")

    copy_files(
                src_directory=src_directory
                ,dest_directory=dest_directory
                ,files_to_transfer=files_to_transfer
                )
    print(f"{len(files_to_transfer)} files moved from {src_directory} to {dest_directory}")

if __name__ == "__main__":
    main()
