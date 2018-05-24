#!/usr/bin/env python3

from os.path import expanduser
import configparser
import argparse
import subprocess
import shutil
import sys
import os

HOME = expanduser("~") + "/"
CONFIG_NAME = 'hearth.cfg'
CONFIG_FILE = HOME + ".hearth/" + CONFIG_NAME

def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except:
        print("Cannot create {}".format(hearth_home))
        sys.exit(1)

def get_args():
    parser = argparse.ArgumentParser(description='Bring your dotfiles to you.')
    parser.add_argument('operation', help='load/save/delete')
    parser.add_argument('file', help='github link, profile name, or file to save', nargs='?')
    args = parser.parse_args()
    return args

def get_config(config_file):
    config = configparser.ConfigParser()
    if not os.path.isfile(CONFIG_FILE):
        config['DEFAULT'] = {'ignores': ['.git', '.gitignore']}
        config['current'] = {}
        save_config(config)
    else:
        try:
            config.read(config_file)
        except:
            print("Cannot read config file: {}".format(config_file))
            sys.exit(1)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as cf:
        config.write(cf)

def get_dotfiles(proj_home, ignores):
    files = os.listdir(proj_home)
    dotfiles = [f for f in files if f not in ignores and f.startswith('.')]
    return dotfiles

def parse_github_link(link, name_only=False):
    git_parts = link.split('/')
    git_name = git_parts[-1].replace(".git", "")
    git_user = git_parts[-2]
    proj_name = ""
    if not name_only:
        proj_name = git_user + "_"
    proj_name += git_name + "/"
    return proj_name

def parse_gitconfig(path):
    config = {}
    with open(path) as f:
        lines = [line.strip(' \n') for line in f.readlines()]
    current_section = None
    for line in lines:
        if line[0] == "[":
            current_section = line[1:-1]
            config[current_section] = {}
        else:
            parts = [part.strip() for part in line.split('=')]
            config[current_section][parts[0]] = parts[1]
    return config

def download_repo(repo, target_dir, skip_check=False):
    reset = True
    if skip_check:
        reset = False
    elif os.path.isdir(target_dir):
        reset = input('Directory exists, redownload? (y/n):  ')
        if reset.lower() == "y":
            shutil.rmtree(target_dir)
        else:
            reset = False
    if reset:
        print("Downloading {}".format(repo))
        git_cmd = "git clone -q {} {}".format(repo, target_dir)
        p = subprocess.Popen(git_cmd, shell=True)
        p.wait()

def initialize_hearth(hearth_home, repo):
    if not os.path.isdir(hearth_home):
        create_dir(hearth_home)

    backup_time = False
    local_backup = hearth_home + "local/"
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
        elif os.path.isfile(loc):
            os.remove(loc)
        else:
            pass

def install_pathogen_packages(proj_home, skip_check):
    loc = proj_home + ".vim/bundle/"
    pack_loc = loc + "packages"

    if os.path.isfile(pack_loc):
        with open(pack_loc, 'r') as f:
            packs = [line.strip() for line in f]
        for pack in packs:
            pack_name = parse_github_link(pack, True)
            pack_dir = loc + pack_name
            download_repo(pack, pack_dir, skip_check)

def install_dotfiles(dotfiles, proj_home, config):
    for f in dotfiles:
        src = proj_home + f
        dst = HOME + f
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dst)
                print("Copied {} to {}".format(src, dst))
            except:
                print("Could not copy {} to {}".format(src, dst))
        else:
            try:
                shutil.copyfile(src, dst)
                print("Copied {} to {}".format(src, dst))
                if f == ".gitconfig":
                    replace_gitconfig_args(src, config)
            except:
                print("Could not copy {} to {}".format(src, dst))

def get_gitconfig_args(config, config_path, args=['name', 'email']):
    gitconfig = parse_gitconfig(config_path)
    for arg in args:
        if gitconfig['user'][arg]:
            config.set('current', arg, gitconfig['user'][arg])
    return config

def replace_gitconfig_args(src, config, args=['name', 'email']):
    with open(src, 'r') as fp:
        lines = fp.readlines()
    print(lines)

def backup(dotfiles, local_backup, config):
    for f in dotfiles:
        backup_path = local_backup + f
        dst = expanduser("~") + "/" + f
        try:
            shutil.move(dst, backup_path)
            print("Backed up {} to {}".format(dst, backup_path))
        except Exception as e:
            print(e)
            print("Failed to backup {} to {}".format(dst, backup_path))

        if f == ".gitconfig" and os.path.isfile(backup_path):
            config = get_gitconfig_args(config, backup_path)
    return config

def main():
    args = get_args()

    hearth_home = HOME + ".hearth/"
    local_backup = hearth_home + "local/"
    needs_backup = initialize_hearth(hearth_home, args.file)

    config = get_config(CONFIG_FILE)
    curr_proj = config.get('current', 'repo', fallback=None)
    ignores = config.get('DEFAULT','ignores', fallback=[])
    
    if args.operation == "list":
        projs = os.listdir(hearth_home)
        projs.remove(CONFIG_NAME)
        print(projs)
    elif args.operation == "save":
        print("Saving!")
    elif args.operation == "load":

        skip_check = False
        if args.file.startswith("https://github.com"):
            proj_name = parse_github_link(args.file)
            proj_home = hearth_home + proj_name
            download_repo(args.file, proj_home)
        else:
            proj_home = hearth_home + args.file + "/"
            skip_check = True

        if curr_proj:
            curr_dotfiles = get_dotfiles(curr_proj, ignores)
            delete_all(curr_dotfiles, HOME)

        install_pathogen_packages(proj_home, skip_check)

        dotfiles = get_dotfiles(proj_home, ignores)
        if needs_backup:
            config = backup(dotfiles, local_backup, config)
        install_dotfiles(dotfiles, proj_home, config)

        config.set('current', 'repo', proj_home)
        save_config(config)

if __name__ == "__main__":
    main()
