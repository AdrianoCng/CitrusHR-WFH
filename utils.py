from datetime import datetime
from bs4 import BeautifulSoup

def get_dates():
    dates = []
    print('Enter dates in the format YYY-MM-DD (type "(D)one" when finished)')

    while True:
        date = input('Date: ')

        if date.lower() == 'done' or date in ['d', 'D']:
            break

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            dates.append(date_obj.isoformat())
        except ValueError:
            print('Invalid date')

    return dates

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup
