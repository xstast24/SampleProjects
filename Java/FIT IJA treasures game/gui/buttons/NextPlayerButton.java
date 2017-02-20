
package Labyrinth.gui.buttons;

import Labyrinth.Game;
import Labyrinth.gui.GameWindow;
import Labyrinth.events.GameListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;

/**
 * Next player button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class NextPlayerButton extends JButton implements ActionListener
{
    private GameWindow window;
    
    /**
     * Create button
     * @param window Actual game window 
     */
    public NextPlayerButton(GameWindow window)
    {
        this.window = window;
        setText("Next player!");
        addActionListener(this);
        setFocusable(false);
    }

    /**
     * Set next player as actual
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.storeState();
        Game.getActualGame().nextPlayer();
        GameListener.getInstance().emit();
    }
}
