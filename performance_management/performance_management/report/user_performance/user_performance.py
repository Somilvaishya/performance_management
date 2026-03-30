import frappe

def execute(filters=None):
	columns = [
		{"fieldname": "assigned_to", "label": "User", "fieldtype": "Data", "width": 120},
		{"fieldname": "score", "label": "Average Score", "fieldtype": "Float", "width": 100}
	]
	
	data = frappe.db.sql('''
		SELECT assigned_to, AVG(score) as score
		FROM `tabPerformance Task`
		WHERE status = 'Approved' AND assigned_to IS NOT NULL
		GROUP BY assigned_to
		ORDER BY score DESC
		LIMIT 5
	''', as_dict=True)
	
	if not data: return columns, [], None, None

	chart = {
		"data": {
			"labels": [d.assigned_to for d in data],
			"datasets": [{"name": "Score", "values": [round(d.score, 1) for d in data]}]
		},
		"type": "bar",
		"colors": ["#8B5CF6"]
	}
	return columns, data, None, chart
