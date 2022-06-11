import os
import time
import subprocess
import io

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


def run(path):
    session_name = path.split("/")[-1]

    os.system(f"tmux new -d -s '{session_name}'")
    os.system(f"tmux send-keys 'cd {path}' C-m")
    os.system(f"tmux send-keys 'python3 {main_file}' C-m")
    names.append(session_name)


def iterate_folders():
    print("Starting new sessions...")

    for dir1 in os.listdir(home):
        if main_file not in os.listdir(home + dir1):
            print(f"Info: Detected {dir1} as subfolder")
            for dir2 in os.listdir(home + dir1):  # subfolder
                if main_file not in os.listdir(home + dir1 + "/" + dir2):
                    print(f"Warning: Detected empty subfolder: {dir1}/{dir2}")
                else:
                    run(dir1 + "/" + dir2)
        else:
            run(dir1)


def check_success():
    print("Checking success...")
    for name in names:
        found_result = False
        result = subprocess.run(['tmux', 'capture-pane', '-pt', name, '-S', '3', '-E', '10'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        for line in io.StringIO(output):
            if "Error" in line:
                error = line.split("\n")[0]
                print(f"Error ({name}): {error}")
                found_result = True
                break
            elif "online" in line:
                print(f"Success:", line)
                found_result = True
                break

        if not found_result:
            print(f"Error ({name}): Could not start main file")


if __name__ == "__main__":
    kill_sessions()
    wait(2)

    iterate_folders()
    wait(3)

    check_success()
    wait(0)
