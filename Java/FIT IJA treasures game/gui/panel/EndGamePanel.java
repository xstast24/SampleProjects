
package Labyrinth.gui.panel;

import Labyrinth.Game;
import Labyrinth.Player;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.util.ArrayList;
import javax.swing.JPanel;

/**
 * End game panel display all cards for players
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class EndGamePanel extends JPanel
{
    /**
     * Create panel with extra card panel for each player
     */
    public EndGamePanel()
    {
        setLayout(new GridBagLayout());
        GridBagConstraints gc1 = new GridBagConstraints();
        ArrayList<Player> players = Game.getActualGame().getPlayers();
        for (int i = 0; i < Game.getActualGame().getCountOfPlayers(); i++) {
            gc1.gridx = 0;
            gc1.gridy = i;
            gc1.anchor = GridBagConstraints.WEST;
            gc1.fill = GridBagConstraints.VERTICAL;
            add(new PlayerCardListPanel(players.get(i)), gc1);
        }       
    }
}
