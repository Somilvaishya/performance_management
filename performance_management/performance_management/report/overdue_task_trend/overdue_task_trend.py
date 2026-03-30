import frappe

def execute(filters=None):
	columns = [
		{"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
		{"fieldname": "count", "label": "Overdue Count", "fieldtype": "Int", "width": 100}
	]
	
	data = frappe.db.sql('''
		SELECT DATE(deadline) as date, count(name) as count
		FROM `tabPerformance Task`
		WHERE status != 'Approved' AND deadline < CURDATE()
		GROUP BY DATE(deadline)
		ORDER BY date ASC
		LIMIT 14
	''', as_dict=True)
	
	if not data: return columns, [], None, None

	chart = {
		"data": {
			"labels": [frappe.utils.formatdate(d.date, "dd-MMM") for d in data],
			"datasets": [{"name": "Overdue", "values": [d.count for d in data]}]
		},
		"type": "line",
		"colors": ["#EF4444"]
	}
	return columns, data, None, chart
