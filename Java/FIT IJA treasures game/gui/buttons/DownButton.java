
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
 * Down button for shift field
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class DownButton extends ShiftButton implements ActionListener
{    
    private GameWindow window;
    
    /**
     * Create a down button
     * @param y cords
     * @param window Actual game window
     */
    public DownButton(int y, GameWindow window)
    {
        super(y, DownButton.class.getClassLoader().getResource("lib/images/arrows/down.png"));
        this.window = window;
        setPreferredSize(new Dimension(60, 16));
        addActionListener(this);
    }
    
    /**
     * Shift column after click
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.storeState();
        if (Game.getActualGame().getActualPlayer().getActualCard() == null) {
            JOptionPane.showMessageDialog(null, "You must first select card from card pack");
        } else {
            FieldManager.shiftColumn(this.cord);
            GameListener.getInstance().emit();
        }
    }
}
