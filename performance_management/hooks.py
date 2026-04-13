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
    # Runs once at midnight — creates today's checklist tasks
    "daily": [
        "performance_management.performance_management.services.checklist_service.create_daily_checklists",
    ],
    # Bug 2 Fix: Run reminder emails at 8 AM every day (after checklist creation at midnight).
    # Previously both jobs were in "daily" with no guaranteed order, so reminders could
    # fire before checklists were created, resulting in empty/missing reminder emails.
    "cron": {
        "0 8 * * *": [
            "performance_management.performance_management.utils.automation.send_daily_reminders",
        ]
    }
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

