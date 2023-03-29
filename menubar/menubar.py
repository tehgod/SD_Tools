from tkinter import *
import webbrowser
from tkinter import simpledialog, messagebox
from .menubar_secrets import *
from tools.credentials import Person, user_credentials
import win32com.client as win32


def open_prefilled_email(
    email_recipient, subject, body, cc_recipient="", attachment=""
):
    if email_recipient != None:
        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.Display(False)
        mail.To = email_recipient
        mail.CC = cc_recipient
        mail.Subject = subject
        mail.Body = body
        if attachment != "":
            mail.Attachments.Add(Source=attachment)
        mail.Send()
    return


class Menubar:
    def __init__(
        self,
        parent_frame,
        app_string,
        current_colleague: Person,
        user_creds=user_credentials(),
    ):
        # Create MenuBar
        self.main_menu = Menu(parent_frame)
        parent_frame.config(menu=self.main_menu)
        # File Menu
        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.credential_menu = Menu(tearoff=0)
        self.credential_menu.add_command(
            label="Store Elevated Username",
            command=lambda: self.set_global_username_action(user_creds),
        )
        self.credential_menu.add_command(
            label="Store Elevated Password",
            command=lambda: self.set_global_password_action(user_creds),
        )
        self.open_submenu = Menu(tearoff=0)
        self.open_submenu.add_command(
            label="CASD Incident Ticket",
            command=lambda: webbrowser.open_new(
                casd_inc_url
                + simpledialog.askstring(
                    "Input", "Please enter the incident number below."
                ).title()
            ),
        )
        self.open_submenu.add_command(
            label="CASD Change Order",
            command=lambda: webbrowser.open_new(
                casd_co_url
                + simpledialog.askstring(
                    "Input", "Please enter the change order number below."
                ).title()
            ),
        )
        self.open_submenu.add_command(
            label="Request",
            command=lambda: webbrowser.open_new(
                qr_order_url
                + simpledialog.askstring(
                    "Input", "Please enter the QR order number below."
                ).title()
            ),
        )
        self.file_menu.add_cascade(label="Open", menu=self.open_submenu)
        self.file_menu.add_cascade(label="Credentials", menu=self.credential_menu)
        self.file_menu.add_command(label="Exit", command=parent_frame.quit)

        # Tools Menu
        self.tools_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(
            label="AD Reset", command=lambda: app_string.set("ad")
        )
        self.tools_menu.add_command(
            label="2FA Reset", command=lambda: app_string.set("2fa")
        )
        self.tools_menu.add_command(
            label="encyrption Reset", command=lambda: app_string.set("encyrption")
        )

        # Email Menu
        self.email_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Email", menu=self.email_menu)
        self.email_menu.add_command(
            label="OKTA Reset",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "2FA Setup instructions",
                ("Please see the URL below for setup instructions." f"\n{okta_setup}"),
            ),
        )
        self.email_menu.add_command(
            label="Shared Mailbox Creation",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "Shared mailbox creation request",
                ("Please see the attached file, fill it out and email as directed."),
                attachment=attachments_folderpath,
            ),
        )
        self.iphone_email_menu = Menu(tearoff=0)
        self.email_menu.add_cascade(label="iPhone", menu=self.iphone_email_menu)
        self.iphone_email_menu.add_command(
            label="New Setup",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "iPhone initial setup instructions",
                ("Please see the URL below for setup instructions." f"\n{enroll_byod}"),
            ),
        )
        self.iphone_email_menu.add_command(
            label="Outlook Setup",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "Outlook Mobile setup instructions",
                (
                    "Please see the URL below for setup instructions."
                    f"\n{setup_outlook_iphone}"
                ),
            ),
        )
        self.iphone_email_menu.add_command(
            label="Outlook Re-Auth",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "Outlook Mobile password update instructions",
                (
                    "Please see the URL below for setup instructions."
                    f"\n{reauth_outlook_iphone}"
                ),
            ),
        )
        self.email_menu.add_command(
            label="Lost Device",
            command=lambda: open_prefilled_email(
                current_colleague.email,
                "Lost Device form",
                (
                    "Please see the attached file, fill it out and email back when completed."
                ),
                attachment=attachments_folderpath,
            ),
        )

        # Help Menu
        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(
            label="Show Current Credential Status",
            command=lambda: self.show_global_credential_action(user_creds),
        )

    def set_global_password_action(self, credentials):
        credentials.password = simpledialog.askstring("Input", "Password:", show="*")
        return

    def set_global_username_action(self, credentials):
        credentials.username = simpledialog.askstring("Input", "Username:")
        if "\\" in credentials.username:
            credentials.domain = credentials.username[
                0 : credentials.username.find("\\")
            ]
            credentials.username = credentials.username[
                credentials.username.find("\\") + 1 : len(credentials.username)
            ]

    def show_global_credential_action(self, credentials):
        if credentials.password != "":
            password_status = "Set"
        else:
            password_status = "Not Set"
        messagebox.showinfo(
            "Credentials",
            "Username: "
            + credentials.domain
            + "\\"
            + credentials.username
            + "\nPassword: "
            + password_status,
        )
