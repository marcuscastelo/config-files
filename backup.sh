#/bin/sh

BACKUP_FOLDER='backup/'
[ -d "$BACKUP_FOLDER" ] || (echo "Backup folder not found: '$BACKUP_FOLDER'" && exit 1);
[ -t $? ] || exit 1

FOLDER='etc/runit/'

echo "sudo rsync -rvcauEgoptUWX /$FOLDER $(pwd)/$BACKUP_FOLDER$FOLDER"

FOLDER='usr/share/X11/symbols/'

echo "sudo rsync -rvcaEgoptUWX /$FOLDER $(pwd)/$BACKUP_FOLDER$FOLDER"
