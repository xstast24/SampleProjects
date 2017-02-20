
package Labyrinth;

import java.io.Serializable;
import java.net.URL;
import java.util.ArrayList;

/**
 * Stone entity
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Stone implements Serializable
{
    /**
     * All valid directions
     */
    public static enum CANGO {
        LEFT, UP, RIGHT, DOWN;
        
        public CANGO next()
        {
            int index = (this.ordinal() + 1) % values().length;
            return values()[index];
        }
    };
    
    /**
     * Stone type
     */
    public static enum TYPE {
        L("l"), T("t"), DIRECT("-");
        
        private String value;
        
        private TYPE(String value)
        {
            this.value = value;
        }
        
        public String getValue()
        {
            return this.value;
        }
    };
    
    /**
     * Allowed directions by stone type
     */
    private ArrayList<CANGO> allowedDirections = new ArrayList<CANGO>();
    
    /**
     * Stone type 
     */
    private TYPE type;
    
    /**
     * Stone position 0 for default 1 is after one turn right 
     */
    private int position;
    
    /**
     * Create a new stone by type
     * @param type Stone type
     */
    public Stone(TYPE type)
    {
        this.position = 0;
        this.type = type;
        if (type == Stone.TYPE.T) {
            allowedDirections.add(Stone.CANGO.LEFT);
            allowedDirections.add(Stone.CANGO.RIGHT);
            allowedDirections.add(Stone.CANGO.DOWN);
        } else if (type == Stone.TYPE.L) {
            allowedDirections.add(Stone.CANGO.UP);
            allowedDirections.add(Stone.CANGO.RIGHT);
        } else if (type == Stone.TYPE.DIRECT) {
            allowedDirections.add(Stone.CANGO.LEFT);
            allowedDirections.add(Stone.CANGO.RIGHT);
        } else {
            throw new IllegalArgumentException("Type can be only L, T or DIRRECT");
        }
    }
    
    /**
     * Turn stone to right
     */
    public void turnRight()
    {
        for (int i = 0; i < this.allowedDirections.size(); i++) {
            this.allowedDirections.set(i, this.allowedDirections.get(i).next());
        }
        this.position = (this.position + 1) % 4;
    }
    
    /**
     * Turn stone to right
     * @param repetition Count of repetitions
     */
    public void turnRight(int repetition)
    {
        for (int i = 0; i < repetition; i++) {
            this.turnRight();
        }
    }
    
    /**
     * @param direction Expected way (LEFT, TOP, DOWN, RIGHT)
     * @return Returns true if stone has correct way
     */
    public boolean canGo(Stone.CANGO direction)
    {
        return this.allowedDirections.contains(direction);
    }
    
    /**
     * @return Returns image resource
     */
    public URL getStoneImage()
    {
        return this.getClass().getClassLoader().getResource("lib/images/stones/" + this.type.getValue() + "-" + this.position + ".png");
    }
}
