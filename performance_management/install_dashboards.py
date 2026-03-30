import frappe
import urllib.request
import re

def install():
	frappe.init(site="workspace.test", sites_path="sites")
	frappe.connect()

	user_url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2E5ZGIzYjE0NTdlMzRiODU4ZGM1MDYyMzViZGY1NDJmEgsSBxDTnO2hxBUYAZIBIwoKcHJvamVjdF9pZBIVQhMxODEwNDUzODA0OTgzNTczOTUw&filename=&opi=96797242"
	admin_url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzRkZTU5ZDFmY2U0ODRiMDM5ZWM0ZjA3NDMyM2NiNDVhEgsSBxDTnO2hxBUYAZIBIwoKcHJvamVjdF9pZBIVQhMxODEwNDUzODA0OTgzNTczOTUw&filename=&opi=96797242"

	req = urllib.request.Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})
	user_html = urllib.request.urlopen(req).read().decode('utf-8')
	
	req = urllib.request.Request(admin_url, headers={'User-Agent': 'Mozilla/5.0'})
	admin_html = urllib.request.urlopen(req).read().decode('utf-8')

	import html

	user_injected_script = """
		<script src="https://unpkg.com/frappe-charts@1.6.1/dist/frappe-charts.min.umd.js"></script>
		<script>
		function render_charts(data) {
			if(document.getElementById('chart_my_completion_trend') && data.chart_my_completion.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_my_completion_trend'), {
					title: "My Task Completion Trend (Last 7 Days)",
					data: { labels: data.chart_my_completion.labels, datasets: [{name: "Completed", values: data.chart_my_completion.values}] },
					type: 'line', height: 300, colors: ['#58e7ab']
				});
			}
			if(document.getElementById('chart_my_status_dist') && data.chart_my_status.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_my_status_dist'), {
					title: "My Task Status Distribution",
					data: { labels: data.chart_my_status.labels, datasets: [{name: "Count", values: data.chart_my_status.values}] },
					type: 'donut', height: 300, colors: ['#8387ff', '#ff6e84', '#69f6b8', '#dae2fd']
				});
			}
		}

		function render_leaderboard(data) {
			if(document.getElementById('top_performers_list') && data.top_performers) {
				let htmlString = '<h3 style="color:#a3a6ff; font-family:Manrope; margin-bottom:15px; border-bottom:1px solid rgba(163,166,255,0.2); padding-bottom:8px;">Global Leaderboard</h3>';
				data.top_performers.forEach((p, i) => {
					let medal = i === 0 ? "🥇 " : i === 1 ? "🥈 " : i === 2 ? "🥉 " : "👤 ";
					htmlString += `<div style="display:flex; justify-content:space-between; margin-bottom: 0.8rem; padding: 0.8rem; background: rgba(255,255,255,0.05); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.2s;" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
						<span style="color:#dfe4fe; font-family:Inter;">${medal} ${p.employee}</span>
						<span style="color:#9bffce; font-weight:bold; font-family:Inter;">${p.score}%</span>
					</div>`;
				});
				document.getElementById('top_performers_list').innerHTML = htmlString;
			}
		}

		window.parent.frappe.call({
			method: 'performance_management.performance_management.utils.dashboard_api.get_user_dashboard_data',
			callback: function(r) {
				if (r.message) {
					let data = r.message;
					if(document.getElementById('motivational_quote')) document.getElementById('motivational_quote').innerText = data.motivational_quote;
					if(document.getElementById('kpi_tc')) document.getElementById('kpi_tc').innerText = data.total_tc;
					if(document.getElementById('kpi_td')) document.getElementById('kpi_td').innerText = data.total_td;
					if(document.getElementById('kpi_pc')) document.getElementById('kpi_pc').innerText = data.pending_pc;
					if(document.getElementById('kpi_pd')) document.getElementById('kpi_pd').innerText = data.pending_pd;
					if(document.getElementById('shortcut_pe')) document.getElementById('shortcut_pe').innerText = data.pending_ext;
					if(document.getElementById('shortcut_ae')) document.getElementById('shortcut_ae').innerText = data.approved_ext;
					if(document.getElementById('shortcut_re')) document.getElementById('shortcut_re').innerText = data.rejected_ext;
					if(document.getElementById('shortcut_aa')) document.getElementById('shortcut_aa').innerText = data.awaiting_approval;

					let checks = 0;
					let intv = setInterval(() => {
						if(typeof frappe !== 'undefined' && typeof frappe.Chart !== 'undefined') {
							clearInterval(intv);
							render_charts(data);
							render_leaderboard(data);
						}
						if(checks++ > 50) clearInterval(intv);
					}, 100);
				}
			}
		});
		</script>
	"""

	admin_injected_script = """
		<script src="https://unpkg.com/frappe-charts@1.6.1/dist/frappe-charts.min.umd.js"></script>
		<script>
		function render_charts(data) {
			if(document.getElementById('chart_completion_trend') && data.chart_completion.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_completion_trend'), {
					title: "Task Completion Trend (Last 7 Days)",
					data: { labels: data.chart_completion.labels, datasets: [{name: "Completed", values: data.chart_completion.values}] },
					type: 'line', height: 300, colors: ['#58e7ab']
				});
			}
			if(document.getElementById('chart_status_dist') && data.chart_status.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_status_dist'), {
					title: "Task Status Distribution",
					data: { labels: data.chart_status.labels, datasets: [{name: "Count", values: data.chart_status.values}] },
					type: 'donut', height: 300, colors: ['#8387ff', '#ff6e84', '#69f6b8', '#dae2fd']
				});
			}
			if(document.getElementById('chart_checklist_comp') && data.chart_compliance.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_checklist_comp'), {
					title: "Checklist Compliance (Last 7 Days)",
					data: { labels: data.chart_compliance.labels, datasets: [{name: "Tasks", values: data.chart_compliance.values}] },
					type: 'donut', height: 300, colors: ['#69f6b8', '#ff6e84']
				});
			}
			if(document.getElementById('chart_overdue_trend') && data.chart_overdue.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_overdue_trend'), {
					title: "Overdue Task Trend",
					data: { labels: data.chart_overdue.labels, datasets: [{name: "Overdue", values: data.chart_overdue.values}] },
					type: 'line', height: 300, colors: ['#ff6e84']
				});
			}
			if(document.getElementById('chart_user_perf') && data.chart_user.values.length > 0) {
				new frappe.Chart(document.getElementById('chart_user_perf'), {
					title: "User Performance",
					data: { labels: data.chart_user.labels, datasets: [{name: "Avg Score", values: data.chart_user.values}] },
					type: 'percentage', height: 300, colors: ['#a3a6ff']
				});
			}
		}

		window.parent.frappe.call({
			method: 'performance_management.performance_management.utils.dashboard_api.get_admin_dashboard_data',
			callback: function(r) {
				if (r.message) {
					let data = r.message;
					if(document.getElementById('kpi_tc')) document.getElementById('kpi_tc').innerText = data.total_tc;
					if(document.getElementById('kpi_td')) document.getElementById('kpi_td').innerText = data.total_td;
					if(document.getElementById('kpi_pc')) document.getElementById('kpi_pc').innerText = data.pending_pc;
					if(document.getElementById('kpi_pd')) document.getElementById('kpi_pd').innerText = data.pending_pd;
					if(document.getElementById('shortcut_pe')) document.getElementById('shortcut_pe').innerText = data.pending_ext;
					if(document.getElementById('shortcut_ae')) document.getElementById('shortcut_ae').innerText = data.approved_ext;
					if(document.getElementById('shortcut_re')) document.getElementById('shortcut_re').innerText = data.rejected_ext;
					if(document.getElementById('shortcut_aa')) document.getElementById('shortcut_aa').innerText = data.awaiting_approval;
					
					let checks = 0;
					let intv = setInterval(() => {
						if(typeof frappe !== 'undefined' && typeof frappe.Chart !== 'undefined') {
							clearInterval(intv);
							render_charts(data);
						}
						if(checks++ > 50) clearInterval(intv);
					}, 100);
				}
			}
		});
		</script>
	"""

	# Inject the leaderboard container into User HTML bottom matrix
	leaderboard_html = """
		<!-- Leaderboard Container -->
		<div class="glass-pane rounded-xxl p-8 relative overflow-hidden group">
			<div class="absolute top-0 right-0 p-4">
				<span class="material-symbols-outlined text-outline-variant/50">military_tech</span>
			</div>
			<div class="mb-6">
				<h4 class="font-semibold text-on-surface">Top Performers</h4>
				<p class="text-xs text-on-surface-variant">Real-time Global Leaderboard</p>
			</div>
			<div id="top_performers_list" class="space-y-3">
				<!-- JS will populate this -->
			</div>
		</div>
	"""
	
	# More robust regex: find the end of the Status Distribution card wrapper and inject after it
	# Looking for the div that contains id="chart_my_status_dist" and its following closing divs
	# The source HTML has chart container inside a glass-pane. We want to inject after the glass-pane.
	# Pattern: find the container with chart_my_status_dist, then match until the second </div>
	user_html = re.sub(r'(<div[^>]*id="chart_my_status_dist".*?</div>\s*</div>)', r'\1' + leaderboard_html, user_html, flags=re.DOTALL)
	
	# Actually, the previous regex might have matched too early. Let's try matching the specific glass-pane wrapper
	# I'll just look for the second glass-pane in the matrix section and append after it.
	# But the current regex actually DID find it, it just pattern-matched the inner </div> first.
	
	# Let's try this instead:
	# Find the second occurrence of '<div class="glass-pane rounded-xxl p-8 relative overflow-hidden group">' in the section
	# and append after its closing </div></div>
	parts = user_html.split('<div class="glass-pane rounded-xxl p-8 relative overflow-hidden group">')
	if len(parts) >= 3:
		# parts[0] is header, parts[1] is first chart, parts[2] is second chart + rest
		# We want to inject after the second chart's </div></div> (one for chart, one for glass-pane)
		# But wait, looking at the dump, the leaderboard was ALREADY injected into parts[2].
		pass

	# I'll just rewrite the whole matrix section to be safe
	matrix_start = user_html.find('<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">')
	if matrix_start == -1:
		matrix_start = user_html.find('<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">')
		
	if matrix_start != -1:
		# Find the end of this grid section
		pass

	# SIMPLER: I'll just use the fact that I know the IDs.
	# I'll remove the previous (failed) injection first if it exists
	user_html = user_html.replace(leaderboard_html, "")
	
	# Now inject properly:
	# Find the div with id="chart_my_status_dist", go up levels to find its closing glass-pane </div>
	# Based on the dump: </div>\n</div>\n</div> for chart, inner grid, and glass-pane? No.
	# Dump shows: <div id="chart_my_status_dist">...</div>\n</div> (glass-pane)
	user_html = user_html.replace('id="chart_my_status_dist" style="height:300px; width:100%;">\n<!-- Chart placeholder aesthetic -->\n<div class="w-full h-full flex items-center justify-center opacity-20">\n<div class="w-48 h-48 rounded-full border-[16px] border-primary-dim border-t-tertiary border-l-secondary-dim border-r-error-dim animate-spin-slow"></div>\n</div>\n</div>', 'id="chart_my_status_dist" style="height:300px; width:100%;">\n<!-- Chart placeholder aesthetic -->\n<div class="w-full h-full flex items-center justify-center opacity-20">\n<div class="w-48 h-48 rounded-full border-[16px] border-primary-dim border-t-tertiary border-l-secondary-dim border-r-error-dim animate-spin-slow"></div>\n</div>\n</div>\n' + leaderboard_html)

	user_html = user_html.replace('lg:grid-cols-2 gap-8', 'lg:grid-cols-3 gap-6')

	user_injected = user_html.replace('</body>', user_injected_script + '\n</body>')
	admin_injected = admin_html.replace('</body>', admin_injected_script + '\\n</body>')

	# Fix double quotes inside srcdoc
	user_srcdoc = html.escape(user_injected)
	admin_srcdoc = html.escape(admin_injected)

	ub = f'<iframe style="width: 100%; height: 900px; border: none; border-radius: 12px;" srcdoc="{user_srcdoc}"></iframe>'
	ab = f'<iframe style="width: 100%; height: 900px; border: none; border-radius: 12px;" srcdoc="{admin_srcdoc}"></iframe>'

	# Overwrite dummy blocks
	if frappe.db.exists("Custom HTML Block", "PM User Dashboard"):
		frappe.delete_doc("Custom HTML Block", "PM User Dashboard")
	if frappe.db.exists("Custom HTML Block", "PM Admin Dashboard"):
		frappe.delete_doc("Custom HTML Block", "PM Admin Dashboard")

	# Create User Block
	frappe.get_doc({
		"doctype": "Custom HTML Block",
		"name": "PM User Dashboard",
		"html_block_name": "PM User Dashboard",
		"html": ub,
		"script": "",
		"style": ""
	}).insert(ignore_permissions=True)

	# Create Admin Block
	frappe.get_doc({
		"doctype": "Custom HTML Block",
		"name": "PM Admin Dashboard",
		"html_block_name": "PM Admin Dashboard",
		"html": ab,
		"script": "",
		"style": ""
	}).insert(ignore_permissions=True)

	frappe.db.commit()
	print("--- Custom HTML Dashboards Successfully Installed with Iframe Isolation! ---")

