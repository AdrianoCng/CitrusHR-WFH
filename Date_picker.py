from calendar import Calendar
from datetime import datetime, date
from tkinter import *
from tkinter.ttk import Style
from tkcalendar import *
from requests import Session, exceptions

class DatePicker:
    def __init__(self, session: Session) -> None:
        self.root = Tk()
        self.root.geometry('900x600')
        self.root.title("citrusHR")
        style = Style(self.root)
        style.theme_use('clam')

        self.calendar = Calendar(self.root, 
                                 selectmode='day', 
                                 selectmultiple=True,
                                 font="Arial 19", 
                                 showweeknumbers=False, 
                                 date_pattern='dd/MM/yyyy', 
                                 background="#353935", 
                                 normalbackground ="#353935",
                                 foreground="#F5F5F5",
                                 normalforeground="#F5F5F5",
                                 borderwidth=0, 
                                 bg_selected='red',
                                disabledforeground="red",
                                style="Custom.TCalendarDay")

        self.selected_dates = set()
        self.label = Label(self.root, text = "")
        self.successful_dates = []
        self.session = session
        self.calendar.bind('<<CalendarSelected>>', self.select_date) 

    def render(self):
        self.calendar.pack(pady=20)
        
        # Pack buttons and label
        Button(self.root, text = "Request WFH", command = self.request_wfh).pack(pady = 10)
        Button(self.root, text="Clear Selection", command=self.clear_selection).pack(pady=10)
        Button(self.root, text = "Quit", command = self.quit).pack(pady = 10)
        self.label.pack(pady = 20)
        self.root.mainloop()
        
    def request_wfh(self):
        user_id = self.session.headers.get('user_id')
        print(f"User ID: {user_id}")
        
        for selected_date in self.selected_dates:
            print(f"Selected Date: {selected_date}")
            
            url = f'https://system.citrushr.com/LocationBooking/CreateHome?userId={user_id}'
            payload = {
                'Startdate': selected_date,
                'StartPoint': 'StartOfDay',
                'StartDateHours': '',
                'EndDate': selected_date,
                'EndPoint': 'EndOfDay',
                'EndDateHours': '',
                'SingleDayPeriod': 'AllDay',
                'SingleDayHours': '',
                'Details': ''
            }

            try:
                response = self.session.post(url, data=payload)
                print(f"Response status code: {response.status_code}")  

                if response.status_code == 200:
                    self.successful_dates.append(selected_date)
            except exceptions.RequestException as e:
                self.label.config(text=f'An https error occurred. Please try again')
            except Exception as e:
                self.label.config(text=f'Request failed with error: {e}')
            
            if self.successful_dates:
                successful_dates_str = ', '.join(self.successful_dates)
                self.label.config(text=f'Work from home successfully requested on {successful_dates_str}')
                self.label.after(10000, lambda: self.clear_dates())

    def clear_dates(self):
        self.label.config(text='')
        self.successful_dates = []

    def select_date(self, event):
        selected_date = self.calendar.selection_get().strftime("%Y-%m-%d")
        selected_date_format = datetime.strptime(selected_date, "%Y-%m-%d").date()
        if selected_date in self.selected_dates:
            self.selected_dates.remove(selected_date)
            self.calendar.calevent_remove(selected_date_format)
            self.calendar.tag_delete(selected_date)
        else: 
            self.selected_dates.add(selected_date)
            self.calendar.calevent_create(selected_date_format, 'Selected already', selected_date)
            self.calendar.tag_config(selected_date, background='red', foreground='yellow')
        print(f"Selected Dates: {self.selected_dates}")

    def clear_selection(self):
        for selected_date in self.selected_dates:
            self.calendar.tag_delete(selected_date)
        self.selected_dates.clear()
        today_date = date.today() 
        self.calendar.selection_set(today_date)

    def quit(self):
        self.root.destroy()
