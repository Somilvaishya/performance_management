app_name = "performance_management"
app_title = "Performance Management"
app_publisher = "Somil Vaishya"
app_description = "Enterprise Task Intelligence System"
app_email = "somilvaishya78@gmail.com"
app_license = "mit"
app_version = "0.0.1"

# ─── Scheduled Jobs ──────────────────────────────────────────────────────────
scheduler_events = {
    "hourly": [
        "performance_management.performance_management.utils.automation.mark_overdue_tasks",
    ],
    "daily": [
        "performance_management.performance_management.services.checklist_service.create_daily_checklists",
        "performance_management.performance_management.utils.automation.send_daily_reminders",
    ],
}

# ─── Doc Events ──────────────────────────────────────────────────────────────
doc_events = {
    "Performance Task": {
        "on_update": "performance_management.performance_management.utils.scoring.calculate_score",
    }
}

# ─── Installation Hooks ───────────────────────────────────────────────────────
after_install = "performance_management.performance_management.setup.after_install"
after_migrate = "performance_management.performance_management.setup.after_migrate"

# ─── Desktop Icon ────────────────────────────────────────────────────────────
# The Workspace "Performance Management" will serve as the app entry point.
