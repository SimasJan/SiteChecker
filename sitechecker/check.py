import asyncio
from time import time
import aiohttp
from http.client import HTTPConnection
from urllib.parse import urlparse

error = Exception("Unknown error")                          # generic exception placeholder

def is_site_online(url, timeout=2):
    """Return True if the target URL is online. Raise an exception otherwise."""

    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]           # extract hostname from the target url
    for port in (80, 443):                                      # http and https ports, to check both
        connection = HTTPConnection(
            host=host, port=port, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            # to always free up the resources close the connection
            connection.close()
    raise error

async def is_site_online_async(url, timeout=2):
    """Return True if the target URL is online. Raises an exception otherwise."""
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]           # extract hostname from the target url
    for scheme in ('http', 'https'):
        target_url = scheme + '://' + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception("Timed out!")
            except Exception as e:
                error = e
    raise error

# --- some tests
def test_is_site_online_python():
    url_to_test = 'python.org'
    assert is_site_online(url_to_test) == True, "Url '{}' is not online.".format(url_to_test)

def test_is_site_online_google():
    url_to_test = 'google.com'
    assert is_site_online(url_to_test) == True, "Url '{}' is not online.".format(url_to_test)


# test_is_site_online_python()
# test_is_site_online_google()