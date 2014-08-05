#!/usr/bin/env sh
MIN_CITY_POP=15000
# download USA place names
echo "Downloading USA state and county information..."
curl "http://download.geonames.org/export/dump/US.zip" > usa.zip
unzip usa.zip
mkdir ./geonames
# only keep states and counties
grep -E "	ADM1	" US.txt > ./geonames/usa_states.tsv
grep -E "	ADM2	" US.txt > ./geonames/usa_counties.tsv
rm US.txt readme.txt usa.zip
# download country names
echo "Downloading country information..."
curl "http://download.geonames.org/export/dump/countryInfo.txt" > ./geonames/countries.tsv
# download cities
echo "Downloading USA city information..."
curl "http://download.geonames.org/export/dump/cities$MIN_CITY_POP.zip" > cities.zip
unzip cities.zip
# only keep USA cities
grep -E '	US	' cities$MIN_CITY_POP.txt > ./geonames/usa_cities.tsv
rm cities$MIN_CITY_POP.txt cities.zip

echo "Downloading USA Postal Code information..."
curl "http://download.geonames.org/export/zip/US.zip" > usazipcodes.zip
unzip usazipcodes.zip
mv US.txt ./geonames/usa_zip.tsv
rm readme.txt usazipcodes.zip

echo "Downloading USA County information..."
curl "https://www.census.gov/geo/reference/codes/files/national_county.txt" > ./geonames/usa_fips.csv