from flask import Flask, render_template
import IPManager as ic

app = Flask(__name__, static_url_path='', static_folder='..', template_folder='../FrontEnd/templates')
ipm = ic.IPManager()

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
        return "Camera not found", 404

@app.route("/p:<id>")
def pauseCamera(id):
    response = ipm.pauseCamera(int(id))
    print("Pause ID: " + id)

    if (response):
        return "OK", 200
    else:
        return "Camera not found", 404

@app.route("/s:<id>")
def startCamera(id):
    response = ipm.startCamera(int(id))
    print("Start ID: " + id)

    if(response) :
        return "OK", 200
    else :
        return "Camera not found", 404


@app.route("/a:<ip>:<name>:<status>")
def addCamera(ip, name, status):
    response = ipm.addCamera(ip, name, status)

    if (response):
        return "OK", 200
    else:
        return "Camera not found", 404


if(__name__ == "__main__"):
   app.run(host='127.0.0.1', port=8000, debug=True)