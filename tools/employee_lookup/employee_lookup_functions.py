from threading import Thread
import requests
import subprocess
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tools.credentials import Person
from time import sleep
import json
from employee_lookup_secrets import domain_dict


class ticketting_system_data:
    def __init__(
        self,
        first_name,
        last_name,
        supervisor,
        opco,
        location,
        wd_status,
        vip_status,
        emp_id_number,
        email,
        preferred_name=None,
    ):
        self.emp_id_number = emp_id_number
        self.first_name = first_name
        self.preferred_name = preferred_name
        self.last_name = last_name
        self.email = email
        self.supervisor = supervisor
        self.location = location
        self.wd_status = wd_status
        self.vip_status = vip_status
        self.opco = opco


class Powershell_data:
    def __init__(
        self, emp_id_number, domain, first_name, last_name, userid, email, hire_date
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.domain = domain
        self.userid = userid
        self.email = email
        self.emp_id_number = emp_id_number
        self.hire_date = hire_date
        pass


def primary_domain_lookup(emp_id_number):
    domain_query_url = f"OMITTED{emp_id_number}INFO"
    my_response = requests.get(domain_query_url)
    text_response = my_response.text
    accounts_located_amount = int(
        text_response[
            text_response.find("<m:count>") + 9 : text_response.find("</m:count>")
        ]
    )
    if accounts_located_amount == 1:
        primary_domain = text_response[
            text_response.find("<d:domain>") + 10 : text_response.find("</d:domain>")
        ]
        guid = text_response[
            text_response.find("<d:guid>") + 8 : text_response.find("</d:guid>")
        ]
        print(
            f"Determined colleague's primary domain and account: {primary_domain} , {guid}"
        )
        return guid, primary_domain
    elif accounts_located_amount < 1:
        print("No account located on domain lookup")
        return False
    elif accounts_located_amount > 1:
        print(
            f"WARNING: Multiple accounts ({accounts_located_amount}) located on domain lookup"
        )
        primary_domain = text_response[
            text_response.find("<d:domain>") + 10 : text_response.find("</d:domain>")
        ]
        guid = text_response[
            text_response.find("<d:guid>") + 8 : text_response.find("</d:guid>")
        ]
        return guid, primary_domain
    else:
        print("Unexpected error on domain lookup")
        return False


def query_powershell(emp_id_number, item_wanted=None, output_var=None):
    print("Attempting to pull user data from Powershell.")
    initial_info = primary_domain_lookup(emp_id_number)
    if initial_info == False:
        return False
    guid = initial_info[0]
    primary_domain = initial_info[1]
    if item_wanted == None:
        search_string = f"""Get-ADUser -Filter 'ObjectGUID -eq "{guid}"' -Properties GivenName, Surname, SAMAccountName, mail, Created -Server {primary_domain}"""
    else:
        search_string = f"""Get-ADUser -Filter 'ObjectGUID -eq "{guid}"' -Properties * -Server {primary_domain}| Select-Object -ExpandProperty {item_wanted}"""
    result = subprocess.run(
        [
            "C:\\Windows\\System32\WindowsPowerShell\\v1.0\\powershell.exe",
            search_string,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    exported_result = result.stdout.decode("utf-8", errors="ignore").strip()
    if item_wanted != None:
        return exported_result
    exported_result = exported_result.split("\r\n")
    items_found = 0
    first_name = None
    last_name = None
    username = None
    email = None
    hire_date = None
    for line in exported_result:
        if items_found == 5:
            break
        if line.startswith("GivenName"):
            first_name = line[line.find(": ") + 1 :].strip()
            items_found += 1
        elif line.startswith("Surname"):
            last_name = line[line.find(": ") + 1 :].strip()
            items_found += 1
        elif line.startswith("SamAccountName"):
            username = line[line.find(": ") + 1 :].strip()
            items_found += 1
        elif line.startswith("mail"):
            email = line[line.find(": ") + 1 :].strip()
            items_found += 1
        elif line.startswith("Created"):
            starting_pos = line.find(": ") + 2
            ending_pos = line.find(" ", starting_pos)
            hire_date = line[line.find(": ") + 1 : ending_pos].strip()
            items_found += 1
    print("successfully pulled data from Powershell.")
    if output_var != None:
        output_var.append(
            Powershell_data(
                emp_id_number,
                primary_domain,
                first_name,
                last_name,
                username,
                email,
                hire_date,
            )
        )
    else:
        return Powershell_data(
            emp_id_number,
            primary_domain,
            first_name,
            last_name,
            username,
            email,
            hire_date,
        )


def query_servicenow(driver, emp_id_number, output_var=None):
    print("attempting to load servicenow")
    wait = WebDriverWait(driver, 30)
    attempt_count = 0
    while attempt_count < 3:
        print(f"Attempt #{attempt_count} to load profile on Servicenow.")
        try:
            driver.get(f"OMITTED{emp_id_number}")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "sys_user.first_name")))
            first_name = driver.find_element(
                By.ID, "sys_user.first_name"
            ).get_attribute("value")
            print("servicenow loaded successfully.")
            attempt_count = 3
        except:
            sleep(1)
            attempt_count += 1
            first_name = False
    if first_name == False:
        print("first name returned false, terminating lookup")
        return False
    print("pulling data now.")
    first_name = driver.find_element(By.ID, "sys_user.first_name").get_attribute(
        "value"
    )
    preferred_first_name = driver.find_element(
        By.ID, "sys_user.u_preferred_first_name"
    ).get_attribute("value")
    last_name = driver.find_element(By.ID, "sys_user.last_name").get_attribute("value")
    supervisor = driver.find_element(By.ID, "sys_user.manager_label").get_attribute(
        "value"
    )
    location = driver.find_element(By.ID, "sys_user.location_label").get_attribute(
        "value"
    )
    active_wd_status = driver.find_element(By.ID, "sys_user.active").get_attribute(
        "value"
    )
    vip_status = driver.find_element(By.ID, "sys_user.vip").get_attribute("value")
    email = driver.find_element(By.ID, "sys_user.email").get_attribute("value")
    opco = email[
        email.find("@") + 1 : email.find(".", email.find("@") + 1)
    ].capitalize()
    if opco == "OMITTED":
        opco = opco.upper()
    elif opco == "OMITTED":
        opco = "OMITTED"
    if first_name == preferred_first_name:
        preferred_first_name = None
    print("Successfully pulled data from Servicenow.")
    if output_var != None:
        output_var.append(
            ticketting_system_data(
                first_name,
                last_name,
                supervisor,
                opco,
                location,
                active_wd_status,
                vip_status,
                emp_id_number,
                email,
                preferred_first_name,
            )
        )
    else:
        return ticketting_system_data(
            first_name,
            last_name,
            supervisor,
            opco,
            location,
            active_wd_status,
            vip_status,
            emp_id_number,
            email,
            preferred_first_name,
        )


