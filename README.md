# hearth
Home is where the [hearthstone](https://wow.gamepedia.com/Hearthstone) is 

hearth is a simple dotfiles manager

## Usage

Download some sweet dotfiles
```
$ python hearth.py https://github.com/pieterbork/dotfiles.git
Cloning into '/home/rick/.hearth/pieterbork_dotfiles'...
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
Checking connectivity... done.
Backing up /home/rick/.vimrc to /home/rick/.hearth/local_backup/.vimrc
Copying /home/rick/.hearth/pieterbork_dotfiles/.vimrc to /home/rick/.vimrc
```

And restore back to your old ones
```
$ python hearth.py local
Copying /home/rick/.hearth/local_backup/.vimrc to /home/rick/.vimrc
```

That's it! Feedback is appreciated!
