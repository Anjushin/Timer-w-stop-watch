import tkinter as tk
from tkinter import messagebox
# removed pdf function
# import fpdf
from datetime import date



class Timer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(10, weight=1)
        container.grid_columnconfigure(10, weight=1)
        # sizes and title
        self.minsize(480, 520)
        self.geometry("480x520")
        self.title("Productive Timer")
        self.frames = {}

        # F=Frame, this is to create key in frames for pages so we can switch pages later, and grab their methods
        for F in (MainPage, Customization, ReportPage):
            # the frame container and things inside that page
            frame = F(container, self)
            # create key in frame dict
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

        # drop down for customization
        # create an empty menu
        menu = tk.Menu(container)
        self.config(menu=menu)
        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        # adding drop down to that(file) menu
        x = file_menu.add_command(label="User Customization", command=lambda: self.show_frame(Customization))
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)

    def show_frame(self, controller):
        """
        Show the window/frame given they key input
        :param controller: The page user want to show
        :return:
        """
        frame = self.frames[controller]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        """
        The Main Page for Timer Class
        :param parent: The Timer container
        :param controller: The Timer class/controller
        """
        # timer list to hold time in it
        global time_hold_work
        global time_hold_slack
        # w and s for changing name customization, w = work s = slack default
        global custom
        # for timer box to easily iterate
        global listbox
        # default 30 minutes
        global time_set
        global time_set_label
        time_set = "00:30:00"
        time_set_label = tk.StringVar()
        time_set_label.set("00:30:00")
        self.button_1 = False
        self.button_2 = False
        custom = {"button_1": "work", "button_2": "slack"}
        # set a holder variable for timer, so it can be display
        self.t = tk.StringVar()
        # set the holder to timer string
        self.t.set("00:00:00")
        self.controller = controller
        tk.Frame.__init__(self, parent)

        # buttons start here
        self.label = tk.Label(self, text="Start Page")
        self.label.grid(row=0, column=1, pady=10, padx=10)

        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=3)

        # timer label
        self.lb = tk.Label(self, textvariable=self.t, font=("Courier 40 bold"), bg="red")
        self.lb.grid(row=2, column= 1)

        # timer limit set label
        self.label_time_limit = tk.Label(self, textvariable=time_set_label, font=("Arial", 25))
        self.label_time_limit.grid(row=1, column= 1)

        # button 1
        self.work_button = tk.Button(self, text=f"{custom['button_1']}", width=10, height=2,
                                     command=self.start_button_1)
        self.work_button.grid(row=3, column=1, pady=10, padx=10)

        # label for button 1
        self.work_label = tk.Label(self, text="Start: ")
        self.work_label.place(x=150, y=175)

        # button 2
        self.slack_button = tk.Button(self, text=f"{custom['button_2']}", width=10, height=2,
                                      command=self.start_button_2)
        self.slack_button.grid(row=4, column=1, pady=10, padx=10)

        # label for button 2
        self.slack_label = tk.Label(self, text="Start: ")
        self.slack_label.place(x=150, y=230)

        self.stop_button = tk.Button(self, text="Reset", state=tk.DISABLED, width=10, height=2, command=self.reset)
        self.stop_button.place(x=280, y=162)

        self.pause_button = tk.Button(self, text="Pause", state=tk.DISABLED, width=10, height=2, command=self.pause)
        self.pause_button.place(x=280, y=224)

        self.resume_button = tk.Button(self, text="Resume", state=tk.DISABLED, width=10, height=2, command=self.resume)
        self.resume_button.place(x=280, y=270)

        # dummy buttons
        # self.printButton = tk.Button(self, text="test", command=self.update_table)
        # self.printButton.grid(row=1, column=3, pady=10, padx=10)
        #
        # self.printButton_2 = tk.Button(self, text="test2", command=self.test_add_time_list)
        # self.printButton_2.grid(row=1, column=4)

        # navigate to different window
        self.window_report = tk.Button(self, text="Report Page", command=lambda: controller.show_frame(ReportPage))
        self.window_report.grid(row=1, column=0, pady=10, padx=10)

        self.window_custom = tk.Button(self, text="Customization",
                                  command=lambda: controller.show_frame(Customization))
        self.window_custom.grid(row=6, column=0, pady=10, padx=10)

        # empty list for two buttons
        # time_hold_work = ["00:00:01", "00:00:02"]
        # time_hold_slack = ["00:00:05", "00:00:05"]
        time_hold_work = []
        time_hold_slack = []
        # used for updating timer table
        listbox = tk.Listbox()


    def start_button_1(self):
        """
        Start the timer that store the data for button 1 name only, disable some buttons
        :return:
        """
        global count
        self.button_1 = True
        self.switch()
        count = 0
        self.timer()

    def start_button_2(self):
        """
        Start the timer that store the data for button 2 name only, disable some buttons
        :return:
        """
        global count
        self.button_2 = True
        self.switch()
        count = 0
        self.timer()

    def reset(self):
        """
        Reset the timer back 0, and store the timer that ran based on which button was pressed
        :return:
        """
        global count
        count = 1
        # actual timer
        #print(self.d)
        # check which button user has clicked to append timer to according list
        if self.button_1 is True:
            time_hold_work.append(self.d)
        else:
            time_hold_slack.append(self.d)
        # call update table function to show/update the list
        self.update_table()
        # reset timer to 00
        self.t.set('00:00:00')
        # call switch function to re enable buttons
        self.switch()
        # set 2 button back to False
        self.button_1 = False
        self.button_2 = False
        # set resume and pause button to be disable when stop button is disabled
        if self.stop_button["state"] == "disabled":
            self.resume_button["state"] = "disabled"
            self.pause_button["state"] = "disabled"


    def update_table(self):
        """
        Shows a timer list and update everytime a new time is added
        :return:
        """
        # disable some button
        #self.switch()
        listbox.delete(0, tk.END)
        # repopulate again, for both button mode
        for i in time_hold_work:
            listbox.insert(tk.END, f"{custom['button_1']}: " + str(i))
        for i in time_hold_slack:
            listbox.insert(tk.END, f"{custom['button_2']}: " + str(i))
        listbox.pack()

    def pause(self):
        """
        Stop the timer but not resetting
        :return:
        """
        global count
        count = 1
        self.switch_2()

    def resume(self):
        """
        Resume the timer, use for after pausing
        :return:
        """
        global count
        count = 0
        self.timer()
        self.switch_2()

    def timer(self):
        """
        Makes timer run like digital clock. Default time alarm is 30 minutes
        :return:
        """
        global count
        global time_set
        if count == 0:
            # get the variable that we set at the main page
            self.d = str(self.t.get())
            #print(self.d)
            # separate each value/variable using split at ':'
            h, m, s = map(int, self.d.split(":"))

            h = int(h)
            m = int(m)
            s = int(s)
            # set logic so that it can function like our time
            if s < 59:
                s += 1
            elif s == 59:
                s = 0
                if m < 59:
                    m += 1
                elif m == 59:
                    m = 0
                    h += 1

            # help to view the timer better by adding 0 in front of the timer when it is less than 10
            if h < 10:
                h = str(0) + str(h)
            else:
                h = str(h)
            if m < 10:
                m = str(0) + str(m)
            else:
                m = str(m)
            if s < 10:
                s = str(0) + str(s)
            else:
                s = str(s)
            self.d = h + ":" + m + ":" + s
            # set the new timer label
            self.t.set(self.d)
            # set the amount of time in millisecond to delay this function to run, 1000 millisecond = 1 second
            if count == 0:
                self.controller.after(1000, self.timer)

            # set the limit of time here
            if self.d == time_set:
                # stop the time
                self.pause()
                # pop up the message
                # msg = "Take a break!" time_set_label.get()
                msg = f"Time's up!"
                tk.messagebox.showinfo(title="Alarm", message=msg)

    def b1_correct_label(self):
        """
        Change the name of the button 1 along how it named in the timer list
        :return:
        """
        # correct the label
        self.work_button.config(text= str(self.controller.SomeVar))
        #w = self.controller.SomeVar
        custom["button_1"] = self.controller.SomeVar

    def b2_correct_label(self):
        """
        Change the name of the button 2 along how it named in the timer list
        :return:
        """
        # correct the label
        self.slack_button.config(text= str(self.controller.SomeVar))
        #s = self.controller.SomeVar
        custom["button_2"] = self.controller.SomeVar
        #print(self.s)

    def switch(self):
        """
        This is to help the user to not click other button while other function is activating
        It makes most of the button not clickable once they are click
        Stop button is clickable once the above condition is apply
        :return:
        """
        # for work button 1
        if self.work_button["state"] == "normal":
            self.work_button["state"] = "disabled"
            self.stop_button["state"] = "active"
            self.stop_button["text"] = "Stop"
            self.window_custom["state"] = "disable"
            self.pause_button["state"] = "normal"
            #self.resume_button["state"] = "normal"

            # self.window_report["state"] = "disable"
        else:
            self.work_button["state"] = "normal"
            self.stop_button["state"] = "disabled"
            self.stop_button["text"] = "Stop"
            self.window_custom["state"] = "active"
            # self.window_report["state"] = "active"

        # for slack button 2
        if self.slack_button["state"] == "normal":
            self.slack_button["state"] = "disabled"
            self.stop_button["state"] = "active"
            self.stop_button["text"] = "Stop"
            self.pause_button["state"] = "active"
        else:
            self.slack_button["state"] = "normal"
            self.stop_button["state"] = "disabled"
            self.stop_button["text"] = "Stop"

    def switch_2(self):
        """
        This is to help the user to not click other button while other function is activating
        It makes most of the button not clickable once they are click
        Stop button is clickable once the above condition is apply
        :return:
        """

        # for resume button
        if self.pause_button["state"] == "normal":
            self.pause_button["state"] = "disable"
            self.resume_button["state"] = "active"

        if self.resume_button["state"] == "normal":
            self.pause_button["state"] = "normal"
            self.resume_button["state"] = "disable"

    def test_add_time_list(self):
        time_hold_work.append("00:30:00")
        #time_hold_slack.append("01:00:00")
        print(time_hold_work)
        #print(time_hold_slack)


