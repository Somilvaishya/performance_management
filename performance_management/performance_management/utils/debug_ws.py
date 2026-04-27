import frappe

def run():
    print("=== WORKSPACE CONTENT ===")
    try:
        doc = frappe.get_doc("Workspace", "Performance Management")
        print("CONTENT:", doc.content)
        print("CUSTOM BLOCKS:", [b.custom_block_name for b in doc.custom_blocks])
    except Exception as e:
        print("Error Workspace:", e)

    print("=== HTML BLOCKS IN DB ===")
    try:
        blocks = frappe.db.get_all("Custom HTML Block", fields=["name"])
        hits = [b.name for b in blocks if "Dashboard" in b.name or "PM" in b.name]
        print("HITS:", hits)
    except Exception as e:
        print("Error Blocks:", e)
        
    print("=== USER WORKSPACES ===")
    user_ws = frappe.db.get_all("Workspace", filters={"name": ("like", "%Performance Management%")}, fields=["name", "for_user", "public"])
    for w in user_ws:
        print(f"User Override: {w.name} | for_user: {w.for_user} | public: {w.public}")
