import sys
from celery import shared_task

if (sys.version_info > (3, 0)):
    # Python 3
    from http import client
    from urllib.parse import urlencode
else:
    import httplib as client
    from urllib import urlencode


@shared_task
def send_report_task(params_dict):
    params = urlencode(params_dict)
    connection = client.HTTPConnection('www.google-analytics.com')
    return connection.request('POST', '/collect', params)
