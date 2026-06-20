import frappe
import requests

@frappe.whitelist()
def send_whatsapp_message(phone, message):
    settings = frappe.get_single("WhatsApp Settings")
    
    # Clean phone number
    phone = "".join([c for c in phone if c.isdigit()])
    
    provider = settings.provider
    
    if provider == "Unofficial (WhatsJet / Codecanyon)":
        base_url = settings.api_url.strip("/") if settings.api_url else ""
        vendor_uid = settings.vendor_uid
        instance = settings.instance_id
        token = settings.get_password("access_token")
        
        url = f"{base_url}/api/{vendor_uid}/contact/send-message"
        payload = {
            "phone": phone,
            "message": message,
            "instance_id": instance
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
    elif provider == "Official Meta Cloud API":
        phone_id = settings.phone_number_id
        token = settings.get_password("access_token")
        
        url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    else:
        frappe.throw("Invalid WhatsApp Provider configured.")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        log_whatsapp_message(phone, message, "Sent", provider)
        return {"status": "success", "response": response.json()}
    except Exception as e:
        err_msg = str(e)
        if hasattr(e, 'response') and e.response:
            err_msg = f"{err_msg}: {e.response.text}"
        frappe.log_error(f"WhatsApp Send Error: {err_msg}", "BizFlow Integrations")
        log_whatsapp_message(phone, message, "Failed", provider)
        return {"status": "error", "message": err_msg}

def log_whatsapp_message(phone, message, status, provider):
    frappe.get_doc({
        "doctype": "WhatsApp Message Log",
        "receiver_phone": phone,
        "message": message,
        "status": status
    }).insert(ignore_permissions=True)
    frappe.db.commit()
