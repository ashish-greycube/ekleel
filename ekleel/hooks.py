# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ekleel"
app_title = "Ekleel"
app_publisher = "GreyCube Technologies"
app_description = "Import daily POS data from pixel point to ERPNext"
app_icon = "octicon octicon-database"
app_color = "#6F4E37"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ekleel/css/ekleel.css"
# app_include_js = "/assets/ekleel/js/ekleel.js"

# include js, css files in header of web template
# web_include_css = "/assets/ekleel/css/ekleel.css"
# web_include_js = "/assets/ekleel/js/ekleel.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ekleel.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ekleel.install.before_install"
# after_install = "ekleel.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ekleel.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ekleel.tasks.all"
# 	],
# 	"daily": [
# 		"ekleel.tasks.daily"
# 	],
# 	"hourly": [
# 		"ekleel.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ekleel.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ekleel.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ekleel.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ekleel.event.get_events"
# }

# Time is as per frappe user time zone
scheduler_events = {
    "cron": {
        "15 5 * * *": [
            "ekleel.api.upload"
        ]
    },

}
fixtures = [
    # 	{
	# 	"dt":"Custom Script",
	# 	"filters":[
	# 		["name", "in", [
	# 		"Sales Order-Client"]],
	# 	]
	# },
	{
	"dt":"Report",
			"filters":[
			["name", "in", [
			"Pixel POS Daily Summary"]],
		]
	}
]