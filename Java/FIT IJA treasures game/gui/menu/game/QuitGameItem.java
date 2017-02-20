
package Labyrinth.gui.menu.game;

import Labyrinth.Game;
import Labyrinth.events.GameListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JMenuItem;

/**
 * Quit game menu item
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class QuitGameItem extends JMenuItem implements ActionListener
{    
    /**
     * Add new Quit game item
     */
    public QuitGameItem()
    {
        setText("Quit game");
        addActionListener(this);
    }

    /**
     * Remove actual game after click
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.quit();
    }    
}
