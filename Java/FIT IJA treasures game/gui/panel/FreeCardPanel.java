
package Labyrinth.gui.panel;

import Labyrinth.gui.buttons.FreeCardButton;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JPanel;

/**
 * Free card panel
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class FreeCardPanel extends JPanel
{
    /**
     * Create a panel
     */
    public FreeCardPanel()
    {
        setBorder(BorderFactory.createTitledBorder("Free card:")); 
        setPreferredSize(new Dimension(100, 100));
        add(new FreeCardButton());
    }
}
