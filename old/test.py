import docker
import json
import jsonpickle




def display_time(seconds, granularity=2):
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
        )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


client = docker.from_env()
#for container in client.containers.list():
#    print(json.dumps(json.loads(jsonpickle.encode(container)), indent=2))

for image in client.images.list():
    print(json.dumps(json.loads(jsonpickle.encode(image)), indent=2))


from datetime import datetime
import time

fmt = '%Y-%m-%dT%H:%M:%S'
d1 = datetime.strptime('2017-06-14T12:25:46.597712665Z'.split(".")[0], fmt)
d2 = datetime.strptime(datetime.now().isoformat().split(".")[0], fmt)

# Convert to Unix timestamp
d1_ts = time.mktime(d1.timetuple())
d2_ts = time.mktime(d2.timetuple())

# They are now in seconds, subtract and then divide by 60 to get minutes.
#print int(d2_ts-d1_ts) / 60

print str(display_time(d2_ts-d1_ts))