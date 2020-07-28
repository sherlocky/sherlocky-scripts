#!/bin/sh
# lazy find

# 自定义命令调用脚本
# vim ~/.bashrc
# alias lfind=/opt/bin/lazy_find.sh
# :wq
# . ~/.bashrc
# lfind java

# GNU All-Permissive License
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

## help function

function helpu {
    echo " "
    echo "Fuzzy search for filename."
    echo "$0 [--match-case|-m|--path}-p] filename"
    echo " "
    exit
}

## set variables

MATCH="-iname"
SEARCH="."

## parse options

while [ True ]; do
if [ "$1" = "--help" -o "$1" = "-h" ]; then
    helpu
elif [ "$1" = "--match-case" -o "$1" = "-m" ]; then
    MATCH="-name"
	### shift命令可以移动位置参数（左移）
    shift 1
elif [ "$1" = "--path" -o "$1" = "-p" ]; then
    SEARCH="${2}"
    shift 2
else
    break
fi
done

## sanitize input filenames
## create array, retain spaces

ARG=( "${@}" ) ### ${@} 所有参数列表
set -e ### 若指令传回值不等于0，则立即退出shell

## catch obvious input error

if [ "X$ARG" = "X" ]; then
    helpu
fi

## perform search

for query in ${ARG[*]}; do ### ${ARG[*]} 返回数组全部元素
    /usr/bin/find "${SEARCH}" "${MATCH}" "*${ARG}*"
done