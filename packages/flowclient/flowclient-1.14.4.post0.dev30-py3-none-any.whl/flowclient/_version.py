
# This file was generated by 'versioneer.py' (0.18) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json

version_json = '''
{
 "date": "2020-12-18T05:10:00+0000",
 "dirty": false,
 "error": null,
 "full-revisionid": "01b4408a8f45d35a6280416a426db78312c5ed96",
 "version": "1.14.4.post.dev30"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
