import frappe
import requests

@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
    if frappe.request.method == "GET":
        mode = frappe.request.args.get("hub.mode")
        token = frappe.request.args.get("hub.verify_token")
        challenge = frappe.request.args.get("hub.challenge")
        
        settings = frappe.get_single("Facebook Settings")
        if mode == "subscribe" and token == settings.verify_token:
            return challenge
        return "Forbidden", 403

    if frappe.request.method == "POST":
        data = frappe.request.json
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("value", {}).get("item") == "leadgen":
                        leadgen_id = change["value"]["leadgen_id"]
                        process_facebook_lead(leadgen_id)
        return "OK"

def process_facebook_lead(leadgen_id):
    settings = frappe.get_single("Facebook Settings")
    token = settings.get_password("page_access_token")
    
    url = f"https://graph.facebook.com/v17.0/{leadgen_id}?access_token={token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        lead_data = response.json()
        
        name, phone, email = "Unknown", "", ""
        for field in lead_data.get("field_data", []):
            if field["name"] == "full_name": name = field["values"][0]
            if field["name"] == "phone_number": phone = field["values"][0]
            if field["name"] == "email": email = field["values"][0]

        frappe.get_doc({
            "doctype": "CRM Deal",
            "organization": name,
            "status": "Qualification",
            "source": "Facebook Ads"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Facebook Lead Processing Error: {str(e)}", "BizFlow Integrations")
