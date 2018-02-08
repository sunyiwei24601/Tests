from urllib.parse import urlparse
result=urlparse("http://baidu.com",
                allow_fragments=False,#是否拼接
                scheme='https')

from urllib.parse import urlunparse
#进行拼接
from urllib.parse import urljoin
#两个链接之间的结合
from urllib.parse import urlencode


