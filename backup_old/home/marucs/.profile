export PATH=/home/marucs/.nimble/bin:$PATH
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
eval "$(pyenv init --path)"
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
. "$HOME/.cargo/env"
alias adbw='adb connect 192.168.0.42:5555'
