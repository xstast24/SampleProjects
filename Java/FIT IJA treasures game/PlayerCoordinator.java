
package Labyrinth;

/**
 * Class for move player figure
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class PlayerCoordinator 
{
    /**
     * Move player into new field
     * @param way Way for next stone
     * @return Returns true if is move OK
     */
    public static boolean move(Stone.CANGO way)
    {
        Player player = Game.getActualGame().getActualPlayer();
        Field field = player.getActualField();
        if (field.getStone().canGo(way)) {
            int x = field.getX(), y = field.getY();
            if (way == Stone.CANGO.LEFT) {
                x = field.getX() - 1;
            } else if (way == Stone.CANGO.UP) {
                y = field.getY() - 1;
            } else if (way == Stone.CANGO.RIGHT) {
                x = field.getX() + 1;
            } else {
                y = field.getY() + 1;
            }
            Field nextField = Game.getActualGame().getBoard().get(x, y);
            way = way.next();
            way = way.next();
            if (nextField != null && nextField.getStone().canGo(way)) {
                Game.storeState();
                field.removePlayer(player);
                nextField.addPlayer(player);
                player.setActualField(nextField);
                
                if (player.getActualCard().equals(nextField.getCard())) {
                    nextField.setCard(null);
                    player.addTreasureCard(player.getActualCard());
                    player.setActualCard(null);
                    Game.checkIfWinner(player);
                }                
                Game.getActualGame().getActualPlayer().setCanMove(false);
                
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }        
    }
}
