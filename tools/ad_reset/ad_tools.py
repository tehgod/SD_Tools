from tkinter import *
from tkinter.ttk import Combobox
from .ad_tools_functions import *
from tools.credentials import user_credentials, Person
from ad_tools_secrets import domain_dict


class ad_tools:
    def __init__(
        self,
        parent_frame,
        results_frame,
        admin_creds: user_credentials,
        current_colleague: Person,
    ):
        self.my_creds = admin_creds
        self.domain_dict = domain_dict
        current_row = 0
        self.main_frame = LabelFrame(
            parent_frame, borderwidth=2, text="AD Tools and Info"
        )
        self.main_frame.grid(row=current_row)
        domain_list = []
        for item in self.domain_dict:
            domain_list.append(item)
        self.ad_reset_domain_dropdown_box = Combobox(
            self.main_frame, values=domain_list, state="readonly"
        )
        Label(self.main_frame, text="Select Domain").grid(row=current_row, column=0)
        self.ad_reset_domain_dropdown_box.grid(row=current_row, column=1)
        self.ad_reset_pull_information = Button(
            self.main_frame,
            text="Pull \n Information",
            command=lambda: self.ad_tool_pull_info(current_colleague),
        )
        self.ad_reset_pull_information.grid(row=current_row, rowspan=2, column=2)
        current_row += 1
        Label(self.main_frame, text="Enter Username").grid(row=current_row, column=0)
        self.ad_reset_userid_entry_stringvar = StringVar()
        self.ad_reset_userid_entry = Entry(
            self.main_frame, textvariable=self.ad_reset_userid_entry_stringvar
        )
        self.ad_reset_userid_entry.grid(row=current_row, column=1)
        current_row += 1
        Label(self.main_frame, text="Enter New Password").grid(
            row=current_row, column=0
        )
        self.new_password_variable = StringVar()
        self.ad_reset_new_password = Entry(
            self.main_frame, textvariable=self.new_password_variable
        )
        self.ad_reset_new_password.grid(row=current_row, column=1)
        ad_reset_generate_password = Button(
            self.main_frame, text="Random", command=self.generate_random_password
        )
        ad_reset_generate_password.grid(row=current_row, column=2)
        current_row += 1
        ad_reset_submit_button = Button(
            self.main_frame,
            text="Reset",
            command=lambda: self.run_ad_reset_tool(admin_creds),
        )
        ad_reset_submit_button.grid(row=current_row, column=0)
        ad_reset_email_button = Button(
            self.main_frame,
            text="Send Email",
            command=lambda: open_prefilled_email("OMITTED INFO"),
        )
        ad_reset_email_button.grid(row=current_row, column=2)
        current_row += 1
        self.ad_results_frame = results_frame

    def ad_tool_pull_info(self, current_colleague):
        try:
            self.ad_reset_domain_dropdown_box.set(current_colleague.domain)
        except:
            pass
        self.ad_reset_userid_entry_stringvar.set(current_colleague.user_id)

    def generate_random_password(self):
        new_password = password_generator(12)
        self.new_password_variable.set(new_password)

    def run_ad_reset_tool(self, creds):
        ad_reset_tool_results = ad_reset(
            self.domain_dict[self.ad_reset_domain_dropdown_box.get()],
            self.ad_reset_userid_entry.get(),
            self.ad_reset_new_password.get(),
            creds.domain,
            creds.username,
            creds.password,
        )
        for widget in self.ad_results_frame.winfo_children():
            widget.destroy()
        Label(self.ad_results_frame, text="Reset Status:").grid(row=0, column=0)
        ad_reset_tool_results_var = StringVar()
        ad_reset_tool_results_var.set(ad_reset_tool_results)
        Label(self.ad_results_frame, textvariable=ad_reset_tool_results_var).grid(
            row=1, column=0
        )
