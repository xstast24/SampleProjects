
package Labyrinth;

import java.net.URL;
import Labyrinth.treasures.TreasureCard;
import java.awt.Color;
import java.io.Serializable;
import java.util.ArrayList;

/**
 * Player entity
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Player implements Serializable
{   
    public static enum COLOR {
        RED("red"), GREEN("green"), BLUE("blue"), YELLOW("yellow");
        
        private String value;
        
        private COLOR(String value)
        {
            this.value = value;
        }
        
        public String getValue()
        {
            return this.value;
        }
    }
 
    private int id;
    private COLOR color;    
    private TreasureCard actualCard;
    private ArrayList<TreasureCard> cards = new ArrayList<TreasureCard>();
    private Field actualField;
    private boolean isWinner = false;
    private boolean canMove = true;
    
    /**
     * Returns color by player id
     * @param index Color index
     * @return Player valid color
     */
    public static COLOR getColor(int index)
    {
        if (index == 1) {
            return COLOR.RED;
        } else if (index == 2) {
            return COLOR.GREEN;
        } else if (index == 3) {
            return COLOR.BLUE;
        } else {
            return COLOR.YELLOW;
        }
    }
    
    /**
     * Create a new player with concrete id and color
     * @param id Id of new player
     * @param color player color
     */
    public Player(int id, Player.COLOR color)
    {
        this.id = id;
        this.color = color;
    }

    /**
     * Returns player color name
     * @return Returns color name
     */
    public String getColorName()
    {
        return this.color.getValue();
    }
    
    /**
     * Returns player id
     * @return Player id
     */
    public int getId()
    {
        return this.id;
    }
    
    /**
     * Returns player color resource
     * @return Image resource for player with concrete color
     */
    public URL getColorResource()
    {
        return this.getClass().getClassLoader().getResource("lib/images/players/" + this.getColorName() + ".png");
    }
    
    /**
     * Return actual selected card
     * @return Actual treasure card
     */
    public TreasureCard getActualCard()
    {
        return this.actualCard;
    }
    
    /**
     * Set actual field
     * @param card Actual card
     */
    public void setActualCard(TreasureCard card)
    {
        this.actualCard = card;
    }

    /**
     * Returns actual field
     * @return Actual field
     */
    public Field getActualField()
    {
        return actualField;
    }

    /**
     * Set actual field
     * @param actualField field with this player
     */
    public void setActualField(Field actualField)
    {
        this.actualField = actualField;
    }
    
    /**
     * Add a new treasure card into list of obtained cards
     * @param card new obtained treasure card
     */
    public void addTreasureCard(TreasureCard card)
    {
        this.cards.add(card);
    }
    
    /**
     * Returns count of obtained treasure cards
     * @return count of obtained treasures cards
     */
    public int getCountOfCards()
    {
        return this.cards.size();
    }
    
    /**
     * Returns list of obtained treasure cards
     * @return List of treasure cards
     */
    public ArrayList<TreasureCard> getCards()
    {
        return this.cards;
    }
    
    /**
     * Set player as winner
     */
    public void setWinner()
    {
        this.isWinner = true;
    }
    
    /**
     * Check if player is winner
     * @return Return true if is winner
     */
    public boolean isWinner()
    {
        return this.isWinner;
    }
    
    /**
     * Returns Color from string
     * @return Player color 
     */
    public Color getColor()
    {
        if (this.color.getValue().compareTo("red") == 0) {
            return new Color(255, 0, 0);
        } else if (this.color.getValue().compareTo("green") == 0) {
            return new Color(48, 138, 4);
        } else if (this.color.getValue().compareTo("blue") == 0) {
            return new Color(0, 148, 252);
        } else {
            return new Color(252, 243, 0);
        }
    }
    
    /**
     * Returns true if can player move field
     * @return Returns true if can move
     */
    public boolean canMove()
    {
        return this.canMove;
    }
    
    /**
     * Set if player can move fields
     * @param canMove True if player can move field
     */
    public void setCanMove(boolean canMove)
    {
        this.canMove = canMove;
    }
}
