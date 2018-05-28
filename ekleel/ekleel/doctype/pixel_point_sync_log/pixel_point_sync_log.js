// Copyright (c) 2018, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pixel Point Sync Log', {
	refresh: function(frm) {
		frm.set_df_property("check_jv","hidden",frm.doc.transaction_link==undefined?1:0)
	},
	load: function(frm) {
		frm.set_df_property("check_jv","hidden",frm.doc.transaction_link==undefined?1:0)
	},
	check_jv: function(frm) {
		frappe.set_route("Form", 'Journal Entry', frm.doc.transaction_link);
	}
});
