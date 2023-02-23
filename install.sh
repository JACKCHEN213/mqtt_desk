#!/bin/bash
#
# generate install package script
# Copyright 2023 jackc

function main() {
    pyinstaller -w -i=images/favicon.ico -n=mqtt桌面工具 main.py
}

main "$@"