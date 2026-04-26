import frappe

def debug():
    try:
        print("\n--- FINDING HTML BLOCKS ---")
        workspaces = frappe.db.get_all("Workspace", fields=["name", "content"])
        for ws in workspaces:
            if "html_block" in (ws.content or ""):
                print(f"Workspace: {ws.name}")
                print(f"Content: {ws.content}")
                break
        else:
            print("No workspace with html_block found besides ours.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
