# Copyright 2018 Google Inc. All rights reserved.
# Use of this source code is governed by the Apache 2.0
# license that can be found in the LICENSE file.

import logging
import json
import datetime

import time
from flask import Flask
from flask import request, Response, render_template, g, jsonify, current_app

from google.cloud import logging as gcplogging
from google.cloud.logging_v2.resource import Resource

from flask_gcp_log_groups.background_thread import BackgroundThreadTransport

_GLOBAL_RESOURCE = Resource(type='global', labels={})

logger = logging.getLogger(__name__)
client = gcplogging.Client()

class GCPHandler(logging.Handler):
    
    def __init__(self, app, parentLogName='request', childLogName='application', 
                traceHeaderName=None,labels=None, resource=None):
        logging.Handler.__init__(self)
        self.app = app
        self.labels=labels
        self.traceHeaderName = traceHeaderName
        if (resource is None):
            resource = _GLOBAL_RESOURCE
        else:
            resource = Resource(type=resource['type'], labels=resource['labels'])
            print(resource)
        self.resource = resource
        self.transport_parent = BackgroundThreadTransport(client, parentLogName)
        self.transport_child = BackgroundThreadTransport(client, childLogName)           
        self.mLogLevels = {}
        if app is not None:
            self.init_app(app)
            
    def emit(self, record):
        msg = self.format(record)
        record_level = record.levelno
        SEVERITY = record.levelname

        # if the current log is at a lower level than is setup, skip it
        if (record_level <= logger.level):
            return
        if SEVERITY not in self.mLogLevels:
            self.mLogLevels[SEVERITY] = record_level
        TRACE = None
        SPAN = None
        if (self.traceHeaderName in request.headers.keys()):
          # trace can be formatted as "X-Cloud-Trace-Context: TRACE_ID/SPAN_ID;o=TRACE_TRUE"
          rawTrace = request.headers.get(self.traceHeaderName).split('/')
          TRACE = rawTrace[0]
          if ( len(rawTrace) > 1) :
              SPAN = rawTrace[1].split(';')[0]

        self.transport_child.send(
                msg,
                timestamp=datetime.datetime.utcnow(),                
                severity=SEVERITY,
                resource=self.resource,
                labels=self.labels,
                trace=TRACE,
                span_id=SPAN)            

    def init_app(self, app):

        # capture the http_request time
        @app.before_request
        def before_request():
            g.request_start_time = time.time()
            g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

        # always log the http_request@ default INFO
        @app.after_request
        def add_logger(response):
            TRACE = None
            SPAN = None
            if (self.traceHeaderName in request.headers.keys()):
              # trace can be formatted as "X-Cloud-Trace-Context: TRACE_ID/SPAN_ID;o=TRACE_TRUE"
              rawTrace = request.headers.get(self.traceHeaderName).split('/')
              TRACE = rawTrace[0]
              if ( len(rawTrace) > 1) :
                SPAN = rawTrace[1].split(';')[0]

            # https://github.com/googleapis/googleapis/blob/master/google/logging/type/http_request.proto
            REQUEST = {
                'requestMethod': request.method,
                'requestUrl': request.url,
                'status': response.status_code,
                'responseSize': response.content_length,
                'latency': g.request_time(),
                'remoteIp': request.remote_addr,
                'requestSize': request.content_length  
            }
     
            if 'user-agent' in request.headers:
                REQUEST['userAgent'] = request.headers.get('user-agent') 

            if request.referrer:
                REQUEST['referer'] = request.referrer

            # add the response status_code based log level
            response_severity = logging.getLevelName(logging.INFO)
            if 400 <= response.status_code < 500:
                response_severity = logging.getLevelName(logging.WARNING)
            elif response.status_code >= 500:
                response_severity = logging.getLevelName(logging.ERROR)
            if response_severity not in self.mLogLevels:
                self.mLogLevels[response_severity] = getattr(logging, response_severity)

            # find the log level priority sub-messages; apply the max level to the root log message
            severity = max(self.mLogLevels, key=self.mLogLevels.get)

            self.mLogLevels = {}
            self.transport_parent.send(
                None,
                timestamp= datetime.datetime.utcnow(),
                severity = severity,
                resource=self.resource,
                labels=self.labels,
                trace=TRACE,
                span_id = SPAN,
                http_request=REQUEST)            
            
            #response.headers['x-upstream-service-time'] = g.request_time()
            return response
