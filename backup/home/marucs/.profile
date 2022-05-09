export PATH=/home/marucs/.nimble/bin:$PATH
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
. "$HOME/.cargo/env"
