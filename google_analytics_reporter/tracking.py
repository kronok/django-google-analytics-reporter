import uuid

from django.utils.functional import cached_property
from django.conf import settings

from .tasks import send_report_task

GOOGLE_ID = settings.GOOGLE_ANALYTICS_ID


class Tracker(object):
    valid_anal_types = ('pageview', 'event', 'social', 'screenview', 'transaction', 'item', 'exception', 'timing')

    def __init__(self, request=None, client_id=None, user_id=None):
        self.request = request
        self.client_id = client_id
        self.user_id = user_id

    @cached_property
    def get_client_id(self):
        if self.client_id:
            return self.client_id
        if not self.request:
            self.client_id = str(uuid.uuid4())
        else:
            _ga = self.request.COOKIES.get('_ga')
            if _ga:
                ga_split = _ga.split('.')
                self.client_id = '.'.join((ga_split[2], ga_split[3]))
        return self.client_id

    @cached_property
    def get_user_id(self):
        if self.user_id:
            return self.user_id
        if self.request and self.request.user.id:
            self.user_id = self.request.user.id
        return self.user_id

    @property
    def default_params(self):
        client_id = self.get_client_id
        user_id = self.get_user_id
        ret = {
            'v': 1,
            'tid': GOOGLE_ID,
            'cid': client_id,
        }
        if user_id:
            ret['uid'] = user_id
        return ret

    def get_payload(self, *args, **kwargs):
        """Receive all passed in args, kwargs, and combine them together with any required params"""
        if not kwargs:
            kwargs = self.default_params
        else:
            kwargs.update(self.default_params)
        for item in args:
            if isinstance(item, dict):
                kwargs.update(item)
        if hasattr(self, 'type_params'):
            kwargs.update(self.type_params(*args, **kwargs))
        return kwargs

    def debug(self, *args, **kwargs):
        return self.get_payload(*args, **kwargs)

    def sync_send(self, *args, **kwargs):
        # For use when you don't want to send as an async task through Celery
        payload = self.get_payload(*args, **kwargs)
        return send_report_task(payload)

    def send(self, *args, **kwargs):
        payload = self.get_payload(*args, **kwargs)
        return send_report_task.delay(payload)


class PageView(Tracker):
    anal_type = 'pageview'

    def type_params(self, *args, **kwargs):
        domain = kwargs.get('domain') or kwargs.get('dh')
        page = kwargs.get('page') or kwargs.get('dp')
        title = kwargs.get('title') or kwargs.get('dt')
        label = kwargs.get('label') or kwargs.get('el')
        value = kwargs.get('value') or kwargs.get('ev')
        params = {
            't': self.anal_type,
            'dh': domain or settings.DEFAULT_TRACKING_DOMAIN, #mydomain.com
            'dp': page, #/home
            'dt': title #hompage
        }
        if label:
            params['el'] = label
        if value:
            params['ev'] = value
        return params


class Event(Tracker):
    anal_type = 'event'

    def type_params(self, *args, **kwargs):
        category = kwargs.get('category') or kwargs.get('ec')
        action = kwargs.get('action') or kwargs.get('ea')
        document_path = kwargs.get('document_path') or kwargs.get('dp')
        document_title = kwargs.get('document_title') or kwargs.get('dt')
        campaign_id = kwargs.get('campaign_id') or kwargs.get('ci')
        campaign_name = kwargs.get('campaign_name') or kwargs.get('cn')
        campaign_source = kwargs.get('campaign_source') or kwargs.get('cs')
        campaign_medium = kwargs.get('campaign_medium') or kwargs.get('cm')
        campaign_content = kwargs.get('campaign_content') or kwargs.get('cc')
        label = kwargs.get('label') or kwargs.get('el')
        value = kwargs.get('value') or kwargs.get('ev')
        params = {
            't': self.anal_type,
            'ec': category, #video
            'ea': action, #play
        }
        if document_path:
            params['dp'] = document_path
        if document_title:
            params['dt'] = document_title
        if campaign_id:
            params['ci'] = campaign_id
        if campaign_name:
            params['cn'] = campaign_name
        if campaign_source:
            params['cs'] = campaign_source
        if campaign_medium:
            params['cm'] = campaign_medium
        if campaign_content:
            params['cc'] = campaign_content
        if label:
            params['el'] = label
        if value:
            params['ev'] = value
        return params
