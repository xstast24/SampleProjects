
package Labyrinth.gui.panel;

import Labyrinth.gui.buttons.CardPackButton;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JPanel;

/**
 * Card pack panel
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CardPackPanel extends JPanel
{
    /**
     * Added card pack panel
     */
    public CardPackPanel()
    {
        setBorder(BorderFactory.createTitledBorder("Card pack:"));
        setPreferredSize(new Dimension(100, 100));
        add(new CardPackButton()); 
    }
}
