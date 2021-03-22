#!/bin/bash

echo "===test==="
echo "$$"
echo "$0"
echo "$?"
#ps | awk '{print $1}' | sort -rn | head -10
python clear_gmsfile.py
echo "====gms temp file clean==="