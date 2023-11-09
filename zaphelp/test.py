#!/usr/bin/env python
import urllib.parse
from zapv2 import ZAPv2

context_id = 1
apikey = "crbrnoifkcppdm27gncvh7atvs"
context_name = 'auth_context'
target_url = 'https://57f106ec-f36a-43a3-8407-8290513a45f7.idocker.vuln.land/'

# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

def set_include_in_context():
    exclude_url = 'https://57f106ec-f36a-43a3-8407-8290513a45f7.idocker.vuln.land/logout'
    include_url = 'https://57f106ec-f36a-43a3-8407-8290513a45f7.idocker.vuln.land/.*'
    zap.context.include_in_context(context_name, include_url)
    zap.context.exclude_from_context(context_name, exclude_url)
    print('Configured include and exclude regex(s) in context')


def set_logged_in_indicator():
    logged_in_regex = '\Q<a href="https://57f106ec-f36a-43a3-8407-8290513a45f7.idocker.vuln.land/logout">\E'
    zap.authentication.set_logged_in_indicator(context_id, logged_in_regex)
    print('Configured logged in indicator regex: ')


def set_form_based_auth():
    login_url = 'https://57f106ec-f36a-43a3-8407-8290513a45f7.idocker.vuln.land/login'
    login_request_data = 'email={%username%}&password={%password%}'
    form_based_config = 'loginUrl=' + urllib.parse.quote(login_url) + '&loginRequestData=' + urllib.parse.quote(login_request_data)
    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', form_based_config)
    print('Configured form based authentication')


def set_user_auth_config():
    user = 'EXAM'
    username = 'corwin.louisa@example.com'
    password = '	user1234'

    user_id = zap.users.new_user(context_id, user)
    user_auth_config = 'username=' + urllib.parse.quote(username) + '&password=' + urllib.parse.quote(password)
    zap.users.set_authentication_credentials(context_id, user_id, user_auth_config)
    zap.users.set_user_enabled(context_id, user_id, 'true')
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled('true')
    print('User Auth Configured')
    return user_id


def start_spider(user_id):
    zap.spider.scan_as_user(context_id, user_id, target_url, recurse='true')
    print('Started Scanning with Authentication')


# Function to generate an HTML report
def generate_html_report():
    report = zap.core.htmlreport()
    report_file = 'zap_report.html'
    with open(report_file, 'w') as file:
        file.write(report)
    print('HTML report generated: {}'.format(report_file))

    

set_include_in_context()
set_form_based_auth()
set_logged_in_indicator()
user_id_response = set_user_auth_config()
start_spider(user_id_response)
generate_html_report()

