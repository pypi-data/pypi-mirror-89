import json


async def json_output(file, response):
    with open(file, "w") as f:
        f.write(json.dumps(response))
