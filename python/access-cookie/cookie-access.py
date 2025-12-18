import requests

# Example 1: Sending cookies with a request
url_send = 'https://www.facebook.com'



# Example 2: Accessing cookies received from a server
url_receive = 'https://www.facebook.com' # A URL that sets a cookie
response_receive = requests.get(url_receive)
print(f"Cookies received from server: {response_receive.cookies.get('server_cookie')}")

# Using a session object for persistent cookies
session = requests.Session()
session.get('http://httpbin.org/cookies/set?session_cookie=persistent')
response_session = session.get('http://httpbin.org/cookies')
print(f"Cookies in session: {response_session.text}")