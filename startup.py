import os
import time


os.system("tmux kill-server")
time.sleep(5)


def run(path):
    name = path.split("/")[-1]

    os.system(f"tmux new -d -s '{name}'")
    os.system(f"tmux send-keys 'cd {path}' C-m")
    os.system(f"tmux send-keys 'python3 main.py' C-m")
    print(f"Started {path}")


home = "../home/"


for dir1 in os.listdir(home):
    if "main.py" not in os.listdir(home + dir1):
        print(f"No main.py in {dir1}")
        for dir2 in os.listdir(home + dir1):  # iterate through subfolder
            if "main.py" not in os.listdir(home + dir1 + "/" + dir2):
                print(f"No main.py in {dir1}/{dir2}")
            else:
                run(dir1 + "/" + dir2)
    else:
        run(dir1)
