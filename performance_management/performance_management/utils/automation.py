import frappe
from frappe.utils import now_datetime, get_datetime, add_days, today


def mark_overdue_tasks():
	"""Hourly job: Mark tasks as overdue if past deadline."""
	tasks = frappe.get_all(
		"Performance Task",
		filters={
			"status": ["in", ["Pending", "In Progress"]],
			"deadline": ["<", now_datetime()],
			"is_overdue": 0
		},
		fields=["name"]
	)
	for t in tasks:
		frappe.db.set_value("Performance Task", t.name, "is_overdue", 1)
	if tasks:
		frappe.db.commit()
	return len(tasks)


def send_daily_reminders():
	"""Daily job: Send reminder email to each user with pending/in-progress tasks due today."""
	today_str = today()
	tasks = frappe.db.sql("""
		SELECT assigned_to, name, task_title, deadline, is_overdue
		FROM `tabPerformance Task`
		WHERE status IN ('Pending', 'In Progress')
		AND DATE(deadline) <= %s
	""", today_str, as_dict=True)

	# Group by user
	from collections import defaultdict
	user_tasks = defaultdict(list)
	for t in tasks:
		user_tasks[t.assigned_to].append(t)

	for user, user_task_list in user_tasks.items():
		try:
			send_reminder_email(user, user_task_list)
		except Exception:
			frappe.log_error(frappe.get_traceback(), f"Reminder failed for {user}")


def send_reminder_email(user, tasks):
	user_doc = frappe.get_doc("User", user)
	if not user_doc.email:
		return

	rows = ""
	for t in tasks:
		overdue_tag = '<span style="color:red; font-weight:bold;"> ⚠ OVERDUE</span>' if t.is_overdue else ""
		rows += f"<tr><td><b>{t.name}</b></td><td>{t.task_title}</td><td>{t.deadline}{overdue_tag}</td></tr>"

	html = f"""
	<p>Hi {user_doc.first_name},</p>
	<p>Here are your open tasks for today.</p>
	<p><i>Note: This includes tasks due today as well as any previously overdue tasks.</i></p>
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
		<thead>
			<tr style="background-color: #f3f4f6;">
				<th style="text-align: left;">Task ID</th>
				<th style="text-align: left;">Title</th>
				<th style="text-align: left;">Deadline</th>
			</tr>
		</thead>
		<tbody>{rows}</tbody>
	</table>
	<p>Please log in to your Workspace and update your task statuses.</p>
	"""

	frappe.sendmail(
		recipients=[user_doc.email],
		subject=f"📋 Your Daily Task Reminder — {len(tasks)} Pending",
		message=html
	)
