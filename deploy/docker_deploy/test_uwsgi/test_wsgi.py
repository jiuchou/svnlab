#!/usr/bin/env python

def application(env, start_response):
    """docstring
    """
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]
