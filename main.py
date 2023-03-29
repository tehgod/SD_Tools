from tkinter import *
from tools.credentials import *
from tools.encryption_reset.encryption_reset import encryption_reset
from menubar.menubar import Menubar
from tools.employee_lookup.employee_lookup import Employee_lookup
from tools.two_fa_reset.two_fa_reset_tool import two_fa_Tool
from tools.ad_reset.ad_tools import ad_tools
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import getenv
from dotenv import load_dotenv


def load_app(x, y, z):
    for widget in app_frame.winfo_children():
        widget.destroy()
    match current_application.get():
        case "ad":
            my_app = ad_tools(app_frame, results_frame, my_creds, current_colleague)
        case "2fa":
            my_app = two_fa_Tool(app_frame, results_frame, my_creds)
        case "encryption":
            my_app = encryption_reset(
                app_webdriver, app_frame, results_frame, my_creds, current_colleague
            )


if __name__ == "__main__":
    load_dotenv()
    # Load default Tkinter instance/window
    application_frame_main = Tk()
    application_frame_main.title("SD Tools")
    application_frame_main.configure(borderwidth=1)
    chromedriver_path = getenv("chromedriver_path")
    chromedriver_hidden = False
    # Load hidden persistent browser for apps to use
    chrome_options = Options()
    if chromedriver_hidden == True:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--no-sandbox")
    app_webdriver = webdriver.Chrome(
        executable_path=chromedriver_path, options=chrome_options
    )

    # Create a frame for employee lookup, apps, and app results
    employee_lookup_frame = Frame(application_frame_main)
    app_frame = Frame(application_frame_main)
    results_frame = LabelFrame(application_frame_main, text="Results", borderwidth=2)
    employee_lookup_frame.grid(row=0, column=0)
    app_frame.grid(row=0, column=1)
    results_frame.grid(row=1, columnspan=2)

    # # # #load credentials file and declare shared variables
    my_creds = user_credentials()
    my_creds.load_saved_creds()
    current_colleague = Person()
    current_application = StringVar()

    # load menubar
    menubar = Menubar(
        application_frame_main, current_application, current_colleague, my_creds
    )

    # load default apps
    employee_lookup_app = Employee_lookup(
        employee_lookup_frame,
        employee_lookup_frame,
        current_colleague,
        chromedriver_path,
        hidden_var=chromedriver_hidden,
    )
    current_application.trace(
        "w", load_app
    )  # set monitor to current application to keep loaded
    current_application.set("ad")  # set current application to ad app

    # run application
    application_frame_main.mainloop()
