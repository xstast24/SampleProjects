
package Labyrinth.gui.buttons;

import Labyrinth.Game;
import java.net.URL;
import javax.swing.ImageIcon;
import javax.swing.JButton;

/**
 * Base shift button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class ShiftButton extends JButton
{
    protected int cord;
    
    /**
     * Create base shift button
     * @param cord Line or column cord
     * @param url image URL
     */
    public ShiftButton(int cord, URL url)
    {
        setFocusable(false);
        this.cord = cord;
        if (cord % 2 == 0) {
            setIcon(new ImageIcon(url));
        } else {
            setEnabled(false);
        } 
        if (!Game.getActualGame().getActualPlayer().canMove()) {
            setEnabled(false);
        }
    }
}
