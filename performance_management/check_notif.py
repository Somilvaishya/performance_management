import frappe
def run():
	docs = frappe.get_all("Notification", filters={"document_type": "Performance Task"}, fields=["name", "subject", "message"])
	if docs:
		print("FOUND NOTIFICATIONS:")
		for d in docs:
			print(d.name, d.subject)
	else:
		print("No Notifications Found.")
