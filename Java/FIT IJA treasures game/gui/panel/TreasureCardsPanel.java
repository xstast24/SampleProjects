
package Labyrinth.gui.panel;

import Labyrinth.Game;
import Labyrinth.gui.lables.CardLabel;
import Labyrinth.treasures.TreasureCard;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.util.ArrayList;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JPanel;

/**
 * Display player obtained cards
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class TreasureCardsPanel extends JPanel
{
    /**
     * Create panel
     */
    public TreasureCardsPanel()
    {
        setLayout(new GridLayout(8, 3));
        setPreferredSize(new Dimension(60*2, 60*6));
        setBorder(BorderFactory.createTitledBorder("Obtained cards:"));
        for (int i = 0; i < 12; i++) {
            ArrayList<TreasureCard> cards = Game.getActualGame().getActualPlayer().getCards();
            CardLabel button = new CardLabel();
            if (i < cards.size()) {
                TreasureCard card = Game.getActualGame().getActualPlayer().getCards().get(i);
                button.setIcon(new ImageIcon(card.getBigImageResource()));                
            }            
            add(button);
        }
    }
}
