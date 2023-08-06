from .formats import *
from ..srv.version import version
class Response(object):
    def __init__(self, status, content_type=None, data=None, location=None, servername=version):
        self.status = status
        self.content_type = content_type
        self.data = data
        self.server = servername
        self.location = location
    def __str__(self):
        if self.status.startswith('3'):
            if self.location is None:
                raise Exception('Must mention Response.location in 3xx responses')
            return start_response.format_map(self.__dict__) + \
                location_header.format_map(self.__dict__) + \
                end_header.format_map(self.__dict__)
        if self.content_type is None:
            return no_data_format.format_map(self.__dict__)
        return reply_format.format_map(self.__dict__)
    __repr__ = __str__

