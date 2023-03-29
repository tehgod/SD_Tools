from dotenv import load_dotenv
from os import getenv


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

    def load_saved_creds(self):
        load_dotenv()
        if getenv("sd_tools_domain") != None:
            self.domain = getenv("sd_tools_domain")
        if getenv("sd_tools_username") != None:
            self.username = getenv("sd_tools_username")
        if getenv("sd_tools_password") != None:
            self.password = getenv("sd_tools_password")
        if getenv("encryption_username") != None:
            self.encryption_username = getenv("encryption_username")
        if getenv("encryption_password") != None:
            self.encryption_password = getenv("encryption_password")


class Person:
    def __init__(
        self,
        first_name=None,
        last_name=None,
        email=None,
        location=None,
        user_id=None,
        opco=None,
        emp_id_number=None,
        domain=None,
        supervisor=None,
        hire_date=None,
        employment_status=None,
        vip_status=False,
        preferred_name=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.domain = domain
        self.user_id = user_id
        self.opco = opco
        self.emp_id_number = emp_id_number
        self.supervisor = supervisor
        self.hire_date = hire_date
        self.employment_status = employment_status
        self.vip_status = vip_status
        self.preferred_name = preferred_name

    def return_attributes_list(self):
        attr_list = []
        for attr, value in self.__dict__.items():
            attr_list.append(attr)
        return attr_list
