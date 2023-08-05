import sys
import json
from autotracer.auto_tracer import AutoTracer


if __name__ == "__main__":

    tracer = AutoTracer()
    tracer.trace_file(sys.argv[1])
    trace = tracer.trace
    try:
        outfile = sys.argv[2]
        if not outfile.endswith('.json'):
            outfile += '.json'
    except IndexError:
        outfile = 'out.json'

    with open(outfile, 'w') as f:
        json.dump(trace, f)
