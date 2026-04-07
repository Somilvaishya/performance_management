import frappe
import html
import re

# This module handles the automated setup of Workspaces and Dashboards
# It is called by hooks.py during after_install and after_migrate

def after_install():
	# Initial setup is identical to migration for now
	after_migrate()

def after_migrate():
	# 0. Ensure essential Roles exist (prevents LinkValidationError)
	ensure_essential_roles()

	# 1. Ensure Custom HTML Blocks exist with latest HTML/JS
	ensure_custom_html_blocks()
	
	# 2. Ensure Workspaces are configured
	ensure_workspaces()
	
	# 3. Ensure Page Proxy exists for sidebar
	ensure_page_proxy()
	
	# 4. Clear cache to reflect changes
	frappe.clear_cache()

def ensure_essential_roles():
	"""Create roles if missing to avoid migration failures."""
	for role in ["Manager", "Performance Admin"]:
		if not frappe.db.exists("Role", role):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role,
				"desk_access": 1
			}).insert(ignore_permissions=True)
			frappe.db.commit()

def ensure_custom_html_blocks():
	from performance_management.performance_management.dashboard_templates import get_raw_admin_html, get_raw_user_html
	
	admin_base = get_raw_admin_html()
	user_base = get_raw_user_html()
	
	# Injected Scripts (Identical to install_dashboards.py)
	user_script = """<script src="https://unpkg.com/frappe-charts@1.6.1/dist/frappe-charts.min.umd.js"></script><script>function render_charts(data) { if(document.getElementById('chart_my_completion_trend') && data.chart_my_completion.values.length > 0) { new frappe.Chart(document.getElementById('chart_my_completion_trend'), { title: "My Task Completion Trend (Last 7 Days)", data: { labels: data.chart_my_completion.labels, datasets: [{name: "Completed", values: data.chart_my_completion.values}] }, type: 'line', height: 260, colors: ['#58e7ab'] }); } if(document.getElementById('chart_my_status_dist') && data.chart_my_status.values.length > 0) { new frappe.Chart(document.getElementById('chart_my_status_dist'), { title: "My Task Status Distribution", data: { labels: data.chart_my_status.labels, datasets: [{name: "Count", values: data.chart_my_status.values}] }, type: 'donut', height: 260, colors: ['#8387ff', '#ff6e84', '#69f6b8', '#dae2fd'] }); } } function render_leaderboard(data) { if(document.getElementById('top_performers_list') && data.top_performers) { let htmlString = '<h3 style="color:#a3a6ff; font-family:Manrope; margin-bottom:10px; border-bottom:1px solid rgba(163,166,255,0.2); padding-bottom:5px; font-size: 13px;">Global Leaderboard</h3>'; data.top_performers.forEach((p, i) => { let medal = i === 0 ? "🥇 " : i === 1 ? "🥈 " : i === 2 ? "🥉 " : "👤 "; htmlString += `<div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem; padding: 0.6rem; background: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.2s;" onmouseover="this.style.transform='translateX(4px)'" onmouseout="this.style.transform='translateX(0)'"> <span style="color:#dfe4fe; font-family:Inter; font-size: 11px;">${medal} ${p.username || p.employee}</span> <span style="color:#9bffce; font-weight:bold; font-family:Inter; font-size: 11px;">${p.score}%</span> </div>`; }); document.getElementById('top_performers_list').innerHTML = htmlString; } } window.parent.frappe.call({ method: 'performance_management.performance_management.utils.dashboard_api.get_user_dashboard_data', callback: function(r) { if (r.message) { let data = r.message; if(document.getElementById('motivational_quote')) document.getElementById('motivational_quote').innerText = data.motivational_quote; if(document.getElementById('kpi_tc')) document.getElementById('kpi_tc').innerText = data.total_tc; if(document.getElementById('kpi_td')) document.getElementById('kpi_td').innerText = data.total_td; if(document.getElementById('kpi_pc')) document.getElementById('kpi_pc').innerText = data.pending_pc; if(document.getElementById('kpi_pd')) document.getElementById('kpi_pd').innerText = data.pending_pd; if(document.getElementById('shortcut_pe')) document.getElementById('shortcut_pe').innerText = data.pending_ext; if(document.getElementById('shortcut_ae')) document.getElementById('shortcut_ae').innerText = data.approved_ext; if(document.getElementById('shortcut_re')) document.getElementById('shortcut_re').innerText = data.rejected_ext; if(document.getElementById('shortcut_aa')) document.getElementById('shortcut_aa').innerText = data.awaiting_approval; let checks = 0; let intv = setInterval(() => { if(typeof frappe !== 'undefined' && typeof frappe.Chart !== 'undefined') { clearInterval(intv); render_charts(data); render_leaderboard(data); } if(checks++ > 50) clearInterval(intv); }, 100); } } }); </script>"""
	
	admin_script = """<script src="https://unpkg.com/frappe-charts@1.6.1/dist/frappe-charts.min.umd.js"></script><script>function render_charts(data) { if(document.getElementById('chart_completion_trend') && data.chart_completion.values.length > 0) { new frappe.Chart(document.getElementById('chart_completion_trend'), { title: "Task Completion Trend (Last 7 Days)", data: { labels: data.chart_completion.labels, datasets: [{name: "Completed", values: data.chart_completion.values}] }, type: 'line', height: 260, colors: ['#58e7ab'] }); } if(document.getElementById('chart_status_dist') && data.chart_status.values.length > 0) { new frappe.Chart(document.getElementById('chart_status_dist'), { title: "Task Status Distribution", data: { labels: data.chart_status.labels, datasets: [{name: "Count", values: data.chart_status.values}] }, type: 'donut', height: 260, colors: ['#8387ff', '#ff6e84', '#69f6b8', '#dae2fd'] }); } if(document.getElementById('chart_checklist_comp') && data.chart_compliance.values.length > 0) { new frappe.Chart(document.getElementById('chart_checklist_comp'), { title: "Checklist Compliance (Last 7 Days)", data: { labels: data.chart_compliance.labels, datasets: [{name: "Tasks", values: data.chart_compliance.values}] }, type: 'donut', height: 260, colors: ['#69f6b8', '#ff6e84'] }); } if(document.getElementById('chart_overdue_trend') && data.chart_overdue.values.length > 0) { new frappe.Chart(document.getElementById('chart_overdue_trend'), { title: "Overdue Task Trend", data: { labels: data.chart_overdue.labels, datasets: [{name: "Overdue", values: data.chart_overdue.values}] }, type: 'line', height: 260, colors: ['#ff6e84'] }); } if(document.getElementById('chart_user_perf') && data.chart_user.values.length > 0) { new frappe.Chart(document.getElementById('chart_user_perf'), { title: "User Performance", data: { labels: data.chart_user.labels, datasets: [{name: "Avg Score", values: data.chart_user.values}] }, type: 'percentage', height: 260, colors: ['#a3a6ff'] }); } } window.parent.frappe.call({ method: 'performance_management.performance_management.utils.dashboard_api.get_admin_dashboard_data', callback: function(r) { if (r.message) { let data = r.message; if(document.getElementById('kpi_tc')) document.getElementById('kpi_tc').innerText = data.total_tc; if(document.getElementById('kpi_td')) document.getElementById('kpi_td').innerText = data.total_td; if(document.getElementById('kpi_pc')) document.getElementById('kpi_pc').innerText = data.pending_pc; if(document.getElementById('kpi_pd')) document.getElementById('kpi_pd').innerText = data.pending_pd; if(document.getElementById('shortcut_pe')) document.getElementById('shortcut_pe').innerText = data.pending_ext; if(document.getElementById('shortcut_ae')) document.getElementById('shortcut_ae').innerText = data.approved_ext; if(document.getElementById('shortcut_re')) document.getElementById('shortcut_re').innerText = data.rejected_ext; if(document.getElementById('shortcut_aa')) document.getElementById('shortcut_aa').innerText = data.awaiting_approval; let checks = 0; let intv = setInterval(() => { if(typeof frappe !== 'undefined' && typeof frappe.Chart !== 'undefined') { clearInterval(intv); render_charts(data); } if(checks++ > 50) clearInterval(intv); }, 100); } } }); </script>"""

	leaderboard_html = '<div class="glass-pane rounded-xxl p-6 relative overflow-hidden group"> <div class="absolute top-0 right-0 p-4"> <span class="material-symbols-outlined text-outline-variant/30 text-base">military_tech</span> </div> <div class="mb-4"> <h4 class="font-semibold text-on-surface text-sm">Top Performers</h4> <p class="text-[10px] text-on-surface-variant">Real-time Stats</p> </div> <div id="top_performers_list" class="space-y-2"> </div> </div>'

	user_injected = user_base.replace('</body>', user_script + '\n</body>')
	admin_injected = admin_base.replace('</body>', admin_script + '\n</body>')

	# Final srcdoc
	import html
	user_srcdoc = f'<iframe style="width: 100%; height: 800px; border: none; border-radius: 12px;" srcdoc="{html.escape(user_injected)}"></iframe>'
	admin_srcdoc = f'<iframe style="width: 100%; height: 800px; border: none; border-radius: 12px;" srcdoc="{html.escape(admin_injected)}"></iframe>'

	# Update or create Custom HTML Blocks
	for block_name, block_html in [("PM Admin Dashboard", admin_srcdoc), ("PM User Dashboard", user_srcdoc)]:
		if frappe.db.exists("Custom HTML Block", block_name):
			doc = frappe.get_doc("Custom HTML Block", block_name)
			doc.html = block_html
			doc.private = 0
			doc.save(ignore_permissions=True)
		else:
			frappe.get_doc({
				"doctype": "Custom HTML Block",
				"name": block_name,
				"html_block_name": block_name,
				"html": block_html,
				"private": 0
			}).insert(ignore_permissions=True)

