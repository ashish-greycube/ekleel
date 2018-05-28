# -*- coding: utf-8 -*-
# Copyright (c) 2018, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import remove_file

class Retrydataimport(Document):
	pass

@frappe.whitelist()
def remove_attachment(fid):
	return remove_file(fid)
