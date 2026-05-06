import frappe
import requests
import json
import re

def send_whatsapp_message(employee_id, mobile_number, message):
	"""
	Sends a WhatsApp message using Green API and logs the status.
	"""
	settings = frappe.get_single("Green API Settings")
	
	if not settings.enabled:
		frappe.log_error("Green API WhatsApp is disabled in Settings", "WhatsApp Notification")
		return False
		
	if not settings.api_url or not settings.id_instance or not settings.get_password("api_token_instance"):
		frappe.log_error("Green API credentials are not fully configured", "WhatsApp Notification")
		return False
		
	api_token = settings.get_password("api_token_instance")
		
	# Clean mobile number: remove all non-digit characters
	clean_number = re.sub(r'\D', '', str(mobile_number))
	
	if len(clean_number) == 10:
		clean_number = "91" + clean_number
		
	chat_id = f"{clean_number}@c.us"
	
	url = f"{settings.api_url}/waInstance{settings.id_instance}/sendMessage/{api_token}"
	
	payload = {
		"chatId": chat_id,
		"message": message
	}
	headers = {
		'Content-Type': 'application/json'
	}
	
	log_doc = frappe.get_doc({
		"doctype": "WhatsApp Message Log",
		"recipient_employee": employee_id,
		"mobile_no": mobile_number,
		"message": message,
		"status": "Failed"
	})
	
	try:
		response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
		response.raise_for_status()
		
		log_doc.status = "Sent"
		log_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		return True
	except Exception as e:
		log_doc.error_log = str(e)
		log_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		frappe.log_error(f"Failed to send WhatsApp message to {mobile_number}: {str(e)}", "WhatsApp Notification")
		return False

def get_employee_mobile(user_email):
	"""Returns a dict with employee details for a given user email."""
	fields = ["name", "cell_number", "employee_name"]
	if frappe.db.has_column("Employee", "custom_company_phone_no"):
		fields.append("custom_company_phone_no")

	employee = frappe.db.get_value("Employee", {"user_id": user_email}, fields, as_dict=True)
	if not employee:
		return None
		
	mobile_no = employee.get("custom_company_phone_no") or employee.get("cell_number")
	if not mobile_no:
		return None
		
	return {
		"employee_id": employee.name,
		"employee_name": employee.employee_name,
		"mobile_no": mobile_no
	}

def send_dual_notification(recipient_email, subject, email_html, whatsapp_text=None):
	"""
	Sends an email via frappe.sendmail and a WhatsApp message if the user has an associated Employee profile.
	"""
	# 1. Send Email
	try:
		actual_email = frappe.db.get_value("User", recipient_email, "email") or recipient_email
		frappe.sendmail(
			recipients=actual_email,
			subject=subject,
			message=email_html,
			header=[subject, "blue"]
		)
	except Exception as e:
		frappe.log_error(f"Failed to send email to {recipient_email}: {str(e)}", "Email Notification Error")

	# 2. Send WhatsApp
	if whatsapp_text:
		emp_data = get_employee_mobile(recipient_email)
		if emp_data:
			# Prefix greeting to the provided text
			greeting = f"Hi {emp_data['employee_name']},\n\n"
			full_wa_msg = greeting + whatsapp_text
			send_whatsapp_message(emp_data['employee_id'], emp_data['mobile_no'], full_wa_msg)

