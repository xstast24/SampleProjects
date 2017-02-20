
package Labyrinth.gui.buttons;

import java.awt.Dimension;
import javax.swing.JButton;

/**
 * Base card button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CardButton extends JButton
{
    /**
     * Create card button
     */
    public CardButton()
    {
        setPreferredSize(new Dimension(60, 60));
        setFocusable(false);
    }
}
