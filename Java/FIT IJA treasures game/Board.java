
package Labyrinth;

import java.util.ArrayList;
import java.util.Random;
import Labyrinth.treasures.CardPack;
import java.io.Serializable;

/**
 * Board
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Board implements Serializable
{
    private int size;
    ArrayList<Field> fields;
    private Stone freeStone;
    
    /**
     * Create a new game board with size and fields
     * @param size
     * @param fields 
     */
    private Board(int size, ArrayList<Field> fields)
    {
        this.size = size;
        this.fields = fields;
    }
    
    /**
     * Create new instance of Board
     * @param size Board size between 5 and 11 and must be odd number
     * @return Returns new Board instance
     */
    public static Board createBoard(int size)
    {
        if (size < 5 || size > 11) {
            throw new IllegalArgumentException("Size can be only bettwen 5 and 11");
        }
        if (size % 2 == 0) {
            throw new IllegalArgumentException("Size must be odd number");
        }
        
        ArrayList<Field> fields = new ArrayList<Field>();
        for (int x = 1; x <= size; x++) {
            for (int y = 1; y <= size; y++) {
                fields.add(new Field(x, y));
            }
        }
        
        return new Board(size, fields);
    }
    
    /**
     * Create a new game
     * Generate stones and place to fields
     */
    public void newGame()
    {
        this.freeStone = new Stone(Stone.TYPE.DIRECT);
        Random random = new Random();
        int maxStones = (this.size * this.size) / 3;
        int tStones = maxStones, lStones = maxStones, lineStones = maxStones;
        int div = (this.size * this.size) % 3;
        if (div != 0) {
            tStones += 1;
            if (div == 2) {
                lStones += 1;
            }                
        }


        ArrayList<Integer> indexs = new ArrayList<Integer>();
        for (int i = 1; i <= this.size * this.size; i++) {
            indexs.add(i);
        }
        indexs.remove(new Integer(1));
        indexs.remove(new Integer(this.size));
        indexs.remove(new Integer((this.size * this.size) - this.size + 1));
        indexs.remove(new Integer(this.size * this.size));

        Field field;
        Stone stone;

        field = this.get(1, 1);
        stone = new Stone(Stone.TYPE.L);
        stone.turnRight();
        field.setStone(stone);
        
        field = this.get(this.size, 1);
        stone = new Stone(Stone.TYPE.L);
        stone.turnRight(2);
        field.setStone(stone);

        field = this.get(1, this.size);
        stone = new Stone(Stone.TYPE.L);
        field.setStone(stone);

        field = this.get(this.size, this.size);
        stone = new Stone(Stone.TYPE.L);
        stone.turnRight(3);
        field.setStone(stone);

        lStones -= 4;
        
        for (int y = 1; y <= this.size; y += 2) {
            for (int x = 1; x <= this.size; x += 2) {
                if ((x == 1 && y == 1) || (y == 1 && x == this.size) || (y == this.size && x == 1) || (y == this.size && x == this.size)) {
                    continue;
                }
                Stone tStone = new Stone(Stone.TYPE.T);
                if (y == 1) {               
                } else if (x == 1) {
                    tStone.turnRight(3);
                } else if (x == this.size) {
                    tStone.turnRight();
                } else if (y == this.size) {
                    tStone.turnRight(2);
                }
                this.get(x, y).setStone(tStone);
                tStones -= 1;
                indexs.remove(new Integer((y - 1) * this.size + x));
            }
        }
        
        ArrayList<Stone.TYPE> types = new ArrayList<Stone.TYPE>();
        types.add(Stone.TYPE.L);
        types.add(Stone.TYPE.T);
        types.add(Stone.TYPE.DIRECT);

        while (indexs.size() > 0) {
            int index;
            if (indexs.size() - 1 == 0) {
                index = 0;
            } else {
                index = random.nextInt(indexs.size() - 1);
            }
            int nextIndex = indexs.get(index);
            int typeIndex;
            if (types.size() - 1 == 0) {
                typeIndex = 0;
            } else {
                typeIndex = random.nextInt(types.size() - 1);
            }
            Stone.TYPE nextStoneType = types.get(typeIndex);
            if (nextStoneType == Stone.TYPE.DIRECT) {
                lineStones -= 1;
                if (lineStones == 0) {
                    types.remove(Stone.TYPE.DIRECT);
                }
            } else if (nextStoneType == Stone.TYPE.T) {
                tStones -= 1;
                if (tStones == 0) {
                    types.remove(Stone.TYPE.T);
                }
            } else if (nextStoneType == Stone.TYPE.L) {
                lStones -= 1;
                if (lStones == 0) {
                    types.remove(Stone.TYPE.L);
                }
            }
            int x = ((nextIndex - 1) / this.size) + 1;
            int y = ((nextIndex - 1) % this.size) + 1;
            Stone newStone = new Stone(nextStoneType);
            newStone.turnRight(random.nextInt(4));
            this.get(x, y).setStone(newStone);
            indexs.remove(index);
        }
    }
    
    /**
     * Set players on game start fields
     * @param players Players
     */
    public void setPlayers(ArrayList<Player> players)
    {
        int[] startPositions = new int[4];
        startPositions[0] = 1;
        startPositions[1] = this.size;
        startPositions[2] = this.size * this.size;
        startPositions[3] = (this.size * this.size) - this.size + 1;
        for (int i = 0; i < players.size(); i++) {
            int position = startPositions[i];
            int x = ((position - 1) / this.size) + 1;
            int y = ((position - 1) % this.size) + 1;
            this.get(x, y).addPlayer(players.get(i));
            players.get(i).setActualField(this.get(x, y));
        }
    }
    
    /**
     * Set randomly treasure cards
     * @param cardPack Generated card pack
     */
    public void setTreasures(CardPack cardPack)
    {        
        ArrayList<Integer> indexs = new ArrayList<Integer>();
        for (int x = 1; x <= this.size * this.size; x++) {
            if (x == 1 || x == this.size || x == this.size * this.size || x == this.size * this.size - this.size + 1) {
                continue;
            }
            indexs.add(x);
        }
        Random random = new Random();
        for (int i = 0; i < cardPack.getCount(); i++) {
            int index = random.nextInt(indexs.size() - 1);
            int position = indexs.get(index);
            int x = ((position - 1) / this.size) + 1;
            int y = ((position - 1) % this.size) + 1;
            this.get(x, y).setCard(cardPack.get(i));
            indexs.remove(index);
        }
    }
    
    /**
     * Return free stone
     * @return Free stone
     */
    public Stone getFreeStone()
    {
        return this.freeStone;
    }
    
    /**
     * Set new free stone
     * @param stone New free stone
     */
    public void setFreeStone(Stone stone)
    {
        this.freeStone = stone;
    }
   
    /**
     * Returns field or null on concrete cords
     * @param x x cord
     * @param y y cord
     * @return Field on row and col or NULL if not exist
     */
    public Field get(int x, int y)
    {
        for (Field field : this.fields) {
            if (field.getX() == x && field.getY() == y) {
                return field;
            }
        }
        
        return null;
    }
    
    /**
     * Returns size of game board
     * @return Game board size
     */
    public int getSize()
    {
        return this.size;
    }
}