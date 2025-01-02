import os
import directories
from colorama import Fore, Style, init

init(autoreset=True)

def CreateDirectory (NewDirectory: str,DestinationPath: str) -> None:
    NewDirectoryPath = os.path.join(DestinationPath,NewDirectory)
    os.makedirs(NewDirectoryPath,exist_ok=True)
    print(f"{Fore.CYAN}Creating New Directory {NewDirectory} in {DestinationPath} - {Fore.LIGHTGREEN_EX}SUCCESS")

def main():
    NewDirectoriesToCreate = ['TestDir1','TestDir2','TestDir3','TestDir4']
    Destination = directories.DESTINATION
    for path in NewDirectoriesToCreate:
        CreateDirectory(NewDirectory=path,DestinationPath=Destination)

if __name__ == '__main__':
    main()