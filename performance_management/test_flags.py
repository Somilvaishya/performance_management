import frappe
def run_test():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()
	frappe.db.sql("DELETE FROM `tabEmail Queue`")

	task = frappe.get_doc({
		"doctype": "Performance Task",
		"task_title": "Test Flag Suppression",
		"task_type": "Delegation",
		"assigned_to": "Administrator",
		"assigned_by": "Administrator",
		"priority": "High",
		"status": "Pending",
		"deadline": "2026-12-31"
	})
	task.flags.ignore_assignment_email = True
	task.insert(ignore_permissions=True)
	
	emails = frappe.get_all("Email Queue", fields=["name"])
	print(f"Emails in Queue: {len(emails)}")

if __name__ == "__main__":
	run_test()
