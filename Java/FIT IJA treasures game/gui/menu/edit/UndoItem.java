
package Labyrinth.gui.menu.edit;

import Labyrinth.Game;
import Labyrinth.events.HistoryListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Observable;
import java.util.Observer;
import javax.swing.JMenuItem;

/**
 * Load game menu item
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class UndoItem extends JMenuItem implements ActionListener, Observer
{
    /**
     * Create undo menu item
     */
    public UndoItem()
    {
        setText("Undo");
        addActionListener(this);
        setEnabled(Game.hasHistory());
        HistoryListener.getInstance().addObserver(this);
    }

    /**
     * Back game undo after click
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.undo();
    }
    
    /**
     * Update game window in depends on Game menu
     * @param o Observable object
     * @param arg Game object
     */
    public void update(Observable o, Object arg)
    {
        setEnabled(Game.hasHistory());        
        revalidate();
   }
}
