
package Labyrinth.gui.panel;

import Labyrinth.Player;
import Labyrinth.gui.lables.CardLabel;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JPanel;
import javax.swing.border.TitledBorder;

/**
 * Display player obtained cards for winner display
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class PlayerCardListPanel extends JPanel
{
    /**
     * Display obtained cards for concrete player
     * @param player Concrete player
     */
    public PlayerCardListPanel(Player player)
    {
        setLayout(new GridLayout(1, 12));
        setPreferredSize(new Dimension(100*12, 100));
        String message = "Player " + player.getId();
        if (player.isWinner()) {
            message += " WINNER";
        }
        TitledBorder border = BorderFactory.createTitledBorder(message);
        border.setTitleColor(player.getColor());
        setBorder(border);
        for (int i = 0; i < 12; i++) {
            CardLabel label = new CardLabel();
            if (i < player.getCards().size()) {
                label.setIcon(new ImageIcon(player.getCards().get(i).getBigImageResource()));
            }
            add(label);
        }
    }
}
