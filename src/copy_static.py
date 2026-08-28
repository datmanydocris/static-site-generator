import os
import shutil


def copy_directory(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    for name in os.listdir(src):
        from_path = os.path.join(src, name)
        to_path = os.path.join(dest, name)
        print(f"Copying {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_directory(from_path, to_path)