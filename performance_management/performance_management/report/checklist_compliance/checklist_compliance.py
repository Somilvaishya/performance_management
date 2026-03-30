import frappe

def execute(filters=None):
	columns = [
		{"fieldname": "compliance", "label": "Compliance", "fieldtype": "Data", "width": 120},
		{"fieldname": "count", "label": "Count", "fieldtype": "Int", "width": 100}
	]
	
	today = frappe.utils.today()
	
	# Completed Checklists
	completed = frappe.db.count("Performance Task", {
		"task_type": "Checklist", 
		"status": "Approved", 
		"creation": [">=", frappe.utils.add_days(today, -7)]
	})
	
	# Missed Checks
	missed = frappe.db.count("Performance Task", {
		"task_type": "Checklist", 
		"status": ["!=", "Approved"], 
		"deadline": ["<", frappe.utils.now()]
	})
	
	data = [
		{"compliance": "Completed", "count": completed},
		{"compliance": "Missed", "count": missed}
	]
	
	chart = {
		"data": {
			"labels": ["Completed", "Missed"],
			"datasets": [{"name": "Compliance", "values": [completed, missed]}]
		},
		"type": "donut",
		"colors": ["#10B981", "#EF4444"]
	}
	return columns, data, None, chart
