module Code {
    requires javafx.fxml;
    requires javafx.controls;
    /*requires org.bytedeco.javacv;
    requires org.bytedeco.opencv;
    requires javafx.swing;
    requires org.bytedeco.ffmpeg;*/
    requires opencv;

    opens logic;
    opens userinterface;
}