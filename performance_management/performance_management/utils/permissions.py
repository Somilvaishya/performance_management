import frappe

def get_permission_query_conditions(user):
    if not user: user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return ""
        
    return f"(`tabPerformance Task`.assigned_to = {frappe.db.escape(user)} OR `tabPerformance Task`.assigned_by = {frappe.db.escape(user)})"

def has_permission(doc, ptype, user):
    if "System Manager" in frappe.get_roles(user):
        return True
        
    if doc.assigned_to == user or doc.assigned_by == user:
        return True
        
    return False
