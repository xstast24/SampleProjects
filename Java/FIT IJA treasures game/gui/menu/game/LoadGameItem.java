
package Labyrinth.gui.menu.game;

import Labyrinth.Game;
import Labyrinth.events.GameListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JMenuItem;

/**
 * Load game menu item
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class LoadGameItem extends JMenuItem implements ActionListener
{
    /**
     * Crate a new load item
     */
    public LoadGameItem()
    {
        setText("Load game");
        addActionListener(this);
    }

    /**
     * Run Game.load() for open load dialog and load game
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.loadGame();
        GameListener.getInstance().emit();
    }
}
