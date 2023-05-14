#/bin/sh

BACKUP_FOLDER='backup/'
[ -d "$BACKUP_FOLDER" ] || (echo "Backup folder not found: '$BACKUP_FOLDER'" && exit 1)
[ -t $? ] || exit 1

function restore_folder() {
  FOLDER="$1"
  cmd="sudo rsync -rvcauEgoptUWX $(pwd)/$BACKUP_FOLDER$FOLDER /$FOLDER"
  echo "> $cmd"
  $cmd
  echo
}

restore_folder 'usr/local/bin/'
restore_folder 'usr/share/X11/xkb/symbols/'
