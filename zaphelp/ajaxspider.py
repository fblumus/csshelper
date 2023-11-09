#!/usr/bin/env python
import time
from zapv2 import ZAPv2

apikey = "crbrnoifkcppdm27gncvh7atvs"

# ZAP Proxy Configuration
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# The target URL
target= 'https://5ab2cfa9-6dfa-416e-ac16-421ab2226e96.idocker.vuln.land/login'

# Authentication and context configuration
context_name = 'auth_context'
login_url = target + 'login'
email_parameter = 'email'  # Use 'email' instead of 'username' as per your specifications
password_parameter = 'password'
logged_in_indicator = '.*Logout.*'  # Adjust to the application's logout regex pattern
logged_out_indicator = '.*Login.*'  # Adjust to the application's login regex pattern

# Credentials (replace with the actual credentials)
email = 'sadie.isobel@example.com'
password = 'reviewer1234'


def ajax_spider_scan_without_auth():
    print('Starting Ajax Spider scan without authentication.')
    zap.ajaxSpider.set_option_max_duration('1') # Limit the scan to 1 minute for example
    scan_id = zap.ajaxSpider.scan(target)
    
    timeout = time.time() + 60 * 2  # 2 minutes timeout
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            print('Ajax Spider scan timed out after 2 minutes.')
            break
        print('Ajax Spider status: ' + zap.ajaxSpider.status)
        time.sleep(2)
    
    print('Ajax Spider scan without authentication completed.')

def ajax_spider_scan_with_auth(context_id, user_id):
    print(f'Starting Ajax Spider scan with authentication for user_id: {user_id}')
    zap.ajaxSpider.set_option_max_duration('1') # Limit the scan to 1 minute for example

    # Set the user for the context
    zap.context.set_context_in_scope(context_id, True)
    zap.users.set_user_enabled(context_id, user_id, True)
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled(True)

    # Now start the Ajax Spider using the authenticated context
    scan_id = zap.ajaxSpider.scan_as_user(context_id, user_id, target, subtreeonly=False)

    timeout = time.time() + 60 * 2  # 2 minutes timeout
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            print('Ajax Spider scan with authentication timed out after 2 minutes.')
            break
        print('Ajax Spider status: ' + zap.ajaxSpider.status)
        time.sleep(2)

    zap.forcedUser.set_forced_user_mode_enabled(False)
    print('Ajax Spider scan with authentication completed.')


# Function to setup authentication
def setup_authentication():
    context_id = zap.context.new_context(context_name)
    zap.context.include_in_context(context_name, target + '.*')
    zap.context.exclude_from_context(context_name, target + 'logout')

    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', 'loginUrl=' + login_url + '&loginRequestData=' + email_parameter + '={%email%}&' + password_parameter + '={%password%}')
    zap.authentication.set_logged_in_indicator(context_id, logged_in_indicator)
    zap.authentication.set_logged_out_indicator(context_id, logged_out_indicator)
    
    user_id = zap.users.new_user(context_id, 'exampleUser')
    zap.users.set_authentication_credentials(context_id, user_id, email_parameter + '=' + email + '&' + password_parameter + '=' + password)
    zap.users.set_user_enabled(context_id, user_id, True)
    
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled(True)
    
    return context_id, user_id

# Function to generate an HTML report
def generate_html_report():
    report = zap.core.htmlreport()
    report_file = 'zap_report.html'
    with open(report_file, 'w') as file:
        file.write(report)
    print('HTML report generated: {}'.format(report_file))


#scan ohne auth.


#scan with auth.

if __name__ == '__main__':
    # Run Ajax Spider without authentication
    ajax_spider_scan_without_auth()
    
    # Setup authentication
    context_id, user_id = setup_authentication()
    
    # Run Ajax Spider with authentication
    ajax_spider_scan_with_auth(context_id, user_id)
    
    # Placeholder for authenticated attack scan
    # We will add this later after testing the Ajax Spider scans
    # ...

    # ...

    # Generate the final report
    generate_html_report()