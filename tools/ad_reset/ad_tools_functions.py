import requests
import win32com.client as win32
import random
from ad_tools_secrets import ad_reset_url


def ad_reset(
    user_domain, user_id, new_password, admin_domain, admin_username, admin_password
):
    ad_reset_payload = {
        "UserPassword": new_password,
        "bChangePWDOnFirstLogon": "false",
        "bResetPassword": "true",
        "bResetPwgMgr": "false",
        "strAdminDomain": admin_domain,
        "strAdminPassword": admin_password,
        "strAdminUser": admin_username,
        "strDomain": user_domain,
        "strUserName": user_id.strip(),
    }
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = requests.post(
        ad_reset_url, headers=headers, json=ad_reset_payload, verify=False
    )
    response = response.json()
    try:
        if response["d"]["Return"] == True:
            return (f"Success:\n{response['d']['Message']}").strip()
        else:
            return (f"Failure:\n{response['d']['Message']}").strip()
    except KeyError:
        return (f"Failure:\n{response['d']['Message']}").strip()


def open_prefilled_email(email_recipient, subject, body, cc_recipient=""):
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = email_recipient
    mail.CC = cc_recipient
    mail.Subject = subject
    mail.Body = body
    mail.Display(False)


def password_generator(desired_length):
    new_password = ""
    possible_characters = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789"
    while len(new_password) < desired_length:
        new_password += random.choice(possible_characters)
    return new_password
