# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'

#Custom terminal colors and stuff
PS1='\[\033[1;38;5;5m\]\u\[\033[0m\]: \[\033[1;38;5;208m\]\w \[\033[0m\]\$ '

#Make programs use vim instead of vi as their default editor
export VISUAL=vim
export EDITOR=vim