class Customization(tk.Frame):
    def __init__(self, parent, controller):
        """
        The Customization page for Timer Class
        :param parent: The Timer container
        :param controller: The Timer class/controller
        """
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Customize")
        self.label.grid(row=0, column=1)
        # navigate back to Main Page
        self.window_1 = tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame(MainPage))
        self.window_1.grid(row=1, column=0, pady=10, padx=10)

        # default label start to let user knows the label button will always be Start: {user_name_choice}
        self.label = tk.Label(self, text="Start: ")
        self.label.grid(row=2, column=0)

        # text box
        self.text_box = tk.Entry(self, bd=5, font=("Times New Roman", 14), width=25)
        self.text_box.grid(row=2, column=1, pady=10, padx=10)

        # self.text_box = tk.Entry(self, bd=5, font=("Times New Roman", 14), width=25)
        # self.text_box.grid(row=7, column=1, pady=10, padx=10)

        self.label_time_limit = tk.Label(self, textvariable=time_set_label, font=("Arial", 25))
        self.label_time_limit.grid(row=1, column= 1)

        self.work_button = tk.Button(self, text=f"Save button 1", width=10, height=2,
                                     command=lambda: self.w_go_to_page_one())
        self.work_button.grid(row=1, column=2, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"Save button 2", width=10, height=2,
                                     command=lambda: self.s_go_to_page_one())
        self.slack_button.grid(row=2, column=2, pady=10, padx=10)

        # instruction labels for name changing
        self.label = tk.Label(self, text="Enter new name to rename the button(s).")
        self.label.grid(row=3, column=1)
        self.label = tk.Label(self, text="Hit save depend on the button you want to change.")
        self.label.grid(row=4, column=1)

        # instruction labels for time changing
        self.label = tk.Label(self, text="Choose the time that you want to be notify below:")
        self.label.grid(row=5, column=1)

        self.slack_button = tk.Button(self, text=f"10 minutes", width=10, height=2,
                                     command=lambda: self.time_set_10_minutes())
        self.slack_button.grid(row=6, column=0, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"15 minutes", width=10, height=2,
                                     command=lambda: self.time_set_15_minutes())
        self.slack_button.grid(row=7, column=0, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"30 minutes", width=10, height=2,
                                     command=lambda: self.time_set_thirty_m())
        self.slack_button.grid(row=6, column=1, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"45 minutes", width=10, height=2,
                                     command=lambda: self.time_set_fourty_five_m())
        self.slack_button.grid(row=6, column=2, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"20 minutes", width=10, height=2,
                                     command=lambda: self.time_set_twenty_m())
        self.slack_button.grid(row=7, column=1, pady=10, padx=10)

        self.slack_button = tk.Button(self, text=f"1 hours", width=10, height=2,
                                     command=lambda: self.time_set_one_hour())
        self.slack_button.grid(row=7, column=2, pady=10, padx=10)


    def w_go_to_page_one(self):
        """
        Store the input from textbox, saving it to button 1, and send user to the main page
        :return:
        """
        self.controller.SomeVar = self.text_box.get()  # save text from entry to some var
        self.controller.frames[MainPage].b1_correct_label()  # call correct_label function
        self.controller.show_frame(MainPage)  # show page one

    def s_go_to_page_one(self):
        """
        Store the input from textbox, saving it to button 2, and send user to the main page
        :return:
        """
        self.controller.SomeVar = self.text_box.get()  # save text from entry to some var
        self.controller.frames[MainPage].b2_correct_label()  # call correct_label function
        self.controller.show_frame(MainPage)  # show page one

    def time_set_10_minutes(self):
        global time_set
        global time_set_label
        time_set = "00:10:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var
        # self.controller.frames[MainPage].time_correct_label()  # call correct_label function
        # self.controller.show_frame(MainPage)  # show page one

    def time_set_15_minutes(self):
        global time_set
        global time_set_label
        time_set = "00:15:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var


    def time_set_twenty_m(self):
        global time_set
        global time_set_label
        time_set = "00:20:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var

    def time_set_thirty_m(self):
        global time_set
        global time_set_label
        time_set = "00:30:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var

    def time_set_fourty_five_m(self):
        global time_set
        global time_set_label
        time_set = "00:45:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var

    def time_set_one_hour(self):
        global time_set
        global time_set_label
        time_set = "01:00:00"
        # display the correct label for time limit
        time_set_label.set(time_set)

        self.controller.SomeVar = time_set_label.get()  # save text from entry to some var


