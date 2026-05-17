import http.client
import json

conn = http.client.HTTPConnection('localhost', 8000, timeout=5)
body = json.dumps({'username': 'login_test_user', 'email': 'login_test@example.com', 'password': 'TestPass123'})
conn.request('POST', '/api/auth/register', body, {'Content-Type': 'application/json'})
r = conn.getresponse()
print('register', r.status, r.reason)
print(r.read().decode('utf-8'))

conn = http.client.HTTPConnection('localhost', 8000, timeout=5)
body = json.dumps({'username': 'login_test_user', 'password': 'TestPass123'})
conn.request('POST', '/api/auth/login', body, {'Content-Type': 'application/json'})
r = conn.getresponse()
print('login', r.status, r.reason)
print(r.read().decode('utf-8'))
