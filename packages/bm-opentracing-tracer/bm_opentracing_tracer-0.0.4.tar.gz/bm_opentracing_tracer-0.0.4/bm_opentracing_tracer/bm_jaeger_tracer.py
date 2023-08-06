import logging
from jaeger_client import Config


def trace(service_name, log_level):
    tracer = initialize_tracer(service_name, log_level)

    def middle(func):
        def wrapper(*args, **kwargs):
            with tracer.start_active_span(func.__name__):
                return func(*args, **kwargs)

        return wrapper

    return middle


def initialize_tracer(service_name, log_level=logging.DEBUG):
    logging.basicConfig(level=log_level)

    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True
        }, service_name=service_name
    )

    return config.initialize_tracer()
