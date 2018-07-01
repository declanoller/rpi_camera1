#!/bin/bash

printf '\n\nFolders and files before:\n\n'
ls --color=auto

printf '\n'

rm -r 2018*

rm Log*

printf '\nFolders and files after:\n\n'
ls --color=auto
printf '\n'
