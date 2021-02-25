package logic;

/*import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.opencv.videoio.VideoCapture;*/

import org.bytedeco.javacv.*;

public class Program {
    public Program(){
        //System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    public void connectCamera(){
        //VideoCapture camera = new VideoCapture("http://192.168.0.176:8080");
        OpenCVFrameGrabber grabber = new OpenCVFrameGrabber(0);
        try{
            grabber.start();
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }

    public void start(){
        /*String imgFile = "images/FacePhoto1.PNG";
        Mat src = Imgcodecs.imread(imgFile);

        String xmlFile = "xml/lbpcascade_frontalface.xml";
        CascadeClassifier cc = new CascadeClassifier(xmlFile);

        MatOfRect faceDetect = new MatOfRect();
        cc.detectMultiScale(src, faceDetect);

        System.out.println(String.format("Detected faces: %d", faceDetect.toArray().length));
        for(Rect rect : faceDetect.toArray())
            Imgproc.rectangle(src, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y+ rect.height), new Scalar(0,0,255), 3);

        Imgcodecs.imwrite("images/FacePhoto1out.PNG", src);
        System.exit(0);*/
    }
}
