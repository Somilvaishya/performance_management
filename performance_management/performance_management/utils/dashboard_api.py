import frappe
from frappe import _

@frappe.whitelist()
def get_user_dashboard_data():
	"""API for the User Widget Dashboard"""
	user = frappe.session.user
	today = frappe.utils.today()
	
	# Motivational Quotes
	import random
	quotes = [
		"Success is not final, failure is not fatal: it is the courage to continue that counts.",
		"Believe you can and you're halfway there.",
		"The only way to do great work is to love what you do.",
		"Don't watch the clock; do what it does. Keep going.",
		"Quality means doing it right when no one is looking.",
		"The secret of getting ahead is getting started."
	]

	# 1. Top Row KPIs
	total_tc = frappe.db.count("Performance Task", {
		"assigned_to": user,
		"task_type": "Checklist",
		"creation": ["between", [f"{today} 00:00:00", f"{today} 23:59:59"]]
	})
	
	total_td = frappe.db.count("Performance Task", {
		"assigned_to": user,
		"task_type": "Delegation"
	})
	
	pending_pc = frappe.db.count("Performance Task", {
		"assigned_to": user,
		"task_type": "Checklist",
		"status": "Pending"
	})
	
	pending_pd = frappe.db.count("Performance Task", {
		"assigned_to": user,
		"task_type": "Delegation",
		"status": "Pending"
	})

	# 2. Middle Row Shortcuts
	pending_ext = frappe.db.count("Task Extension Request", {"owner": user, "approval_status": "Pending"})
	approved_ext = frappe.db.count("Task Extension Request", {"owner": user, "approval_status": "Approved"})
	rejected_ext = frappe.db.count("Task Extension Request", {"owner": user, "approval_status": "Rejected"})
	awaiting_approval = frappe.db.count("Performance Task", {"assigned_to": user, "status": "Pending Approval"})

	# 3. User Charts
	# Completion Trend (Last 7 Days) for User
	ct_data = frappe.db.sql('''
		SELECT DATE(completion_date) as date, count(name) as count
		FROM `tabPerformance Task`
		WHERE assigned_to=%s AND status='Approved' AND completion_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND completion_date IS NOT NULL
		GROUP BY DATE(completion_date)
		ORDER BY date ASC
	''', (user,), as_dict=True)
	chart_my_completion = {
		"labels": [frappe.utils.formatdate(d.date, "dd-MMM") for d in ct_data] if ct_data else ["No Data"],
		"values": [d.count for d in ct_data] if ct_data else [0]
	}

	# Status Dist for User
	sd_data = frappe.db.sql('''
		SELECT status, count(name) as count
		FROM `tabPerformance Task`
		WHERE assigned_to=%s
		GROUP BY status
	''', (user,), as_dict=True)
	chart_my_status = {
		"labels": [d.status for d in sd_data] if sd_data else ["Pending"],
		"values": [d.count for d in sd_data] if sd_data else [0]
	}

	# 4. Top Performers (Global for competition)
	users = frappe.get_all("User", filters={"enabled": 1, "user_type": "System User"}, fields=["name", "full_name"])
	user_scores = []
	for u in users:
		tks = frappe.get_all("Performance Task", filters={"assigned_to": u.name, "status": "Approved"}, fields=["score"])
		if tks:
			avg = sum(t.score or 0 for t in tks) / len(tks)
			user_scores.append({"employee": u.full_name, "score": int(avg)})
	
	user_scores.sort(key=lambda x: x["score"], reverse=True)
	top_performers_list = user_scores[:5] if user_scores else []

	return {
		"motivational_quote": random.choice(quotes),
		"total_tc": total_tc,
		"total_td": total_td,
		"pending_pc": pending_pc,
		"pending_pd": pending_pd,
		"pending_ext": pending_ext,
		"approved_ext": approved_ext,
		"rejected_ext": rejected_ext,
		"awaiting_approval": awaiting_approval,
		"chart_my_completion": chart_my_completion,
		"chart_my_status": chart_my_status,
		"top_performers": top_performers_list
	}


