from calendar import Calendar
from tkinter import *
from tkcalendar import *
from requests import Session, exceptions

class DatePicker:

    def __init__(self, session: Session) -> None:
        self.root = Tk()
        self.root.title("citrusHR")
        self.calendar = Calendar(self.root, selectmode='day', selectmultiple=True)
        self.selected_dates = []
        self.label = Label(self.root, text = "")
        self.successful_dates = []
        self.session = session
        self.calendar.bind('<<CalendarSelected>>', self.select_date) 
        self.date_listbox = Listbox(self.root, selectmode=MULTIPLE)

    def render(self):
        self.calendar.pack(pady=20)
        
        # Pack buttons and label
        Button(self.root, text = "Request WFH", command = self.request_wfh).pack(pady = 10)
        Button(self.root, text = "Quit", command = self.quit).pack(pady = 10)
        self.label.pack(pady = 20)
        self.date_listbox.pack(pady=10)

        self.root.mainloop()
        
    def request_wfh(self):
        user_id = self.session.headers.get('user_id')
        print(f"User ID: {user_id}")
        
        cur_selection = self.date_listbox.curselection()
        print("Current selection:", cur_selection)
        
        for index in cur_selection:
            selected_date = self.date_listbox.get(index)
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

    def select_date(self, event):
        selected_date = self.calendar.selection_get().strftime("%Y-%m-%d")
        if selected_date not in self.selected_dates:
            self.selected_dates.append(selected_date)
            self.label.config(text=f"Selected dates: {', '.join(self.selected_dates)}")
            self.date_listbox.insert(END, selected_date)
        else:
            self.label.config(text=f"Date already selected: {selected_date}")
    def quit(self):
        self.root.destroy()
