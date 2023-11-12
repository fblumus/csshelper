from zapv2 import ZAPv2
import urllib.parse

# API key for ZAP instance
apikey = "crbrnoifkcppdm27gncvh7atvs"

# ZAP Proxy Configuration
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# Authentication and context configuration
context_name = 'auth_context'
username_parameter = 'username'  
password_parameter = 'password'
#logged_in_indicator = '.*Logout.*'  # Adjust to the application's logout regex pattern
#logged_out_indicator = '.*Login.*'  # Adjust to the application's login regex pattern

# Credentials (replace with the actual credentials)
username = 'corwin.louisa@example.com'
password = 'user1234'

def setup_authentication(target_url, login_url):
    context_id = zap.context.new_context(context_name)
    zap.context.include_in_context(context_name, target_url + '.*')
    zap.context.exclude_from_context(context_name, target_url + 'logout')

    login_request_data = 'email={%username%}&password={%password%}' # Use 'email' instead of 'username' as per your specifications
    form_based_config = 'loginUrl=' + urllib.parse.quote(login_url) + '&loginRequestData=' + urllib.parse.quote(login_request_data)
    zap.authentication.set_authentication_method(context_id, 'formBasedAuthentication', form_based_config)
    #zap.authentication.set_logged_in_indicator(context_id, logged_in_indicator)
    #zap.authentication.set_logged_out_indicator(context_id, logged_out_indicator)
    
    user_id = zap.users.new_user(context_id, 'Auth User')
    zap.users.set_authentication_credentials(context_id, user_id, username_parameter + '=' + username + '&' + password_parameter + '=' + password)
    zap.users.set_user_enabled(context_id, user_id, True)
    
    zap.forcedUser.set_forced_user(context_id, user_id)
    zap.forcedUser.set_forced_user_mode_enabled(True)
    
    return context_id, user_id


if __name__ == '__main__':
    target_url = input("Target URL:")
    login_url = input("Login-URL:")
    context_id, user_id = setup_authentication(target_url, login_url)
    print(f'Context_id: {context_id} Context_name: {context_name}')