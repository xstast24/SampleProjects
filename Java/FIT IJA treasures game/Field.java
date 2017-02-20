
package Labyrinth;

import java.util.ArrayList;
import Labyrinth.treasures.TreasureCard;
import java.io.Serializable;

/**
 * Field entity
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Field implements Serializable
{
    private int x;
    private int y;
    private Stone stone;
    private TreasureCard card;
    private ArrayList<Player> players = new ArrayList<Player>();

    /**
     * Create a new field with concrete cords
     * @param x X cord
     * @param y Y cord
     */
    public Field(int x, int y)
    {
        this.y = y;
        this.x = x;
    }

    /**
     * Returns X cords
     * @return X cords
     */
    public int getX()
    {
        return this.x;
    }
    
    /**
     * Returns Y cords
     * @return Y cords
     */
    public int getY()
    {
        return this.y;
    }
    
    /**
     * Add player into this field
     * @param player Player entity
     */
    public void addPlayer(Player player)
    {
        this.players.add(player);
    }

    /**
     * Remove player from this field
     * @param player Player entity
     */
    public void removePlayer(Player player)
    {
        this.players.remove(player);
    }

    /**
     * Returns list of players on this field
     * @return Player list
     */
    public ArrayList<Player> getPlayers()
    {
        return this.players;
    }
    
    /**
     * Set list of players
     * @param players List of players
     */
    public void setPlayers(ArrayList<Player> players)
    {
        this.players = players;
    }

    /**
     * Set stone for this field
     * @param stone Stone for this field
     */
    public void setStone(Stone stone)
    {
        this.stone = stone;
    }
    
    /**
     * Returns field stone
     * @return Stone of this field
     */
    public Stone getStone()
    {
        return this.stone;
    }

    /**
     * Returns Treasure card
     * @return Treasure card on this field
     */
    public TreasureCard getCard()
    {
        return card;
    }

    /**
     * Set treasure card
     * @param card Treasure card for this field
     */
    public void setCard(TreasureCard card)
    {
        this.card = card;
    }
}
