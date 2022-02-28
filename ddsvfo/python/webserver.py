#!/usr/bin/env python3

from bottle import route, run, static_file, request, subprocess

controller = None

@route("/")
def index():
    return static_file("static/index.html", root=".")

@route("/ddsweb.js")
def ddsweb_js():
    return static_file("static/ddsweb.js", root=".")

@route("/ddsweb.css")
def ddsweb_css():
    return static_file("static/ddsweb.css", root=".")

@route("/status")
def status():
    return {"curBand": controller.curBand,
            "frequency": controller.frequency,
            "bands": controller.getBandList()}

@route("/setfreq")
def setfreq():
    freq = request.query.freq
    if not freq:
        return {"status":"nope"}

    freq = int(freq)
    controller.setFrequencyAsync(freq)

    return {"status": "okay"}

def webRun(ctrl):
    global controller
    controller = ctrl
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)
