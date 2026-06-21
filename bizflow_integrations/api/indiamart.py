import frappe
import requests

@frappe.whitelist()
def fetch_leads():
    settings = frappe.get_single("IndiaMart Settings")
    key = settings.get_password("glusr_usr_key")
    
    url = f"https://mapi.indiamart.com/wservce/crm/crmListing/v2/?glusr_crm_key={key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for lead in data.get("RESPONSE", []):
                frappe.get_doc({
                    "doctype": "CRM Deal",
                    "organization": lead.get("SENDERNAME", "IndiaMart Lead"),
                    "status": "Qualification",
                    "source": "IndiaMart"
                }).insert(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success", "fetched": len(data.get("RESPONSE", []))}
    except Exception as e:
        frappe.log_error(f"IndiaMart Fetch Error: {str(e)}", "BizFlow Integrations")
        return {"status": "error"}
