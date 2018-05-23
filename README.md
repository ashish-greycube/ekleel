## Ekleel

Import daily POS data from pixel point to ERPNext

## Path where pixel point data to be dropped
/home/frappe/frappe-bench/sites/site1.local/public/pixelposdata



## To retry failed upload for single file
~/frappe-bench$ 
bench --site site1.local execute ekleel.api.upload_file --args "site1.local/public/pixelposdata/PURDATA20180521.csv"

## To retry failed upload for all files
bench --site site1.local execute ekleel.api.upload


#### License

MIT