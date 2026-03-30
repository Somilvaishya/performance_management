import frappe
from frappe import _, db

def run():
	# 1. Number Card: Tasks Due Today
	if not db.exists("Number Card", "Tasks Due Today"):
		frappe.get_doc({
			"doctype": "Number Card",
			"name": "Tasks Due Today",
			"document_type": "Performance Task",
			"type": "Document Type",
			"function": "Count",
			"is_standard": 1,
			"module": "Performance Management",
			"filters_json": '[["Performance Task","deadline","Timespan","today"]]',
			"color": "#e0584b"
		}).insert(ignore_permissions=True)
		
	# 2. Number Card: My Pending Tasks
	if not db.exists("Number Card", "My Pending Tasks"):
		frappe.get_doc({
			"doctype": "Number Card",
			"name": "My Pending Tasks",
			"document_type": "Performance Task",
			"type": "Document Type",
			"function": "Count",
			"is_standard": 1,
			"module": "Performance Management",
			"filters_json": '[["Performance Task","status","in",["Pending","In Progress"]]]',
			"color": "#f1a830"
		}).insert(ignore_permissions=True)

	# 3. Dashboard Chart: Task Status Breakdown
	if not db.exists("Dashboard Chart", "Task Status Over Time"):
		frappe.get_doc({
			"doctype": "Dashboard Chart",
			"chart_name": "Task Status Over Time",
			"document_type": "Performance Task",
			"is_standard": 1,
			"module": "Performance Management",
			"chart_type": "Group By",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"based_on": "creation",
			"timespan": "Last Month",
			"time_interval": "Daily",
			"color": "#187db1"
		}).insert(ignore_permissions=True)

	frappe.db.commit()
	print("Dashboard Elements Created Successfully")
