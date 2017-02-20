
package Labyrinth.gui.lables;

import java.awt.Dimension;
import java.net.URL;
import javax.swing.ImageIcon;
import javax.swing.JLabel;

/**
 * Base label for card
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CardLabel extends JLabel
{
    /**
     * Create a new card label with image
     * @param resource Image card resource
     */
    public CardLabel(URL resource)
    {
        setPreferredSize(new Dimension(60, 60));
        setIcon(new ImageIcon(resource));
    }
    
    /**
     * Create a new card label
     */
    public CardLabel()
    {
        setPreferredSize(new Dimension(60, 60));
    }
}
