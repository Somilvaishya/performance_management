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
	items = frappe.get_all(
		"Checklist Template Item",
		filters={"parent": template.name},
		fields=["item_title", "description"]
	)
	if not items:
		return 0
		
	if not template.assigned_to:
		frappe.logger("performance").warning(f"Checklist Template {template.name} has no assigned user.")
		return 0
		
	count = 0
	today_str = today()
	
	# Bug 1 Fix: Set deadline to end-of-day so the hourly mark_overdue_tasks
	# job does NOT immediately mark newly-created tasks as overdue.
	# The field type is Datetime; a plain date string resolves to 00:00:00
	# which is immediately in the past for any job running after midnight.
	deadline_eod = today_str + " 23:59:59"
	
	for item in items:
		# Anti-duplicate check: use date portion of deadline for matching
		exists = frappe.db.sql("""
			SELECT name FROM `tabPerformance Task`
			WHERE task_title = %s
			  AND assigned_to = %s
			  AND DATE(deadline) = %s
			  AND checklist_template = %s
			LIMIT 1
		""", (item.item_title, template.assigned_to, today_str, template.name))
		
		if not exists:
			# Bug 3 Fix: Copy frequency from the template so the Performance Task
			# correctly reflects which frequency generated it.
			doc = frappe.get_doc({
				"doctype": "Performance Task",
				"task_title": item.item_title,
				"description": item.description or "",
				"task_type": "Checklist",
				"frequency": template.frequency,          # ← Bug 3 fix
				"priority": template.default_priority or "Medium",
				"department": template.department,
				"assigned_to": template.assigned_to,
				"assigned_by": "Administrator",
				"deadline": deadline_eod,                 # ← Bug 1 fix
				"checklist_template": template.name,
				"status": "Pending",
				"requires_approval": 0
			})
			doc.flags.ignore_assignment_email = True
			doc.insert(ignore_permissions=True)
			count += 1
			
	return count
