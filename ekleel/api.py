from __future__ import unicode_literals
import frappe
from frappe import _
import os
import time
from frappe.utils import encode, cstr, get_link_to_form, get_site_base_path, today,get_backups_path,get_datetime,split_emails
from frappe.core.doctype.data_import.data_import import import_file_by_path
from frappe.core.doctype.data_import import importer
from frappe.utils.csvutils import read_csv_content
from frappe.utils.file_manager import save_file, get_file,get_file_path
from datetime import datetime, timedelta


def send_email(status,transactiontype,error_status=None,pos_transaction_date=None,log_name=None,attachment=None):
    if not frappe.db:
	    frappe.connect()    

    if status=='Successful':
        subject = """Ekleel data imported Successful for %s dated %s as on """%(transactiontype,pos_transaction_date) + (datetime.now()).strftime("%Y%m%d")
        message ="""<h3>Pixel-point POS data imported successfully for --<i> %s </i></h3><p>Hi there,<br> This is just to inform you that your POS data for %s was successfully imported to ERPNext account. So relax!</p>""" % (transactiontype,transactiontype)
    elif status=='Failed':
        subject = """[Warning] Ekleel data import failed for %s dated %s as on """%(transactiontype,pos_transaction_date) + (datetime.now()).strftime("%Y%m%d")
        message ="""<h3>Pixel-point POS data import failed for --<i> %s </i></h3><p>Oops, your automated import to ERPNext	failed for - %s</p><p><h4>Error message: </h4><br><pre><code>%s</code></pre></p><p><h4>Detailed sync log at :%s </h4><br><hr><h2>Instructions</h2><ol type="1"><li>Download the attached file</li><li>Correct the file content with respect to above mentioned error message</li><li>Retry the data import at %s</li></ol> """ % (transactiontype,transactiontype,error_status,get_link_to_form('Pixel Point Sync Log',log_name,'LogLink'),get_link_to_form('Retry data import','Retry data import','Retry'))
    elif status=='File not found failure':
        subject = """[Warning] Ekleel data import failed for %s dated %s as on """%(transactiontype,pos_transaction_date) + (datetime.now()).strftime("%Y%m%d")
        message ="""<h3>Pixel-point POS data import failed for --<i> %s </i></h3><p>Oops, your automated import to ERPNext failed for - %s</p><p><h4>Error message: </h4><br><pre><code>%s</code></pre></p><p><h4>Detailed sync log at :%s </h4><br><hr><h2>Instructions</h2><ol type="1"><li>It appears no file was kept by Pixel point POS</li><li>Check with pixel point POS and get the required file</li><li>Retry the data import at %s</li></ol> """ % (transactiontype,transactiontype,error_status,get_link_to_form('Pixel Point Sync Log',log_name,'Log link'),get_link_to_form('Retry data import','Retry data import','Retry'))
        
    recipients = split_emails(frappe.db.get_value("PixelPoint Settings", None, "send_notifications_to"))
    frappe.sendmail(recipients=recipients, subject=subject, message=message,attachments=attachment,now=True)


def make_sync_log(status,transactiontype,sync_details,status_color,pos_transaction_date=None,transaction_link=None):
    try:
        sync_log = frappe.new_doc("Pixel Point Sync Log")
        sync_log.sync_date = frappe.utils.now()
        sync_log.sync_status = status
        sync_log.transaction_type = transactiontype
        sync_log.pos_transaction_date =pos_transaction_date
        sync_log.details = cstr(sync_details)
        sync_log.transaction_link=transaction_link
        sync_log.status_color=status_color
        sync_log.save()
        frappe.db.commit()
        return sync_log.name
    except Exception as e:
        raise e


@frappe.whitelist()
def upload_file(path,transactiontype,pos_transaction_date,filename,client=None):
    try:
        if client=='yes':
            path=get_file_path(path)
        with open(encode(path), 'r') as f:
            content = f.read()
        rows = read_csv_content(content)
        result=importer.upload(rows,submit_after_import=True,update_only =False,ignore_encoding_errors=True, no_email=True)
        # generate JV name        
        title=result['messages'][0]['title']
        st=title.rfind('J')
        en=title.rfind('<')
        JV_name=title[st:en]
        transaction_link=JV_name

        error_status=result['error']
        
        # failed due to content error
        if error_status==True:
            log_name= make_sync_log("Failed",transactiontype,result,'#fff168',pos_transaction_date,None)
            attachments = [{
				'fname': filename,
				'fcontent': content
			}]
            send_email('Failed',transactiontype,result,pos_transaction_date,log_name,attachments)
            os.remove(path)
            return log_name
        #import is successful
        elif error_status==False:
            log_name=make_sync_log("Successful",transactiontype,result,'#9deca2',pos_transaction_date,transaction_link)
            os.remove(path)
            send_email('Successful',transactiontype,result,pos_transaction_date)
            return log_name

    except Exception as e:
        error = True
        log_name=make_sync_log("File not found failure",transactiontype,frappe.get_traceback(),'#ff4d4d',None,None)
        send_email('File not found failure',transactiontype,frappe.get_traceback(),pos_transaction_date,log_name)
        return log_name

	if error:
		frappe.db.rollback()
	else:
		frappe.db.commit()
	return {"error": error}

@frappe.whitelist()
# main function
def upload():
#guess file name
    base_dir=os.path.join(get_site_base_path(),"public/pixelposdata/")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    pos_filename='POSDATA'+yesterday+'.csv'
    cogs_filename='COGSDATA'+yesterday+'.csv'
    purdata_filename='PURDATA'+yesterday+'.csv'
    pos_filepath=os.path.join(base_dir,pos_filename)
    cogs_filepath=os.path.join(base_dir,cogs_filename)
    purdata_filepath=os.path.join(base_dir,purdata_filename)
#check for JV creation permission
    if not frappe.has_permission("Journal Entry", "create"):
        raise frappe.PermissionError
#Import files to JV
    upload_file(pos_filepath,'POS Summary',yesterday,pos_filename)
    upload_file(cogs_filepath,'Cost of Goods Sold',yesterday,cogs_filename)
    upload_file(purdata_filepath,'Purchase data',yesterday,purdata_filename)