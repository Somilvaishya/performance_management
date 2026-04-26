import frappe
import os

def install():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	frappe.flags.in_import = True
	frappe.flags.in_patch = True
	frappe.conf.developer_mode = 1

	reports = [
		("Task Completion Trend", "Line"),
		("Task Status Distribution", "Donut"),
		("Checklist Compliance", "Donut"),
		("Overdue Task Trend", "Line"),
		("User Performance", "Bar")
	]

	for r_name, c_type in reports:
		report_id = frappe.db.exists("Report", r_name)
		if not report_id:
			doc = frappe.get_doc({
				"doctype": "Report",
				"report_name": r_name,
				"ref_doctype": "Performance Task",
				"report_type": "Script Report",
				"is_standard": "Yes",
				"module": "Performance Management"
			})
			doc.insert(ignore_permissions=True)
		
		# Now create Dashboard Chart
		chart_id = frappe.db.exists("Dashboard Chart", r_name)
		if not chart_id:
			frappe.get_doc({
				"doctype": "Dashboard Chart",
				"chart_name": r_name,
				"chart_type": "Report",
				"report": r_name,
				"filters_json": "{}",
				"is_standard": 1,
				"module": "Performance Management"
			}).insert(ignore_permissions=True)

	frappe.db.commit()
	print("Reports and Dashboard Charts Scaffolded Successfully!")

if __name__ == "__main__":
	install()
