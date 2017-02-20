
package Labyrinth.gui.menu.game;

import Labyrinth.Game;
import Labyrinth.events.NewGameListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Observer;
import javax.swing.JMenuItem;

/**
 * Save game menu item
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class SaveGameItem extends JMenuItem implements ActionListener, Observer
{
    /**
     * Added a new menu item
     */
    public SaveGameItem()
    {
        setText("Save game");
        addActionListener(this);
        if (Game.getActualGame() == null) {
            setEnabled(false);
        }
        NewGameListener.getInstance().addObserver(this);
    }
 
    /**
     * Open file save dialog and store actual game
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.saveGame();
    }
    
    public void update(java.util.Observable o, Object arg)
    {
        setEnabled(true);
        revalidate();
    }
}
