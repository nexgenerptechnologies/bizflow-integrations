import frappe

@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
    if frappe.request.method == "POST":
        data = frappe.request.json
        if data:
            name = data.get("name", "Website Lead")
            frappe.get_doc({
                "doctype": "CRM Deal",
                "organization": name,
                "status": "Qualification",
                "source": "Website Form"
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success"}
    return {"status": "error"}
