
package Labyrinth.gui.buttons;

import Labyrinth.FieldManager;
import Labyrinth.Game;
import Labyrinth.gui.GameWindow;
import Labyrinth.events.GameListener;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JOptionPane;

/**
 * Right button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class RightButton extends ShiftButton implements ActionListener
{    
    private GameWindow window;
    
    /**
     * Create button
     * @param y Cords
     * @param window Actual game window
     */
    public RightButton(int y, GameWindow window)
    {
        super(y, RightButton.class.getClassLoader().getResource("lib/images/arrows/right.png"));
        this.window = window;
        setPreferredSize(new Dimension(16, 60));
        addActionListener(this);
    }

    /**
     * Shift line after click
     * @param e Action event 
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.storeState();
        if (Game.getActualGame().getActualPlayer().getActualCard() == null) {
            JOptionPane.showMessageDialog(null, "You must first select card from card pack");
        } else {
            FieldManager.shiftLine(this.cord);
            GameListener.getInstance().emit();
        }
    }
}
