import json
from requests import Session
from cryptography.fernet import Fernet
from utils import parse_html
from getpass import getpass

class Login_manager:
    URL = 'https://system.citrushr.com/Login'
    ACCOUNTS_FILE_PATH = './accounts.json'
    KEY_FILE_PATH = './key.key'
    logged_in = False
    user_id = ''
    is_saved_account = False

    def __init__(self, session: Session):
        self.session = session
        self.fernet = Fernet(self.load_key())

    def login(self):
        while not self.logged_in:
            try:
                username, password = self.get_credentials()
                request_verification_token = self.get_verification_token()
                
                data = {
                    'Username': username,
                    'Password': password,
                    '__RequestVerificationToken': request_verification_token
                }

                self.session.post(self.URL, data)

                # Successfully Login
                if 'HrCogAuth' in self.session.cookies.keys():
                    self.user_id = self.get_user_id()
                    self.session.headers.update({'user_id': self.user_id})
                    self.logged_in = True
                    print('Login successful')

                    if not self.is_saved_account:
                        self.save_credentials(username, password)
                else:
                    print('Email or password incorrect. Please try again')
            except ValueError as e:
                print('Login Failed: ', e)
                exit()

    def get_credentials(self):
        username = input('Enter username: ')
        saved_password = self.get_saved_password(username)

        if saved_password:
            print('Account found')
            self.is_saved_account = True
            return username, saved_password

        password = getpass('Enter password: ')
        return username, password
    
    def save_credentials(self, username: str, password: str):
        preference = input('Do you want to save this credentials? (y/n): ')
        if preference.lower() == 'y':
            encrypted_password = self.fernet.encrypt(password.encode()).decode()
            credentials = {
                'username': username,
                'password': encrypted_password
            }

            try:
                with open(self.ACCOUNTS_FILE_PATH, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            data.append(credentials)

            with open(self.ACCOUNTS_FILE_PATH, 'w') as file:
                json.dump(data, file)
            print('Credentials saved successfully')

    def get_verification_token(self):
        html = self.session.get(self.URL).text
        soup = parse_html(html)
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        return token
                    
    def get_user_id(self):
        dashboard_url = 'https://system.citrushr.com/Dashboard/Index'
        html = self.session.get(dashboard_url).text
        soup = parse_html(html)
        user_id = soup.find('body')['data-uid']
        return user_id
    
    def load_key(self):
        try:
            with open(self.KEY_FILE_PATH, 'rb') as file:
                key = file.read()
        except FileNotFoundError:
            with open(self.KEY_FILE_PATH, 'wb') as file:
                key = Fernet.generate_key()
                file.write(key)

        return key

    def get_saved_password(self, username: str):
        try:
            with open(self.ACCOUNTS_FILE_PATH, 'r') as file:
                data = json.load(file)
                for account in data:
                    if 'username' not in account or account['username'] != username:
                        continue

                    password = self.fernet.decrypt(account['password'].encode()).decode()

                    return password
        except FileNotFoundError:
            pass
    
        return None
