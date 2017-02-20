
package Labyrinth.gui.panel;

import Labyrinth.gui.GameWindow;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import javax.swing.JPanel;

/**
 * Game panel
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GamePanel extends JPanel
{
    /**
     * Create game panel
     * @param window Actual game window
     */
    public GamePanel(GameWindow window)
    {
        setLayout(new GridBagLayout());

        GridBagConstraints gc1 = new GridBagConstraints();
        
        gc1.gridx = 0;
        gc1.gridy = 1;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new ActualPlayerPanel(), gc1);
        
        gc1.gridx = 0;
        gc1.gridy = 2;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new NexPlayerPanel(window), gc1);
        
        gc1.gridx = 0;
        gc1.gridy = 3;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new FreeCardPanel(), gc1);
        
        gc1.gridx = 0;
        gc1.gridy = 4;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new CardPackPanel(), gc1);
        
        gc1.gridx = 0;
        gc1.gridy = 5;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new GameInfoPanel(), gc1);        
        
        gc1.gridx = 1;
        gc1.gridy = 0;
        gc1.gridheight = 7;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new BodyPanel(window), gc1);
        
        gc1.gridx = 3;
        gc1.gridy = 0;
        gc1.gridheight = 8;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new TreasureCardsPanel(), gc1);
    }
}
