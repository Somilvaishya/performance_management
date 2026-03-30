import frappe

def execute(filters=None):
	columns = [
		{"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 120},
		{"fieldname": "count", "label": "Count", "fieldtype": "Int", "width": 100}
	]
	
	data = frappe.db.sql('''
		SELECT status, count(name) as count
		FROM `tabPerformance Task`
		GROUP BY status
	''', as_dict=True)
	
	if not data: return columns, [], None, None

	chart = {
		"data": {
			"labels": [d.status for d in data],
			"datasets": [{"name": "Tasks", "values": [d.count for d in data]}]
		},
		"type": "donut",
		"colors": ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#6B7280"]
	}
	return columns, data, None, chart
