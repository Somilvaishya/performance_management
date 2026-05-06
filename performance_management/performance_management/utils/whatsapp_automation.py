import frappe
from frappe.utils import today
from performance_management.performance_management.utils.whatsapp import send_whatsapp_message

def send_daily_whatsapp_reminders():
	"""
	Daily job: Send WhatsApp reminder to each user
	with pending/in-progress tasks due today or already overdue.
	"""
	today_str = today()
	tasks = frappe.db.sql("""
		SELECT assigned_to, name, task_title, deadline, is_overdue, task_type
		FROM `tabPerformance Task`
		WHERE status IN ('Pending', 'In Progress')
		AND DATE(deadline) <= %s
	""", today_str, as_dict=True)

	if not tasks:
		return

	# Group by user
	from collections import defaultdict
	user_tasks = defaultdict(list)
	for t in tasks:
		user_tasks[t.assigned_to].append(t)

	for user, user_task_list in user_tasks.items():
		try:
			send_reminder_whatsapp(user, user_task_list)
		except Exception as e:
			frappe.log_error(f"WhatsApp Reminder failed for {user}: {str(e)}", "WhatsApp Automation")


def send_reminder_whatsapp(user, tasks):
	fields = ["name", "cell_number", "employee_name"]
	if frappe.db.has_column("Employee", "custom_company_phone_no"):
		fields.append("custom_company_phone_no")

	employee = frappe.db.get_value("Employee", {"user_id": user}, fields, as_dict=True)
	
	if not employee:
		# User doesn't have an associated employee record
		return

	mobile_no = employee.get("custom_company_phone_no") or employee.get("cell_number")
	if not mobile_no:
		# Employee doesn't have a mobile number configured
		return

	overdue_tasks = [t for t in tasks if t.is_overdue]
	checklist_tasks = [t for t in tasks if not t.is_overdue and t.task_type == "Checklist"]
	other_tasks = [t for t in tasks if not t.is_overdue and t.task_type != "Checklist"]
	
	# Build WhatsApp Message Text
	message = f"Hi {employee.employee_name},\n\n"
	message += f"📋 *Your Daily Task Summary*\n"
	message += f"You have {len(tasks)} tasks requiring your attention:\n\n"
	
	if overdue_tasks:
		message += "🚨 *OVERDUE TASKS*\n"
		for t in overdue_tasks:
			message += f"• *{t.task_title}* (Due: {t.deadline})\n"
		message += "\n"
		
	if checklist_tasks:
		message += "✅ *DAILY CHECKLIST*\n"
		for t in checklist_tasks:
			message += f"• *{t.task_title}*\n"
		message += "\n"
		
	if other_tasks:
		message += "📝 *STANDARD TASKS DUE TODAY*\n"
		for t in other_tasks:
			message += f"• *{t.task_title}*\n"
		message += "\n"
		
	message += "Please log in to your Workspace and update your task statuses.\n"
	message += "Have a great day!"

	# Send via Green API
	send_whatsapp_message(employee.name, mobile_no, message)
