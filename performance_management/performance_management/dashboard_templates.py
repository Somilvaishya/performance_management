def get_raw_user_html():
	return """<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PM Employee Dashboard Widget</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&amp;family=Manrope:wght@600;700;800&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "on-primary": "#0f00a4",
                        "primary-fixed-dim": "#8387ff",
                        "outline-variant": "#41475b",
                        "surface-container-highest": "#1c253e",
                        "on-surface": "#dfe4fe",
                        "secondary-dim": "#ccd4ee",
                        "on-tertiary-fixed-variant": "#006544",
                        "background": "#070d1f",
                        "tertiary-container": "#69f6b8",
                        "tertiary": "#9bffce",
                        "surface-container-lowest": "#000000",
                        "surface": "#070d1f",
                        "inverse-primary": "#494bd7",
                        "on-tertiary": "#006443",
                        "tertiary-fixed": "#69f6b8",
                        "secondary-container": "#3f465c",
                        "primary": "#a3a6ff",
                        "tertiary-fixed-dim": "#58e7ab",
                        "on-tertiary-fixed": "#00452d",
                        "surface-dim": "#070d1f",
                        "on-secondary-fixed": "#373f54",
                        "on-background": "#dfe4fe",
                        "tertiary-dim": "#58e7ab",
                        "surface-bright": "#222b47",
                        "on-primary-container": "#0a0081",
                        "surface-tint": "#a3a6ff",
                        "inverse-surface": "#faf8ff",
                        "on-surface-variant": "#a5aac2",
                        "on-primary-fixed-variant": "#0e009d",
                        "primary-container": "#9396ff",
                        "secondary-fixed-dim": "#ccd4ee",
                        "on-error": "#490013",
                        "inverse-on-surface": "#4f5469",
                        "on-secondary": "#4a5167",
                        "secondary-fixed": "#dae2fd",
                        "on-primary-fixed": "#000000",
                        "on-error-container": "#ffb2b9",
                        "surface-container-low": "#0c1326",
                        "surface-container": "#11192e",
                        "surface-container-high": "#171f36",
                        "primary-fixed": "#9396ff",
                        "on-tertiary-container": "#005a3c",
                        "secondary": "#dae2fd",
                        "primary-dim": "#6063ee",
                        "on-secondary-fixed-variant": "#535b71",
                        "outline": "#6f758b",
                        "error-dim": "#d73357",
                        "surface-variant": "#1c253e",
                        "error": "#ff6e84",
                        "on-secondary-container": "#c8d0ea",
                        "error-container": "#a70138"
                    },
                    fontFamily: {
                        "headline": ["Manrope"],
                        "body": ["Inter"],
                        "label": ["Inter"]
                    },
                    borderRadius: {"DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "xxl": "1.5rem", "full": "9999px"},
                },
            },
        }
    </script>
<style>
        .glass-pane {
            background: rgba(28, 37, 62, 0.4);
            backdrop-filter: blur(20px) saturate(150%);
            border: 1px solid rgba(65, 71, 91, 0.2);
        }
        .glass-card-hover:hover {
            background: rgba(147, 150, 255, 0.1);
            border-color: rgba(163, 166, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 20px 40px -15px rgba(163, 166, 255, 0.15);
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
    </style>
</head>
<body class="bg-background text-on-surface font-body p-8 min-h-screen">
<div class="max-w-7xl mx-auto space-y-8">
<!-- Row 1: Motivational Header -->
<header class="relative overflow-hidden rounded-xxl glass-pane p-12 flex flex-col justify-center min-h-[200px] group">
<div class="absolute inset-0 bg-gradient-to-r from-primary/10 via-transparent to-tertiary/10 opacity-50"></div>
<div class="relative z-10 max-w-4xl">
<span class="text-primary-fixed-dim font-label text-xs tracking-[0.2em] uppercase mb-4 block">Executive Vision</span>
<h1 class="font-headline text-3xl md:text-4xl lg:text-5xl font-extrabold leading-tight tracking-tight text-on-surface" id="motivational_quote">
                    Success is not final, failure is not fatal: it is the courage to continue that counts.
                </h1>
</div>
<!-- Decorative Element -->
<div class="absolute -right-20 -bottom-20 w-64 h-64 bg-primary/20 rounded-full blur-[100px]"></div>
</header>
<!-- Row 2: 4 KPI Cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<!-- Today's Tasks -->
<button class="glass-pane glass-card-hover rounded-xl p-6 text-left transition-all duration-300 group" onclick="window.parent.frappe.set_route('List', 'Performance Task', {'task_type':'Checklist', 'creation':['Timespan', 'today']});">
<div class="flex items-center justify-between mb-4">
<div class="p-3 rounded-lg bg-primary/10 text-primary">
<span class="material-symbols-outlined">calendar_today</span>
</div>
<span class="text-[10px] font-bold text-primary-fixed-dim tracking-widest uppercase opacity-60">Real-time</span>
</div>
<h3 class="text-on-surface-variant text-sm font-medium mb-1">Today's Tasks</h3>
<div class="flex items-baseline gap-2">
<span class="font-headline text-3xl font-bold text-on-surface" id="kpi_tc">--</span>
<span class="text-tertiary text-xs font-medium">Active</span>
</div>
</button>
<!-- Total Delegation -->
<button class="glass-pane glass-card-hover rounded-xl p-6 text-left transition-all duration-300" onclick="window.parent.frappe.set_route('List', 'Performance Task', {'task_type':'Delegation'});">
<div class="flex items-center justify-between mb-4">
<div class="p-3 rounded-lg bg-secondary-container/30 text-secondary">
<span class="material-symbols-outlined">account_tree</span>
</div>
</div>
<h3 class="text-on-surface-variant text-sm font-medium mb-1">Total Delegation</h3>
<span class="font-headline text-3xl font-bold text-on-surface" id="kpi_td">--</span>
</button>
<!-- Pending Checklist -->
<button class="glass-pane glass-card-hover rounded-xl p-6 text-left transition-all duration-300" onclick="window.parent.frappe.set_route('List', 'Performance Task', {'task_type':'Checklist', 'status': 'Pending'});">
<div class="flex items-center justify-between mb-4">
<div class="p-3 rounded-lg bg-error-container/20 text-error">
<span class="material-symbols-outlined">assignment_late</span>
</div>
</div>
<h3 class="text-on-surface-variant text-sm font-medium mb-1">Pending Checklist</h3>
<span class="font-headline text-3xl font-bold text-on-surface" id="kpi_pc">--</span>
</button>
<!-- Pending Delegation -->
<button class="glass-pane glass-card-hover rounded-xl p-6 text-left transition-all duration-300" onclick="window.parent.frappe.set_route('List', 'Performance Task', {'task_type':'Delegation', 'status': 'Pending'});">
<div class="flex items-center justify-between mb-4">
<div class="p-3 rounded-lg bg-tertiary-container/10 text-tertiary">
<span class="material-symbols-outlined">pending_actions</span>
</div>
</div>
<h3 class="text-on-surface-variant text-sm font-medium mb-1">Pending Delegation</h3>
<span class="font-headline text-3xl font-bold text-on-surface" id="kpi_pd">--</span>
</button>
</div>
<!-- Row 3: 4 Quick Shortcut Pill Buttons -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
<button class="glass-pane glass-card-hover flex items-center justify-between px-5 py-4 rounded-full transition-all duration-300 group" onclick="window.parent.frappe.set_route('List', 'Task Extension Request', {'approval_status':'Pending'});">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary-fixed-dim group-hover:rotate-12 transition-transform">hourglass_empty</span>
<span class="text-xs font-semibold text-on-surface-variant group-hover:text-on-surface">Pending Extension</span>
</div>
<span class="bg-primary/20 text-primary-fixed-dim text-[10px] font-bold px-2 py-0.5 rounded-full" id="shortcut_pe">--</span>
</button>
<button class="glass-pane glass-card-hover flex items-center justify-between px-5 py-4 rounded-full transition-all duration-300 group" onclick="window.parent.frappe.set_route('List', 'Task Extension Request', {'approval_status':'Approved'});">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-tertiary group-hover:scale-110 transition-transform">check_circle</span>
<span class="text-xs font-semibold text-on-surface-variant group-hover:text-on-surface">Approved Requests</span>
</div>
<span class="bg-tertiary/10 text-tertiary text-[10px] font-bold px-2 py-0.5 rounded-full" id="shortcut_ae">--</span>
</button>
<button class="glass-pane glass-card-hover flex items-center justify-between px-5 py-4 rounded-full transition-all duration-300 group" onclick="window.parent.frappe.set_route('List', 'Task Extension Request', {'approval_status':'Rejected'});">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-error group-hover:shake transition-transform">cancel</span>
<span class="text-xs font-semibold text-on-surface-variant group-hover:text-on-surface">Rejected Requests</span>
</div>
<span class="bg-error/10 text-error text-[10px] font-bold px-2 py-0.5 rounded-full" id="shortcut_re">--</span>
</button>
<button class="glass-pane glass-card-hover flex items-center justify-between px-5 py-4 rounded-full transition-all duration-300 group" onclick="window.parent.frappe.set_route('List', 'Performance Task', {'status':'Pending Approval'});">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-secondary group-hover:translate-x-1 transition-transform">verified</span>
<span class="text-xs font-semibold text-on-surface-variant group-hover:text-on-surface">Awaiting Approval</span>
</div>
<span class="bg-secondary/10 text-secondary text-[10px] font-bold px-2 py-0.5 rounded-full" id="shortcut_aa">--</span>
</button>
</div>
<!-- Bottom Section: Performance Matrix -->
<section class="space-y-6">
<div class="flex items-center gap-4">
<h2 class="font-headline text-xl font-bold text-on-surface tracking-tight">My Performance Matrix</h2>
<div class="h-[1px] flex-grow bg-gradient-to-r from-outline-variant/30 to-transparent"></div>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
<!-- Completion Trend Container -->
<div class="glass-pane rounded-xxl p-8 relative overflow-hidden group">
<div class="absolute top-0 right-0 p-4">
<span class="material-symbols-outlined text-outline-variant/50">trending_up</span>
</div>
<div class="mb-6">
<h4 class="font-semibold text-on-surface">Completion Velocity</h4>
<p class="text-xs text-on-surface-variant">Task completion rate over the last 30 days</p>
</div>
<div class="relative z-10 transition-opacity duration-500" id="chart_my_completion_trend" style="height:300px; width:100%;">
<!-- Chart placeholder aesthetic -->
<div class="w-full h-full flex items-end justify-between gap-2 px-2 pb-4 opacity-20">
<div class="bg-primary-dim w-full rounded-t-lg h-[40%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[60%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[45%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[80%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[55%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[90%]"></div>
<div class="bg-primary-dim w-full rounded-t-lg h-[70%]"></div>
</div>
</div>
</div>
<!-- Status Distribution Container -->
<div class="glass-pane rounded-xxl p-8 relative overflow-hidden group">
<div class="absolute top-0 right-0 p-4">
<span class="material-symbols-outlined text-outline-variant/50">pie_chart</span>
</div>
<div class="mb-6">
<h4 class="font-semibold text-on-surface">Status Distribution</h4>
<p class="text-xs text-on-surface-variant">Current workload breakdown by lifecycle stage</p>
</div>
<div class="relative z-10" id="chart_my_status_dist" style="height:300px; width:100%;">
<!-- Chart placeholder aesthetic -->
<div class="w-full h-full flex items-center justify-center opacity-20">
<div class="w-48 h-48 rounded-full border-[16px] border-primary-dim border-t-tertiary border-l-secondary-dim border-r-error-dim animate-spin-slow"></div>
</div>
</div>
</div>
</div>
</section>
</div>
<!-- Decorative background blobs -->
<div class="fixed top-0 left-0 -z-10 w-full h-full pointer-events-none overflow-hidden">
<div class="absolute -top-[20%] -left-[10%] w-[60%] h-[60%] bg-primary/5 rounded-full blur-[120px]"></div>
<div class="absolute top-[40%] -right-[10%] w-[50%] h-[50%] bg-tertiary/5 rounded-full blur-[120px]"></div>
</div>
</body></html>"""

