
#Blacklist
#step 0
./mysql.sh ./step0.sql > ./blacklist_customers.tsv

#dv_prospects
#step1
./mysql.sh ./step1.sql > ./prospect_location.tsv

#all the prospects
#step1
./mysql.sh ./step2.sql > ./prospects_resumes.tsv