package userinterface;

import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.layout.StackPane;

import java.util.HashMap;

public class ScreenController extends StackPane {
    private HashMap<String, Node> screens = new HashMap<>();

    public void loadScreen(String name, String fxml) {
        try {
            FXMLLoader myLoader = new FXMLLoader(getClass().getResource(fxml));
            Parent loadScreen = (Parent) myLoader.load();
            ControlledScreen actScreen = ((ControlledScreen) myLoader.getController());

            actScreen.setActualScreen(this);
            screens.put(name, loadScreen);
        } catch (Exception e) {
            System.out.println(e.getLocalizedMessage());
        }
    }
    public void setScreen(String name) {
        if (screens.get(name) != null)
            getChildren().add(screens.get(name));
        else
            System.out.println("Nem töltött be!");
    }
    public void removeScreen(String name){
        if (screens.get(name) != null) {
            getChildren().removeAll(screens.get(name));
            screens.remove(name);
        }
    }
}