def ensure_workspaces():
	"""Consolidate all dashboards into a single, clean 'Performance Management' workspace."""
	# 1. Handle the main "Performance Management" workspace
	ws_name = "Performance Management"
	if frappe.db.exists("Workspace", ws_name):
		doc = frappe.get_doc("Workspace", ws_name)
	else:
		doc = frappe.new_doc("Workspace")
		doc.name = ws_name

	doc.label = ws_name
	doc.title = ws_name
	doc.type = "Workspace"
	doc.public = 1
	doc.module = "Performance Management"
	doc.icon = "octicon-graph"
	doc.parent_page = ""
	
	# CLEANUP: Remove all default components
	doc.links = []
	doc.shortcuts = []
	doc.number_cards = []
	doc.charts = []
	
	# ENSURE CUSTOM BLOCKS ONLY
	doc.custom_blocks = []
	doc.append("custom_blocks", {
		"custom_block_name": "PM Admin Dashboard",
		"label": "Admin Overview",
		"idx": 0
	})
	doc.append("custom_blocks", {
		"custom_block_name": "PM User Dashboard",
		"label": "My Performance",
		"idx": 1
	})
	
	# Clear "content" field to ensure fallback to child tables in newer Frappe versions
	# MUST be a JSON list string to pass Workspace.validate()
	doc.content = "[]"
	
	# Ensure roles include "All" for broad accessibility
	if not any(r.role == "All" for r in doc.roles):
		doc.append("roles", {"role": "All"})
		
	doc.save(ignore_permissions=True)

	# 2. DELETE redundant workspaces
	old_ws = "User Performance Dashboard"
	if frappe.db.exists("Workspace", old_ws):
		frappe.delete_doc("Workspace", old_ws, force=True, ignore_permissions=True)

def ensure_page_proxy():
	p_id = "pm-user-dashboard"
	if not frappe.db.exists("Page", p_id):
		# SQL insert to bypass Developer Mode safely during installation
		frappe.db.sql(f"""
			INSERT INTO `tabPage` (name, page_name, title, module, standard, creation, modified, owner, modified_by)
			VALUES ('{p_id}', '{p_id}', 'User Dashboard', 'Performance Management', 1, NOW(), NOW(), 'Administrator', 'Administrator')
		""")
		frappe.db.sql(f"INSERT INTO `tabHas Role` (name, parent, parenttype, parentfield, role, idx) VALUES (UUID(), '{p_id}', 'Page', 'roles', 'All', 1)")
