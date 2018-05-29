// Copyright (c) 2018, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Retry data import', {
	onload: function (frm) {
		//empty attachments
		frm.set_value('import_file', undefined)
		frm.get_files().forEach(function (file) {
			frappe.call({
				method: "ekleel.ekleel.doctype.retry_data_import.retry_data_import.remove_attachment",
				args: {
					fid: file.name
				},
				callback: (r) => {
					frm.set_value('import_file', undefined);
					// window.location.reload();
				}
			});
		})
		frm.refresh_fields();
		// window.location.reload();
	},
	retry: function (frm) {
		if (frm.doc.import_file) {
			pos_transaction_date = frm.doc.import_file.substr(frm.doc.import_file.indexOf('DATA') + 4, 8)
			transactiontype = frm.doc.import_file.substring(frm.doc.import_file.indexOf('s') + 2, frm.doc.import_file.indexOf('DATA'))
			filename = frm.doc.import_file.substr(frm.doc.import_file.indexOf('s') + 2)
			if (transactiontype == 'POS') {
				transactiontype = 'POS Total';
			}
			else if(transactiontype == 'COGS') {
				transactiontype = 'Cost of Goods Sold';
			}
			else if(transactiontype == 'PUR') {
				transactiontype = 'Purchase data';
			}

			frappe.call({
				method: "ekleel.api.upload_file",
				args: {
					path:  frm.doc.import_file,
					transactiontype: transactiontype,
					pos_transaction_date: pos_transaction_date,
					filename:filename,
					client:'yes'

				},
				callback: (r) => {
					frm.doc.sync_log = r.message;
					
					frm.set_df_property("section_break_4", "hidden", frm.doc.sync_log == undefined ? 1 : 0)
					frm.set_df_property("check_log", "hidden", frm.doc.sync_log == undefined ? 1 : 0)
					frm.refresh_fields();
				}
			});

		}
	},
	fresh_run: function (frm) {
		window.location.reload();
		
	},
	import_file: function (frm) {

		
		frm.set_df_property("section_break_2", "hidden", frm.doc.import_file == undefined ? 1 : 0)
		frm.set_df_property("retry", "hidden", frm.doc.import_file == undefined ? 1 : 0)
		frm.refresh_fields();
	},
	check_log: function (frm) {
		frappe.set_route("Form", 'Pixel Point Sync Log', frm.doc.sync_log);
	}
});