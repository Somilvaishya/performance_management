import frappe
from frappe.utils import today, getdate

def create_daily_checklists():
	"""
	Scheduler job running daily.
	Fetches all active Checklist Templates and generates Tasks based on frequency.
	"""
	templates = frappe.get_all("Checklist Template", filters={"active": 1}, fields=["*"])
	current_date = getdate(today())
	
	count = 0
	
	for template in templates:
		if should_run_today(template.frequency, current_date):
			count += create_tasks_for_template(template)
			
	frappe.logger("performance").info(f"Checklist Service: Auto-generated {count} tasks for {today()}")


def should_run_today(frequency, current_date):
	"""Determine if a template should generate tasks for the current_date based on frequency"""
	if not frequency:
		return False
		
	if frequency == "Daily":
		return True
		
	# Weekly: Run on Monday
	if frequency == "Weekly" and current_date.weekday() == 0:
		return True
		
	# Monthly: Run on the 1st
	if frequency == "Monthly" and current_date.day == 1:
		return True
		
	# Quarterly: Run on 1st of Jan, Apr, Jul, Oct
	if frequency == "Quarterly" and current_date.day == 1 and current_date.month in [1, 4, 7, 10]:
		return True
		
	# Half-Yearly: Run on 1st of Jan, Jul
	if frequency == "Half-Yearly" and current_date.day == 1 and current_date.month in [1, 7]:
		return True
		
	# Yearly: Run on 1st of Jan
	if frequency == "Yearly" and current_date.day == 1 and current_date.month == 1:
		return True
		
	return False


def create_tasks_for_template(template):
	"""Iterates through template items and creates tasks"""
	items = frappe.get_all("Checklist Template Item", filters={"parent": template.name}, fields=["item_title", "description"])
	if not items:
		return 0
		
	if not template.assigned_to:
		frappe.logger("performance").warning(f"Checklist Template {template.name} has no assigned user.")
		return 0
		
	count = 0
	today_str = today()
	
	for item in items:
		# Anti-duplicate check (same title, user, and deadline)
		exists = frappe.db.exists("Performance Task", {
			"task_title": item.item_title,
			"assigned_to": template.assigned_to,
			"deadline": today_str,
			"checklist_template": template.name
		})
		
		if not exists:
			doc = frappe.get_doc({
				"doctype": "Performance Task",
				"task_title": item.item_title,
				"description": item.description or "",
				"task_type": "Checklist",
				"priority": template.default_priority or "Medium",
				"department": template.department,
				"assigned_to": template.assigned_to,
				"assigned_by": "Administrator",
				"deadline": today_str,
				"checklist_template": template.name,
				"status": "Pending",
				"requires_approval": 0 # Default for checklist
			})
			doc.flags.ignore_assignment_email = True
			doc.insert(ignore_permissions=True)
			count += 1
			
	return count
