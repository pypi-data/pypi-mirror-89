
import json

version_json = '''
{"date": "2020-12-18T09:51:10.461784", "dirty": false, "error": null, "full-revisionid": "3c52ff484d846585eefe729d498b0b4a81dd2d7d", "version": "0.9.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

