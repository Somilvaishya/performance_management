import frappe
import json

def run():
    print("----- WORKSPACES -----")
    ws = frappe.db.get_all("Workspace", filters={"name": ("like", "%Performance%")}, fields=["name", "for_user", "public"])
    for w in ws:
        print(f"Workspace: {w.name} | for_user: {w.for_user} | public: {w.public}")
        try:
            doc = frappe.get_doc("Workspace", w.name)
            content = doc.content
            print("Content snippet:", content[:150] if content else "None")
        except Exception as e:
            print(f"Error reading {w.name}: {e}")

    print("\n----- CUSTOM BLOCKS IN DB -----")
    blocks = frappe.db.get_all("Custom HTML Block", fields=["name", "private"])
    for b in blocks:
        if "Dashboard" in b.name or "PM" in b.name:
            print(f"Custom Block: {b.name} | private: {b.private}")
            
    print("\n----- CURRENT USER -----")
    print("User:", frappe.session.user)
