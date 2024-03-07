from requests import Session
from utils import parse_html

class Login_manager:
    url = 'https://system.citrushr.com/Login'
    logged_in = False
    user_id = ''

    def __init__(self, session: Session):
        self.session = session

    def login(self):
        while not self.logged_in:
            try:
                username, password = self.get_credentials()

                html = self.session.get(self.url).text
                request_verification_token = self.get_verification_token(html)
                
                data = {
                    'Username': username,
                    'Password': password,
                    '__RequestVerificationToken': request_verification_token
                }

                self.session.post(self.url, data)

                if 'HrCogAuth' in self.session.cookies.keys():
                    self.logged_in = True
                    self.user_id = self.get_user_id()
                    self.session.headers.update({'user_id': self.user_id})
                    print('Login successful')
                else:
                    print('Email or password incorrect. Please try again')
            except Exception as e:
                print('Login Failed: ', e)
                exit()

    def get_credentials(self):
        username = input('Enter username: ')
        password = input('Enter password: ')
        return username, password

    def get_verification_token(self, html: str):
        soup = parse_html(html)
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        return token
                    
    def get_user_id(self):
        dashboard_url = 'https://system.citrushr.com/Dashboard/Index'
        html = self.session.get(dashboard_url).text
        soup = parse_html(html)
        user_id = soup.find('body')['data-uid']
        return user_id

