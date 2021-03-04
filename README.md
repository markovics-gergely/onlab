# Önlab
## Ütemterv
- OpenCV: Perzisztencia, Intervallum szerinti lementés
- OpenCV: Szálkezelés, Indítás/Leállítás
- Prophet: Váz elkészítése, Adatok olvasása
- Prophet: Befejezés, Bemenet/Kimenet kész
- Web: Kezdetleges váz elkészítése
- Web: Szerver/Kliens kommunikáció a vázzal
- Web: Felhasználói felület kialakítása
## Specifikáció
> Pláza kamerafigyelő alkalmazás => emberek életkora(kbra)/neme felismerés
- Idő intervallumokra osztása (pl 2-3 órákra)
- Intervallumokat felismert emberek alapján csoportokba rendezése (ez az alapja a reklámoknak):
	- Családok: Kb ugyanannyi felnőtt és gyerek
	- Férfi: nagyrészt férfiak
	- Női: nagyrészt nők
	- Párok: kb ugyanannyi férfi és nő
	- Fiatalok: nagyrészt fiatalok
	- Idősek: nagyrészt idősek
	- Még jó lenne pár megkülönböztethető csoport
- Tulajdonképpen reklámfigyelő helyett kamerában megjelenő emberek csoportokba osztása
- Eddigi adatok alapján az intervallum kezdése előtt megtippeli a következőt (Idősávok alapján is nézi)
## Linkek:
- [Face api](https://github.com/justadudewhohacks/face-api.js)
- [OpenCV](https://www.youtube.com/watch?v=oXlwWbU8l2o)
- [Prophet](https://facebook.github.io/prophet/)
- [Python threading tutorial](https://realpython.com/intro-to-python-threading/)

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
	- (Később kelleni fog egy age és gender detection, sokféle van)
		- https://www.youtube.com/watch?v=bAOdXTDuha8
		- https://www.youtube.com/watch?v=q_JF0GSRPXA
	- django (web framework)
	
## Felhasznált segítségek
- [Webcam Face Recognition](https://www.youtube.com/watch?v=lC_y8wD7F3Y)
- [IPcam Face Detection](https://www.youtube.com/watch?v=0hT2cGSqPfk)

## Dokumentáció
- Függvények:
	- **ipcamFaceDetect()**: Ez nem ismeri fel ki van rajta, csak az arcot, azonban itt nem framenként veszi, hanem a tényleges videót rakja ki.
