import json
import os


with open("settings.json", "r") as file:
    settings = json.load(file)


def check_start_dirs() -> bool:
    if os.path.isdir(settings['input_dir']) and os.path.isdir(settings['output_dir']):
        return True
    else:
        return False


def get_input_files() -> list:
    dir_path = settings['input_dir']

    files_name = [
        f for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f)) and not f.startswith(".")
    ]

    print(files_name)

    return files_name


def sorting_ulp_list(file_name: str) -> list:
    sorted_list: list = []

    tmp = False
    print(f"{settings["input_dir"]}/{file_name}")
    with open(f"{settings["input_dir"]}/{file_name}", "r", encoding="utf-8", errors="replace") as file:
        with open(f"{settings["bad_tlds_list"]}", "r", encoding="utf-8") as bad_tlds:
            bad_tlds = bad_tlds.readlines()

            lines = file.readlines()

            for line in lines:
                line = line.strip()
                for ue in settings["useful_endpoints"]:
                    if ue in line:
                        tmp = True
                        for i in bad_tlds:
                            if f"{i.strip()}." in line \
                                    or f"{i.strip()}/" in line \
                                    or f"{i.strip()}\\" in line \
                                    or "localhost" in line \
                                    or "[NOT_SAVED]" in line:
                                tmp = False
                                break
                        break
                if tmp:
                    sorted_list.append(line)
                    tmp = False
    return sorted_list


def save_list(sorted_list: list,
              restrictions: int = settings["restrictions_lines_per_one_file"]) -> bool:
    try:
        for name in os.listdir(settings["output_dir"]):
            file_path = os.path.join(settings["output_dir"], name)
            if os.path.isfile(file_path):
                if ".gitkeep" not in name:
                    os.remove(file_path)


        index: int = 0

        for i in range(0, len(sorted_list), restrictions):
            with open(f"{settings['output_dir']}/Out_{index}.txt", "w", encoding="utf-8") as file:
                for sorted_line in sorted_list[i:i + restrictions]:
                    file.write(sorted_line + "\n")
            index += 1

        return True
    except:
        return False



