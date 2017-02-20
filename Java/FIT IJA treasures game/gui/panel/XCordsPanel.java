
package Labyrinth.gui.panel;

import Labyrinth.Game;
import Labyrinth.gui.GameWindow;
import Labyrinth.gui.buttons.DownButton;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.JPanel;

/**
 * X cords panel for display shift buttons
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class XCordsPanel extends JPanel
{
    /**
     * Create a new panel
     * @param window Actual game window
     */
    public XCordsPanel(GameWindow window)
    {
        int size = Game.getActualGame().getBoard().getSize();
        setLayout(new GridLayout(1, size));
        setPreferredSize(new Dimension(60 * size, 16));
        for (int i = 1; i <= size; i++) {
            add(new DownButton(i, window));
        }
    }
}
