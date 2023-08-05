# -*- coding: utf-8  -*-

# file: uri_helper.py
# date: 2020-12-18


import pdb
import os
import typing


class URIBase(object):
    def __init__(self, raw_uri: str, host: str=None, port: str=None):
        self.raw_uri = raw_uri
        self.host = host
        self.port = port
        self.proto = "file" if len(raw_uri.split("://")) == 1 else raw_uri.split("://")[0]
        self.uri = raw_uri.split("://")[-1] if self.proto == "file" else raw_uri
   
        self.__limited_proto = {"http": None, "ftp": None}
        self._check_uri()

    def __base_limited_op(self):
        if self.proto in self.__limited_proto: 
            return None   
        else:
            raise NotImplementedError

    def _check_uri(self):
        self.__base_limited_op()   

    def read(self):
        raise NotImplementedError

    def write(self):
        self.__base_limited_op()

    def ls(self):
        """same with linux `ls` command."""
        self.__base_limited_op()    

    def mkdir(self):
        """same with linux `mkdir` command."""
        self.__base_limited_op()  


class LocalFS(URIBase):
    def _check_uri(self):
        if not os.path.isfile(self.uri) and not os.path.exists(self.uri):
            raise ValueError("%s does not exits" % self.uri)
        return None

    def read(self) -> str:
        f = open(self.uri, 'r')
        f_read = f.read()
        f.close()
        return f_read

    def write(self, content: str, mode: str='w') -> str:
        f = open(self.uri, mode)
        f.write(content)
        f.close()
        return self.uri

    def ls(self, file_or_filepath: str="filepath") -> str:
        if file_or_filepath != "filepath" and file_or_filepath != "file":
            raise ValueError("param `file_or_filepath` can only be 'filepath' or 'file'")

        result = []
        if os.path.isdir(self.uri):
            result = [os.path.join(self.uri, x) for x in os.listdir(self.uri)]
        else:
            result.append(self.uri)
        
        return [x.split("/")[-1] for x in result] if file_or_filepath == "file" else result


class URIFactory(URIBase):
    @classmethod
    def get_api(cls, raw_uri: str, host: str=None, port: str=None):
        proto = "file" if len(raw_uri.split("://")) == 1 else raw_uri.split("://")[0] 
        if proto == "file":
            return LocalFS(raw_uri, host, port)
        return None
