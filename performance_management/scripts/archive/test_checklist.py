import frappe
def run():
	frappe.init(site='workspace.test', sites_path='sites')
	frappe.connect()
	frappe.db.sql("DELETE FROM `tabEmail Queue`")
	
	import performance_management.performance_management.services.checklist_service as cs
	cs.create_daily_checklists()
	
	emails = frappe.get_all("Email Queue", fields=["name", "message"])
	print(f"Emails in queue after running checklist_service: {len(emails)}")
	for e in emails:
		print("Subject/Body snippet:", e.message[:100])
