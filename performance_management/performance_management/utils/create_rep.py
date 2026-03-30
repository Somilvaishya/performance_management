import frappe

def run():
	report_name = "Team Performance Report"
	if not frappe.db.exists("Report", report_name):
		doc = frappe.get_doc({
			"doctype": "Report",
			"report_name": report_name,
			"ref_doctype": "Performance Task",
			"report_type": "Script Report",
			"is_standard": "Yes",
			"module": "Performance Management"
		})
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		print(f"Created Script Report: {report_name}")
	else:
		print(f"Script Report {report_name} already exists.")
