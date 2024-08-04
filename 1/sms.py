from base64 import b64encode
import requests

def send_sms(receivers, message,user_id='whitesox56', secure='a544d1f915606855c739539dd2521b18', sender='01033047382'):
    params = {
        'user_id': user_id,
        'secure': secure,
        'mode': '1',
        'sphone1': sender[:3],   # 해당 발신번호를 확인하여 변수 변경이 필요함.
        'sphone2': sender[3:7], # 해당 발신번호를 확인하여 변수 변경이 필요함. 
        'sphone3': sender[7:11], # 해당 발신번호를 확인하여 변수 변경이 필요함.
        'rphone': ','.join(receivers),
        'msg': message,
    }


    response = requests.post('https://sslsms.cafe24.com/sms_sender.php',data=params)
    return response.text


#result = send_sms('whitesox56', 'a544d1f915606855c739539dd2521b18', '01033047382',['01033047382'], '문자발신 테스트')
#print(result)  # SMS 발송이 정상적으로 되지 않을 경우 ERROR CODE 확인
