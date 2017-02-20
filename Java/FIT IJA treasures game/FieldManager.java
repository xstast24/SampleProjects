
package Labyrinth;

import Labyrinth.treasures.TreasureCard;
import java.util.ArrayList;

/**
 * Field manager
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class FieldManager 
{
    /**
     * Shift board line to right
     * @param line Number of line
     */
    public static void shiftLine(int line)
    {
        Board board = Game.getActualGame().getBoard();
        Field field = board.get(board.getSize(), line);
        TreasureCard lastTreasureCard = field.getCard();
        Stone lastStone = field.getStone();
        ArrayList<Player> lastPlayers = field.getPlayers();
        for (int i = board.getSize(); i > 1; i--) {
            Field actualField = board.get(i, line);
            Field prevField = board.get(i - 1, line);
            TreasureCard tmpCard = prevField.getCard();
            Stone tmpStone = prevField.getStone();
            ArrayList<Player> tmpPlayers = prevField.getPlayers();
            actualField.setCard(tmpCard);
            actualField.setPlayers(tmpPlayers);
            actualField.setStone(tmpStone);
            for (Player player : tmpPlayers) {
                player.setActualField(actualField);
            }
        }
        for (Player player : lastPlayers) {
            player.setActualField(board.get(1, line));
        }
        board.get(1, line).setStone(board.getFreeStone());
        board.get(1, line).setPlayers(lastPlayers);
        board.get(1, line).setCard(lastTreasureCard);
        board.setFreeStone(lastStone);
        updatePlayers();
    }
    
    /**
     * Move column down
     * @param column Number of column
     */
    public static void shiftColumn(int column)
    {
        Board board = Game.getActualGame().getBoard();
        Field field = board.get(column, board.getSize());
        TreasureCard lastTreasureCard = field.getCard();
        Stone lastStone = field.getStone();
        ArrayList<Player> lastPlayers = field.getPlayers();
        for (int i = board.getSize(); i > 1; i--) {
            Field actualField = board.get(column, i);
            Field prevField = board.get(column, i - 1);
            TreasureCard tmpCard = prevField.getCard();
            Stone tmpStone = prevField.getStone();
            ArrayList<Player> tmpPlayers = prevField.getPlayers();
            actualField.setCard(tmpCard);
            actualField.setPlayers(tmpPlayers);
            actualField.setStone(tmpStone); 
            for (Player player : tmpPlayers) {
                player.setActualField(actualField);
            }
        }
        for (Player player : lastPlayers) {
            player.setActualField(board.get(column, 1));
        }
        board.get(column, 1).setStone(board.getFreeStone());
        board.get(column, 1).setPlayers(lastPlayers);
        board.get(column, 1).setCard(lastTreasureCard);
        board.setFreeStone(lastStone);
        updatePlayers();
    }
    
    private static void updatePlayers()
    {
        for (Player player : Game.getActualGame().getPlayers()) {
            player.setCanMove(true);
        }
        Game.getActualGame().getActualPlayer().setCanMove(false);
    }
}
