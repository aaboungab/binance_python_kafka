#!/bin/bash

GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
symbols=("BTCUSDT" "ETHUSDT" "XRPUSDT" "DOGEUSDT" "LTCUSDT")

cd "$SCRIPT_DIR"

for symbol in "${symbols[@]}";
do
    echo -e "${ORANGE}Running checks for $symbol..${NC}"
    cd "$symbol/"
    year="$(ls | cut -d'_' -f2)"
    for file in $(ls | grep csv);
    do  
        
        file_year="$(echo $file | cut -d'_' -f2)"
        line_first_year="$(head -n2 $file | awk 'NR==2{print}'|cut -d',' -f1 | cut -d'-' -f1)" 
        line_last_year="$(tail -n1 $file | awk '{print}'|cut -d',' -f1 | cut -d'-' -f1)"
        
        if [ "$line_first_year" != "$file_year" ]; then
            echo -e "${GREEN} $file_year cleaned${NC}"
            sed -i '2d' $file
        elif [ "$line_last_year" != "$file_year" ]; then
            echo -e "${GREEN} $file_year cleaned${NC}"
            sed -i '$d' $file
        fi
    done
    cd ../
    echo -e "${GREEN}Completed checks for $symbol..${NC}"

done