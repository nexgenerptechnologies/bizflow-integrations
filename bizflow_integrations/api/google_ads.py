import frappe
import json

@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
    if frappe.request.method == "POST":
        data = frappe.request.json
        if data:
            name = data.get("user_column_data", [{}])[0].get("string_value", "Unknown Google Lead")
            email = data.get("user_column_data", [{}])[1].get("string_value", "")
            
            frappe.get_doc({
                "doctype": "CRM Deal",
                "organization": name,
                "status": "Qualification",
                "source": "Google Ads"
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success"}
    return {"status": "error"}
