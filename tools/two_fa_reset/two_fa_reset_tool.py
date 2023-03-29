from tkinter import *
from .two_fa_reset_tool_functions import unlock_two_fa
from tools.credentials import user_credentials


class two_fa_Tool:
    def __init__(self, parent_frame, parent_results_frame, creds: user_credentials):
        self.main_frame = LabelFrame(parent_frame, borderwidth=2, text="2fa Reset")
        self.main_frame.pack()
        Label(self.main_frame, text="Enter two_fa EmpID Number: ").grid(row=0, column=0)
        self.two_fa_reset_entry = Entry(self.main_frame)
        self.two_fa_reset_entry.bind(
            "<Return>", lambda event: self.run_two_fa_reset_tool(creds)
        )
        self.two_fa_reset_entry.grid(row=0, column=1)
        self.two_fa_unlock_button_status = BooleanVar()
        self.two_fa_reset_button_status = BooleanVar()
        self.two_fa_unlock_button = Checkbutton(
            self.main_frame,
            text="Unlock Account",
            variable=self.two_fa_unlock_button_status,
            onvalue=True,
            offvalue=False,
            height=5,
            width=20,
        )
        self.two_fa_reset_button = Checkbutton(
            self.main_frame,
            text="Reset two_fa Methods",
            variable=self.two_fa_reset_button_status,
            onvalue=True,
            offvalue=False,
            height=5,
            width=20,
        )
        self.two_fa_unlock_button.grid(row=1, column=0)
        self.two_fa_unlock_button.select()
        self.two_fa_reset_button.grid(row=1, column=1)
        self.two_fa_tool_button = Button(
            self.main_frame,
            text="Check two_fa Status",
            command=lambda: self.run_two_fa_reset_tool(creds),
        )
        self.two_fa_tool_button.grid(row=2, column=0, columnspan=2)
        self.two_fa_results_frame = parent_results_frame
        self.two_fa_results_frame.grid(row=3, columnspan=2)

    def run_two_fa_reset_tool(self, creds):
        target_colleague = self.two_fa_reset_entry.get()
        run_two_fa_reset_results = unlock_two_fa(
            target_colleague,
            self.two_fa_reset_button_status.get(),
            self.two_fa_unlock_button_status.get(),
            creds.domain,
            creds.username,
            creds.password,
        )
        for widget in self.two_fa_results_frame.winfo_children():
            widget.destroy()
        current_colleague_reset = StringVar()
        current_colleague_reset.set("2fa Reset results for: " + target_colleague)
        Label(self.two_fa_results_frame, textvariable=current_colleague_reset).grid(
            row=0, column=0
        )
        if type(run_two_fa_reset_results) == list:
            Label(self.two_fa_results_frame, text="Authentication methods set: ").grid(
                row=1, column=0
            )
            x = 2
            if run_two_fa_reset_results == []:
                Label(
                    self.two_fa_results_frame, text="No authentication method setup"
                ).grid(row=x, column=0)
            else:
                for item in run_two_fa_reset_results:
                    two_fa_auth_method = StringVar()
                    two_fa_auth_method.set(item)
                    Label(
                        self.two_fa_results_frame, textvariable=two_fa_auth_method
                    ).grid(row=x, column=0)
                    x += 1
            return
        else:
            two_fa_message = StringVar()
            two_fa_message.set(run_two_fa_reset_results)
            Label(self.two_fa_results_frame, textvariable=two_fa_message).grid(
                row=1, column=0, columnspan=3
            )
            print(run_two_fa_reset_results)
        return
