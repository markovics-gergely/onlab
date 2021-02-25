module Code {
    requires javafx.fxml;
    requires javafx.controls;
    requires opencv;
    requires org.bytedeco.javacv;
    requires org.bytedeco.javacpp;

    opens logic;
}