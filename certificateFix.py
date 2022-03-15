import requests


# Fix to get right certificates, based on stackoverflow
class SSLContextAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = requests.packages.urllib3.util.ssl_.create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs()  # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)


def get_from_url(url):
    # Certificate fix
    s = requests.Session()
    s.mount(url, SSLContextAdapter())
    return s.get(url)
