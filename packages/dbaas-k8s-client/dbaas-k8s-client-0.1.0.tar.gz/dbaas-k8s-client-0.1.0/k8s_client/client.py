from kubernetes.client import (Configuration, ApiClient,
                               AppsV1beta1Api, CoreV1Api)


class K8sAPI(AppsV1beta1Api, CoreV1Api):
    pass


class K8sClient(object):

    def __init__(self, token, endpoint, verify_ssl=False):
        configuration = Configuration()
        configuration.api_key['authorization'] = "Bearer {}".format(token)
        configuration.host = endpoint
        configuration.verify_ssl = verify_ssl
        api_client = ApiClient(configuration)
        self._client = K8sAPI(api_client)

    def __getattr__(self, item):
        return self._client.__getattribute__(item)

    def __dir__(self):
        return dir(self._client)