def fetch_and_freeze():
	import urllib.request
	import os
	
	user_url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2E5ZGIzYjE0NTdlMzRiODU4ZGM1MDYyMzViZGY1NDJmEgsSBxDTnO2hxBUYAZIBIwoKcHJvamVjdF9pZBIVQhMxODEwNDUzODA0OTgzNTczOTUw&filename=&opi=96797242"
	admin_url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzRkZTU5ZDFmY2U0ODRiMDM5ZWM0ZjA3NDMyM2NiNDVhEgsSBxDTnO2hxBUYAZIBIwoKcHJvamVjdF9pZBIVQhMxODEwNDUzODA0OTgzNTczOTUw&filename=&opi=96797242"

	req = urllib.request.Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})
	user_html = urllib.request.urlopen(req).read().decode('utf-8')
	
	req = urllib.request.Request(admin_url, headers={'User-Agent': 'Mozilla/5.0'})
	admin_html = urllib.request.urlopen(req).read().decode('utf-8')

	# Path to save
	save_path = os.path.join(os.path.dirname(__file__), "performance_management", "dashboard_templates.py")
	
	# We'll use the injection logic from the current install script
	# But even better, we'll just save the BASE and let setup.py handle injection.
	# Actually, to be simple, I'll save the fully injected srcdoc.
	
	# I'll just save the raw HTML for now and let setup.py handle the rest.
	with open(save_path, "w") as f:
		f.write("def get_raw_user_html():\n\treturn \"\"\"" + user_html.replace('"""', '\\"\\"\\"') + "\"\"\"\n\n")
		f.write("def get_raw_admin_html():\n\treturn \"\"\"" + admin_html.replace('"""', '\\"\\"\\"') + "\"\"\"\n")

	print(f"Froze dashboards to {save_path}")
