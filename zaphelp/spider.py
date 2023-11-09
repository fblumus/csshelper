#!/usr/bin/env python
import time
from zapv2 import ZAPv2


max_duration = 120  # Maximale Dauer in Sekunden
start_time = time.time()


# API key for ZAP instance
apikey = "crbrnoifkcppdm27gncvh7atvs"

# ZAP Proxy Configuration
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# The target URL
target_url = 'https://5ab2cfa9-6dfa-416e-ac16-421ab2226e96.idocker.vuln.land/login'

# Authentication and context configuration
context_name = 'auth_context'
login_url = target_url + 'login'
email_parameter = 'email'  # Use 'email' instead of 'username' as per your specifications
password_parameter = 'password'
logged_in_indicator = '.*Logout.*'  # Adjust to the application's logout regex pattern
logged_out_indicator = '.*Login.*'  # Adjust to the application's login regex pattern

# Credentials (replace with the actual credentials)
email = 'sadie.isobel@example.com'
password = 'reviewer1234'

# Function to start spidering
def start_spider():
    print('Starting Spider for target URL:', target_url)
    scan_id = zap.spider.scan(target_url)
    return scan_id

# Function to monitor the spidering process
def wait_for_scan_to_complete(scan_id):
    while True:
        time.sleep(5)
        progress = int(zap.spider.status(scan_id))
        print('Spider scan progress: {}%'.format(progress))
        if progress >= 100:
            break
    print('Spider scan completed!')

# Function to retrieve spider results
def get_spider_results(scan_id):
    spider_results = zap.spider.results(scan_id)
    print('Spider results found the following URLs:')
    for result in spider_results:
        print(result)

# Function to generate an HTML report
def generate_html_report():
    report = zap.core.htmlreport()
    report_file = 'zap_report.html'
    with open(report_file, 'w') as file:
        file.write(report)
    print('HTML report generated: {}'.format(report_file))

# Function to setup authentication
def setup_authentication():
    context_id = zap.context.new_context(context_name)
    zap.context.include_in_context(context_name, target_url + '.*')
    zap.context.exclude_from_context(context_name, target_url + 'logout')

    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', 'loginUrl=' + login_url + '&loginRequestData=' + email_parameter + '={%email%}&' + password_parameter + '={%password%}')
    zap.authentication.set_logged_in_indicator(context_id, logged_in_indicator)
    zap.authentication.set_logged_out_indicator(context_id, logged_out_indicator)
    
    user_id = zap.users.new_user(context_id, 'exampleUser')
    zap.users.set_authentication_credentials(context_id, user_id, email_parameter + '=' + email + '&' + password_parameter + '=' + password)
    zap.users.set_user_enabled(context_id, user_id, True)
    
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled(True)
    
    return context_id, user_id

# Function to start spidering as an authenticated user
def start_authenticated_spider(context_id, user_id):
    print('Starting Authenticated Spider for target URL:', target_url)
    scan_id = zap.spider.scan_as_user(context_id, user_id, target_url, recurse=True)
    return scan_id


def start_authenticated_active_scan(context_id, user_id):
    print('Starting Authenticated Active Scan for target URL:', target_url)
    scan_id = zap.ascan.scan_as_user(target_url, context_id, user_id, recurse=True)
    return scan_id


# Run the spider without authentication
print("Running spider without authentication...")
spider_scan_id = start_spider()
wait_for_scan_to_complete(spider_scan_id)
get_spider_results(spider_scan_id)

# Setup authentication and run the spider with authentication
context_id, user_id = setup_authentication()
print("Running spider with authentication...")
auth_spider_scan_id = start_authenticated_spider(context_id, user_id)
wait_for_scan_to_complete(auth_spider_scan_id)
get_spider_results(auth_spider_scan_id)

# Run the authenticated active scan
print("Running authenticated active scan...")
active_scan_id = start_authenticated_active_scan(context_id, user_id)
wait_for_scan_to_complete(active_scan_id)  # You can reuse this function if it's suitable for active scans too

# Generate the final report
generate_html_report()


