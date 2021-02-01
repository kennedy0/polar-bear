import os
import sys
import zipfile


def create_archive(folder_path: str) -> int:
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a directory.")
        return 1

    zip_file = f"{folder_path}.zip"
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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(1)
    sys.exit(create_archive(folder_path=sys.argv[1]))
