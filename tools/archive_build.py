import os
import re
import platform
import sys
import tarfile
import zipfile


version_re = re.compile(r"^__version__ = \"(.*)\"$", re.I)


def create_archive(folder_path: str) -> int:
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a directory.")
        return 1

    version = get_version()
    if platform.system() == "Windows":
        return create_archive_windows(folder_path, version)
    elif platform.system() == "Linux":
        return create_archive_linux(folder_path, version)
    else:
        raise NotImplementedError(f"OS not supported: {platform.system()}")


def create_archive_windows(folder_path: str, version: str) -> int:
    zip_file = f"{folder_path}_{version}_win.zip"

    if os.path.isfile(zip_file):
        print(f"{zip_file} already exists.")
        return 1

    with zipfile.ZipFile(zip_file, 'w') as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname=rel_path)
    return 0


def create_archive_linux(folder_path: str, version: str) -> int:
    tar_file = f"{folder_path}_{version}_linux.tar.gz"

    if os.path.isfile(tar_file):
        print(f"{tar_file} already exists.")
        return 1

    with tarfile.open(tar_file, 'w:gz') as tf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                tf.add(full_path, arcname=rel_path)
    return 0


def get_version() -> str:
    tools_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.dirname(tools_dir)
    version_file = os.path.join(project_dir, "__version__.py")

    with open(version_file, 'r') as fp:
        line = fp.read().strip()

    match = version_re.match(line)
    version = match.group(1)

    return version


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(1)
    sys.exit(create_archive(folder_path=sys.argv[1]))
