module Code {
    requires javafx.fxml;
    requires javafx.controls;
    requires org.bytedeco.javacv;
    //requires opencv;

    opens logic;
    opens userinterface;
}