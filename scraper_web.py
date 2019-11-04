
import aiohttp
import asyncio
import ssl
import urllib.request


##
# CONSTANTS

UNVERIFIED_REQUEST_CONTEXT = ssl._create_unverified_context()


##
# PUBLIC

def request(url):
    with urllib.request.urlopen(url, context=UNVERIFIED_REQUEST_CONTEXT) as response:
        content_charset = response.headers.get_content_charset()
        return response.read().decode(content_charset)

async def async_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=UNVERIFIED_REQUEST_CONTEXT) as response:
            content = await response.read()
            return content.decode(response.charset) if response.charset else None
