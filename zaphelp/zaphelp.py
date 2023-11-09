#!/usr/bin/env python
import time
import urllib.parse
from zapv2 import ZAPv2

context_id = 1
apikey = 'crbrnoifkcppdm27gncvh7atvs'
context_name = 'Default Context'
target_url = 'https://1ebff3fe-7154-4945-97ff-5fff580ba50d.idocker.vuln.land/'

zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

def set_include_in_context():
    include_url = target_url + '.*'
    exclude_url = target_url + 'logout'
    zap.context.include_in_context(context_name, include_url)
    zap.context.exclude_from_context(context_name, exclude_url)
    print('Configured include and exclude regex(s) in context')

def set_logged_in_indicator():
    logged_in_regex = '\Q<a href="logout">Logout</a>\E'
    zap.authentication.set_logged_in_indicator(context_id, logged_in_regex)
    print('Configured logged in indicator regex: ')

def set_form_based_auth():
    login_url = target_url + 'login'
    login_request_data = 'email={%username%}&password={%password%}'
    encoded_login_request_data = urllib.parse.quote(login_request_data)
    form_based_config = 'loginUrl=' + urllib.parse.quote(login_url) + '&loginRequestData=' + encoded_login_request_data
    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', form_based_config)
    print('Configured form based authentication')

def set_user_auth_config():
    user = 'Test User'
    username = 'corwin.louisa@example.com'
    password = 'user1234'
    user_id = zap.users.new_user(context_id, user)
    user_auth_config = 'email=' + urllib.parse.quote(username) + '&password=' + urllib.parse.quote(password)
    zap.users.set_authentication_credentials(context_id, user_id, user_auth_config)
    zap.users.set_user_enabled(context_id, user_id, 'true')
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled('true')
    print('User Auth Configured')
    return user_id

def start_spider(user_id):
    print('Starting Spider as User with ID:', user_id)
    scan_id = zap.spider.scan_as_user(context_id, user_id, target_url, recurse='true')
    return scan_id

def wait_for_scan_to_complete(scan_id):
    while True:
        try:
            progress = int(zap.spider.status(scan_id))
            print('Spider scan progress: {}%'.format(progress))
            if progress >= 100:
                break
            time.sleep(5)
        except ValueError as e:
            print(f"Error reading spider status: {e}")
            break
    print('Spider scan completed!')

def start_active_scan(user_id):
    print('Starting Active Scan as User with ID:', user_id)
    scan_id = zap.ascan.scan_as_user(target_url, context_id, user_id, recurse=True, scanpolicyname='Default Policy')
    return scan_id

def wait_for_active_scan_to_complete(scan_id):
    while True:
        try:
            progress = int(zap.ascan.status(scan_id))
            print('Active Scan progress: {}%'.format(progress))
            if progress >= 100:
                break
            time.sleep(10)
        except ValueError as e:
            print(f"Error reading active scan status: {e}")
            break
    print('Active Scan completed!')

def get_spider_results(scan_id):
    spider_results = zap.spider.results(scan_id)
    print('Spider results found the following URLs:')
    for result in spider_results:
        print(result)

def generate_html_report():
    report = zap.core.htmlreport(apikey=apikey)
    report_file = 'zap_report.html'
    with open(report_file, 'w') as file:
        file.write(report)
    print('HTML report generated: {}'.format(report_file))

# Setup ZAP context and authentication
set_include_in_context()
set_logged_in_indicator()
set_form_based_auth()

# Configure user and start spider
user_id = set_user_auth_config()
spider_scan_id = start_spider(user_id)
wait_for_scan_to_complete(spider_scan_id)

# Start the active scanner
active_scan_id = start_active_scan(user_id)
wait_for_active_scan_to_complete(active_scan_id)

# Get the results
get_spider_results(spider_scan_id)

# Generate the report
generate_html_report()
