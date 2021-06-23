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
> Kamera Figyelő Alkalmazás
Koncepció:
- Az alkalmazás megfigyeli a kamera előtt elhaladó embereket
- Elhaladó emberek életkora és neme alapján csoportokba osztja őket
- A csoportokat adott intervallumok szerint határozza meg
- Az intervallumok előre meg vannak határozva, egy napot kisebb egységekre bontva (pl. a napot 1-2 órás darabokra szedjük)
- Képes megtippelni, hogy a felhasználó által megadott jövőbeli időponthoz tartozó intervallumban milyen csoportból mennyi van

## Linkek:
- [Face api](https://github.com/justadudewhohacks/face-api.js)
- [OpenCV](https://www.youtube.com/watch?v=oXlwWbU8l2o)
- [Prophet](https://facebook.github.io/prophet/)

## Felhasználói felület
- Felhasználó bead ip-címet/címeket amiket figyel
- Le lehessen állítani a kamerák figyelését
- Felhasználó választhasson egy jövőbeli időpontot, és megtippeli milyen csoportból mennyi lesz jelen az idősávban amibe esik
### Képek
> Kamera Kezelő Felület
![Camera Manager felület](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/cam1.png)
![Camera hozzáadása](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/camadd.png)
![Camera lementett értékei](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/camtable.png)
> Predikció lekérdezés felülete
![Predikció indítása](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/predstart.png)
![Predikció életkor érték](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/pred1.png)
![Predikció nem érték](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/pred2.png)
![Predikció nem grafikon](https://github.com/markovics-gergely/onlab/blob/main/Dokumentáció/pics/pred3.png)

## Felhasznált könyvtárak és útmutató
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
	5. a vscode/pycharmban rakd be interpreterként a C:\Users\NEVED\anaconda3\envs\v-env\python.exe
	6. conda install libpython m2w64-toolchain -c msys2
	7. Ha nincs \Lib\distutils\distutils.cfg akkor csináld meg ezzel a kóddal:
[build]
compiler=mingw32
	8. conda install numpy cython -c conda-forge
	9. conda install matplotlib scipy pandas -c conda-forge
	10. conda install pystan -c conda-forge
	11. conda install -c conda-forge fbprophet
	12. pip install --upgrade plotly (hogy ne dobjon hibát)
