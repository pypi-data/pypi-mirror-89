# -*- python -*-
"""
djfim.settings
"""

from django.conf import settings
from django.test.signals  import setting_changed


class DjFIMSetting(object):
    '''
    setting provider
    '''

    SETTING_NAME = 'DJFIM'

    DEFAULT = {
        'RELEASE_INCREMENT_POLICY': 'PLUS_ONE',
        'MODEL': {
            'app_name': 'djfim',
            'app_label': 'FURecord',
        },
    }

    def __init__(self, **kwargs):
        self._default = self.DEFAULT
        self._cache = set()

    @property
    def user_setting(self):
        '''
        :return: dict
        '''
        if not hasattr(self, '_user_setting'):
            self._user_setting = getattr(
                settings,
                self.SETTING_NAME,
                dict()
            )
        return self._user_setting

    def __getattr__(self, attr):
        try:
            val = self.user_setting[attr]
        except KeyError:
            if attr not in self._default:
                raise AttributeError("Invalid API setting: '%s'" % attr)
            val = self._default[attr]
        self._cache.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        if hasattr(self, '_user_setting'):
            delattr(self, '_user_setting')
        for attr in self._cache:
            delattr(self, attr)
        self._cache.clear()
        return None


app_settings = DjFIMSetting()


def reload_setting(*args, **kwarg):  # pragma: no cover
    if kwarg['settings'] == app_settings.SETTING_NAME:
        app_settings.reload()

setting_changed.connect(reload_setting)
