import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	report_summary = get_report_summary(data)
	return columns, data, None, chart, report_summary

def get_columns():
	return [
		{"fieldname": "employee", "label": _("Employee"), "fieldtype": "Link", "options": "User", "width": 150},
		{"fieldname": "department", "label": _("Department"), "fieldtype": "Link", "options": "Department", "width": 150},
		{"fieldname": "total_tasks", "label": _("Total Tasks"), "fieldtype": "Int", "width": 100},
		{"fieldname": "completed_tasks", "label": _("Completed"), "fieldtype": "Int", "width": 100},
		{"fieldname": "completion_rate", "label": _("Completion Rate %"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "average_score", "label": _("Avg Score"), "fieldtype": "Float", "width": 100},
		{"fieldname": "overdue_tasks", "label": _("Overdue"), "fieldtype": "Int", "width": 100},
		{"fieldname": "extensions", "label": _("Extensions"), "fieldtype": "Int", "width": 100}
	]

def get_data(filters):
	conditions, filter_values = get_conditions(filters)
	tasks = frappe.db.sql(f"""
		SELECT 
			assigned_to as employee,
			department,
			count(name) as total_tasks,
			sum(case when status='Approved' then 1 else 0 end) as completed_tasks,
			avg(case when status='Approved' then score else null end) as average_score,
			sum(is_overdue) as overdue_tasks,
			sum(extension_count) as extensions
		FROM 
			`tabPerformance Task`
		WHERE 
			status != 'Cancelled' {conditions}
		GROUP BY 
			assigned_to, department
		ORDER BY 
			average_score DESC
	""", filter_values, as_dict=1)
	
	for row in tasks:
		row.completion_rate = (row.completed_tasks / row.total_tasks) * 100 if row.total_tasks else 0
		row.average_score = round(row.average_score or 0.0, 2)
		
	return tasks

def get_conditions(filters):
	conditions = ""
	filter_values = {}
	
	if filters:
		if filters.get("department"):
			conditions += " AND department = %(department)s"
			filter_values["department"] = filters.get("department")
		if filters.get("assigned_to"):
			conditions += " AND assigned_to = %(assigned_to)s"
			filter_values["assigned_to"] = filters.get("assigned_to")
		if filters.get("task_type"):
			conditions += " AND task_type = %(task_type)s"
			filter_values["task_type"] = filters.get("task_type")
		if filters.get("date_range"):
			conditions += " AND creation BETWEEN %(start_date)s AND %(end_date)s"
			filter_values["start_date"] = filters.get("date_range")[0]
			filter_values["end_date"] = filters.get("date_range")[1]
			
	return conditions, filter_values

def get_chart(data):
	if not data:
		return None
	
	labels = [d.employee for d in data]
	scores = [d.average_score for d in data]
	completion = [d.completion_rate for d in data]
	
	return {
		"data": {
			"labels": labels[:10], # Top 10
			"datasets": [
				{"name": _("Avg Score"), "values": scores[:10]},
				{"name": _("Completion %"), "values": completion[:10]}
			]
		},
		"type": "bar",
		"colors": ["#28a745", "#007bff"]
	}

def get_report_summary(data):
	if not data:
		return []
		
	total = sum(d.total_tasks for d in data)
	completed = sum(d.completed_tasks for d in data)
	overdue = sum(d.overdue_tasks for d in data)
	avg_score = sum(d.average_score for d in data) / len(data) if data else 0
	
	return [
		{"value": total, "indicator": "Blue", "label": _("Total Tasks")},
		{"value": completed, "indicator": "Green", "label": _("Completed")},
		{"value": overdue, "indicator": "Red", "label": _("Overdue")},
		{"value": f"{round(avg_score, 1)}", "indicator": "Orange", "label": _("Team Avg Score")}
	]
