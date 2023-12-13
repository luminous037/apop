PAYLOADS: dict = {
    'tokens_amazfit': {
        'state': 'REDIRECTION',
        'client_id': 'HuaMi',
        'password': None,
        'redirect_uri': 'https://s3-us-west-2.amazonws.com/hm-registration/successsignin.html',
        'region': 'us-west-2',
        'token': 'access',
        'country_code': 'KR'
    },
    'login_amazfit': {
        'dn': 'account.huami.com,api-user.huami.com,app-analytics.huami.com,'
              'api-watch.huami.com,'
              'api-analytics.huami.com,api-mifit.huami.com',
        'app_version': '5.9.2-play_100355',
        'source': 'com.huami.watch.hmwatchmanager',
        'country_code': None,
        'device_id': None,
        'third_name': 'huami',
        'lang': 'en',
        'device_model': 'android_phone',
        'allow_registration': 'false',
        'app_name': 'com.huami.midong',
        'code': None,
        'grant_type': 'access_token'
    },
    'logout': {
        'login_token': None
    },
    'devices': {
        'enableMultiDevice': 'true'
    },
    'band_data': {
        'query_type': 'detail',
        'device_type': 'android_phone',
        'userid': None,
        'from_date': None,  # 2021-07-01
        'to_date': None,
    },
    'stress': {
        'limit': 9999,
        'from': None, #Timestamp
        'to': None,
        'eventType': 'all_day_stress',
        'reverse': True,
    },
    'blood_oxygen': {
        'limit': 1000,
        'from': None, #yyyy-mm-ddThh:mm:ss (T는 문자 그대로)
        'to': None,
        'eventType': 'blood_oxygen',
        'subType': 'click',
        'reverse': True,
        'timeZone': 'Asia/Seoul'
    },
}
