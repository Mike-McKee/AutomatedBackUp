import directories
import os
import shutil
import datetime

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

SOURCE = 'C:\\Users\\mike\\AutomatedBackUpTest\\Source_Files'

print(list_files_in_directory(SOURCE,threshold_time=500))
