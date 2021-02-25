package userinterface;

import javafx.scene.image.ImageView;
import javafx.scene.layout.Background;

import java.util.ArrayList;

public class Menu implements ControlledScreen {
    private ScreenController actualScreen;

    @Override
    public void setActualScreen(ScreenController actScreen) {
        actualScreen = actScreen;
    }
    @Override
    public void setNextField() { }
    @Override
    public void initialize() { }
}
