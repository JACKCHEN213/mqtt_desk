#!/bin/bash
#
# generate install package script
# Copyright 2023 jackc

function main() {
    pyinstaller mqtt桌面工具.spec
}

main "$@"