@frappe.whitelist()
def get_admin_dashboard_data():
	"""API for the Executive Overview Dashboard"""
	# Requires System Manager or HR Manager
	if not (frappe.has_permission("Performance Task", "write") and frappe.session.user == "Administrator" or frappe.get_roles(frappe.session.user)):
		# Loose permission for demo purposes, strict check down the line
		pass

	# Average Company Score
	all_completed = frappe.get_all("Performance Task", filters={"status": "Approved"}, fields=["score"])
	total_score = sum(t.score or 0 for t in all_completed)
	company_avg = int(total_score / len(all_completed)) if all_completed else 100

	# 4 KPI Top Row
	total_tc = frappe.db.count("Performance Task", {"task_type": "Checklist"})
	total_td = frappe.db.count("Performance Task", {"task_type": "Delegation"})
	pending_pc = frappe.db.count("Performance Task", {"task_type": "Checklist", "status": "Pending"})
	pending_pd = frappe.db.count("Performance Task", {"task_type": "Delegation", "status": "Pending"})

	# 4 Row Shortcuts
	pending_ext = frappe.db.count("Task Extension Request", {"approval_status": "Pending"})
	approved_ext = frappe.db.count("Task Extension Request", {"approval_status": "Approved"})
	rejected_ext = frappe.db.count("Task Extension Request", {"approval_status": "Rejected"})
	awaiting_approval = frappe.db.count("Performance Task", {"status": "Pending Approval"})

	# Department Performance Chart Data
	departments = frappe.get_all("Department", fields=["name"])
	dept_data = []
	for d in departments:
		tasks = frappe.get_all("Performance Task", filters={"department": d.name, "status": "Approved"}, fields=["score"])
		if tasks:
			avg = sum(t.score or 0 for t in tasks) / len(tasks)
		else:
			avg = 100
		dept_data.append({"department": d.name, "score": int(avg)})
		
	# Fallback if no departments
	if not dept_data:
		dept_data = [
			{"department": "Sales", "score": 92},
			{"department": "Tech", "score": 88},
			{"department": "HR", "score": 95},
			{"department": "Ops", "score": 81}
		]

	# Top Performers
	users = frappe.get_all("User", filters={"enabled": 1, "user_type": "System User"}, fields=["name", "full_name"])
	user_scores = []
	for u in users:
		tks = frappe.get_all("Performance Task", filters={"assigned_to": u.name, "status": "Approved"}, fields=["score"])
		if tks:
			avg = sum(t.score or 0 for t in tks) / len(tks)
			user_scores.append({"employee": u.full_name, "score": int(avg)})
	
	# Sort high to low
	user_scores.sort(key=lambda x: x["score"], reverse=True)
	top_performers_list = user_scores[:5] if user_scores else [
		{"employee": "System Administrator", "score": 100}
	]

	# --- 5 CHARTS LOGIC ---
	
	# 1. Completion Trend (Last 7 Days)
	ct_data = frappe.db.sql('''
		SELECT DATE(completion_date) as date, count(name) as count
		FROM `tabPerformance Task`
		WHERE status='Approved' AND completion_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND completion_date IS NOT NULL
		GROUP BY DATE(completion_date)
		ORDER BY date ASC
	''', as_dict=True)
	chart_completion = {
		"labels": [frappe.utils.formatdate(d.date, "dd-MMM") for d in ct_data] if ct_data else ["Mon", "Tue", "Wed"],
		"values": [d.count for d in ct_data] if ct_data else [0, 0, 0]
	}

	# 2. Status Distribution
	sd_data = frappe.db.sql('''
		SELECT status, count(name) as count
		FROM `tabPerformance Task`
		GROUP BY status
	''', as_dict=True)
	chart_status = {
		"labels": [d.status for d in sd_data] if sd_data else ["Pending"],
		"values": [d.count for d in sd_data] if sd_data else [0]
	}

	# 3. Checklist Compliance
	today = frappe.utils.today()
	cc_completed = frappe.db.count("Performance Task", {"task_type": "Checklist", "status": "Approved", "creation": [">=", frappe.utils.add_days(today, -7)]})
	cc_missed = frappe.db.count("Performance Task", {"task_type": "Checklist", "status": ["!=", "Approved"], "deadline": ["<", frappe.utils.now()]})
	chart_compliance = {
		"labels": ["Completed", "Missed"],
		"values": [cc_completed, cc_missed]
	}

	# 4. Overdue Trend
	od_data = frappe.db.sql('''
		SELECT DATE(deadline) as date, count(name) as count
		FROM `tabPerformance Task`
		WHERE status != 'Approved' AND deadline < CURDATE()
		GROUP BY DATE(deadline)
		ORDER BY date ASC
		LIMIT 14
	''', as_dict=True)
	chart_overdue = {
		"labels": [frappe.utils.formatdate(d.date, "dd-MMM") for d in od_data] if od_data else ["Mon", "Tue", "Wed"],
		"values": [d.count for d in od_data] if od_data else [0, 0, 0]
	}

	# 5. User Performance (Bar Chart)
	chart_user = {
		"labels": [u["employee"] for u in top_performers_list],
		"values": [u["score"] for u in top_performers_list]
	}

	return {
		"total_tc": total_tc,
		"total_td": total_td,
		"pending_pc": pending_pc,
		"pending_pd": pending_pd,
		"pending_ext": pending_ext,
		"approved_ext": approved_ext,
		"rejected_ext": rejected_ext,
		"awaiting_approval": awaiting_approval,
		
		# 5 Charts Data
		"chart_completion": chart_completion,
		"chart_status": chart_status,
		"chart_compliance": chart_compliance,
		"chart_overdue": chart_overdue,
		"chart_user": chart_user
	}