class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        """
        The Report Page for Timer Class
        :param parent: The Timer container
        :param controller: The Timer class/controller
        """
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Report Page")
        #label.grid(row=0, column=1, pady=10, padx=10)
        self.label.place(x=200, y=10)
        # navigate back to Main Page
        self.window_1 = tk.Button(self, text="Back to Home", command=lambda: self.controller.show_frame(MainPage))
        self.window_1.grid(row=1, column=0, pady=10, padx=10)

        # report
        self.button_sort = tk.Button(self, text="Sort", command=lambda: self.sort_time_table())
        self.button_sort.grid(row=2, column=0, pady=10, padx=10)

        # pdf function here
        # uncomment & import/install pdf to use
        self.button_report = tk.Button(self, text="Report", command=lambda: self.pdf_not_support())
        self.button_report.grid(row=3, column=0, pady=10, padx=10)

        #self.button_report['state'] = 'disabled'

    def pdf_not_support(self):
        tk.messagebox.showinfo("Save to pdf", "This function is currently disabled, enable it in code")

    def sort_time_table(self):
        """
        sort both timer button 1 & 2, show it, and make report button clickable
        :return:
        """
        #print(f"{custom['button_1']}: {time_hold_work}")
        #print(f"{custom['button_2']}: {time_hold_slack}")
        try:
            self.sort_time_work()
            self.sort_time_slack()
            self.controller.frames[MainPage].update_table()
            self.button_report_on()
        except:
            raise ValueError

    def sort_time_work(self):
        """
        Add the button 1 timer list together
        :return:
        """
        global time_hold_work
        h_result = 0
        m_result = 0
        s_result = 0

        # going through each time
        for i in time_hold_work:
            #print("Item is", i)
            # parse the time
            h, m, s = map(int, i.split(":"))
            h_result = int(h_result) + h
            m_result = int(m_result) + m
            s_result = int(s_result) + s

            if h_result < 10:
                h_result = str(0) + str(h_result)
            else:
                h_result = str(h_result)
            if m_result < 10:
                m_result = str(0) + str(m_result)
            else:
                m_result = str(m_result)
            if s_result < 10:
                s_result = str(0) + str(s_result)
            else:
                s_result = str(s_result)

            # if more than 60m convert to hour
            if int(m_result) > 59:
                m_result = int(m_result)
                m_result -= 60
                print(m_result)
                h_result = int(h_result)
                h_result += 1

        time_hold_work = [str(h_result) + ":" + str(m_result) + ":" + str(s_result)]
        return time_hold_work

    def sort_time_slack(self):
        """
        Add the button 2 timer list together
        :return:
        """
        global time_hold_slack
        h_result = 0
        m_result = 0
        s_result = 0
        # going through each time
        for i in time_hold_slack:
            #print("Item is", i)
            # parse the time
            h, m, s = map(int, i.split(":"))
            h_result = int(h_result) + h
            m_result = int(m_result) + m
            s_result = int(s_result) + s

            if h_result < 10:
                h_result = str(0) + str(h_result)
            else:
                h_result = str(h_result)
            if m_result < 10:
                m_result = str(0) + str(m_result)
            else:
                m_result = str(m_result)
            if s_result < 10:
                s_result = str(0) + str(s_result)
            else:
                s_result = str(s_result)
            #print(type(s_result))
            #print(type(s))
            # print("h", h_result)
            # print("m", m_result)
            # print("s", s_result)
        time_hold_slack = [str(h_result) + ":" + str(m_result) + ":" + str(s_result)]
        return time_hold_slack

    def show_pdf(self):
        """
        Save time list to pdf. Disabled by default
        :return:
        """
        global listbox
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i in time_hold_work:
            pdf.write(5, custom["button_1"] + " " + str(i))
            pdf.ln()
            for j in time_hold_slack:
                pdf.write(5, custom["button_2"] + " " + str(j))
            today = date.today()
            pdf.output(f'{today}.pdf')

    def button_report_on(self):
        """
        Make report button clickable
        :return:
        """
        self.button_report['state'] = 'normal'


if __name__ == '__main__':
    #root = tk
    #root.title("TAAA")
    timer = Timer()
    timer.mainloop()