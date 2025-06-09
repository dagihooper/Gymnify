
def safe_capitalize(value, default="Guest"):
    """
    Capitalize the input string if it is not None.
    If the input is None, return the default value.
    
    Args:
        value (str or None): The string to be capitalized or None.
        default (str): The value to return if `value` is None.
        
    Returns:
        str: Capitalized string or the default value.
    """
    return value.capitalize() if isinstance(value, str) else default

import requests
from django.shortcuts import render, redirect

def send_verification_code():
  
    session = requests.Session()
    base_url = 'https://api.afromessage.com/api/challenge'
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiMEFKejNPVzRHcjlhdThXeVpta0Fvd002bk1JWldYT3UiLCJleHAiOjE5MDAzNDQ2MzksImlhdCI6MTc0MjU3ODIzOSwianRpIjoiMjQ5MWNiYjktYWZjNy00YjU0LWE2NTYtZDg3MWNiYTE0NjQzIn0.yb7MRuEXD5frdYLbahG5EwFvLwY8NlkoyiRr5TljJ0o'
    headers = {'Authorization': 'Bearer ' + token}
    callback = 'validation'
    from_id = 'e80ad9d8-adf3-463f-80f4-7c4b39f7f164'
    sender = ''
    recipient = '+251973927576'  
    prefix = f"Here is your verification code for password reset from Gymnify:"
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
            return {'status': 'success', 'redirect': 'password_reset'}
        else:
            print('API error:', response_json.get('response'))
            return {'status': 'error', 'message': response_json.get('response')}
    else:
        print(f'HTTP error ... code: {result.status_code}, msg: {result.text}')
        return {'status': 'http_error', 'code': result.status_code, 'message': result.text}