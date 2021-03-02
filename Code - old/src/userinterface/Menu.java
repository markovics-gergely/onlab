package userinterface;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Pane;
import org.opencv.core.Core;
import org.opencv.video.Video;

public class Menu implements ControlledScreen {
    private ScreenController actualScreen;

    @FXML
    private Pane webcamPlace = new Pane();
    @FXML
    private Button connectButton = new Button();
    @FXML
    private Button disconnectButton = new Button();
    @FXML
    private AnchorPane menu = new AnchorPane();

    @FXML
    public void connectCamera(){
        Cv
    }
    @FXML
    public void disconnectCamera(){
    }


    @Override
    public void setActualScreen(ScreenController actScreen) {
        actualScreen = actScreen;
    }
    @Override
    public void setNextScreen() { }
    @Override
    public void initialize() {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }
}