def get_raw_admin_html():
	return """<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PM Admin Custom Widget</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Manrope:wght@700;800&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "tertiary": "#9bffce",
                        "error": "#ff6e84",
                        "secondary-dim": "#ccd4ee",
                        "primary-dim": "#6063ee",
                        "primary-fixed": "#9396ff",
                        "on-error": "#490013",
                        "on-surface": "#dfe4fe",
                        "on-secondary-fixed": "#373f54",
                        "on-secondary-container": "#c8d0ea",
                        "error-container": "#a70138",
                        "surface": "#070d1f",
                        "on-secondary": "#4a5167",
                        "on-primary-container": "#0a0081",
                        "tertiary-dim": "#58e7ab",
                        "tertiary-fixed-dim": "#58e7ab",
                        "background": "#070d1f",
                        "on-surface-variant": "#a5aac2",
                        "surface-variant": "#1c253e",
                        "inverse-on-surface": "#4f5469",
                        "primary": "#a3a6ff",
                        "on-tertiary-fixed-variant": "#006544",
                        "secondary-fixed-dim": "#ccd4ee",
                        "inverse-primary": "#494bd7",
                        "tertiary-fixed": "#69f6b8",
                        "error-dim": "#d73357",
                        "outline-variant": "#41475b",
                        "secondary-container": "#3f465c",
                        "on-tertiary-container": "#005a3c",
                        "primary-fixed-dim": "#8387ff",
                        "surface-dim": "#070d1f",
                        "secondary-fixed": "#dae2fd",
                        "secondary": "#dae2fd",
                        "on-tertiary-fixed": "#00452d",
                        "on-error-container": "#ffb2b9",
                        "inverse-surface": "#faf8ff",
                        "surface-tint": "#a3a6ff",
                        "on-primary-fixed-variant": "#0e009d",
                        "surface-container": "#11192e",
                        "surface-container-high": "#171f36",
                        "on-primary-fixed": "#000000",
                        "on-primary": "#0f00a4",
                        "outline": "#6f758b",
                        "on-tertiary": "#006443",
                        "primary-container": "#9396ff",
                        "surface-container-low": "#0c1326",
                        "surface-bright": "#222b47",
                        "surface-container-lowest": "#000000",
                        "tertiary-container": "#69f6b8",
                        "on-background": "#dfe4fe",
                        "on-secondary-fixed-variant": "#535b71",
                        "surface-container-highest": "#1c253e"
                    },
                    fontFamily: {
                        "headline": ["Manrope"],
                        "body": ["Inter"],
                        "label": ["Inter"]
                    },
                    borderRadius: {"DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"},
                },
            },
        }
    </script>
<style>
        .glass-card {
            background: rgba(28, 37, 62, 0.6);
            backdrop-filter: blur(20px) saturate(150%);
            border-top: 1px solid rgba(65, 71, 91, 0.15);
            border-left: 1px solid rgba(65, 71, 91, 0.15);
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body {
            background-color: #070d1f;
            color: #dfe4fe;
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="p-6 md:p-8 space-y-8">
<!-- Top Row: KPI Cards -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<!-- Card 1 -->
<button class="glass-card p-6 rounded-xl flex flex-col items-start gap-4 group transition-all duration-300 hover:scale-[1.02] hover:bg-surface-container-highest text-left" onclick='window.parent.frappe.set_route("List", "Performance Task", {"task_type":"Checklist"});'>
<div class="flex items-center justify-between w-full">
<span class="material-symbols-outlined text-primary text-2xl group-hover:scale-110 transition-transform">checklist</span>
<span class="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold">Volume</span>
</div>
<div class="space-y-1">
<h3 class="text-on-surface-variant text-sm font-medium">Total Checklist tasks</h3>
<p class="font-headline text-3xl font-extrabold text-on-surface" id="kpi_tc">0</p>
</div>
</button>
<!-- Card 2 -->
<button class="glass-card p-6 rounded-xl flex flex-col items-start gap-4 group transition-all duration-300 hover:scale-[1.02] hover:bg-surface-container-highest text-left" onclick='window.parent.frappe.set_route("List", "Performance Task", {"task_type":"Delegation"});'>
<div class="flex items-center justify-between w-full">
<span class="material-symbols-outlined text-tertiary text-2xl group-hover:scale-110 transition-transform">assignment_ind</span>
<span class="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold">Volume</span>
</div>
<div class="space-y-1">
<h3 class="text-on-surface-variant text-sm font-medium">Total Delegation tasks</h3>
<p class="font-headline text-3xl font-extrabold text-on-surface" id="kpi_td">0</p>
</div>
</button>
<!-- Card 3 -->
<button class="glass-card p-6 rounded-xl flex flex-col items-start gap-4 group transition-all duration-300 hover:scale-[1.02] hover:bg-surface-container-highest text-left" onclick='window.parent.frappe.set_route("List", "Performance Task", {"task_type":"Checklist", "status": "Pending"});'>
<div class="flex items-center justify-between w-full">
<span class="material-symbols-outlined text-error text-2xl group-hover:scale-110 transition-transform">pending_actions</span>
<span class="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold">Priority</span>
</div>
<div class="space-y-1">
<h3 class="text-on-surface-variant text-sm font-medium">Pending Checklist tasks</h3>
<p class="font-headline text-3xl font-extrabold text-on-surface" id="kpi_pc">0</p>
</div>
</button>
<!-- Card 4 -->
<button class="glass-card p-6 rounded-xl flex flex-col items-start gap-4 group transition-all duration-300 hover:scale-[1.02] hover:bg-surface-container-highest text-left" onclick='window.parent.frappe.set_route("List", "Performance Task", {"task_type":"Delegation", "status": "Pending"});'>
<div class="flex items-center justify-between w-full">
<span class="material-symbols-outlined text-primary-fixed text-2xl group-hover:scale-110 transition-transform">hourglass_empty</span>
<span class="text-[10px] uppercase tracking-widest text-on-surface-variant font-semibold">Priority</span>
</div>
<div class="space-y-1">
<h3 class="text-on-surface-variant text-sm font-medium">Pending Delegation tasks</h3>
<p class="font-headline text-3xl font-extrabold text-on-surface" id="kpi_pd">0</p>
</div>
</button>
</div>
<!-- Middle Row: Quick Shortcut Pills -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
<button class="flex items-center justify-between px-5 py-3 rounded-full glass-card hover:bg-surface-bright transition-all duration-200 group active:scale-95 border border-outline-variant/10" onclick='window.parent.frappe.set_route("List", "Task Extension Request", {"approval_status": "Pending"});'>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary text-xl">history</span>
<span class="text-xs font-semibold text-on-surface-variant">Pending Extension</span>
</div>
<span class="bg-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded-full" id="shortcut_pe">0</span>
</button>
<button class="flex items-center justify-between px-5 py-3 rounded-full glass-card hover:bg-surface-bright transition-all duration-200 group active:scale-95 border border-outline-variant/10" onclick='window.parent.frappe.set_route("List", "Task Extension Request", {"approval_status": "Approved"});'>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-tertiary text-xl">verified</span>
<span class="text-xs font-semibold text-on-surface-variant">Approved Extension</span>
</div>
<span class="bg-tertiary/20 text-tertiary text-xs font-bold px-2 py-0.5 rounded-full" id="shortcut_ae">0</span>
</button>
<button class="flex items-center justify-between px-5 py-3 rounded-full glass-card hover:bg-surface-bright transition-all duration-200 group active:scale-95 border border-outline-variant/10" onclick='window.parent.frappe.set_route("List", "Task Extension Request", {"approval_status": "Rejected"});'>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-error text-xl">cancel</span>
<span class="text-xs font-semibold text-on-surface-variant">Rejected Extension</span>
</div>
<span class="bg-error/20 text-error text-xs font-bold px-2 py-0.5 rounded-full" id="shortcut_re">0</span>
</button>
<button class="flex items-center justify-between px-5 py-3 rounded-full glass-card hover:bg-surface-bright transition-all duration-200 group active:scale-95 border border-outline-variant/10" onclick='window.parent.frappe.set_route("List", "Performance Task", {"status": "Pending Approval"});'>
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary-fixed text-xl">visibility</span>
<span class="text-xs font-semibold text-on-surface-variant">Awaiting Approval</span>
</div>
<span class="bg-primary-fixed/20 text-primary-fixed text-xs font-bold px-2 py-0.5 rounded-full" id="shortcut_aa">0</span>
</button>
</div>
<!-- Live Reporting Matrix -->
<div class="space-y-6">
<div class="flex items-center gap-3 px-2">
<div class="h-8 w-1 bg-primary rounded-full"></div>
<h2 class="font-headline text-xl font-bold tracking-tight text-on-surface">Live Reporting Matrix</h2>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
<!-- Completion Trend -->
<div class="glass-card rounded-2xl p-6 overflow-hidden relative">
<div class="flex items-center justify-between mb-6">
<div>
<h4 class="text-on-surface font-semibold text-sm">Completion Trend</h4>
<p class="text-xs text-on-surface-variant">Efficiency over time</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-50">show_chart</span>
</div>
<div class="bg-surface-container-lowest/20 rounded-lg" id="chart_completion_trend" style="height:300px; width:100%;"></div>
</div>
<!-- Status Distribution -->
<div class="glass-card rounded-2xl p-6 overflow-hidden relative">
<div class="flex items-center justify-between mb-6">
<div>
<h4 class="text-on-surface font-semibold text-sm">Status Distribution</h4>
<p class="text-xs text-on-surface-variant">Task lifecycle spread</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-50">pie_chart</span>
</div>
<div class="bg-surface-container-lowest/20 rounded-lg" id="chart_status_dist" style="height:300px; width:100%;"></div>
</div>
<!-- Checklist vs Delegation -->
<div class="glass-card rounded-2xl p-6 overflow-hidden relative">
<div class="flex items-center justify-between mb-6">
<div>
<h4 class="text-on-surface font-semibold text-sm">Checklist Comparison</h4>
<p class="text-xs text-on-surface-variant">Categorical performance</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-50">bar_chart</span>
</div>
<div class="bg-surface-container-lowest/20 rounded-lg" id="chart_checklist_comp" style="height:300px; width:100%;"></div>
</div>
<!-- Overdue Trend -->
<div class="glass-card rounded-2xl p-6 overflow-hidden relative">
<div class="flex items-center justify-between mb-6">
<div>
<h4 class="text-on-surface font-semibold text-sm text-error">Critical Overdue Trend</h4>
<p class="text-xs text-on-surface-variant">Risk assessment tracker</p>
</div>
<span class="material-symbols-outlined text-error opacity-50">warning</span>
</div>
<div class="bg-surface-container-lowest/20 rounded-lg" id="chart_overdue_trend" style="height:300px; width:100%;"></div>
</div>
</div>
<!-- Wide User Performance Ranking -->
<div class="glass-card rounded-2xl p-6 overflow-hidden relative">
<div class="flex items-center justify-between mb-6">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-tertiary">leaderboard</span>
<div>
<h4 class="text-on-surface font-semibold text-sm">User Performance Ranking</h4>
<p class="text-xs text-on-surface-variant">Top contributors and efficiency scores</p>
</div>
</div>
<div class="flex gap-2">
<div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
<span class="text-[10px] text-on-surface-variant font-medium">LIVE UPDATES</span>
</div>
</div>
<div class="bg-surface-container-lowest/20 rounded-lg" id="chart_user_perf" style="height:300px; width:100%;"></div>
</div>
</div>
<!-- Background Decoration (Ethereal feel) -->
<div class="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/5 blur-[120px] rounded-full -z-10 pointer-events-none"></div>
<div class="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-tertiary/5 blur-[120px] rounded-full -z-10 pointer-events-none"></div>
</body></html>"""
