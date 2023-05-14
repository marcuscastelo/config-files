#/bin/sh

BACKUP_FOLDER='backup/'
[ -d "$BACKUP_FOLDER" ] || (echo "Backup folder not found: '$BACKUP_FOLDER'" && exit 1)
[ -t $? ] || exit 1

# Initially, I am going to test with a low-impact folder
FOLDER='usr/local/bin/'

echo "sudo rsync -rvcauEgoptUWX $(pwd)/$BACKUP_FOLDER$FOLDER /$FOLDER"

FOLDER='usr/share/X11/xkb/symbols/'

echo "sudo rsync -rvcauEgoptUWX $(pwd)/$BACKUP_FOLDER$FOLDER /$FOLDER"
