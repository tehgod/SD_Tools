import requests
from two_fa_reset_secrets import domain_dict, two_fa_reset_link


def unlock_two_fa(
    employee_id_number,
    reset_bool,
    unlock_bool,
    admin_domain,
    admin_username,
    admin_password,
):
    if employee_id_number == "" or employee_id_number.isnumeric() == False:
        return "Please enter a valid employee ID"
    bool_list = [reset_bool, unlock_bool]

    for var in bool_list:
        if var == True:
            var = "true"
        else:
            var = "false"
    try:
        domain_dict[admin_domain.upper()]
    except:
        return "Invalid domain provided for username"
    two_fa_reset_payload = {
        "bPopulateAppList": "false",  # not used
        "bPopulateFactorsList": "true",  # show setup methods
        "bResetMFA": bool_list[0],  # Resettwo_fa
        "bUnlock": bool_list[1],  # unlock account
        "strAdminDomain": domain_dict[admin_domain.upper()],
        "strAdminPassword": admin_password,
        "strAdminUser": admin_username,
        "strEmplNumber": employee_id_number,
    }
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    try:
        response = requests.post(
            two_fa_reset_link, headers=headers, json=two_fa_reset_payload, verify=False
        )
    except ConnectionError:
        return "Received Connection Error when submitting request."
    response = response.json()
    unlock_status = response["d"]["Item2"]
    if unlock_status == (
        "Failed to connect to OMITTED domain. Error: The user name or password is incorrect.\r\n</br>"
    ):
        return "Incorrect password"
    elif (
        unlock_status.find("user account could not be found in two_fa environment")
        != -1
    ):
        return "Unable to locate user account, possibly wrong employee ID number?"
    mfa_devices_response = response["d"]["Item4"]
    mfa_devices_list = []
    for auth_method in mfa_devices_response:
        if auth_method["Status"] == "ACTIVE":
            mfa_devices_list.append(auth_method["FactorName"])
    if mfa_devices_list == []:
        return "Account has been unlocked. No devices setup for two_fa"
    else:
        return mfa_devices_list
