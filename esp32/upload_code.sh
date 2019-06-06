#!/bin/bash
set -e 
export AMPY="ampy --port /dev/ttyUSB0"
export AMPYPUT="$AMPY put" 
export AMPYRESET="$AMPY reset"

# Start in script current directory
cd "$(dirname "$(realpath "$0")")";

# add mfrc522 library
echo mfrc522...
$AMPYPUT mfrc522.py

# add lock library
echo lock...
$AMPYPUT lock.py

$AMPYRESET