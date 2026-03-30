import frappe

def fix_charts():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	frappe.flags.in_import = True
	frappe.flags.in_patch = True
	frappe.conf.developer_mode = 1

	reports = [
		{"name": "Task Completion Trend", "type": "Line"},
		{"name": "Task Status Distribution", "type": "Donut"},
		{"name": "Checklist Compliance", "type": "Donut"},
		{"name": "Overdue Task Trend", "type": "Line"},
		{"name": "User Performance", "type": "Bar"}
	]

	for r in reports:
		r_name = r["name"]
		c_type = r["type"]
		try:
			if frappe.db.exists("Dashboard Chart", r_name):
				frappe.delete_doc("Dashboard Chart", r_name, ignore_permissions=True, force=1)
			
			frappe.get_doc({
				"doctype": "Dashboard Chart",
				"chart_name": r_name,
				"chart_type": "Report",
				"type": c_type,
				"report_name": r_name,
				"use_report_chart": 1,
				"filters_json": "{}",
				"is_standard": 1,
				"module": "Performance Management"
			}).insert(ignore_permissions=True)
			print(f"Re-created {r_name}")
		except Exception as e:
			print(f"Error fixing {r_name}: {e}")

	frappe.db.commit()
	print("Charts fixed!")

if __name__ == "__main__":
	fix_charts()
