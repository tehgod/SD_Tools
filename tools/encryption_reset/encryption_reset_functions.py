import string
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import win32com.client as win32


class user_credentials:
    def __init__(
        self,
        Domain="",
        Username="",
        Password="",
        encryption_Username="",
        encryption_Password="",
    ):
        self.domain = Domain
        self.username = Username
        self.password = Password
        self.encryption_username = encryption_Username
        self.encryption_password = encryption_Password


def open_prefilled_email(email_recipient, subject, body, cc_recipient=""):
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = email_recipient
    mail.CC = cc_recipient
    mail.Subject = subject
    mail.Body = body
    mail.Display(False)


# Note that when working below, all pageloads may have extreme latency. Work around with this in mind.
def encryption_reset(
    webdriver, reset_type, reset_code: string, userid, credentials: user_credentials
):
    wait = WebDriverWait(webdriver, 5)
    webdriver.get("OMITTED_URL")
    if webdriver.current_url == "OMITTED_URL":
        pass
    elif webdriver.current_url == "OMITTED_URL":
        wait.until(EC.presence_of_element_located((By.ID, "name")))
        webdriver.find_element(By.ID, "name").send_keys(credentials.encryption_username)
        webdriver.find_element(By.ID, "password").send_keys(
            credentials.encryption_password
        )
        print(credentials.encryption_password)
        webdriver.find_element(By.ID, "login.button").click()
        wait.until(EC.url_matches, "OMITTED_URL")
    wait = WebDriverWait(webdriver, 90)
    webdriver.get("OMITTED_URL")
    wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "mfs-container-iframe"))
    )
    wait.until(EC.visibility_of_element_located((By.ID, "challengeCode")))
    webdriver.find_element(By.ID, "challengeCode").send_keys(reset_code)
    webdriver.find_element(By.ID, "challengeCode").send_keys(Keys.RETURN)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "orionInputErrorText")))
    error_messages = webdriver.find_elements(By.CLASS_NAME, "orionInputErrorText")
    if len(error_messages) == 3:
        return False, error_messages[2].text
    wait.until(EC.element_to_be_clickable((By.ID, "userRecovery_label")))
    match reset_type:
        case "OMIT1":
            if webdriver.find_element(By.ID, "machineRecovery").is_selected() == True:
                webdriver.find_element(By.ID, "orion_prevnext_next").click()
                code_type = "OMIT1"
        case "OMIT2":
            webdriver.find_element(By.ID, "userRecovery_label").click()
            if webdriver.find_element(By.ID, "machineRecovery").is_selected() == True:
                code_type = "OMIT1"
            elif (
                webdriver.find_element(By.ID, "unlockDisabledUser").is_selected()
                == True
            ) and (webdriver.find_element(By.ID, "userRecovery").is_selected() == True):
                webdriver.find_element(By.ID, "orion_prevnext_next").click()
                code_type = "OMIT2"
                wait.until(EC.element_to_be_clickable((By.ID, "userList_quickFind")))
                attempts = 0
                fully_loaded = False
                while attempts < 5:
                    if "yui-verlay-hidden" in webdriver.find_element(
                        By.ID, "timerOverlay"
                    ).get_attribute("class"):
                        sleep(1)
                        attempts += 1
                    else:
                        attempts = 5
                        fully_loaded = True
                if fully_loaded == False:
                    print("failed to load encryption users list.")
                    return False, "Failed to load encryption users list."
                table_pulled = False
                while table_pulled == False:
                    my_table = webdriver.find_element(
                        By.ID, "userList_dataBody"
                    ).find_elements(By.TAG_NAME, "tr")
                    if "Traceback" not in my_table[0].text:
                        table_pulled = True
                    else:
                        sleep(1)
                my_checkbox = None
                for item in my_table:
                    while item.text == "   ":
                        sleep(1)
                    if item.text.strip() == userid:
                        my_checkbox = item.find_element(By.TAG_NAME, "input")
                        break
                if my_checkbox != None:
                    my_checkbox.click()
                    webdriver.find_element(By.ID, "orion_prevnext_next").click()
                else:
                    print("user not assigned to machine. proceeding to get OMIT1")
                    webdriver.find_element(By.ID, "recoveryWizard_step_2").click()
                    wait.until(
                        EC.visibility_of_element_located(
                            (By.CLASS_NAME, "orionInputErrorText")
                        )
                    )
                    wait.until(
                        EC.element_to_be_clickable((By.ID, "userRecovery_label"))
                    )
                    if (
                        webdriver.find_element(By.ID, "machineRecovery").is_selected()
                        == True
                    ):
                        webdriver.find_element(By.ID, "orion_prevnext_next").click()
                        code_type = "OMIT1"
        case "user_reset":
            webdriver.find_element(By.ID, "userRecovery_label").click()
            webdriver.find_element(By.ID, "resetToken_label").click()
            if webdriver.find_element(By.ID, "machineRecovery").is_selected() == True:
                webdriver.find_element(By.ID, "orion_prevnext_next").click()
                code_type = "OMIT1"
            elif (
                webdriver.find_element(By.ID, "resetToken").is_selected() == True
            ) and (webdriver.find_element(By.ID, "userRecovery").is_selected() == True):
                webdriver.find_element(By.ID, "orion_prevnext_next").click()
                code_type = "user_reset"
                wait.until(EC.element_to_be_clickable((By.ID, "userList_quickFind")))
                attempts = 0
                fully_loaded = False
                while attempts < 5:
                    if "yui-verlay-hidden" in webdriver.find_element(
                        By.ID, "timerOverlay"
                    ).get_attribute("class"):
                        sleep(1)
                        attempts += 1
                    else:
                        attempts = 5
                        fully_loaded = True
                if fully_loaded == False:
                    print("failed to load encryption users list.")
                    return False, "Failed to load encryption users list."
                table_pulled = False
                while table_pulled == False:
                    my_table = webdriver.find_element(
                        By.ID, "userList_dataBody"
                    ).find_elements(By.TAG_NAME, "tr")
                    if "Traceback" not in my_table[0].text:
                        table_pulled = True
                    else:
                        sleep(1)
                my_checkbox = None
                for item in my_table:
                    while item.text == "   ":  # StaleElementReferenceException possible
                        sleep(1)
                    if item.text.strip() == userid:
                        my_checkbox = item.find_element(By.TAG_NAME, "input")
                        break
                if my_checkbox != None:
                    my_checkbox.click()
                    webdriver.find_element(By.ID, "orion_prevnext_next").click()
                else:
                    print("user not assigned to machine. proceeding to get OMIT1")
                    webdriver.find_element(By.ID, "recoveryWizard_step_2").click()
                    wait.until(
                        EC.visibility_of_element_located(
                            (By.CLASS_NAME, "orionInputErrorText")
                        )
                    )
                    wait.until(
                        EC.element_to_be_clickable((By.ID, "userRecovery_label"))
                    )
                    if (
                        webdriver.find_element(By.ID, "machineRecovery").is_selected()
                        == True
                    ):
                        webdriver.find_element(By.ID, "orion_prevnext_next").click()
                        code_type = "OMIT1"
            else:
                if (
                    webdriver.find_element(By.ID, "machineRecovery").is_selected()
                    == True
                ):
                    code_type = "OMIT1"
                    webdriver.find_element(By.ID, "orion_prevnext_next").click()
    response_code = (webdriver.find_element(By.ID, "responseCode").text).split("\n")
    line_3 = None
    for line in response_code:
        if line.startswith("Line 1"):
            line_1 = line.strip()[7:]
        if line.startswith("Line 2"):
            line_2 = line.strip()[7:]
        if line.startswith("Line 3"):
            line_3 = line.strip()[7:]
    return True, {
        "code_type": code_type,
        "line_1": line_1,
        "line_2": line_2,
        "line_3": line_3,
    }


def login(webdriver, credentials):
    wait = WebDriverWait(webdriver, 5)
    webdriver.get("OMITTED_URL")
    if webdriver.current_url == "OMITTED_URL":
        pass
    elif webdriver.current_url == "OMITTED_URL":
        wait.until(EC.presence_of_element_located((By.ID, "name")))
        webdriver.find_element(By.ID, "name").send_keys(credentials.encryption_username)
        webdriver.find_element(By.ID, "password").send_keys(
            credentials.encryption_password
        )
        webdriver.find_element(By.ID, "login.button").click()
        wait.until(EC.url_matches, "OMITTED_URL")
        print("completed login.")
        pass


if __name__ == "__main__":
    pass
