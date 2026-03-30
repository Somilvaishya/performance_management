frappe.ui.form.on("Task Extension Request", {
	refresh(frm) {
		const is_manager = frappe.user.has_role("System Manager") || frappe.user.has_role("HR Manager");

		if (frm.doc.approval_status === "Pending" && !frm.is_new() && is_manager) {
			frm.add_custom_button(__("Approve Extension"), () => {
				frappe.confirm(__("Are you sure you want to approve this extension request? This will automatically update the parent task's deadline."), () => {
					frappe.call({
						method: "performance_management.performance_management.doctype.task_extension_request.task_extension_request.approve_extension",
						args: { request_name: frm.doc.name },
						callback() {
							frm.reload_doc();
							frappe.show_alert({ message: "Extension Approved and Task Deadline Updated!", indicator: "green" });
						}
					});
				});
			}, __("Actions"));

			frm.add_custom_button(__("Reject Extension"), () => {
				frappe.prompt([
					{ label: "Rejection Reason", fieldname: "reason", fieldtype: "Text", reqd: 1 }
				], (values) => {
					frappe.call({
						method: "performance_management.performance_management.doctype.task_extension_request.task_extension_request.reject_extension",
						args: { request_name: frm.doc.name, reason: values.reason },
						callback() {
							frm.reload_doc();
							frappe.show_alert({ message: "Extension Rejected.", indicator: "orange" });
						}
					});
				});
			}, __("Actions"));
		}

		// Disable form if not pending
		if (frm.doc.approval_status !== "Pending") {
			frm.disable_form();
		}
	}
});
