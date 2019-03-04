cat $1 | awk -F"\t" '{print $4}' | sed '1d' | tr '\n' ' ' | perl -pe 's/<eos>/\n/g' | sed "s/^ //g"
