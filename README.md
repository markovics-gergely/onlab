# Onlab
## Specifikáció
> Pláza kamerafigyelő alkalmazás => emberek életkora(kbra)/neme felismerés
- Idő intervallumokra osztása (pl 2-3 órákra)
- Intervallumokat felismert emberek alapján csoportokba rendezése (ez az alapja a reklámoknak):
	1. Családok: Kb ugyanannyi felnőtt és gyerek
	2. Férfi: nagyrészt férfiak
	3. Női: nagyrészt nők
	4. Párok: kb ugyanannyi férfi és nő
	5. Fiatalok: nagyrészt fiatalok
	6. Még jó lenne pár megkülönböztethető csoport
- Tulajdonképpen reklámfigyelő helyett kamerában megjelenő emberek csoportokba osztása
- Eddigi adatok alapján az intervallum kezdése előtt megtippeli a következőt (mint egy időjárásjelentő)

## Linkek:
- [Face api](https://github.com/justadudewhohacks/face-api.js)
- [OpenCV](https://www.youtube.com/watch?v=oXlwWbU8l2o)
- [Amazon](https://docs.aws.amazon.com/rekognition/latest/dg/faces.html)
- [Tensorflow](https://www.codeproject.com/Articles/5276827/AI-Age-Estimation-in-the-Browser-using-face-api-an)

- [Prophet](https://facebook.github.io/prophet/)

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
