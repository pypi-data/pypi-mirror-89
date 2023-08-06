import logging
from jaeger_client import Config


class Trace:
    def __init__(self, func, service_name, log_level):
        self.func = func
        self.tracer = Trace.initialize_tracer(service_name, log_level)

    def __call__(self):
        with self.tracer.start_active_span(self.func.__name__):
            self.func()

    @staticmethod
    def initialize_tracer(service_name, log_level=logging.DEBUG):
        logging.basicConfig(level=log_level)

        config = Config(
            config={
                'sampler': {'type': 'const', 'param': 1},
                'logging': True
            }, service_name=service_name
        )

        return config.initialize_tracer()
