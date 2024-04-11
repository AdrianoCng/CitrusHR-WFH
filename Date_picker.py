from tkinter import *
from tkcalendar import *
from requests import Session, exceptions

class DatePicker:

    def __init__(self, session: Session) -> None:
        self.root = Tk()
        self.root.title("citrusHR")
        self.calendar = Calendar(self.root, selectmode='day')
        self.label = Label(self.root, text = "")
        self.session = session

    def render(self):
        self.calendar.pack(pady=20)
        
        # Pack buttons and label
        Button(self.root, text = "Request WFH", command = self.request_wfh).pack(pady = 10)
        Button(self.root, text = "Quit", command = self.quit).pack(pady = 10)
        self.label.pack(pady = 20)

        # Execute Tkinter
        self.root.mainloop()
        
    def request_wfh(self):
        url = f'https://system.citrushr.com/LocationBooking/CreateHome?userId={self.session.headers.get('user_id')}'
        selected_date = self.calendar.selection_get().strftime("%Y-%m-%d")

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

            if response.status_code == 200:
                self.label.config(text=f'Work from home successfully request on {selected_date}')
        except exceptions.RequestException as e:
            self.label.config(text=f'An https error occurred. Please try again')
        except Exception as e:
            self.label.config(text=f'Request failed with error: {e}')

    def quit(self):
        self.root.destroy()
        
