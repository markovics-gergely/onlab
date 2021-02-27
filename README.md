# Önlab
## Specifikáció
> Pláza kamerafigyelő alkalmazás => emberek életkora(kbra)/neme felismerés
- Idő intervallumokra osztása (pl 2-3 órákra)
- Intervallumokat felismert emberek alapján csoportokba rendezése (ez az alapja a reklámoknak):
	1. Családok: Kb ugyanannyi felnőtt és gyerek
	2. Férfi: nagyrészt férfiak
	3. Női: nagyrészt nők
	4. Párok: kb ugyanannyi férfi és nő
	5. Fiatalok: nagyrészt fiatalok
	6. Idősek: nagyrészt idősek
	7. Még jó lenne pár megkülönböztethető csoport
- Tulajdonképpen reklámfigyelő helyett kamerában megjelenő emberek csoportokba osztása
- Eddigi adatok alapján az intervallum kezdése előtt megtippeli a következőt (Idősávok alapján is nézi)
## Linkek:
- [Face api](https://github.com/justadudewhohacks/face-api.js)
- [OpenCV](https://www.youtube.com/watch?v=oXlwWbU8l2o)
- [Amazon](https://docs.aws.amazon.com/rekognition/latest/dg/faces.html) *Favorite*
- [Tensorflow](https://www.codeproject.com/Articles/5276827/AI-Age-Estimation-in-the-Browser-using-face-api-an)
- [Prophet](https://facebook.github.io/prophet/)

## Felhasználói felület
- Felhasználó bead ip-címet/címeket amiket figyel
- Le lehessen állítani a kamerák figyelését
- Felhasználó választhasson egy jövőbeli időpontot, és megtippeli milyen csoport lesz jelen az idősávban amibe esik

## Felhasznált cuccok
- Python 3.6.8
- Python libek:
	- numpy
	- opencv-python
	- urllib3
	- face_recognition (kell hozzá cmake és dlib)
	
## Felhasznált segítségek
-[Webcam Face Recognition](https://www.youtube.com/watch?v=lC_y8wD7F3Y)
-[IPcam Face Detection](https://www.youtube.com/watch?v=0hT2cGSqPfk)

## Dokumentáció
- Függvények:
	- webcam(): Egyszerűen beveszi a webkamera videó képét és kivetíti.
	- ipcam(): Az IP kamera képét framenként veszi be és kívetíti.
	- webcamFaceDetect(): Ez fel is ismeri, hogy ki van a képen egy előre megadott kép alapján és a webcamera képét adja vissza egy kerettel és névvel.
	- ipcamFaceDetect(): Ez nem ismeri fel ki van rajta, csak az arcot, azonban itt nem framenként veszi, hanem a tényleges videót rakja ki.
