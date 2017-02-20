
package Labyrinth.gui.panel;

import Labyrinth.gui.GameWindow;
import Labyrinth.gui.buttons.NextPlayerButton;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JPanel;

/**
 * Panel with next player button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class NexPlayerPanel extends JPanel
{
    /**
     * Create panel
     * @param window Actual game window
     */
    public NexPlayerPanel(GameWindow window)
    {
        setBorder(BorderFactory.createTitledBorder("Next player:")); 
        setPreferredSize(new Dimension(150, 60));
        add(new NextPlayerButton(window));
    }
}
