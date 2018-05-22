from __future__ import unicode_literals
import frappe
from frappe import _
import os
from frappe.utils import encode, cstr, get_site_base_path, today,get_backups_path,get_datetime
from frappe.core.doctype.data_import.data_import import import_file_by_path
from frappe.core.doctype.data_import import importer
from frappe.utils.csvutils import read_csv_content

def make_sync_log(status,transactiontype,sync_details,transaction_date,transaction_link):
    try:
        sync_log = frappe.new_doc("Pixel Point Sync Log")
        sync_log.sync_date = frappe.utils.now()
        sync_log.sync_status = status
        sync_log.transaction_type = transactiontype
        sync_log.transaction_date =transaction_date
        sync_log.details = cstr(sync_details)
        sync_log.transaction_link=transaction_link
        sync_log.save()
        frappe.db.commit()
    except Exception as e:
        print frappe.get_traceback()
        raise e

@frappe.whitelist()
def upload_file(path,transactiontype=None,transaction_date=None):
    try:
        # result=import_file_by_path(path,ignore_links=False, overwrite=False, submit=True, pre_process=None, no_email=True)
        with open(encode(path), 'r') as f:
		    content = f.read()
        rows = read_csv_content(content)
        result=importer.upload(rows,submit_after_import=True,update_only =False,ignore_encoding_errors=True, no_email=True)
        
        transaction_link=[result['messages'][0]['title'].split('for',1)[1]]
        error_status=result['error']

        if error_status==True:
            make_sync_log("Failed",transactiontype,result,transaction_date,transaction_link=None)
        elif error_status==False:
            make_sync_log("Successful",transactiontype,result,transaction_date,transaction_link[0])
            os.remove(path)
            print("file delted")

    except Exception as e:
        error = True
        make_sync_log(status="Failed",transactiontype=transactiontype,sync_details=frappe.get_traceback(),transaction_date=transaction_date,transaction_link=None)
        frappe.errprint(frappe.get_traceback())

	if error:
		frappe.db.rollback()
	else:
		frappe.db.commit()
	return {"error": error}


@frappe.whitelist()
def upload():

# create file name
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    
    pos_filename='POSDATA'+yesterday+'.csv'
    cogs_filename='COGSDATA'+yesterday+'.csv'
    purdata_filename='PURDATA'+yesterday+'.csv'

    base_dir=os.path.join(get_site_base_path(),"public/pixelposdata/")
    
    pos_filepath=os.path.join(base_dir,pos_filename)
    cogs_filepath=os.path.join(base_dir,cogs_filename)
    purdata_filepath=os.path.join(base_dir,purdata_filename)

# Check Permission
    if not frappe.has_permission("Journal Entry", "create"):
        raise frappe.PermissionError

#Import files to JV
    upload_file(pos_filepath,'POS',yesterday)
    upload_file(cogs_filepath,'Cost of Goods Sold',yesterday)
    upload_file(purdata_filepath,'Purchase data',yesterday)



