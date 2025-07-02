# syncast/core/options.py

import syncast

class SyncCastRequestConfig:
    '''
    SyncCastRequestConfig provides access to the current runtime 
    configuration for SyncCast API requests.
    This includes API base URL, application credentials, 
    maximum retries, and API version.
    '''

    @property
    def base_url(self):
        return syncast.api_base

    @property
    def app_id(self):
        return syncast.app_id

    @property
    def app_secret(self):
        return syncast.app_secret

    @property
    def max_retries(self):
        return syncast.max_network_retries

    @property
    def api_version(self):
        return syncast.api_version
