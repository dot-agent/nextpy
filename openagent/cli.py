import subprocess
import sys

def main():
    if len(sys.argv) > 3 and sys.argv[1] == "run" and sys.argv[2] == "--ui":
        command = ["python", "-m", "openagent.ui.run"] + sys.argv[3:]
        subprocess.run(command)
    else:
        print("Invalid command. Usage: openagent run --ui <file.py>")

if __name__ == "__main__":
    main()