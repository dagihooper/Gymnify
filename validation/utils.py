import requests
from django.shortcuts import render, redirect

def send_verification_code():
  
    session = requests.Session()
    base_url = 'https://api.afromessage.com/api/challenge'
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoidkc4ZUZacm55eW1xbDVMQ3VSVEZwRmlRZUxhNmhxVnoiLCJleHAiOjE5MTAwMTI4NTUsImlhdCI6MTc1MjI0NjQ1NSwianRpIjoiN2ZkZmUyZWMtMGUwYS00YTNiLWIyNjgtYTYzZDk1NmE1YWU4In0.cx3izFES9LXG_LfSOf0jCa0USP9zl1iacbrAL29Sr44'
    headers = {'Authorization': 'Bearer ' + token}
    callback = 'validation'
    from_id = 'e80ad9d8-adf3-463f-80f4-7c4b39f7f164'
    sender = ''
    recipient = '+251963719303'  
    prefix = f"Here is your verification code from Gymnify:"
    postfix = "Don't share your code with anyone."
    sb = 2  
    sa = 2  
    ttl = 1000
    code_length = 5
    code_type = 0  

      
    url = (
          f"{base_url}?from={from_id}&sender={sender}&to={recipient}"
          f"&pr={prefix}&ps={postfix}&callback={callback}&sb={sb}&sa={sa}"
          f"&ttl={ttl}&len={code_length}&t={code_type}"
      )

    result = session.get(url, headers=headers)

    if result.status_code == 200:
        response_json = result.json()
        if response_json.get('acknowledge') == 'success':
            print('API success')
            print('Response:', response_json)
            return {'status': 'success', 'redirect': 'validation'}
        else:
            print('API error:', response_json.get('response'))
            return {'status': 'error', 'message': response_json.get('response')}
    else:
        print(f'HTTP error ... code: {result.status_code}, msg: {result.text}')
        return {'status': 'http_error', 'code': result.status_code, 'message': result.text}