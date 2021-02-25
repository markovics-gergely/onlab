package userinterface;

import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {
    public static String menuID = "menu";
    public static String menuFXML = "menu.fxml";

    @Override
    public void start(Stage primaryStage) {
        ScreenController actualScreen = new ScreenController();

        actualScreen.loadScreen(Main.menuID, Main.menuFXML);
        actualScreen.setScreen(Main.menuID);

        primaryStage.setResizable(false);

        Group root = new Group();
        root.getChildren().addAll(actualScreen);
        Scene scene = new Scene(root);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
