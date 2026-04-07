import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime


VALID_STATUSES = ["Draft", "Pending", "In Progress", "Pending Approval", "Approved", "Reopened", "Cancelled"]


class PerformanceTask(Document):

	def validate(self):
		self._set_assigned_by()
		self._set_approval_requirement()
		self._check_overdue()

	def before_save(self):
		self._handle_completion()
		
	def after_insert(self):
		if not self.flags.ignore_assignment_email:
			self._send_assignment_email()

	def on_update(self):
		if self.has_value_changed("status") and self.status == "Pending Approval":
			self._send_submission_email()
		self._log_audit("Update")

	# ── Internal helpers ──────────────────────────────────────────────────────

	def _set_assigned_by(self):
		if not self.assigned_by:
			self.assigned_by = frappe.session.user

	def _set_approval_requirement(self):
		"""Auto-check 'Requires Approval' for High/Critical/Compliance tasks."""
		if self.priority in ("High", "Critical") or self.task_type == "Compliance":
			self.requires_approval = 1

	def _check_overdue(self):
		if self.deadline and self.status not in ("Approved", "Cancelled"):
			self.is_overdue = 1 if get_datetime(self.deadline) < now_datetime() else 0

	def _handle_completion(self):
		"""When marked Approved, set completion date and calculate score."""
		if self.status == "Approved" and not self.completion_date:
			self.completion_date = now_datetime()
			self._calculate_score()
		if self.status == "Reopened":
			self.score = max(0.0, (self.score or 100.0) - 20.0)

	def _calculate_score(self):
		base = 100.0
		base -= (self.extension_count or 0) * 20.0
		if self.deadline and self.completion_date:
			delay = (get_datetime(self.completion_date) - get_datetime(self.deadline)).days
			if delay > 0:
				base -= min(delay * 10, 50)
		self.score = max(0.0, base)

	def _log_audit(self, action):
		try:
			frappe.get_doc({
				"doctype": "PM Audit Log",
				"reference_doctype": self.doctype,
				"reference_name": self.name,
				"action": action,
				"user": frappe.session.user,
				"timestamp": now_datetime(),
				"details": f"Status: {self.status} | Priority: {self.priority}"
			}).insert(ignore_permissions=True)
		except Exception:
			pass  # Never let logging break the main flow

	def _send_notification(self, recipient, subject, message):
		try:
			recipient_email = frappe.db.get_value("User", recipient, "email") or recipient
			frappe.sendmail(
				recipients=recipient_email,
				subject=subject,
				message=message,
				header=[subject, "blue"]
			)
		except Exception as e:
			frappe.log_error(f"Failed to send email to {recipient}: {str(e)}", "Email Notification Error")

	def _send_assignment_email(self):
		if self.assigned_to:
			msg = f"<p>Hello,</p><p>You have been assigned a new task: <strong>{self.task_title}</strong>.</p><p>Priority: <b>{self.priority}</b><br>Deadline: <b>{self.deadline or 'None'}</b></p>"
			self._send_notification(self.assigned_to, f"New Task Assigned: {self.task_title}", msg)

	def _send_submission_email(self):
		if self.assigned_by:
			msg = f"<p>Hello,</p><p><strong>{self.assigned_to}</strong> has submitted the task <strong>{self.task_title}</strong> for your approval.</p>"
			self._send_notification(self.assigned_by, f"Task Pending Approval: {self.task_title}", msg)

	def _send_decision_email(self, decision, reason=None):
		if self.assigned_to:
			reason_html = f"<p>Manager Comments: {reason}</p>" if reason else ""
			color = "green" if decision == "Approved" else "red"
			msg = f"<p>Hello,</p><p>Your task <strong>{self.task_title}</strong> has been <b><span style='color:{color}'>{decision}</span></b>.</p>{reason_html}"
			self._send_notification(self.assigned_to, f"Task {decision}: {self.task_title}", msg)

	# ── Whitelisted APIs ──────────────────────────────────────────────────────

@frappe.whitelist()
def approve_task(task_name):
	"""Manager approves a task — sets Approved status directly."""
	task = frappe.get_doc("Performance Task", task_name)
	if task.status != "Pending Approval":
		frappe.throw(_("Task must be in 'Pending Approval' status to approve."))
	task.status = "Approved"
	task.approved_by = frappe.session.user
	task.approval_status = "Approved"
	task.save(ignore_permissions=True)
	task._send_decision_email("Approved")
	return {"status": "approved", "score": task.score}


@frappe.whitelist()
def reject_task(task_name, reason):
	"""Manager rejects — moves task to Reopened."""
	task = frappe.get_doc("Performance Task", task_name)
	if task.status != "Pending Approval":
		frappe.throw(_("Task must be in 'Pending Approval' status to reject."))
	task.status = "Reopened"
	task.rejection_reason = reason
	task.approval_status = "Rejected"
	task.save(ignore_permissions=True)
	task._send_decision_email("Rejected", reason)
	return {"status": "rejected"}


@frappe.whitelist()
def get_my_tasks(user=None):
	"""Returns open tasks for the current user (for dashboard)."""
	user = user or frappe.session.user
	return frappe.get_all(
		"Performance Task",
		filters={"assigned_to": user, "status": ["not in", ["Approved", "Cancelled"]]},
		fields=["name", "task_title", "status", "priority", "deadline", "is_overdue"],
		order_by="deadline asc"
	)


@frappe.whitelist()
def generate_tasks_from_template(template_name, assigned_to, deadline):
	"""Bulk create Performance Tasks from a Checklist Template."""
	template = frappe.get_doc("Checklist Template", template_name)
	created = []
	for item in template.items:
		task = frappe.get_doc({
			"doctype": "Performance Task",
			"task_title": item.item_title,
			"description": item.description or "",
			"task_type": template.task_type,
			"priority": template.default_priority,
			"department": template.department,
			"assigned_to": assigned_to,
			"assigned_by": frappe.session.user,
			"deadline": deadline,
			"checklist_template": template_name,
			"frequency": template.frequency,
			"status": "Pending"
		})
		task.flags.ignore_assignment_email = True
		task.insert(ignore_permissions=True)
		created.append(task.name)
	return {"created": created, "count": len(created)}


def get_permission_query_conditions(user):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return ""
	return f"(`tabPerformance Task`.assigned_to = '{frappe.db.escape(user)}' OR `tabPerformance Task`.assigned_by = '{frappe.db.escape(user)}')"


def has_permission(doc, ptype="read", user=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return True
	if doc.assigned_to == user or doc.assigned_by == user:
		return True
	return False
