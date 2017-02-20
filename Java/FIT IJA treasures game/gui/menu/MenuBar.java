
package Labyrinth.gui.menu;

import Labyrinth.gui.menu.game.GameMenu;
import Labyrinth.gui.menu.edit.EditMenu;
import javax.swing.JMenuBar;

/**
 * Menu for game
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class MenuBar extends JMenuBar
{
    /**
     * Create menu bar
     */
    public MenuBar()
    {
        add(new GameMenu());
        add(new EditMenu()); 
    }
}
