import time
import tkinter as tk
from tkinter import font



root = tk.Tk()





f = font.nametofont('TkMenuFont')
f['size'] = 38

class pomodor:
    def __init__(self, root, title, geometry):
        self.root = root
        self.after_id = None
        self.is_running = False
        self.current_mode = "work"
        self.title = title
        self.geometry = geometry
        self.root.title(self.title)
        self.root.geometry(self.geometry)
        self.completed_sessions = 3
        self.work_duration = 8 # 25 minutes in seconds
        self.rest_duration = 6   # 5 minutes in seconds
        self.long_rest_duration = 10  # 20 minutes in seconds
        self.work_seconds = self.work_duration
        self.rest_seconds = self.rest_duration
        self.long_rest_seconds = self.long_rest_duration
        self.configure_button = tk.Button(self.root, text="configure", width=7,height=3, command= self.configure_window)
        self.configure_button.pack()
        self.timer_label = tk.Label(self.root, text="Ready!",font=f)
        self.timer_label.pack(padx=20,pady=80)
        self.current_mode_label = tk.Label(self.root, text="Work",font=f, bg="green", fg="white")
        self.current_mode_label.pack(pady=15)
        self.start_button = tk.Button(
                    self.root,
                    text="start",
                    font=f,
                    width=25,
                    command= self.set_button,
                    )
        self.start_button.pack(
                    padx=120,)
        self.completed_sessions_label = tk.Label(self.root, text=f"Completed Sessions: {self.completed_sessions}",font=f)
        self.completed_sessions_label.pack(pady=20)
    
    def configure_window(self):
        if self.is_running:
            self.set_button()
        self.config_window = tk.Toplevel(self.root)
        self.config_window.geometry("700x400")
        self.work_timer_var = tk.StringVar(value="25")
        work_timer_label = tk.Label(self.config_window, text="work timer", font=f)
        work_timer_entry = tk.Entry(self.config_window, textvariable=self.work_timer_var, font=f)
        self.rest_timer_var = tk.StringVar(value="5")
        rest_timer_label = tk.Label(self.config_window, text="rest timer", font=f )
        rest_timer_entry = tk.Entry(self.config_window, textvariable=self.rest_timer_var,font=f, width=2)
        submit_button = tk.Button(self.config_window,text="Submit" ,font=f, command=self.save_configuration)
        work_timer_label.grid(row=0,column=0)
        work_timer_entry.grid(row=0,column=1)
        rest_timer_label.grid(row=1,column=0)
        rest_timer_entry.grid(row=1,column=1)
        submit_button.grid(row=3, column=1)
    def save_configuration(self):
        try:
            work_duration = int(self.work_timer_var.get())
            rest_duration = int(self.rest_timer_var.get())
            if work_duration <= 0 or rest_duration <= 0:
                raise ValueError("Durations must be positive integers.")
            self.work_duration = work_duration * 60
            self.rest_duration = rest_duration * 60
            self.long_rest_duration = self.rest_duration * 4
            self.work_seconds = self.work_duration
            self.rest_seconds = self.rest_duration
            self.long_rest_seconds = self.long_rest_duration
            self.update_display()
            self.config_window.destroy()
        except ValueError as e:
            print(f"Invalid input: {e}")
            
    def set_button(self):
        if self.start_button["text"] == "start":
            self.is_running = not self.is_running
            self.after_id = self.root.after(1000,self.update_timer)
            self.start_button["text"] = "pause"
        else:
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.start_button["text"] = "start"
            self.is_running = not self.is_running
        
       
    def update_timer(self):
        if self.is_running:
            #Check if the current mode is work or rest and update the timer accordingly
            if self.current_mode == "work":
                if self.work_seconds > 0:
                    self.work_seconds -= 1
                #When the work timer reaches 0, switch to rest mode
                else:
                    self.work_seconds = self.work_duration
                    self.completed_sessions += 1
                    self.completed_sessions_label.config(text=f"Completed Sessions: {self.completed_sessions}")
                    self.current_mode = "rest"
                    if self.completed_sessions % 4 == 0:
                        self.current_mode_label.config(text="Long Rest")
                    else:
                        self.current_mode_label.config(text="Rest")
            else:
                if self.completed_sessions % 4 == 0:
                    if self.long_rest_seconds > 0:
                        self.long_rest_seconds -= 1
                    else:
                        self.long_rest_seconds = self.long_rest_duration
                        self.current_mode = "work"
                        self.current_mode_label.config(text="Work")
                        
                else:
                    if self.rest_seconds > 0:
                        self.rest_seconds -= 1
                    #When the rest timer reaches 0, switch to work mode
                    else:
                        self.rest_seconds = self.rest_duration
                        self.timer_label.config(text="Work Time!")
                        self.current_mode = "work"
            self.update_display()
            self.after_id = self.root.after(1000, self.update_timer)
        
    def update_display(self):
        if self.current_mode == "work":
            remaining_seconds = self.work_seconds % 60
            remaining_minutes = self.work_seconds // 60
            self.timer_label.config(text=f"{remaining_minutes:02d} : {remaining_seconds:02d}")
        #check if the current mode is rest or longrest and update the timer
        else:
            if self.completed_sessions % 4 == 0:
                remaining_seconds = self.long_rest_seconds % 60
                remaining_minutes = self.long_rest_seconds // 60
                self.timer_label.config(text=f"{remaining_minutes:02d} : {remaining_seconds:02d}")
            else:
                remaining_seconds = self.rest_seconds % 60
                remaining_minutes = self.rest_seconds // 60
                self.timer_label.config(text=f"{remaining_minutes:02d} : {remaining_seconds:02d}")

########   
pomi = pomodor(root, "Pomodoro Timer", "600x600")
root.mainloop()
