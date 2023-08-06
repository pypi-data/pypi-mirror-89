#!/usr/bin/env python
""" bm_ja eger_tracer.py: Jaeger instrumentation """

import logging
import functools
from jaeger_client import Config

TRACERS = dict()


def initialize_tracer(service_name, log_level=logging.DEBUG):
    logging.basicConfig(level=log_level)

    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True
        }, service_name=service_name
    )

    return config.initialize_tracer()


def create_tracer_if_absent(service_name, log_level):
    if TRACERS.get(service_name) is None:
        TRACERS[service_name] = initialize_tracer(service_name, log_level)


def get_tracer(service_name):
    return TRACERS[service_name]


def trace(service_name, log_level):
    create_tracer_if_absent(service_name, log_level)

    def middle(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer(service_name)
            with tracer.start_active_span(func.__name__):
                res = func(*args, **kwargs)
                return res

        return wrapper

    return middle
