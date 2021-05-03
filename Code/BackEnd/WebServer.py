from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import IPManager as manager
import Prediction as prediction

app = Flask(__name__, static_url_path='', static_folder='..', template_folder='../FrontEnd/templates')
ipm = manager.IPManager()
pre = prediction.Prediction()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prediction/")
def prediction():
    return render_template("prediction.html")

@app.route("/prediction/p", methods=['POST'])
def getPrediction():
    data = request.get_json()
    request.close()

    date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    date = date + timedelta(hours=2)
    predicted = pre.getPrediction(date.strftime("%Y-%m-%d %H:%M:%S"), data['camera'])
    print(predicted)
    return jsonify(predicted)

@app.route("/prediction/img")
def getProgression():
    response = pre.processPlot()
    
    if (response):
        return "OK", 200
    else:
        return "Camera cannot be deleted", 502


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
        writeable = ipm.editCameraStatus(id, 0)
        if(writeable) :
            return "OK", 200
        else :
            return "Camera cannot be written", 502
    else:
        return "Camera cannot be paused", 502

@app.route("/s:<id>")
def startCamera(id):
    response = ipm.startCamera(int(id))
    print("Start ID: " + id)

    if(response) :
        writeable = ipm.editCameraStatus(id, 1)
        if(writeable) :
            return "OK", 200
        else :
            return "Camera cannot be written", 502
    else :
        return "Camera cannot be started", 502

@app.route("/a", methods=['POST'])
def addCamera():
    data = request.get_json()
    request.close()
    response = ipm.addCamera(data['ip'], data['name'], int(data['status']), data['imgType'])
    if (response):
        return "OK", 200
    else:
        return "Camera not found", 502

@app.route("/clist", methods=['GET'])
def getCameraList():
    return jsonify(ipm.getJsonData())

@app.route("/alive:<id>")
def cameraAlive(id):
    response = ipm.cameraList[int(id)].cameraAlive()
    print("Alive ID: " + id)

    if(response) :
        return "OK", 200
    else :
        ipm.pauseCamera(int(id))
        ipm.editCameraStatus(id, 0)
        return "Camera cannot be started", 502

@app.route("/atstart")
def cameraCheck():
    for id in range(len(ipm.cameraList)) :
        try :
            ipm.editCameraStatus(id, ipm.cameraList[id].status.value)
        except :
            return "Camera cannot be started", 502
    return "OK", 200

@app.route("/data:<id>", methods=['GET'])
def cameraData(id):
    try :
        json = jsonify(ipm.getDataframe(id))
        return json
    except :
        return "Data cannot read", 502

if(__name__ == "__main__"):
   app.run(host='127.0.0.1', port=8000, threaded=True, debug=True, use_reloader=False)