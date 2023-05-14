#/bin/sh

BACKUP_FOLDER='backup/'
[ -d "$BACKUP_FOLDER" ] || (echo "Backup folder not found: '$BACKUP_FOLDER'" && exit 1);
[ -t $? ] || exit 1

function backup_folder() {
  FOLDER="$1"
  cmd="sudo rsync -rvcauEgoptUWX /$FOLDER $(pwd)/$BACKUP_FOLDER$FOLDER"
  echo "> $cmd"
  $cmd
  echo
}

backup_folder 'etc/runit/'
backup_folder 'usr/share/X11/symbols/'
