import requests
import json

# 测试登录
resp = requests.post('http://localhost:8001/api/login', json={
    'username': 'admin',
    'password': 'admin123'
})
print('Login:', resp.status_code)
print(json.dumps(resp.json(), ensure_ascii=False, indent=2))