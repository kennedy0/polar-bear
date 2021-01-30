import os
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UI_DIR = os.path.join(PROJECT_DIR, "ui")
PY_DIR = os.path.join(PROJECT_DIR, "gui")


def main():
    for file in os.listdir(UI_DIR):
        src = os.path.join(UI_DIR, file)
        dst = os.path.join(PY_DIR, file.replace(".ui", ".py"))
        print(f"compiling {dst}")
        cmd = ['python', '-m', 'PyQt5.uic.pyuic', '-x', src, '-o', dst]
        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
