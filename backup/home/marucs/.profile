export PATH="$HOME/.nimble/bin:$PATH:.local/bin:/opt/cmake-3.21.1/bin"
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

. "$HOME/.cargo/env"
alias adbw='adb connect 192.168.0.42:5555'

export AUDIO_RECORDINGS_PATH="/home/marucs/Recordings"

# For anki blank screen issue (https://forums.ankiweb.net/t/fedora-35-and-anki-2-1-47-updates-with-blank-anki-window/13431/11)
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
export EDITOR='nvim'

alias vim='nvim'
