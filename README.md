# hearth
Home is where the [hearthstone](https://wow.gamepedia.com/Hearthstone) is 

hearth is a simple dotfiles manager

## Usage

Download some sweet dotfiles
```
$ python hearth.py https://github.com/Airblader/dotfiles-manjaro.git
Cloning into '/home/rick/.hearth/Airblader_dotfiles-manjaro'...
remote: Counting objects: 1855, done.
remote: Total 1855 (delta 0), reused 0 (delta 0), pack-reused 1855
Receiving objects: 100% (1855/1855), 23.84 MiB | 11.75 MiB/s, done.
Resolving deltas: 100% (993/993), done.
Checking connectivity... done.
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.Xresources to /home/rick/.Xresources
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.bash.d to /home/rick/.bash.d
Could not copy /home/rick/.hearth/Airblader_dotfiles-manjaro/.bash.d
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.bash_profile to /home/rick/.bash_profile
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.bashrc to /home/rick/.bashrc
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.compton.conf to /home/rick/.compton.conf
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.config to /home/rick/.config
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.gitconfig to /home/rick/.gitconfig
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.gtkrc-2.0 to /home/rick/.gtkrc-2.0
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.i3 to /home/rick/.i3
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.npmrc to /home/rick/.npmrc
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.vim to /home/rick/.vim
Backed up /home/rick/.vimrc to /home/rick/.hearth/local_backup/.vimrc
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.vimrc to /home/rick/.vimrc
Copying /home/rick/.hearth/Airblader_dotfiles-manjaro/.xinitrc to /home/rick/.xinitrc
```

And restore back to your old ones
```
$ python hearth.py local
Deleting /home/rick/.Xresources
Deleting /home/rick/.bash.d
Deleting /home/rick/.bash_profile
Deleting /home/rick/.bashrc
Deleting /home/rick/.compton.conf
Deleting /home/rick/.config
Deleting /home/rick/.gitconfig
Deleting /home/rick/.gtkrc-2.0
Deleting /home/rick/.i3
Deleting /home/rick/.npmrc
Deleting /home/rick/.vim
Deleting /home/rick/.vimrc
Deleting /home/rick/.xinitrc
Copying /home/rick/.hearth/local_backup/.vimrc to /home/rick/.vimrc
Deleting /home/rick/.hearth/local_backup/
```

That's it! Feedback is appreciated!
