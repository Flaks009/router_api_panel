import json
import requests
import netifaces

gws = netifaces.gateways()
gws = gws['default'][2][0]
BASE_URL = 'https://{}/cgi-bin'.format(gws)

API = {
    'apply': BASE_URL+'/api/v3/system/apply',
    'login': BASE_URL+'/api/v3/system/login',
    'service_led': BASE_URL+'/api/v3/service/leds',
    'service_ssh': BASE_URL+'/api/v3/service/ssh',
    'reboot':BASE_URL+'/api/v3/system/reboot'
    }
headers = {'content-type': 'application/json'}


def auth(username, password):
    data = {'data': {'username': username, 'password': password}}
    response = requests.post(API['login'], data=json.dumps(data), headers=headers, verify=False)
    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))['data']['Token']
        headers['Authorization'] = 'Bauer ' + token
        return True

    return False


def apply():
    response = requests.post(API['apply'], headers=headers, verify=False)
    result = json.loads(response.content.decode('utf-8'))
    if result['data']['sucess']:
        return result['data']['config_hash']

    return False


def change_led_color(color):
    response = requests.get(API['service_led'], headers=headers, verify=False)
    led_options = json.loads(response.content.decode('utf-8'))
    if color == 'off':
        led_options['data']['action']['value'] = 'off'
    else:
        led_options['data']['color']['value'] = color

    requests.put(API['service_led'], data=json.dumps(led_options), headers=headers, verify=False)


def ssh_config(enabled=True, port=22, wan_access=True):
    data = {'data': {'enabled': enabled, 'port': port, 'wan_access': wan_access}}
    requests.put(API['service_ssh'], data=json.dumps(data), headers=headers, verify=False)

def reboot():
    requests.put(API['reboot'],headers=headers,verify=False)

'''
if auth('admin', 'admin123'):
    print('Gateway: {}'.format(gws))
    change_led_color('green')
    ssh_config()
    apply()
    reboot()
else:
    print('Username or password is invalid')
'''