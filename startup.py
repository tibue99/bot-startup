import os
import time
import subprocess
import io

print("\nDeleting old sessions...")
os.system("tmux kill-server")

print("Starting new sessions...")
print("----------------------------------")
time.sleep(5)

names = []


def run(path):
    name = path.split("/")[-1]

    os.system(f"tmux new -d -s '{name}'")
    os.system(f"tmux send-keys 'cd {path}' C-m")
    os.system(f"tmux send-keys 'python3 main.py' C-m")
    names.append(name)


home = "../home/"


for dir1 in os.listdir(home):
    if "main.py" not in os.listdir(home + dir1):
        print(f"Info: Detected {dir1} as subfolder")
        for dir2 in os.listdir(home + dir1):  # iterate through subfolder
            if "main.py" not in os.listdir(home + dir1 + "/" + dir2):
                print(f"Warning: Detected empty subfolder: {dir1}/{dir2}")
            else:
                run(dir1 + "/" + dir2)
    else:
        run(dir1)


print("----------------------------------")
time.sleep(2)
for name in names:
    found_result = False
    result = subprocess.run(['tmux', 'capture-pane', '-pt', name, '-S', '3', '-E', '10'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    for line in io.StringIO(output):
        if "Error" in line:
            print(f"Error for {name}: {line}")
            found_result = True
            break
        elif "online" in line:
            print(f"Success:", line)
            found_result = True
            break

    if not found_result:
        print(f"Error: Could not start {name}")
