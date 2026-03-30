frappe.query_reports["Team Performance Report"] = {
	"filters": [
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "assigned_to",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "task_type",
			"label": __("Task Type"),
			"fieldtype": "Select",
			"options": "\nDelegation\nChecklist\nCompliance\nOperational"
		},
		{
			"fieldname": "date_range",
			"label": __("Creation Date"),
			"fieldtype": "DateRange",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today(), -1), frappe.datetime.get_today()]
		}
	]
};
