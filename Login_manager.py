import json
from requests import Session
from utils import parse_html
from getpass import getpass

class Login_manager:
    url = 'https://system.citrushr.com/Login'
    accounts_file_path = './accounts.json'
    logged_in = False
    user_id = ''
    is_saved_account = False

    def __init__(self, session: Session):
        self.session = session

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

                self.session.post(self.url, data)

                if 'HrCogAuth' in self.session.cookies.keys():
                    self.user_id = self.get_user_id()
                    self.session.headers.update({'user_id': self.user_id})
                    self.logged_in = True

                    if not self.is_saved_account:
                        self.save_credentials(username, password)

                    print('Login successful')
                else:
                    print('Email or password incorrect. Please try again')
            except ValueError as e:
                print('Login Failed: ', e)
                exit()

    def get_credentials(self):
        username = input('Enter username: ')
        try:
            with open(self.accounts_file_path, 'r') as file:
                accounts = json.load(file)
                for account in accounts:
                    if 'username' not in account or account['username'] != username:
                        continue
                    
                    print('Account found')
                    self.is_saved_account = True
                    password = account['password']

                    return username, password
        except FileNotFoundError:
            pass

        password = getpass('Enter password: ')
        return username, password

    def get_verification_token(self):
        html = self.session.get(self.url).text
        soup = parse_html(html)
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        return token
                    
    def get_user_id(self):
        dashboard_url = 'https://system.citrushr.com/Dashboard/Index'
        html = self.session.get(dashboard_url).text
        soup = parse_html(html)
        user_id = soup.find('body')['data-uid']
        return user_id
    
    def save_credentials(self, username, password):            
        credentials = {
            'username': username,
            'password': password
        }
        
        preference = input('Do you want to save this credentials? (y/n): ')
        if preference.lower() == 'y':
            try:
                with open(self.accounts_file_path, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            data.append(credentials)

            with open(self.accounts_file_path, 'w') as file:
                json.dump(data, file)
            print('Credentials saved successfully')


