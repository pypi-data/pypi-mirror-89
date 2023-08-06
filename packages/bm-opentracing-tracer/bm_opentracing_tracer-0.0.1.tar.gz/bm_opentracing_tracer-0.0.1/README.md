# Opentracing tracers
Jaeger tracer instrumentation implemented

# GitHub url: https://github.com/beyondminds/bm-opentracing

# Usage:

```Python
from bm_opentracing_tracer.bm_jaeger_tracer import initialize_tracer
tracer = initialize_tracer(service_name, log_level)
```
use open tracing api with 'tracer'