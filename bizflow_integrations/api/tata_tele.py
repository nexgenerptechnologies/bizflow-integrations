import frappe

@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
    if frappe.request.method == "POST":
        data = frappe.request.json
        if data:
            caller_id = data.get("caller_id", "Unknown")
            frappe.get_doc({
                "doctype": "CRM Deal",
                "organization": f"Call from {caller_id}",
                "status": "Qualification",
                "source": "Tata Tele"
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success"}
    return {"status": "error"}
