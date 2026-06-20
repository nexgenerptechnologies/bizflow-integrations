import frappe
import requests

@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
    frappe.get_doc({
        "doctype": "Exotel Call Log",
        "call_sid": kwargs.get("CallSid"),
        "from_number": kwargs.get("From"),
        "to_number": kwargs.get("To"),
        "status": kwargs.get("Status"),
        "duration": kwargs.get("DialCallDuration") or 0,
        "recording_url": kwargs.get("RecordingUrl")
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    return "OK"

@frappe.whitelist()
def click_to_call(from_number, to_number):
    settings = frappe.get_single("Exotel Settings")
    sid = settings.exotel_sid
    token = settings.get_password("exotel_token")
    api_key = settings.exotel_api_key
    virtual_num = settings.virtual_number
    
    url = f"https://api.exotel.com/v1/Accounts/{sid}/Calls/connect.json"
    
    data = {
        "From": from_number,
        "To": to_number,
        "CallerId": virtual_num
    }
    
    try:
        response = requests.post(url, data=data, auth=(api_key, token))
        response.raise_for_status()
        return {"status": "success", "message": "Call initiated"}
    except Exception as e:
        frappe.log_error(f"Exotel Click-to-Call Error: {str(e)}", "BizFlow Integrations")
        return {"status": "error", "message": str(e)}
