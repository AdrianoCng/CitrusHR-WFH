from requests import Session
from Login_manager import Login_manager
from Request_handler import Request_handler

def main():
    session = Session()
    login_manager = Login_manager(session)
    request_handler = Request_handler(session)

    login_manager.login()
    request_handler.request_wfh()

if __name__ == '__main__':
    main()