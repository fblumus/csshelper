zap-cli context create 'mycontext'
zap-cli context include 'mycontext' 'https://66e9595b-5ed2-4a4b-b6f9-eac223198c3f.idocker.vuln.land/.*'
zap-cli context exclude 'mycontext' 'https://66e9595b-5ed2-4a4b-b6f9-eac223198c3f.idocker.vuln.land/logout'
zap-cli users create 'mycontext' 'corwin.louisa@example.com' 'user1234'
zap-cli users set-auth-url 'mycontext' 'corwin.louisa@example.com' 'https://66e9595b-5ed2-4a4b-b6f9-eac223198c3f.idocker.vuln.land/login' 'POST' 'username=corwin.louisa%40example.com&password=user1234'
zap-cli users set-auth-method 'mycontext' 'corwin.louisa@example.com' 'form-based' 'loginUrl=https://66e9595b-5ed2-4a4b-b6f9-eac223198c3f.idocker.vuln.land/login&loginRequestData=username%3D%7B%25username%25%7D%26password%3D%7B%25password%25%7D'
zap-cli users set-auth-credentials 'mycontext' 'corwin.louisa@example.com' 'username=corwin.louisa@example.com&password=user1234'
