import dropbox

app_key = 'zqjc4ggntvp0k2r'
app_secret = 'eyy060u2uifbv4e'

auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = auth_flow.start()

# Print the authorize_url and visit it in your browser
print("Please visit this website and authorize the application:")
print(authorize_url)

# After authorizing, enter the code from the redirect URL
auth_code = input("Enter the authorization code: ")

# Exchange the authorization code for an access token
auth_result = auth_flow.finish(auth_code)

# Retrieve the access token from the auth_result object
access_token = auth_result.access_token

# Print the access token
print("Access token:", access_token)