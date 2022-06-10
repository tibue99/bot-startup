import os
import time

print("\nDeleting old sessions...")
os.system("tmux kill-server")

print("Starting new sessions...")
print("----------------------------------")
time.sleep(5)


def run(path):
    name = path.split("/")[-1]

    os.system(f"tmux new -d -s '{name}'")
    os.system(f"tmux send-keys 'cd {path}' C-m")
    result = os.system(f"tmux send-keys 'python3 main.py' C-m")

    if result == 0:
        print(f"Successfully started {path}")
    else:
        print(f"Error: Could not start {path}")


home = "../home/"


for dir1 in os.listdir(home):
    if "main.py" not in os.listdir(home + dir1):
        print(f"Detected {dir1} as subfolder")
        for dir2 in os.listdir(home + dir1):  # iterate through subfolder
            if "main.py" not in os.listdir(home + dir1 + "/" + dir2):
                print(f"Warning: Detected empty subfolder: {dir1}/{dir2}")
            else:
                run(dir1 + "/" + dir2)
    else:
        run(dir1)
