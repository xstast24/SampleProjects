
package Labyrinth.gui.buttons;

import Labyrinth.Game;
import Labyrinth.Player;
import Labyrinth.treasures.TreasureCard;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;
import javax.swing.ImageIcon;

/**
 * Card pack button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CardPackButton extends CardButton implements ActionListener
{
    /**
     * Create card pack button and display image
     */
    public CardPackButton()
    {
        Player player = Game.getActualGame().getActualPlayer();
        URL resource;
        if (player.getActualCard() == null) {
            resource = TreasureCard.getDefaultCard();
            addActionListener(this);
        } else {
            resource = player.getActualCard().getBigImageResource();
        }
        setIcon(new ImageIcon(resource));
        setFocusable(false);
    }

    /**
     * Pop card
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e) {
        Game.storeState();
        if (Game.getActualGame().getCardPack().getCount() == 0) {
            setIcon(new ImageIcon(TreasureCard.getDefaultCard()));
        } else {
            Player player = Game.getActualGame().getActualPlayer();
            if (player.getActualCard() == null) {
                player.setActualCard(Game.getActualGame().getCardPack().popCard());
                setIcon(new ImageIcon(player.getActualCard().getBigImageResource()));
            }
        }
        revalidate();
    }
}
