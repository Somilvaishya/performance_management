import frappe
import json

def run():
    doc = frappe.get_doc("Workspace", "Performance Management")
    
    # We serialize list into string manually, avoiding double escapes in json file
    payload = [
        {
            "id": "user_dash_row",
            "type": "custom_block",
            "data": {
                "custom_block_name": "PM User Dashboard",
                "col": 12
            }
        },
        {
            "id": "admin_dash_row",
            "type": "custom_block",
            "data": {
                "custom_block_name": "PM Admin Dashboard",
                "col": 12
            }
        },
        {
            "id": "links_row",
            "type": "card",
            "data": {
                "card_name": "Core Modules",
                "col": 12
            }
        }
    ]
    
    doc.content = json.dumps(payload)
    
    doc.custom_blocks = []
    doc.append("custom_blocks", {
        "custom_block_name": "PM User Dashboard",
        "label": "My Status"
    })
    doc.append("custom_blocks", {
        "custom_block_name": "PM Admin Dashboard",
        "label": "Admin Status"
    })
    
    # Fix links visually 
    doc.links = []
    doc.append("links", {"label": "Core Modules", "type": "Card Break", "icon": "folder"})
    dt = ["Performance Task", "Checklist Template", "Task Extension Request", "Checklist Template Item", "PM Audit Log"]
    for d in dt:
        doc.append("links", {"label": d, "link_to": d, "link_type": "DocType", "type": "Link"})
    
    doc.append("links", {"label": "Team Performance Report", "link_to": "Team Performance Report", "link_type": "Report", "type": "Link"})

    doc.flags.ignore_permissions = True
    doc.save()
    
    print("SUCCESS: Workspace saved with proper framework JSON parsing.")

