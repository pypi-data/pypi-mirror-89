import logging
import re
from typing import Optional

from starlette.datastructures import URL
from starlette.requests import Request

from . import exceptions, glove
from .settings import BaseSettings
from .utils import get_ip

logger = logging.getLogger('foxglove.recaptcha')
TESTING_SECRET = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


async def check_recaptcha(request: Request, recaptcha_token: Optional[str], *, error_headers=None) -> None:
    client_ip = get_ip(request)

    if not recaptcha_token:
        logger.warning('recaptcha token not provided, path="%s" ip=%s', request.url.path, client_ip)
        raise exceptions.HttpBadRequest('No recaptcha value', headers=error_headers)

    settings: BaseSettings = glove.settings

    post_data = {'secret': settings.recaptcha_secret, 'response': recaptcha_token, 'remoteip': client_ip}
    r = await glove.http.post(settings.recaptcha_url, data=post_data)
    r.raise_for_status()
    data = r.json()

    # if settings.origin exists, use that instead of the request to avoid problems with old browsers that don't include
    # the Origin header
    if origin := getattr(settings, 'origin', None):
        request_host = URL(origin).hostname
    else:
        request_host = request.url.hostname
        # using the origin here if available instead of host avoids problems when requests are proxied e.g. with netlify
        if origin := request.headers.get('origin'):
            request_host = re.sub('^https?://', '', origin)

    if data['success']:
        hostname = data['hostname']
        if hostname == request_host:
            logger.info('recaptcha success')
            return
        elif settings.dev_mode and settings.recaptcha_secret == TESTING_SECRET and hostname == 'testkey.google.com':
            logger.info('recaptcha test key success')
            return

    logger.warning(
        'recaptcha failure, path=%s request_host=%s ip=%s response=%s',
        request.url.path,
        request_host,
        client_ip,
        r.text,
        extra={'recaptcha_response': data, 'recaptcha_token': recaptcha_token, 'headers': dict(request.headers)},
    )
    raise exceptions.HttpBadRequest('Invalid recaptcha value', headers=error_headers)


class RecaptchaDepends:
    __slots__ = ('request',)

    def __init__(self, request: Request):
        self.request = request

    async def __call__(self, recaptcha_token: Optional[str], *, error_headers=None) -> None:
        return await check_recaptcha(self.request, recaptcha_token, error_headers=error_headers)
