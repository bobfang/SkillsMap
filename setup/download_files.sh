#!/usr/bin/env sh
MIN_CITY_POP=15000
# download USA place names
echo "Downloading USA state and county information..."
curl "http://download.geonames.org/export/dump/US.zip" > usa.zip
unzip usa.zip
# only keep states and counties
grep -E "	ADM1	" US.txt > usa_states.tsv
grep -E "	ADM2	" US.txt > usa_counties.tsv
rm US.txt readme.txt usa.zip
# download country names
echo "Downloading country information..."
curl "http://download.geonames.org/export/dump/countryInfo.txt" > countries.tsv
# download cities
echo "Downloading USA city information..."
curl "http://download.geonames.org/export/dump/cities$MIN_CITY_POP.zip" > cities.zip
unzip cities.zip
# only keep USA cities
grep -E '	US	' cities$MIN_CITY_POP.txt > usa_cities.tsv
rm cities$MIN_CITY_POP.txt cities.zip

echo "Downloading USA city information..."
curl "http://download.geonames.org/export/zip/US.zip" > usazipcodes.zip
unzip usazipcodes.zip
mv US.txt usa_zip.tsv
rm readme.txt