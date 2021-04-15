import pandas as pd
import os.path
import IPCamera as ic

class IPManager:
    def __init__(self):
        self.cameraList = self.parseCameras()

    def addCamera(self, ipaddr, name, status, imgType):
        self.persistCamera(ipaddr, name, status, imgType)

        ipcamera = ic.IPCamera(ipaddr, name, ic.CameraStatus(status), imgType)
        self.cameraList.append(ipcamera)

        return True

    def deleteCamera(self, id):
        if(len(self.cameraList) <= id):
            return False
        self.pauseCamera(id)
        self.deleteCameraFromDB(id)
        self.cameraList.pop(id)
        return True


    def startCamera(self, id):
        if(len(self.cameraList) <= id):
            return False
        
        success = self.cameraList[id].startCameraThread()
        return success

    def pauseCamera(self, id):
        if(len(self.cameraList) <= id):
            return False
        return self.cameraList[id].pauseCameraThread()

    def parseCameras(self):
        clist = []
        path='DB/cameraList.csv'
        df = pd.read_csv(path)

        iplist = df["ipaddress"].tolist()
        namelist = df["name"].tolist()
        statuslist = df["status"].tolist()
        imgTypelist = df["imgType"].tolist()

        for i in range(len(iplist)) :
            ipcamera = ic.IPCamera(iplist[i], namelist[i], ic.CameraStatus(statuslist[i]), imgTypelist[i])
            clist.append(ipcamera)

        return clist

    def persistCamera(self, ipaddr, name, status, imgType):
        path='DB/cameraList.csv'

        notExist = True
        if(os.path.isfile(path)): 
            notExist=False
        
        df = pd.read_csv(path, usecols= ['ipaddress'])
        for b in df["ipaddress"].isin([ipaddr]).tolist() :
            if(b) :
                return False
        
        writer = pd.DataFrame([[ipaddr, name, status, imgType]], columns=['ipaddress', 'name', 'status', 'imgType'])
        writer.to_csv(path, mode='a', index=False, header=notExist)

        return True

    def deleteCameraFromDB(self, id) :
        path='DB/cameraList.csv'

        if(not os.path.isfile(path)): 
            return

        df = pd.read_csv(path)
        df.drop(id, axis=0, inplace=True)
        df.to_csv(path, index=False)

        url = self.cameraList[id].getFileNameFromUrl()

        path = "DB/cameras/" + url + ".csv"
        if(os.path.isfile(path)):
            os.remove(path)

    def editCameraStatus(self, id, status) :
        path='DB/cameraList.csv'
        print(str(id) + " " + str(status))
        try :
            df = pd.read_csv(path)
            df.loc[int(id),'status'] = status
            df.to_csv(path, index=False)
            return True
        except :
            return False

    def getJsonData(self):
        json = {
            "clist": []
        }
        for cam in self.cameraList :
            camera = {
                "name": cam.name,
                "ip": cam.url,
                "status": cam.status.value,
                "imgType": cam.imgType
            }
            json["clist"].append(camera)
        return json