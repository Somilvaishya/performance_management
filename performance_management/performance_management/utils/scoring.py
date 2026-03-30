from frappe.utils import get_datetime, now_datetime


def calculate_score(doc, method=None):
	"""Called on Performance Task on_update via doc_events in hooks.py"""
	if doc.status == "Approved" and not doc.score:
		base = 100.0
		base -= (doc.extension_count or 0) * 5
		if doc.deadline and doc.completion_date:
			delay = (get_datetime(doc.completion_date) - get_datetime(doc.deadline)).days
			if delay > 0:
				base -= min(delay * 10, 50)
		doc.db_set("score", max(0, base))
