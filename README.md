## Ekleel

Import daily POS data from pixel point to ERPNext at 5:15 am

## Path where pixel point data to be dropped
/home/frappe/frappe-bench/sites/site1.local/public/pixelposdata

File format has to be
    COGSDATAYYYYMMDD.csv
    POSDATAYYYYMMDD.csv
    PURDATAYYYYMMDD.csv
On auto import it will check YYYYMMDD as yesterday date

## Technical failure email list
set email id (if multiple emailid it should be comma seperated list)
http://93.104.208.110/desk#Form/PixelPoint%20Settings

## To retry failed upload for single file
http://93.104.208.110/desk#Form/Retry%20data%20import
File format has to be
    COGSDATAYYYYMMDD.csv
    POSDATAYYYYMMDD.csv
    PURDATAYYYYMMDD.csv
where, YYYYMMDD could be any date

## To retry failed upload for all files from command prompt
bench --site site1.local execute ekleel.api.upload


#### License

MIT