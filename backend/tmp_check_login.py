import http.client
import json

paths = ['/', '/api/auth/login']
for path in paths:
    try:
        conn = http.client.HTTPConnection('localhost', 8000, timeout=5)
        if path == '/api/auth/login':
            body = json.dumps({'username': 'test', 'password': 'test'})
            conn.request('POST', path, body, {'Content-Type': 'application/json'})
        else:
            conn.request('GET', path)
        r = conn.getresponse()
        print(path, r.status, r.reason)
        print(r.read().decode('utf-8'))
    except Exception as e:
        print('ERROR', path, e)
