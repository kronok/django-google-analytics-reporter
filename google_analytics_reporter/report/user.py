from ..tracking import Event


class AnalUser(Event):

    def static_params(self, action):
        return {'category': 'user', 'action': action}

    def create(self, *args, **kwargs):
        action = 'create'
        kwargs.update(self.static_params(action))
        return self.send(*args, **kwargs)

    def optin(self, *args, **kwargs):
        action = 'optin'
        kwargs.update(self.static_params(action))
        return self.send(*args, **kwargs)

    def verify(self, *args, **kwargs):
        action = 'verify'
        kwargs.update(self.static_params(action))
        return self.send(*args, **kwargs)
