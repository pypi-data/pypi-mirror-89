import logging
from jaeger_client import Config


def initialize_tracer(service_name, log_level=logging.DEBUG):
    logging.basicConfig(level=log_level)

    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True
        }, service_name=service_name
    )

    return config.initialize_tracer()
