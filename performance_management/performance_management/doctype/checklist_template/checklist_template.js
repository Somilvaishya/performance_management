frappe.ui.form.on("Checklist Template", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.items && frm.doc.items.length > 0) {
			frm.add_custom_button(__("Generate Tasks from Template"), () => {
				frappe.prompt([
					{ label: "Assign To", fieldname: "assigned_to", fieldtype: "Link", options: "User", reqd: 1 },
					{ label: "Deadline", fieldname: "deadline", fieldtype: "Datetime", reqd: 1 }
				], (values) => {
					frappe.call({
						method: "performance_management.performance_management.doctype.performance_task.performance_task.generate_tasks_from_template",
						args: {
							template_name: frm.doc.name,
							assigned_to: values.assigned_to,
							deadline: values.deadline
						},
						freeze: true,
						freeze_message: "Generating Checklist Tasks...",
						callback(r) {
							if (r.message && r.message.count) {
								frappe.msgprint({
									title: "Success",
									indicator: "green",
									message: `Successfully generated ${r.message.count} tasks assigned to ${values.assigned_to}.`
								});
							}
						}
					});
				}, __("Assign Checklist Tasks"), __("Generate"));
			}, __("Actions"));
		}
	}
});
