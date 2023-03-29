from tkinter import *
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .employee_lookup_functions import Person, find_local_team, pull_user_data
import pyperclip


class Employee_lookup:
    def __init__(
        self,
        parent_frame,
        parent_frame2,
        current_colleague: Person,
        chromedriver_path,
        hidden_var=True,
    ):
        # EmpID entry Box
        self.main_frame = LabelFrame(
            parent_frame, borderwidth=2, text="Employee Lookup"
        )
        Label(self.main_frame, text="EmployeeID Number:").pack(side=TOP, fill=X)
        self.main_frame.pack()
        self.employee_search_entry = Entry(
            self.main_frame, width=25, font=("Arial", 10)
        )
        self.employee_search_entry.bind(
            "<Return>",
            func=lambda event: Thread(
                target=self.employee_search_submit_button_action,
                args=(current_colleague,),
            ).start(),
        )
        self.employee_search_submit_button = Button(
            self.main_frame,
            text="Verify ID",
            command=lambda: Thread(
                target=self.employee_search_submit_button_action,
                args=(current_colleague,),
            ).start(),
        )
        self.employee_search_submit_button.pack(side=BOTTOM, fill=X)
        self.employee_search_entry.pack(side=TOP)

        # EID InfoBox
        results_frame = LabelFrame(parent_frame2, borderwidth=2, text="Results:")
        results_frame.pack()
        self.eid_search_number_var = StringVar()
        self.eid_search_name_var = StringVar()
        self.eid_search_userid_var = StringVar()
        self.eid_search_email_var = StringVar()
        self.eid_search_location_var = StringVar()
        self.eid_search_supervisor_var = StringVar()
        self.eid_search_hire_date_var = StringVar()
        self.eid_search_employment_status_var = StringVar()
        self.eid_search_local_team_var = StringVar()
        self.eid_search_number_var.set("empty")
        self.eid_search_name_var.set("empty")
        self.eid_search_userid_var.set("empty")
        self.eid_search_email_var.set("empty")
        self.eid_search_location_var.set("empty")
        self.eid_search_supervisor_var.set("empty")
        self.eid_search_hire_date_var.set("empty")
        self.eid_search_employment_status_var.set("empty")
        self.eid_search_local_team_var.set("empty")
        # Sadly, after a LOT of looking into the above, it can not be cleaned up to be any better.
        Label(results_frame, text="Name:").grid(sticky="W", row=0, column=0)
        self.eid_search_name_label = Label(
            results_frame, textvariable=self.eid_search_name_var
        )
        self.eid_search_name_label.grid(row=0, column=1)
        self.eid_search_name_label.bind(
            "<Button-1>", lambda event: pyperclip.copy(self.eid_search_name_var.get())
        )
        Label(results_frame, text="EmployeeID:").grid(sticky="W", row=1, column=0)
        self.eid_search_number_label = Label(
            results_frame, textvariable=self.eid_search_number_var
        )
        self.eid_search_number_label.grid(row=1, column=1)
        self.eid_search_number_label.bind(
            "<Button-1>", lambda event: pyperclip.copy(self.eid_search_number_var.get())
        )
        Label(results_frame, text="UserID:").grid(sticky="W", row=2, column=0)
        self.eid_search_userid_label = Label(
            results_frame, textvariable=self.eid_search_userid_var
        )
        self.eid_search_userid_label.grid(row=2, column=1)
        self.eid_search_userid_label.bind(
            "<Button-1>", lambda event: pyperclip.copy(self.eid_search_userid_var.get())
        )
        Label(results_frame, text="Email:").grid(sticky="W", row=3, column=0)
        self.eid_search_email_label = Label(
            results_frame, textvariable=self.eid_search_email_var
        )
        self.eid_search_email_label.grid(row=3, column=1)
        self.eid_search_email_label.bind(
            "<Button-1>", lambda event: pyperclip.copy(self.eid_search_email_var.get())
        )
        Label(results_frame, text="Location:").grid(sticky="W", row=4, column=0)
        self.eid_search_location_label = Label(
            results_frame, textvariable=self.eid_search_location_var
        )
        self.eid_search_location_label.grid(row=4, column=1)
        self.eid_search_location_label.bind(
            "<Button-1>",
            lambda event: pyperclip.copy(self.eid_search_location_var.get()),
        )
        Label(results_frame, text="Supervisor:").grid(sticky="W", row=5, column=0)
        self.eid_search_supervisor_label = Label(
            results_frame, textvariable=self.eid_search_supervisor_var
        )
        self.eid_search_supervisor_label.grid(row=5, column=1)
        self.eid_search_supervisor_label.bind(
            "<Button-1>",
            lambda event: pyperclip.copy(self.eid_search_supervisor_var.get()),
        )
        Label(results_frame, text="Hire Date:").grid(sticky="W", row=6, column=0)
        self.eid_search_hire_date_label = Label(
            results_frame, textvariable=self.eid_search_hire_date_var
        )
        self.eid_search_hire_date_label.grid(row=6, column=1)
        self.eid_search_hire_date_label.bind(
            "<Button-1>",
            lambda event: pyperclip.copy(self.eid_search_hire_date_var.get()),
        )
        Label(results_frame, text="Employment Status:").grid(
            sticky="W", row=7, column=0
        )
        self.eid_search_employment_status_label = Label(
            results_frame, textvariable=self.eid_search_employment_status_var
        )
        self.eid_search_employment_status_label.grid(row=7, column=1)
        self.eid_search_employment_status_label.bind(
            "<Button-1>",
            lambda event: pyperclip.copy(self.eid_search_employment_status_var.get()),
        )

        Label(results_frame, text="Local Team:").grid(sticky="W", row=8, column=0)
        self.eid_search_local_team_label = Label(
            results_frame, textvariable=self.eid_search_local_team_var
        )
        self.eid_search_local_team_label.grid(row=8, column=1)
        self.eid_search_local_team_label.bind(
            "<Button-1>",
            lambda event: pyperclip.copy(self.eid_search_local_team_var.get()),
        )

        chrome_options = Options()
        if hidden_var == True:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")
        self.service_now_browser = webdriver.Chrome(
            executable_path=chromedriver_path, options=chrome_options
        )
        Thread(target=self.service_now_browser.get, args=["OMITTED INFO"]).start()
        self.run_times = 0
        self.main_frame.after(600 * 1000, self.stay_loaded)

    def employee_search_submit_button_action(self, colleague_stuff):
        self.employee_search_submit_button.config(state="disabled")
        if (self.employee_search_entry.get()).isdigit() == False:
            self.employee_search_submit_button.config(state="normal")
            self.main_frame.configure(background="red")
            return False
        else:
            self.main_frame.configure(background="yellow")
            if self.run_times == 0:
                try:
                    WebDriverWait(self.service_now_browser, 90).until(
                        EC.title_contains("New Record")
                    )
                    print("Finished initial loading of Servicenow.")
                    self.run_times += 1
                except:
                    self.employee_search_submit_button.config(state="normal")
                    self.main_frame.configure(background="red")
                    return False
            print("Proceeding to data lookup of the colleague.")
            self.employee_search_current_colleague = pull_user_data(
                self.service_now_browser, self.employee_search_entry.get()
            )
            print("initial lookup finished.")
            if isinstance(self.employee_search_current_colleague, Person) == True:
                attempt_count = 3
            else:
                print("person not returned from SN lookup")
                attempt_count = 1
            while (
                isinstance(self.employee_search_current_colleague, Person) != True
            ) and (attempt_count < 3):
                self.employee_search_current_colleague = pull_user_data(
                    self.service_now_browser, self.employee_search_entry.get()
                )
                if isinstance(self.employee_search_current_colleague, Person) == True:
                    attempt_count = 3
                else:
                    attempt_count += 1
            if isinstance(self.employee_search_current_colleague, Person) != True:
                self.employee_search_submit_button.config(state="normal")
                self.main_frame.configure(background="red")
                return False
        for attr, value in self.employee_search_current_colleague.__dict__.items():
            setattr(colleague_stuff, attr, value)
        # colleague_stuff.email = self.employee_search_current_colleague.email
        self.eid_search_number_var.set(
            self.employee_search_current_colleague.emp_id_number
        )
        if self.employee_search_current_colleague.preferred_name != None:
            self.eid_search_name_var.set(
                self.employee_search_current_colleague.preferred_name
                + " "
                + self.employee_search_current_colleague.last_name
            )
        else:
            self.eid_search_name_var.set(
                self.employee_search_current_colleague.first_name
                + " "
                + self.employee_search_current_colleague.last_name
            )
        if self.employee_search_current_colleague.vip_status == True:
            self.eid_search_name_label.config(fg="red")
            current_name_text = self.eid_search_name_var.get()
            self.eid_search_name_var.set(f"{current_name_text} (VIP)")
        else:
            self.eid_search_name_label.config(fg="black")
        self.eid_search_userid_var.set(
            f"{self.employee_search_current_colleague.domain}\{self.employee_search_current_colleague.user_id}"
        )
        self.eid_search_email_var.set(self.employee_search_current_colleague.email)
        self.eid_search_location_var.set(
            self.employee_search_current_colleague.location
        )
        self.eid_search_supervisor_var.set(
            self.employee_search_current_colleague.supervisor
        )
        self.eid_search_hire_date_var.set(
            self.employee_search_current_colleague.hire_date
        )
        self.eid_search_employment_status_var.set(
            self.employee_search_current_colleague.employment_status
        )
        self.eid_search_local_team_var.set(
            find_local_team(
                self.eid_search_email_var.get(),
                self.eid_search_location_var.get(),
                "./config/OMITTED_FILENAME.json",
            )
        )
        self.main_frame.configure(background="green")
        self.employee_search_submit_button.config(state="normal")

    def stay_loaded(self):
        Thread(target=self.service_now_browser.get, args=["OMITTED URL"]).start()
        print("refreshing OMITTED Browser.")
        self.main_frame.after(600 * 1000, self.stay_loaded)


if __name__ == "__main__":
    current_colleague = Person()
    application_frame_main = Tk()
    application_frame_main.title("test")
    test_frame = Employee_lookup(
        application_frame_main, application_frame_main, current_colleague
    )
    application_frame_main.mainloop()
