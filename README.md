## Ekleel

Import daily POS data from pixel point to ERPNext

## Path where pixel point data to be dropped
/home/frappe/frappe-bench/sites/site1.local/public/pixelposdata



## To retry failed upload
~/frappe-bench$ 
bench --site site1.local execute ekleel.api.upload_file --args "site1.local/public/pixelposdata/PURDATA20180521.csv"




#### License

MIT