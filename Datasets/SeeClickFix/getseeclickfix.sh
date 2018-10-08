#!/bin/bash

outfile_index=8
number_per_file=500
OUTPUT_FILE=scf_${outfile_index}.csv
# I checked manually, this is how many pages size 100
for i in $(seq 4001 5401)
do
	if [[ $(( $i % $number_per_file )) -eq 1 ]]
	then
		(( outfile_index++ ))
		echo "$(date): incrementing output file index to $outfile_index"
		OUTPUT_FILE=scf_${outfile_index}.csv
		sleep 60
	fi
	wget -q -O - https://seeclickfix.com/api/v2/issues?page=${i}\&per_page=100 | jq -j -r '.issues[] | [.status,.summary,.description,.lat,.lng,.address,.created_at,.request_type.title,.request_type.organization,.reporter.name]' | sed -e 's/\\n/ /g' | sed -e 's/\\r/ /g' | sed -e 's/^  *//g' -e 's/ *$//g' | sed -e 's/,$/|/g' | sed -e 's/,//g' | sed -e 's/|$/,/g' | sed -e ':a /,$/{N;s/,\n/,/; t a}' -e '/\]\[/d' -e '/^\[$/d' -e '/^\]$/d' >> $OUTPUT_FILE
done
