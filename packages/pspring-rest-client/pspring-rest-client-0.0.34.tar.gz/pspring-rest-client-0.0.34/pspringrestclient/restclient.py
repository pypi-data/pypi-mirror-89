import requests

from requests.exceptions import HTTPError

from pspring import *

import logging
import json
import inspect

logger = logging.getLogger("pspring-rest-client")

class PayloadException(Exception):
    def __init__(self,*args):
        super().__init__(*args)
        self.response = args[2]
        self.statusCode = args[1]

class Mapping():
    def __init__(self,*args,**kargs):
        self.method = kargs.get("method")
        self.url = kargs.get("url")
        self.data = kargs.get("data")
        self.timeout = kargs.get("timeout")

    def __call__(self,funcObj):
        def newFunc(*args,**kargs):
            argspec = inspect.getfullargspec(funcObj)
            argumentNames = argspec[0]
            url = self.url
            for i in range(len(argumentNames)):
                if(len(args) > i ):
                    url = url.replace("{"+argumentNames[i]+"}",str(args[i]))

            for (kargKey,kargVal) in kargs.items():
                url = url.replace("{"+kargKey+"}",str(kargVal))

            selfObj = args[0]
            kargs.update({
                "url" : selfObj.getUrl()+url
            })
            kargs.update({
                "method" : self.method
            })

            if(self.timeout != None):
                kargs.update({
                    "timeout" : float(self.timeout)
                })

            if self.data != None:
                kargs.update({
                    "data" : self.data
                })

            kargsToUpdate = funcObj(*args,**kargs)

            if(kargs != None and kargsToUpdate != None):
                kargs.update(kargsToUpdate)

            if(hasattr(selfObj,"queryString") and selfObj.queryString != None):
                kargs.update({
                    "url" : kargs.get("url") + "?" + selfObj.queryString
                })

            if (hasattr(selfObj,"proxies") and selfObj.proxies != None):
                kargs.update({
                    "proxies" : selfObj.proxies
                })

            if(hasattr(selfObj,"timeout") and selfObj.timeout != None):
                kargs.update({
                    "timeout" : float(selfObj.timeout)
                })

            if (hasattr(selfObj,"data") and selfObj.data != None):
                kargs.update({
                    "data" : selfObj.data
                })

            if (hasattr(selfObj,"json") and selfObj.json != None):
                kargs.update({
                    "json" : selfObj.json
                })


            return selfObj.send(**kargs)
        return newFunc


class RestClient():
    middlewares = []
    def __init__(self,*args,**kargs):
        self.url = kargs.get("url")
        self.headers = kargs.get("headers",{})
        self.middlewares = kargs.get("middlewares",[])
        self.timeout = kargs.get("timeout")
        self.responsemapper = kargs.get("responsemapper")

    def __call__(self,classObj):
        prevInit = classObj.__init__

        def constructor(*args,**kargs):

            selfOrig = args[0]
            def middleware(*args,**kargs):
                index = args[0] if len(args) == 1 else None
                def newfunc(func_obj):
                    selfOrig.add_middleware(func_obj,index)
                    return func_obj
                return newfunc
            selfOrig.headers = self.headers
            selfOrig.url = self.url
            selfOrig.middleware = middleware
            selfOrig.middlewares = RestClient.middlewares+ self.middlewares
            prevInit(*args,**kargs)

        def add_middleware(selfOrig,func_obj,index=None):
            if index is not None:
                selfOrig.middlewares.insert(index,func_obj)
            else:
                selfOrig.middlewares.append(func_obj)

        def addHeader(selfOrig,name,value):
            selfOrig.headers.update({name:value})

        def send(*args,**kargs):
            selfOrig = args[0]
            additionalArgs = selfOrig.finalize()

            if isinstance(additionalArgs,dict):
                kargs.update(additionalArgs)

            if kargs.get("timeout") == None and self.timeout != None:
                kargs["timeout"] = float(self.timeout)

            kargs["headers"] = selfOrig.headers

            for middleware in selfOrig.middlewares:
                middleware(kargs,None)
            
            logger.info({
                "message" : "request details",
                "timeout" : kargs.get("timeout"),
                "method" : kargs.get("method"),
                "url" : kargs.get("url"),
                "data" : kargs.get("data"),
                "json" : kargs.get("json"),
                "proxies" : kargs.get("proxies"),
                "headers" : selfOrig.headers
            })
            try:
                response = requests.request(**kargs)

                finalresponse = {}
                response.raise_for_status()

                if "json" in response.headers.get("Content-Type",""):
                    responseJson = {}
                    if response.status_code != 204:
                        responseJson = response.json()

                    if self.responsemapper != None:
                        responseJson = self.responsemapper.map(responseJson)
                    
                    finalresponse = {
                        "body":responseJson,
                        "headers" : response.headers
                    }

                    logger.info({
                        "message" : "response details",
                        "method" : kargs.get("method"),
                        "url" : kargs.get("url"),
                        "data" : kargs.get("data"),
                        "json" : kargs.get("json"),
                        "proxies" : kargs.get("proxies"),
                        "headers" : selfOrig.headers,
                        "status_code" : response.status_code,
                        "responseHeaders" : str(response.headers),
                        "response" : responseJson,
                        "elapsed" : response.elapsed.total_seconds()
                    })
                
                else:
                    
                    finalresponse = {
                        "body":response.text,
                        "headers" : response.headers
                    }

                    logger.info({
                        "message" : "response details",
                        "method" : kargs.get("method"),
                        "url" : kargs.get("url"),
                        "data" : kargs.get("data"),
                        "json" : kargs.get("json"),
                        "proxies" : kargs.get("proxies"),
                        "headers" : selfOrig.headers,
                        "status_code" : response.status_code,
                        "responseHeaders" : str(response.headers),
                        "response" : response.text,
                        "elapsed" : response.elapsed.total_seconds()
                    })

                for middleware in reversed(selfOrig.middlewares):
                    middleware(kargs,finalresponse)
                return finalresponse
            except HTTPError as ex:
                logger.error({
                    "message" : str(ex)
                })
                logger.info({
                    "message" : "response details",
                    "method" : kargs.get("method"),
                    "url" : kargs.get("url"),
                    "data" : kargs.get("data"),
                    "proxies" : kargs.get("proxies"),
                    "headers" : selfOrig.headers,
                    "status_code" : response.status_code,
                    "responseHeaders" : response.headers,
                    "response" : response.text,
                    "elapsed" : response.elapsed.total_seconds()
                })
                raise ex



        def getUrl(*args,**kargs):
            selfOrig = args[0]
            return selfOrig.url

        def finalize(*args,**kargs):
            pass

        classObj.__init__ = constructor
        classObj.addHeader = addHeader
        classObj.send = send
        classObj.getUrl = getUrl
        if not hasattr(classObj,"finalize"):
            classObj.finalize = finalize

        return classObj
