import csv
from django.conf import settings
from django.http import HttpResponse

def _make_list(data: list) -> list:
    """데이터가 존재하면 하루를 1분단위로 나누어 반환
    데이터가 존재하지 않으면 빈 배열을 반환

    Args:
        data (list): 데이터가 담긴 배열

    Returns:
        list: 가공된 데이터가 담긴 배열
    """
    if data == None:
        return [None for i in range(1440)]
    return [int(i.strip()) for i in data[1:-1].split(",")]

def make_csv_response(user: settings.AUTH_USER_MODEL, response: HttpResponse) -> HttpResponse:
    """유저의 healthData를 csv로 만들어서 response에 저장

    Args:
        user (settings.AUTH_USER_MODEL): 유저 모델
        response (HttpResponse): csv를 작성할 Response

    Returns:
        HttpResponse: csv 데이터로 채워진 Response
    """
    writer = csv.writer(response)
    writer.writerow(['year', 'month', 'day', 'hour', 'minute', 
                        'age', 'height', 'weight', 'bmi', 
                        'heart', 'sleep', 'step', 'stress', 'spo2'])
    for health in user.huami.health.all():
        heart = _make_list(health.heart_rate)
        sleep = _make_list(health.sleep_quality)
        steps = _make_list(health.step_count)
        stress = _make_list(health.stress)
        spo2 = _make_list(health.spo2)
        for minute in range(0, 1440):
            writer.writerow([health.date.year, health.date.month, health.date.day, minute // 60, minute % 60,
                            health.age, health.height, health.weight, health.bmi,
                            heart[minute], sleep[minute], steps[minute], stress[minute], spo2[minute]
                            ])
    
    return response