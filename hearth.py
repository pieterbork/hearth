from os.path import expanduser
import configparser
import argparse
import subprocess
import shutil
import sys
import os

def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except:
        print("Cannot create {}".format(hearth_home))
        sys.exit(1)

def get_args():
    parser = argparse.ArgumentParser(description='Bring your dotfiles to you.')
    parser.add_argument('repo', help='Either a github link or simply "local"')
    args = parser.parse_args()
    return args

def get_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except:
        print("Cannot read config file: {}".format(config_file))
        sys.exit(1)
    return config

def save_config(config_file, config):
    with open(config_file, 'w') as cf:
        config.write(cf)

def get_dotfiles(proj_home, ignores):
    files = os.listdir(proj_home)
    dotfiles = [f for f in files if f not in ignores and f.startswith('.')]
    return dotfiles

def parse_github_link(link):
    git_parts = link.split('/')
    git_user = git_parts[-2]
    proj_name = git_user + "_" + git_parts[-1].strip(".git") + "/"
    return proj_name

def download_repo(repo, proj_home):
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

def initialize_hearth(hearth_home, repo):
    if not os.path.isdir(hearth_home):
        create_dir(hearth_home)

    if not repo:
        print("No repo provided!")
        sys.exit(1)

    backup_time = False
    local_backup = hearth_home + "local_backup/"
    if not os.path.isdir(local_backup):
        create_dir(local_backup)
        backup_time = True
    return backup_time

def delete_all(files, path=None):
    if isinstance(files, str):
        files = [files]
    for f in files:
        loc = f
        if path:
            loc = path + f 
        print("Deleting {}".format(loc))
        if os.path.isdir(loc):
            shutil.rmtree(loc)
        else:
            os.remove(loc)

def main():
    args = get_args()
    config = get_config('hearth.cfg')

    home = expanduser("~") + "/"
    hearth_home = home + ".hearth/"
    local_backup = hearth_home + "local_backup/"
    backup_time = initialize_hearth(hearth_home, args.repo)

    if args.repo == "local":
        proj_home = local_backup
    else:
        proj_name = parse_github_link(args.repo)
        proj_home = hearth_home + proj_name
        download_repo(args.repo, proj_home)

    ignores = config['DEFAULT']['ignores']

    old_proj = config.get('current', 'repo', fallback=None)
    if old_proj:
        dotfiles = get_dotfiles(old_proj, ignores)
        delete_all(dotfiles, home)

    dotfiles = get_dotfiles(proj_home, ignores)
    for f in dotfiles:
        src = proj_home + f
        dst = home + f
        if backup_time:
            backup_path = local_backup + f
            try:
                shutil.move(dst, backup_path)
                print("Backed up {} to {}".format(dst, backup_path))
            except:
                pass
        print("Copying {} to {}".format(src, dst))
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dst)
            except:
                print("Could not copy {}".format(src))
        else:
            shutil.copyfile(src, dst)

    if proj_home == local_backup:
        delete_all(local_backup)
        if old_proj:
            config.remove_option('current', 'repo')
            save_config('hearth.cfg', config)
    else:
        config.set('current', 'repo', proj_home)
        save_config('hearth.cfg', config)

if __name__ == "__main__":
    main()
