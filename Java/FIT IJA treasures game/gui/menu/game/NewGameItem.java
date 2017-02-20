
package Labyrinth.gui.menu.game;

import Labyrinth.Game;
import Labyrinth.gui.GameWindow;
import Labyrinth.gui.dialogs.NewGameDialog;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;

/**
 * New game item for game menu
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class NewGameItem extends JMenuItem implements ActionListener
{
    /**
     * Create new game menu item
     */
    public NewGameItem()
    {
        setText("New game");
        addActionListener(this);
    }

    /**
     * Open new game dialog
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        NewGameDialog newGameDialog = new NewGameDialog();
        newGameDialog.open();
    }
}