def merge_datasets(input_list):
    print("attempting to merge datasets.")
    if len(input_list) != 2:
        print("invalid amount of items in list.")
        exit()
    for item in input_list:
        if type(item) == ticketting_system_data:
            sn_data = item
        elif type(item) == Powershell_data:
            ps_data = item
        else:
            print("Invalid datatype.")
            exit()
    if type(sn_data) == bool:
        print("SN data error")
        return False
    elif type(ps_data) == bool:
        print("PS data error")
        return False
    if sn_data.emp_id_number == ps_data.emp_id_number:
        emp_id_number = sn_data.emp_id_number
    else:
        print("Difference between SN and PS emp_id_number.")
        print(
            f"Servicenow: {sn_data.emp_id_number} |Powershell: {ps_data.emp_id_number}"
        )
        return False
    if sn_data.first_name.lower() == ps_data.first_name.lower():
        first_name = sn_data.first_name
    else:
        print("Difference between SN and PS first_name.")
        first_name = sn_data.first_name
    if sn_data.email.lower() == ps_data.email.lower():
        email = ps_data.email
    else:
        print("Difference between SN and PS email.")
        print(f"Servicenow: {sn_data.email} |Powershell: {ps_data.email}")
        email = ps_data.email
    last_name = sn_data.last_name
    if sn_data.preferred_name != None:
        preferred_name = sn_data.preferred_name
    else:
        preferred_name = None
    if sn_data.vip_status == "true":
        vip_status = True
    else:
        vip_status = False
    location = sn_data.location
    username = ps_data.userid
    domain = domain_dict[ps_data.domain]
    opco = sn_data.opco
    supervisor = sn_data.supervisor
    hire_date = ps_data.hire_date
    if sn_data.wd_status == "true":
        employment_status = "Active"
    else:
        employment_status = "Inactive"
    print("Successfully merged datasets for the colleague.")
    return Person(
        first_name,
        last_name,
        email,
        location,
        username,
        opco,
        emp_id_number,
        domain,
        supervisor,
        hire_date,
        employment_status,
        vip_status,
        preferred_name,
    )


def pull_user_data(driver, emp_id_number):
    user_data = []
    sn_thread = Thread(target=query_servicenow, args=[driver, emp_id_number, user_data])
    ps_thread = Thread(
        target=query_powershell, args=[emp_id_number], kwargs={"output_var": user_data}
    )
    sn_thread.start()
    ps_thread.start()
    sn_thread.join()
    ps_thread.join()
    if len(user_data) != 2:
        print("failed to obtain data from at least one source.")
        return False
    if user_data[0] == False or user_data[1] == False:
        print("failed obtaining data from one source.")
        return False
    return merge_datasets(user_data)


def find_local_team(email, location, locations_json_filename):
    with open(locations_json_filename, "r") as json_file:
        json_data = json.load(json_file)
        colleague_location = location.strip()
        colleague_email_ending = email.lower()
        colleague_email_ending = (
            colleague_email_ending[colleague_email_ending.find("@") + 1 :]
        ).strip()
        try:
            return json_data[colleague_location][colleague_email_ending]
        except:
            return "Not Found"
