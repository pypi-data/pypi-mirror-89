# -*- coding: utf-8 -*-

from requests import Response, Session


class SafeResponse(object):
    def __init__(self, success, response=None, session=None):
        self.__success: bool = success
        self.__response: Response = response
        self.__session: Session = session

    def __repr__(self):
        if self.success:
            status = "Success: %s" % self.response.status_code
        else:
            status = "Failed"
        return '<SafeResponse [%s]>' % status

    @property
    def success(self):
        return self.__success

    @property
    def response(self):
        if self.success:
            return self.__response
        else:
            return None

    @property
    def status_code(self):
        if self.success:
            return self.__response.status_code
        else:
            return None

    @property
    def session(self):
        if self.success:
            return self.__session
        else:
            return None
