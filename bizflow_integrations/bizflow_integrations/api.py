import frappe
import requests

def send_whatsapp_message(mobile_number, message_text, ref_doctype=None, ref_name=None):
    "A universal API that other Frappe apps can call to send messages."
    # Creates a log entry and triggers API
    pass
