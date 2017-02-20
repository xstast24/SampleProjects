
package Labyrinth.gui;

/**
 * Core Game GUI
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GameGUI
{
    /**
     * Create a new Game window
     */
    public void create()
    {
        GameWindow window = GameWindow.create();        
        window.pack();        
        window.setVisible(true);
    }
}
