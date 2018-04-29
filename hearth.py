from os.path import expanduser
import subprocess
import shutil
import sys
import os

ignores = ['.git', '.gitignore']

repo = sys.argv[1]
home = expanduser("~") + "/"

hearth_home = home + ".hearth/"
if not os.path.isdir(hearth_home):
    try:
        os.makedirs(hearth_home)
    except:
        print("Cannot create {}".format(hearth_home))
        sys.exit(1)

backup_time = False
local_backup = hearth_home + "local_backup/"
if not os.path.isdir(local_backup):
    try:
        os.makedirs(local_backup)
        backup_time = True
    except:
        print("Cannot create {}".format(local_backup))
        sys.exit(1)

if repo == "local":
    proj_home = local_backup
else:
    git_parts = repo.split('/')
    git_user = git_parts[-2]
    proj_name = git_parts[-1].strip(".git")
    proj_home = hearth_home + git_user + "_" + proj_name + "/"
    reset = True
    if os.path.isdir(proj_home):
        reset = input('Directory exists, redownload? (y/n):  ')
        if reset.lower() == "y":
            shutil.rmtree(proj_home)
        else:
            reset = False

    if reset:
        git_cmd = "git clone {} {}".format(repo, proj_home)
        p = subprocess.Popen(git_cmd, shell=True)
        p.wait()

files = os.listdir(proj_home)
dotfiles = [f for f in files if f not in ignores and not os.path.isdir(f)]
for f in dotfiles:
    src = proj_home + f
    dst = home + f
    if backup_time:
        backup_path = local_backup + f
        print("Backing up {} to {}".format(dst, backup_path))
        os.rename(dst, backup_path)
    print("Copying {} to {}".format(src, dst))
    shutil.copyfile(src, dst)

