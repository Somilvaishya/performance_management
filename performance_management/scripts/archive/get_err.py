import frappe
def run():
	for e in frappe.get_all('Error Log', fields=['method', 'error'], limit=3, order_by='creation desc'):
		print(f"Error Method: {e.method}\n{e.error[:200]}\n---")
