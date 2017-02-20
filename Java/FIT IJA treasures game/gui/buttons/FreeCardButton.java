
package Labyrinth.gui.buttons;

import Labyrinth.Board;
import Labyrinth.Game;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.ImageIcon;

/**
 * Free card button
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class FreeCardButton extends CardButton implements ActionListener
{
    /**
     * Create free card button
     */
    public FreeCardButton()
    {
        Board board = Game.getActualGame().getBoard();
        setIcon(new ImageIcon(board.getFreeStone().getStoneImage()));
        addActionListener(this);
        setFocusable(false);
    }

    /**
     * Turn right free stone after click
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        Game.storeState();
        Board board = Game.getActualGame().getBoard();
        board.getFreeStone().turnRight();
        setIcon(new ImageIcon(board.getFreeStone().getStoneImage()));
        revalidate();
    }
}
