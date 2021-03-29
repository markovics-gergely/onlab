from flask import Flask, render_template, g, jsonify, request
import IPManager as manager
import json
from IPCamera import CameraStatus as cs

app = Flask(__name__, static_url_path='', static_folder='..', template_folder='../FrontEnd/templates')

ipm = manager.IPManager()
print("asdasdasdasd")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prediction/")
def prediction():
    return render_template("prediction.html")

@app.route("/d:<id>")
def deleteCamera(id):
    response = ipm.deleteCamera(int(id))
    print("Delete ID: " + id)

    if (response):
        return "OK", 200
    else:
        return "Camera cannot be deleted", 502

@app.route("/p:<id>")
def pauseCamera(id):
    response = ipm.pauseCamera(int(id))
    print("Pause ID: " + id)

    if (response):
        return "OK", 200
    else:
        return "Camera cannot be paused", 502

@app.route("/s:<id>")
def startCamera(id):
    response = ipm.startCamera(int(id))
    print("Start ID: " + id)

    if(response) :
        return "OK", 200
    else :
        return "Camera cannot be started", 502


@app.route("/a", methods=['POST'])
def addCamera():
    data = request.get_json()
    request.close()
    response = ipm.addCamera(data['ip'], data['name'], int(data['status']))
    if (response):
        return "OK", 200
    else:
        return "Camera not found", 404

@app.route("/clist", methods=['GET'])
def getCameraList():
    return jsonify(ipm.gtJsonData())

if(__name__ == "__main__"):
   app.run(host='127.0.0.1', port=8000, threaded=True, debug=True, use_reloader=False)