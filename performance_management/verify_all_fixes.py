"""
verify_all_fixes.py
Run via: bench --site workspace.test execute performance_management.verify_all_fixes.run
Tests all 3 bug fixes applied on 2026-04-13:
  1. Deadline set to end-of-day (no immediate overdue)
  2. Frequency field copied from template to task
  3. Reminder email queued correctly
"""
import frappe
from frappe.utils import today, now_datetime


def run():
	print("\n" + "=" * 60)
	print("  Performance Management - Post-Fix Verification")
	print("=" * 60)

	# ────────────────────────────────────────────────────────────
	# 0. Find a suitable Checklist Template to use
	# ────────────────────────────────────────────────────────────
	template = frappe.db.get_value(
		"Checklist Template",
		{"active": 1, "assigned_to": ["!=", ""]},
		["name", "frequency", "assigned_to"],
		as_dict=True
	)

	if not template:
		print("\n[SKIP] No active Checklist Template with assigned_to found.")
		print("       Create one in the UI first, then re-run this script.")
	else:
		print(f"\n[INFO] Using template: {template.name} (frequency={template.frequency}, assigned={template.assigned_to})")

		# ─────────────────────────────────────────────────────────
		# TEST 1 & 3: Create daily checklists and check task fields
		# ─────────────────────────────────────────────────────────
		print("\n[TEST 1 + 3] Running create_daily_checklists()...")

		# Delete any existing tasks from today for this template to allow fresh creation
		existing = frappe.db.sql("""
			SELECT name FROM `tabPerformance Task`
			WHERE checklist_template = %s AND DATE(deadline) = %s
		""", (template.name, today()), as_dict=True)
		for e in existing:
			frappe.delete_doc("Performance Task", e.name, ignore_permissions=True)
		frappe.db.commit()
		print(f"  Cleared {len(existing)} existing today-tasks for clean test.")

		from performance_management.performance_management.services.checklist_service import create_daily_checklists
		create_daily_checklists()

		tasks = frappe.db.sql("""
			SELECT name, task_title, deadline, is_overdue, frequency, status
			FROM `tabPerformance Task`
			WHERE checklist_template = %s AND DATE(deadline) = %s
		""", (template.name, today()), as_dict=True)

		if not tasks:
			print("  [FAIL] No tasks were created — check template has items and correct frequency for today.")
		else:
			all_ok = True
			for t in tasks:
				deadline_str = str(t.deadline)
				freq_ok      = bool(t.frequency)
				eod_ok       = "23:59:59" in deadline_str
				overdue_ok   = t.is_overdue == 0

				status_line = (
					f"  Task {t.name}: deadline={deadline_str} | "
					f"frequency={t.frequency!r} | is_overdue={t.is_overdue}"
				)
				print(status_line)

				if not eod_ok:
					print(f"    [FAIL] Deadline is NOT end-of-day! Got: {deadline_str}")
					all_ok = False
				else:
					print(f"    [PASS] Deadline correctly set to 23:59:59")

				if not freq_ok:
					print(f"    [FAIL] Frequency field is blank/None!")
					all_ok = False
				else:
					print(f"    [PASS] Frequency field set: {t.frequency}")

				if not overdue_ok:
					print(f"    [FAIL] Task is already marked overdue on creation!")
					all_ok = False
				else:
					print(f"    [PASS] is_overdue = 0 (not overdue on creation)")

			if all_ok:
				print("\n  ✅ TEST 1 + 3 PASSED — Deadline, Frequency, and Overdue all correct.")
			else:
				print("\n  ❌ TEST 1 + 3 FAILED — See errors above.")

	# ────────────────────────────────────────────────────────────
	# TEST 2: mark_overdue_tasks should NOT touch today's tasks
	# ────────────────────────────────────────────────────────────
	print("\n[TEST 2] Running mark_overdue_tasks() — today's tasks must remain NOT overdue...")

	from performance_management.performance_management.utils.automation import mark_overdue_tasks
	marked = mark_overdue_tasks()
	print(f"  Marked {marked} task(s) as overdue (should be 0 for today's tasks).")

	if template:
		fresh_tasks = frappe.db.sql("""
			SELECT name, is_overdue FROM `tabPerformance Task`
			WHERE checklist_template = %s AND DATE(deadline) = %s
		""", (template.name, today()), as_dict=True)
		any_overdue = any(t.is_overdue for t in fresh_tasks)
		if any_overdue:
			print("  [FAIL] Today's checklist tasks were marked overdue by mark_overdue_tasks()!")
		else:
			print("  [PASS] ✅ Today's tasks are still NOT overdue after running mark_overdue_tasks().")

	# ────────────────────────────────────────────────────────────
	# TEST 4: Reminder email queued
	# ────────────────────────────────────────────────────────────
	print("\n[TEST 4] Clearing email queue and running send_daily_reminders()...")
	frappe.db.sql("DELETE FROM `tabEmail Queue`")
	frappe.db.sql("DELETE FROM `tabEmail Queue Recipient`")
	frappe.db.commit()

	from performance_management.performance_management.utils.automation import send_daily_reminders
	send_daily_reminders()

	emails = frappe.get_all("Email Queue", fields=["name", "status"])
	print(f"  Emails queued: {len(emails)}")
	if not emails:
		print("  [INFO] No emails queued — this is expected if no pending tasks exist due today.")
		print("         If tasks were created above, check that the assigned user has a valid email address.")
	else:
		print("  [PASS] ✅ Reminder emails are being queued correctly.")
		for e in emails:
			print(f"    - {e.name}  status={e.status}")

	# ────────────────────────────────────────────────────────────
	# TEST 5: Verify scheduled hooks are registered correctly
	# ────────────────────────────────────────────────────────────
	print("\n[TEST 5] Verifying scheduler hooks registration...")
	from frappe import get_hooks
	hooks = frappe.get_hooks("scheduler_events", app_name="performance_management")

	daily  = hooks.get("daily", [])
	cron   = hooks.get("cron", {})
	hourly = hooks.get("hourly", [])

	create_job   = "performance_management.performance_management.services.checklist_service.create_daily_checklists"
	reminder_job = "performance_management.performance_management.utils.automation.send_daily_reminders"
	overdue_job  = "performance_management.performance_management.utils.automation.mark_overdue_tasks"

	# create_daily should be in daily
	if create_job in daily:
		print(f"  [PASS] create_daily_checklists is in 'daily'")
	else:
		print(f"  [FAIL] create_daily_checklists NOT found in 'daily' hooks!")

	# send_daily_reminders should be in cron 0 8 * * *
	cron_8am = cron.get("0 8 * * *", [])
	if reminder_job in cron_8am:
		print(f"  [PASS] send_daily_reminders is in cron '0 8 * * *'")
	else:
		print(f"  [FAIL] send_daily_reminders NOT found in cron '0 8 * * *'!")
		print(f"         Registered cron: {cron}")

	# reminder should NOT be in daily anymore
	if reminder_job in daily:
		print(f"  [FAIL] send_daily_reminders is STILL in 'daily' (should be removed)!")
	else:
		print(f"  [PASS] send_daily_reminders correctly removed from 'daily'")

	# overdue should be in hourly
	if overdue_job in hourly:
		print(f"  [PASS] mark_overdue_tasks is in 'hourly'")
	else:
		print(f"  [FAIL] mark_overdue_tasks NOT found in 'hourly'!")

	print("\n" + "=" * 60)
	print("  Verification complete.")
	print("=" * 60 + "\n")
