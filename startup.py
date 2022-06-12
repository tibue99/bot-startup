import os
import io
import time
import subprocess

import config


names = []
home = config.bot_directory
main_file = config.main


def wait(sec):
    txt = "" if sec == 0 else "----------------------------------"
    print(txt)
    time.sleep(sec)


def kill_sessions():
    print("\nDeleting old sessions...")
    os.system("tmux kill-server")


def run(path, subdir=None):
    session_name = path.split("/")[-1]
    if subdir is not None:
        session_name = f"{subdir[0].lower()}_{session_name}"

    os.system(f"tmux new -d -s '{session_name}'")
    os.system(f"tmux send-keys 'cd {home + path}' C-m")
    os.system(f"tmux send-keys 'python3 {main_file}' C-m")
    names.append(session_name)


def iterate_directory():
    print("Starting new sessions...\n")

    for dir1 in os.listdir(home):
        if main_file not in os.listdir(home + dir1):
            print(f"Info: Detected {dir1} as subdirectory")
            for dir2 in os.listdir(home + dir1):
                subdir_path = home + dir1 + "/" + dir2
                if not os.path.isdir(subdir_path):  # subdirectory should only contain directories, not files
                    continue

                if main_file not in os.listdir(subdir_path):
                    print(f"Warning: Detected directory without main file: {dir1}/{dir2}")
                else:
                    run(dir1 + "/" + dir2, dir1)
        else:
            run(dir1)


def check_success():
    print("Checking sessions...\n")
    for name in names:
        found_result = False
        result = subprocess.run(['tmux', 'capture-pane', '-pt', name, '-S', '1', '-E', '30'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        for line in io.StringIO(output):
            line = line.split("\n")[0]
            if "Error" in line:
                print(f"Error ({name}): {line}")
                found_result = True
                break
            elif "online" in line:
                print(f"Success ({name}):", line)
                found_result = True
                break

        if not found_result:
            print(f"Error ({name}): Could not start bot")


if __name__ == "__main__":
    kill_sessions()
    wait(2)

    iterate_directory()
    wait(5)

    check_success()
    wait(0)
