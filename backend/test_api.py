import subprocess
import sys
import time
import requests
import json

# 启动服务器
proc = subprocess.Popen([sys.executable, "main.py"], cwd="C:/Users/25771/Desktop/marriage-registration/backend")
time.sleep(3)

try:
    # 测试登录
    resp = requests.post('http://localhost:8001/api/login', json={
        'username': 'admin',
        'password': 'admin123'
    }, timeout=10)
    print('Login status:', resp.status_code)
    data = resp.json()
    print('Login response:', json.dumps(data, ensure_ascii=False, indent=2))
    
    # 测试获取菜单
    resp2 = requests.get('http://localhost:8001/api/menus', timeout=10)
    print('\nMenus status:', resp2.status_code)
    print('Menus:', json.dumps(resp2.json(), ensure_ascii=False, indent=2))
    
    # 测试角色列表
    resp3 = requests.get('http://localhost:8001/api/roles', timeout=10)
    print('\nRoles status:', resp3.status_code)
    print('Roles:', json.dumps(resp3.json(), ensure_ascii=False, indent=2))
    
except Exception as e:
    print('Error:', e)
finally:
    proc.terminate()
    proc.wait()