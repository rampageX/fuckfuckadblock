#!/bin/sh

PWD="`pwd`"
FETCH_URLS="https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/EnglishFilter/sections/antiadblock.txt \
            https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/ChineseFilter/sections/antiadblock.txt \
            https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/RussianFilter/sections/antiadblock.txt \
            https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/AnnoyancesFilter/sections/antiadblock.txt"

echo "Fetching files..."

for URL in $FETCH_URLS; do
    tmp_name=$(echo ${URL} | awk -F"/" '{print $7}')
    curl -sL ${URL} -o antiadblock_${tmp_name}
done

title_file="${PWD}/title.txt"
final_file="${PWD}/my_antiadblock_selection.txt"

find . -maxdepth 1 -name "antiadblock_*" | xargs sed 'a\' > ${final_file}_

cat ${title_file} ${final_file}_ > $final_file

rm -f antiadblock_*
rm -f ${final_file}_
