"""
Test the updated Team Performance Report SQL.
Run via: bench --site workspace.test execute performance_management.test_team_report.run
"""
import frappe
import importlib

def run():
	print("\n--- Testing Team Performance Report ---")

	# Import the report module dynamically using the correct Frappe app path
	module = importlib.import_module(
		"performance_management.performance_management.report.team_performance_report.team_performance_report"
	)
	columns, data, _, chart, summary = module.execute(filters={})

	# Print column names
	print(f"\nColumns ({len(columns)}):")
	for c in columns:
		print(f"  {c['fieldname']:25} | {c['label']}")

	# Print first 5 rows
	print(f"\nData rows ({len(data)}):")
	for row in data[:5]:
		emp  = str(row.get('employee') or '')
		ttyp = str(row.get('task_type') or '')
		print(f"  Employee: {emp:25} | Task Type: {ttyp:15} | Total: {row.get('total_tasks')} | Score: {row.get('average_score')}")

	# Verify task_type column present
	col_names = [c['fieldname'] for c in columns]
	if 'task_type' in col_names:
		print("\n[PASS] task_type column exists in report")
	else:
		print("\n[FAIL] task_type column MISSING from report columns!")

	# Check that employee column has names not emails
	found_email = False
	for row in data[:5]:
		emp = str(row.get('employee') or '')
		if '@' in emp:
			print(f"[FAIL] Employee showing email: {emp}")
			found_email = True
		elif emp:
			print(f"[PASS] Employee shows full name: {emp}")
	if not found_email and data:
		print("[PASS] No email addresses found in employee column")

	print("\n--- Done ---\n")

