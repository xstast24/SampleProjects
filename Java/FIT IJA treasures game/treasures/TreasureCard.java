
package Labyrinth.treasures;

import java.io.Serializable;
import java.net.URL;

/**
 * Treasure card entity
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class TreasureCard implements Serializable
{
    public static String[] types = {"beer", "boat", "cake", "car", "chair", 
        "clear", "coin", "crown", "cup", "diamond", "dog", "gun", "house", 
        "leaf", "map", "mouse", "pen", "phone", "scroll", "sword", "treasure", 
        "tree", "cheese", "clock"
    };
    
    private String type;
    
    /**
     * Create a new card
     * @param type Type from TreasureCard.types
     */
    public TreasureCard(String type) 
    {
        this.type = type;
    }
    
    /**
     * @return Small image resource
     */
    public URL getSmallImageResource()
    {
        return this.getClass().getClassLoader().getResource("lib/images/treasures/small/" + this.type + ".png");
    }
    
    /**
     * @return Big image resource
     */
    public URL getBigImageResource()
    {
        return this.getClass().getClassLoader().getResource("lib/images/treasures/big/" + this.type + ".png");
    }
    
    /**
     * Returns default card
     * @return default card
     */
    public static URL getDefaultCard()
    {
        return TreasureCard.class.getClassLoader().getResource("lib/images/treasures/no-card.png");
    }

    /**
     * Returns hash code
     * @return Hash code of type
     */
    @Override
    public int hashCode() 
    {
        return this.type.hashCode();
    }

    /**
     * Compare two cards 
     * @param obj TreasureCard 
     * @return True if is same
     */
    @Override
    public boolean equals(Object obj)
    {
        if (!(obj instanceof TreasureCard)) {
            return false;
        }
        TreasureCard compare = (TreasureCard) obj;
        if (compare == null) {
            return false;
        }
        return this.type.hashCode() == compare.type.hashCode();
    }
}
