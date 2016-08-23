import httplib
import urllib

from celery import shared_task


@shared_task
def send_report_task(params_dict):
    params = urllib.urlencode(params_dict)
    connection = httplib.HTTPConnection('www.google-analytics.com')
    return connection.request('POST', '/collect', params)
