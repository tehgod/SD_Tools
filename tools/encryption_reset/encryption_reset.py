from .encryption_reset_functions import *
from tools.credentials import Person, user_credentials
from tkinter import *
from tkinter.ttk import Combobox
from threading import Thread


class encryption_Tool:
    def __init__(
        self,
        webdriver,
        parent_frame,
        results_frame,
        creds: user_credentials,
        current_colleague: Person = Person(
            email="", supervisor="", first_name="", last_name=""
        ),
    ):
        self.webdriver = webdriver
        self.main_frame = LabelFrame(
            parent_frame, borderwidth=2, text="Encryption Reset"
        )
        self.main_frame.pack()

        Label(self.main_frame, text="Client Code: ").grid(row=0, column=0)
        self.encryption_reset_client_code = Entry(self.main_frame)
        self.encryption_reset_client_code.bind(
            "<Return>", lambda event: self.run_encryption_reset_tool(creds)
        )
        self.encryption_reset_client_code.grid(row=0, column=1, columnspan=2)

        Label(self.main_frame, text="UserID: ").grid(row=1, column=0)
        self.encryption_reset_user_id_entry = StringVar()
        self.encryption_reset_user_id = Entry(
            self.main_frame, textvariable=self.encryption_reset_user_id_entry
        )
        self.encryption_reset_user_id.grid(row=1, column=1, columnspan=2)

        Label(self.main_frame, text="Reset Type: ").grid(row=2, column=0)
        reset_types = ["OMIT1", "OMIT2", "User Unlock"]
        self.encryption_reset_dropdown = Combobox(
            self.main_frame, values=reset_types, state="readonly"
        )
        self.encryption_reset_dropdown.grid(row=2, column=1, columnspan=2)

        self.encryption_reset_pull = Button(
            self.main_frame,
            text="Pull User",
            command=lambda: (
                self.encryption_reset_user_id_entry.set(current_colleague.emp_id_number)
                if (current_colleague != None)
                else self.encryption_reset_user_id_entry.set("")
            ),
        )
        self.encryption_reset_pull.grid(row=3, column=0)

        self.encryption_reset_submit = Button(
            self.main_frame,
            text="Submit",
            command=lambda: Thread(
                target=self.run_encryption_reset_tool, args=(creds,)
            ).start(),
        )
        self.encryption_reset_submit.grid(row=3, column=1)

        self.code_type = StringVar()
        self.line_1 = StringVar()
        self.line_2 = StringVar()
        self.line_3 = StringVar()

        self.email_button = Button(
            self.main_frame,
            text="Send Email",
            command=lambda: self.generate_email(current_colleague),
        )
        self.email_button.grid(row=3, column=2)

        self.encryption_results_frame = results_frame

    def generate_email(self, current_colleague):
        if current_colleague.first_name != None:
            first_name = current_colleague.first_name
        else:
            first_name = ""
        if current_colleague.last_name != None:
            last_name = current_colleague.last_name
        else:
            last_name = ""
        if current_colleague.supervisor != None:
            supervisor = current_colleague.supervisor
        else:
            supervisor = ""
        if current_colleague.email != None:
            email = current_colleague.email
        else:
            email = ""
        if self.line_3.get() != "None":
            open_prefilled_email("OMITTED")
        else:
            open_prefilled_email("OMITTED")
        return True

    def run_encryption_reset_tool(self, creds):
        for widget in self.encryption_results_frame.winfo_children():
            widget.destroy()
        client_code = self.encryption_reset_client_code.get()
        reset_type = self.encryption_reset_dropdown.get()
        user_id = self.encryption_reset_user_id_entry.get()
        match reset_type:
            case "User Reset":
                reset_type = "OMIT1"
            case "Bootonce":
                reset_type = "OMIT2"
            case "User Unlock":
                reset_type = "OMIT3"
        run_encryption_reset_tool_results = encryption_reset(
            self.webdriver, reset_type, client_code, user_id, creds
        )
        print(run_encryption_reset_tool_results)
        if run_encryption_reset_tool_results[0] == True:
            self.code_type.set(run_encryption_reset_tool_results[1]["code_type"])
            self.line_1.set(run_encryption_reset_tool_results[1]["line_1"])
            self.line_2.set(run_encryption_reset_tool_results[1]["line_2"])
            self.line_3.set(run_encryption_reset_tool_results[1]["line_3"])
            Label(self.encryption_results_frame, text="Code Type: ").grid(
                row=0, column=0
            )
            Label(self.encryption_results_frame, textvariable=self.code_type).grid(
                row=0, column=1
            )
            Label(self.encryption_results_frame, text="Line 1: ").grid(row=1, column=0)
            Label(self.encryption_results_frame, textvariable=self.line_1).grid(
                row=1, column=1
            )
            Label(self.encryption_results_frame, text="Line 2: ").grid(row=2, column=0)
            Label(self.encryption_results_frame, textvariable=self.line_2).grid(
                row=2, column=1
            )
            if self.line_3.get() != "None":
                Label(self.encryption_results_frame, text="Line 3: ").grid(
                    row=3, column=0
                )
                Label(self.encryption_results_frame, textvariable=self.line_3).grid(
                    row=3, column=1
                )
            else:
                pass
        elif run_encryption_reset_tool_results[0] == False:
            pass


if __name__ == "__main__":
    application_frame_main = Tk()
    application_frame_main.title("encryption Reset")
    application_frame_main.configure(borderwidth=1)
    my_creds = user_credentials()
    my_creds.load_saved_creds()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    encryption_browser = webdriver.Chrome(
        executable_path="local_filepath", options=chrome_options
    )
    my_frame = encryption_Tool(
        encryption_browser, application_frame_main, None, my_creds
    )
    application_frame_main.mainloop()
