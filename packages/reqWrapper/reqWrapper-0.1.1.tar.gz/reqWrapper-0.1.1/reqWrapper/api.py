# -*- coding: utf-8 -*-

from time import sleep
from requests import Session
from warnings import warn
from .model import SafeResponse


def request(method, url, session=None, retry=5, wait=1, need_200=False, **kwargs):
    session: Session
    if session is None:
        session = Session()

    try_count = 0

    while try_count < retry:
        try_count += 1
        if try_count != 1:
            sleep(wait)
        try:
            res = session.request(method=method, url=url, **kwargs)
            session.close()
            if need_200 and res.status_code != 200:
                continue
            else:
                return SafeResponse(success=True, response=res, session=session)
        except Exception:
            continue
    return SafeResponse(success=False)


def get(url, params=None, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)


def options(url, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    kwargs.setdefault('allow_redirects', True)
    return request('options', url, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)


def head(url, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes. If
        `allow_redirects` is not provided, it will be set to `False` (as
        opposed to the default :meth:`request` behavior).
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    kwargs.setdefault('allow_redirects', False)
    return request('head', url, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)


def post(url, data=None, json=None, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    return request('post', url, data=data, json=json, session=session,
                   retry=retry, wait=wait, need_200=need_200, **kwargs)


def put(url, data=None, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    return request('put', url, data=data, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)


def patch(url, data=None, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    return request('patch', url, data=data, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)


def delete(url, session=None, retry=5, wait=1, need_200=False, **kwargs):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param session: request with session
    :type session: requests.Session
    :param retry: Max retry count.
    :param wait: Time(seconds) between retry
    :param need_200: Set True if you only need status code 200
        else -> fail
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: reqWrapper.SafeResponse
    """

    return request('delete', url, session=session, retry=retry, wait=wait, need_200=need_200, **kwargs)
