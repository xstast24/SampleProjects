
package Labyrinth.gui.menu.game;

import javax.swing.JMenu;

/**
 * Game menu
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GameMenu extends JMenu
{
    /**
     * Create game menu
     */
    public GameMenu()
    {
        setText("Game");
        add(new NewGameItem());
        add(new LoadGameItem());
        add(new SaveGameItem());
        add(new QuitGameItem());
    }
}
