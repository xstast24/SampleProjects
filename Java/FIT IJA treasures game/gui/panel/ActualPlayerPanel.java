
package Labyrinth.gui.panel;

import Labyrinth.Game;
import Labyrinth.Player;
import java.awt.Color;
import java.awt.Dimension;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JPanel;

/**
 * Actual player info panel
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class ActualPlayerPanel extends JPanel
{
    /**
     * Create panel
     */
    public ActualPlayerPanel()
    {
        Player player = Game.getActualGame().getActualPlayer();
        setBorder(BorderFactory.createTitledBorder("Actual player (" + player.getId() + "):")); 
        setPreferredSize(new Dimension(140, 100));
        JButton button = new JButton();
        button.setBackground(this.getPlayerColor(player));
        button.setPreferredSize(new Dimension(60, 60));
        button.setEnabled(false);
        add(button);
    }
    
    /**
     * Translate string color name to Color constant
     * @param player Player entity
     * @return Player color
     */
    private Color getPlayerColor(Player player)
    {
        if (player.getColorName().compareTo("red") == 0) {
            return Color.RED;
        } else if (player.getColorName().compareTo("green") == 0) {
            return Color.GREEN;
        } else if (player.getColorName().compareTo("blue") == 0) {
            return Color.BLUE;
        } else {
            return Color.YELLOW;
        }
    }
}
