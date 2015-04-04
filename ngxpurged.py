#! /usr/bin/env python
# vim:sw=4 ts=4 et:
#
# Copyright (c) 2015 Torchbox Ltd.
# 2015-04-02 <felicity@torchbox.com>
#

from flask import Flask, make_response
app = Flask(__name__)

import os

import settings

def text_response(text):
    response = make_response(text)
    response.headers['Content-Type'] = 'text/plain;charset=UTF-8'
    return response

def do_purge(path):
    deleted = 0
    errs = 0

    for subdir, dirs, files in os.walk(path):
        for file in files:
            try:
                os.remove(os.path.join(subdir, file))
                deleted += 1
            except OSError:
                errs += 1

    return (deleted, errs)

@app.route("/")
def main():
    return text_response("Ready.\n")

@app.route("/purge/<path:path>", methods=[ 'POST' ])
def purge(path):
    if "/" in path or path[0] == '.':
        return text_response("Path may not contain '/', '.' or '..'.\n")

    fs_path = "%s/%s" % (settings.NGX_CACHE_DIR, path)
    (deleted, errs) = do_purge(fs_path)

    return text_response("Purged <%s>, %d deleted, %d errors.\n" % (path, deleted, errs))
    
if __name__ == "__main__":
    app.run(debug = settings.DEBUG)
