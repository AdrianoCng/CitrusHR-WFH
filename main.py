from requests import Session
from Login_manager import Login_manager
from Date_picker import DatePicker

def main():
    session = Session()
    login_manager = Login_manager(session)

    login_manager.login()

    if login_manager.logged_in:
        date_picker = DatePicker(session)
        date_picker.render()

if __name__ == '__main__':
    main()