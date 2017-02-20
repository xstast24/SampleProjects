
package Labyrinth.gui.panel;

import Labyrinth.Game;
import Labyrinth.gui.GameWindow;
import Labyrinth.gui.buttons.RightButton;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.JPanel;

/**
 * Y cords panel for display shift buttons
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class YCordsPanel extends JPanel
{
    /**
     * Create a new panel
     * @param window Actual game window
     */
    public YCordsPanel(GameWindow window)
    {
        int size = Game.getActualGame().getBoard().getSize();
        setLayout(new GridLayout(size, 1));
        setPreferredSize(new Dimension(16, 60 * size));
        for (int i = 1; i <= size; i++) {
            add(new RightButton(i, window));
        }
    }
}
