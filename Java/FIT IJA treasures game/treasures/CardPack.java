
package Labyrinth.treasures;

import java.io.Serializable;
import java.util.Collections;
import java.util.Stack;

/**
 * Card pack entity
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CardPack  implements Serializable
{
    private int countOfCards;
    
    private Stack<TreasureCard> cards = new Stack<TreasureCard>();
    
    /**
     * Create a new card pack
     * @param size Card pack size (only 12 or 24)
     */
    public CardPack(int size)
    {
        if (size > TreasureCard.types.length) {
            throw new IllegalArgumentException("Card pack size must be max " + TreasureCard.types.length);
        }
        for (int i = 0; i < size; i++) {
           this.cards.push(new TreasureCard(TreasureCard.types[i]));
        }
        this.countOfCards = size;
    }
    
    /**
     * @return Returns first card from pack
     */
    public TreasureCard popCard()
    {
        this.countOfCards--;
        
        return this.cards.pop();
    }
    
    /**
     * 
     * @param index Index in stack
     * @return Treasure card on index
     */
    public TreasureCard get(int index)
    {
        return this.cards.get(index);
    }
    
    /**
     * @return Count of cards in stack
     */
    public int getCount()
    {
        return this.cards.size();
    }
    
    /**
     * Shuffle
     */
    public void shuffle()
    {
        Collections.shuffle(this.cards);
    }
}
