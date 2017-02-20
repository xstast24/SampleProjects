
package Labyrinth.gui.panel;

import Labyrinth.Game;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;

/**
 * Game info panel
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GameInfoPanel extends JPanel
{
    /**
     * Create game info panel
     */
    public GameInfoPanel()
    {
        setLayout(new GridBagLayout());
        setBorder(BorderFactory.createTitledBorder("Game:"));
        setMinimumSize(new Dimension(200, 100));
        
        GridBagConstraints cs = new GridBagConstraints();
        
        cs.fill = GridBagConstraints.HORIZONTAL;
        
        cs.gridx = 0;
        cs.gridy = 0;
        cs.gridwidth = 2;
        add(new JLabel("Name: "), cs);
        
        cs.gridx = 2;
        cs.gridy = 0;
        cs.gridwidth = 3;        
        add(new JLabel(Game.getActualGame().getName()), cs);
        
        cs.gridx = 0;
        cs.gridy = 1;
        cs.gridwidth = 2;
        add(new JLabel("Count of players: "), cs);
        
        cs.gridx = 2;
        cs.gridy = 1;
        cs.gridwidth = 2;
        int coutOfPlayers = Game.getActualGame().getCountOfPlayers();
        add(new JLabel(String.valueOf(coutOfPlayers)), cs);
        
        cs.gridx = 0;
        cs.gridy = 2;
        cs.gridwidth = 2;
        add(new JLabel("Size: "), cs);
        
        cs.gridx = 2;
        cs.gridy = 2;
        cs.gridwidth = 3;        
        add(new JLabel(String.valueOf(Game.getActualGame().getBoard().getSize())), cs);
    }
}
