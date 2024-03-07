from datetime import datetime
from requests import Session

class Request_handler:
    dates = []

    def __init__(self, session: Session):
        self.session = session

    def request_wfh(self):
        self.dates = self.get_dates()
        url = f'https://system.citrushr.com/LocationBooking/CreateHome?userId={self.session.headers.get('user_id')}'
        
        for date in self.dates:
            payload = {
                'Startdate': date,
                'StartPoint': 'StartOfDay',
                'StartDateHours': '',
                'EndDate': date,
                'EndPoint': 'EndOfDay',
                'EndDateHours': '',
                'SingleDayPeriod': 'AllDay',
                'SingleDayHours': '',
                'Details': ''
            }

            try:
                response = self.session.post(url, data=payload)

                if response.status_code == 200:
                    print('Work from home successfully requested on ', date)
            except Exception as e:
                print('Request failed with error: ', e)

    def get_dates(self):
        _dates = []
        print('Enter dates in the format YYYY-MM-DD. Type "(D)one" when finished')
        
        while True:
            date = input('Date: ')

            if date.lower() == 'done' or date.lower() == 'd':
                break

            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                if date_obj:
                    _dates.append(date)
            except ValueError:
                print('Invalid date')
            except Exception as e:
                print(e)

        return _dates