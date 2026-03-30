import frappe
from frappe import _
from frappe.model.document import Document

class TaskExtensionRequest(Document):

	def validate(self):
		if self.task:
			task_doc = frappe.get_doc("Performance Task", self.task)
			if task_doc.task_type != "Delegation":
				frappe.throw(_("Extensions are only allowed for tasks of type 'Delegation'."))
			if (task_doc.extension_count or 0) >= 5:
				frappe.throw(_("Maximum of 5 extensions are allowed per task."))

	def on_update(self):
		if self.has_value_changed("approval_status") and self.approval_status == "Approved":
			self.update_parent_task_deadline()

	def after_insert(self):
		if self.task:
			task_doc = frappe.get_doc("Performance Task", self.task)
			msg = f"<p>Hello,</p><p><strong>{self.requested_by}</strong> has requested to extend the deadline for task <strong>{task_doc.task_title}</strong> to <strong>{self.requested_deadline}</strong>.</p><p>Reason: {self.reason}</p>"
			self._send_notification(task_doc.assigned_by, f"Extension Requested: {task_doc.task_title}", msg)

	def _send_notification(self, recipient, subject, message):
		try:
			recipient_email = frappe.db.get_value("User", recipient, "email") or recipient
			frappe.sendmail(recipients=recipient_email, subject=subject, message=message, header=[subject, "blue"])
		except Exception as e:
			frappe.log_error(f"Failed to send email to {recipient}: {str(e)}", "Email Notification Error")

	def _send_decision_email(self, decision, reason=None):
		task_title = frappe.db.get_value("Performance Task", self.task, "task_title") or self.task
		reason_html = f"<p>Manager Comments: {reason}</p>" if reason else ""
		color = "green" if decision == "Approved" else "red"
		msg = f"<p>Hello,</p><p>Your extension request for <strong>{task_title}</strong> has been <b><span style='color:{color}'>{decision}</span></b>.</p>{reason_html}"
		self._send_notification(self.requested_by, f"Extension {decision}: {task_title}", msg)

	def update_parent_task_deadline(self):
		if not self.task:
			return

		task = frappe.get_doc("Performance Task", self.task)
		task.deadline = self.requested_deadline
		task.extension_count = (task.extension_count or 0) + 1
		
		# Immediately deduct 20% for this extension
		task.score = max(0.0, (task.score or 100.0) - 20.0)

		# If the task was overdue, clearing the overdue flag since deadline is extended
		task.is_overdue = 0
		task.save(ignore_permissions=True)

		frappe.msgprint(_("Task Deadline Updated Successfully to: {0}").format(self.requested_deadline), alert=True, indicator="green")


@frappe.whitelist()
def approve_extension(request_name):
	req = frappe.get_doc("Task Extension Request", request_name)
	if req.approval_status != "Pending":
		frappe.throw(_("Can only approve Pending requests."))
	req.approval_status = "Approved"
	req.save(ignore_permissions=True)
	req._send_decision_email("Approved")
	return {"status": "approved"}

@frappe.whitelist()
def reject_extension(request_name, reason):
	req = frappe.get_doc("Task Extension Request", request_name)
	if req.approval_status != "Pending":
		frappe.throw(_("Can only reject Pending requests."))
	req.approval_status = "Rejected"
	req.rejection_reason = reason
	req.save(ignore_permissions=True)
	req._send_decision_email("Rejected", reason)
	return {"status": "rejected"}


def get_permission_query_conditions(user):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return ""
	return f"(`tabTask Extension Request`.requested_by = '{frappe.db.escape(user)}')"


def has_permission(doc, ptype="read", user=None):
	if not user:
		user = frappe.session.user
	if user == "Administrator":
		return True
	if doc.requested_by == user:
		return True
	return False
