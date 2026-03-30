import frappe

def run_test():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()

	# Clear old email queue for clean testing
	frappe.db.sql("DELETE FROM `tabEmail Queue`")
	frappe.db.sql("DELETE FROM `tabEmail Queue Recipient`")
	frappe.db.commit()

	print("--- Creating Test Task ---")
	# Create a Performance Task assigned to Administrator
	task = frappe.get_doc({
		"doctype": "Performance Task",
		"task_title": "Test Email Notifications Task",
		"description": "This is a system test.",
		"task_type": "Delegation",
		"priority": "High",
		"assigned_to": "Administrator",
		"assigned_by": "Administrator",
		"status": "Pending",
		"deadline": "2026-12-31"
	})
	task.insert(ignore_permissions=True)
	frappe.db.commit()
	print(f"Task created: {task.name}")

	# Check Email Queue
	emails = frappe.get_all("Email Queue", fields=["name", "status", "sender", "message_id", "creation"])
	print(f"--- Emails in Queue after Insert: {len(emails)} ---")
	for e in emails:
		doc = frappe.get_doc("Email Queue", e.name)
		print(f"Subject: {doc.get('message', '')[:150]}")
		
	print("--- Checking Error Logs ---")
	errors = frappe.get_all("Error Log", fields=["method", "error"], limit=3, order_by="creation desc")
	for err in errors:
		print(f"Error: {err.method}\n{err.error}")

if __name__ == "__main__":
	run_test()
