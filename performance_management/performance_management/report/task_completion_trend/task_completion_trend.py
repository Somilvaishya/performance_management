import frappe

def execute(filters=None):
	columns = [
		{"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
		{"fieldname": "count", "label": "Completed Tasks", "fieldtype": "Int", "width": 100}
	]
	
	data = frappe.db.sql('''
		SELECT DATE(completion_date) as date, count(name) as count
		FROM `tabPerformance Task`
		WHERE status='Approved' AND completion_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND completion_date IS NOT NULL
		GROUP BY DATE(completion_date)
		ORDER BY date ASC
	''', as_dict=True)
	
	chart = {
		"data": {
			"labels": [frappe.utils.formatdate(d.date, "dd-MMM") for d in data],
			"datasets": [{"name": "Completed", "values": [d.count for d in data]}]
		},
		"type": "line",
		"colors": ["#4F46E5"]
	}
	return columns, data, None, chart
