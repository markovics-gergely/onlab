from flask import Flask, render_template
import IPManager as ic

app = Flask(__name__, static_url_path='', static_folder='../FrontEnd/static', template_folder='../FrontEnd/templates')
ipm = ic.IPManager()

@app.route("/index/")
def index():
    return render_template("index.html")

@app.route("/prediction/")
def prediction():
    return render_template("prediction.html")

@app.route("/d:<id>")
def deleteCamera(id):
    #ipm.deleteCamera(ip)

    print("Delete ID: " + id)
    return render_template("index.html")

@app.route("/p:<id>")
def pauseCamera(id):
    #ipm.pauseCamera(ip)

    print("Pause ID: " + id)
    return render_template("index.html")

@app.route("/s:<id>")
def startCamera(id):
    #ipm.startCamera(ip)

    print("Start ID: " + id)
    return render_template("index.html")


if(__name__ == "__main__"):
   app.run(host='127.0.0.1', port=8000, debug=True)