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
	- pip install numpy
	- pip install opencv-python (opencv-python==4.4.0.46 -> előfordulhat hogy a legújabb nem jó)
	- pip install urllib3
	- pip install pandas
	- pip install flask
	- pip install requests
	- conda install pystan -c conda-forge
	- conda install -c conda-forge fbprophet
- Anaconda telepítés: (A prophethez kelleni fog)
	1. https://www.anaconda.com/products/individual#windows -> alján a 64 bites verziót
	2. Indítsd el a telepített parancssort rendszergazdaként
	3. conda create -n v-env python=3.6.8
	4. Innentől jobb ha a vscode/pycharm konzolából nyomod tovább
	5. a vscode/pycharmban rakd be interpreterként a C:\Users\<NEVED>\anaconda3\envs\v-env\python.exe
	6. conda install libpython m2w64-toolchain -c msys2
	7. Ha nincs \Lib\distutils\distutils.cfg akkor csináld meg ezzel a kóddal:
[build]
compiler=mingw32
	8. conda install numpy cython -c conda-forge
	9. conda install matplotlib scipy pandas -c conda-forge
	10. conda install pystan -c conda-forge
	11. conda install -c conda-forge fbprophet
	12. Elv így működik, "from fbprophet import Prophet és import pystan" nézd meg dob a hibát

