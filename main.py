from utils import *
import json
from colorama import init, Fore
init(autoreset=True)


with open("settings.json", "r") as file:
    settings = json.load(file)


def run():
    input("==Any button for start==")

    if not check_start_dirs():
        print(f"==Directories not found "
              f"{Fore.RED}{{{settings['input_dir']}{Fore.RESET}"
              f" or {Fore.RED}{settings['output_dir']}}}{Fore.RESET}==")
        input("==Any button for exit==")
        return 0

    files_name: list = get_input_files()
    if not files_name:
        print(Fore.RED + "==Input files not found==")
        input("==Any button for exit==")
        return 0

    sorted_list: list = []
    for i in range(len(files_name)):
        sorted_list.extend(sorting_ulp_list(files_name[i]))
        if not sorted_list:
            print(f"{Fore.RED}=={files_name[i]} is empty==")
            input("==Any button for exit==")
            return 0

        if len(sorted_list) >= settings["restrictions_lines_per_one_file"] \
            or i == len(files_name) - 1:

            if not save_list(sorted_list):
                print(f"{Fore.RED}=={i} save error==")
                input("==Any button for exit==")
                return 0

            sorted_list: list = []

    print(Fore.GREEN + "==All done!==")
    input("==Any button for exit==")
    return 0

if __name__ == '__main__':
    run()