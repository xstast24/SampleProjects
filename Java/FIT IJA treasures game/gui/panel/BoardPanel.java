
package Labyrinth.gui.panel;

import Labyrinth.Board;
import Labyrinth.Field;
import Labyrinth.Game;
import Labyrinth.Player;
import Labyrinth.Stone;
import Labyrinth.gui.lables.CardLabel;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;
import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.border.Border;

/**
 * Panel with game map
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class BoardPanel extends JPanel
{
    /**
     * Create map
     */
    public BoardPanel()
    {
        Board board = Game.getActualGame().getBoard();
        int size = Game.getActualGame().getBoard().getSize();
        setLayout(new GridLayout(size, size));
        setPreferredSize(new Dimension(60*size, 60*size));
        
        try {
            for (int y = 1; y <= size; y++) {
                for (int x = 1; x <= size; x++) {
                Field field = board.get(x, y);
                Stone stone =  field.getStone();
                ArrayList<Player> players = field.getPlayers();

                BufferedImage image = ImageIO.read(stone.getStoneImage());
                for (Player player : players) {
                    BufferedImage overlay = ImageIO.read(player.getColorResource());
                    Graphics g = image.getGraphics();
                    g.drawImage(image, 0, 0, null);
                    g.drawImage(overlay, 0, 0, null);
                }
                if (field.getCard() != null) {
                    BufferedImage overlay = ImageIO.read(field.getCard().getSmallImageResource());
                    Graphics g = image.getGraphics();
                    g.drawImage(image, 0, 0, null);
                    g.drawImage(overlay, 0, 0, null);
                }
                CardLabel cardLabel = new CardLabel();
                cardLabel.setIcon(new ImageIcon(image));
                cardLabel.setBorder(BorderFactory.createLineBorder(Color.GRAY));
                add(cardLabel);
            }
            }
        } catch (IOException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Missing image resource");
        }
    }
}
