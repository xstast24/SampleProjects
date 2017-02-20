
package Labyrinth;

import Labyrinth.events.GameListener;
import Labyrinth.events.HistoryListener;
import Labyrinth.treasures.CardPack;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Stack;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

/**
 * Core Game class
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Game implements Serializable
{
    private static Game actualGame;
    private static Stack<String> history = new Stack<String>();
    private static HistoryListener historyState = new HistoryListener();
    private static boolean isEnd = false;
    
    private String name;
    private int playersCount;
    private Player actualPlayer;
    private Board board;
    private ArrayList<Player> players = new ArrayList<Player>();
    private CardPack cardPack;
    private int cardPackSize;
    
    /**
     * Create a new game
     * @param name Game name
     * @param playersCount Count of players
     */
    private Game(String name, int playersCount, Board board, CardPack cardPack)
    {
        this.name = name;
        this.playersCount = playersCount;
        this.board = board;
        this.players = this.generatePlayers();
        this.actualPlayer = this.players.get(0);        
        this.cardPack = cardPack;
        this.cardPackSize = cardPack.getCount();
        this.board.newGame();
        this.board.setPlayers(this.players);
        this.board.setTreasures(this.cardPack);        
    }

    /**
     * Create a new game and control if play
     * @param name Game name
     * @param playersCount Count of players
     * @param size Board size
     * @return new game
     */
    public static Game createGame(String name, int playersCount, int size)
    {
        CardPack cardPack;
        if (size <= 7) {
            cardPack = new CardPack(12);
        } else {
            cardPack = new CardPack(24);
        }
        cardPack.shuffle();
        actualGame = new Game(name, playersCount, Board.createBoard(size), cardPack);
        return actualGame;
    }
    
    /**
     * Open file browser and save game
     */
    public static void saveGame()
    {
        try {
            final JFileChooser fc = new JFileChooser();
            fc.showSaveDialog(null);
            FileOutputStream fileOut = new FileOutputStream(fc.getSelectedFile());
            ObjectOutputStream out = new ObjectOutputStream(fileOut);
            out.writeObject(Game.getActualGame());
            out.close();
            fileOut.close();
        } catch (IOException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Invalid output file");
        }
    }
    
    /**
     * Open file browser and load select game
     */
    public static void loadGame()
    {
        try {
            final JFileChooser fc = new JFileChooser();
            if (fc.showOpenDialog(null) == JFileChooser.APPROVE_OPTION) {
                FileInputStream fileIn = new FileInputStream(fc.getSelectedFile());
                ObjectInputStream in = new ObjectInputStream(fileIn);
                Game game = (Game) in.readObject();
                in.close();
                fileIn.close();
                actualGame = game;
            }            
        } catch (IOException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Invalid file");
        } catch (ClassNotFoundException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Invalid serialization");
        }
    }
    
    /**
     * Returns history state observable class
     * @return Observable class for history state
     */
    public static HistoryListener getHistoryStateObservable()
    {
        return historyState;
    }
    
    /**
     * Step back
     */
    public static void undo()
    {
        try {
            byte [] data = Base64.getDecoder().decode(history.pop());
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(  data ) );
            Game game = (Game) ois.readObject();
            ois.close();
            actualGame = game;
            HistoryListener.getInstance().emit();
            GameListener.getInstance().emit();
        } catch (ClassNotFoundException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Invalid serialization");
        } catch (IOException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Problem with game storage");
        }
    }
    
    /**
     * Store actual game state
     */
    public static void storeState()
    {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream( baos );
            oos.writeObject(actualGame);
            oos.close();
            history.push(new String( Base64.getEncoder().encode(baos.toByteArray() ) ));
            HistoryListener.getInstance().emit();
        } catch (IOException e) {
            Game.quit();
            System.err.println(e.getMessage());
            JOptionPane.showMessageDialog(null, "Problem with game storage");
        }
    }
    
    /**
     * Check if any stored history
     * @return True if has any history
     */
    public static boolean hasHistory()
    {
        return history.size() > 0; 
    }
    
    

    /**
     * Returns actual game
     * @return Returns actual game
     */
    public static Game getActualGame()
    {
        return actualGame;
    }
    
    /**
     * Remove actual game
     */
    public static void quit()
    {
        Game.actualGame = null;
        GameListener.getInstance().emit();
    }
    
    /**
     * Set game over
     */
    public static void end()
    {
        Game.isEnd = true;
    }
    
    /**
     * Check if player is winner
     * @param player Actual player
     */
    public static void checkIfWinner(Player player)
    {
        int winCount = Game.getActualGame().cardPackSize / Game.getActualGame().getCountOfPlayers();
        if (winCount <= player.getCountOfCards()) 
        {
            player.setWinner();
            end();
        }
    }
    
    /**
     * Check if is game over
     * @return Returns true if game is over
     */
    public static boolean isEnd()
    {
        return isEnd;
    }
    
    /**
     * Set next player
     */
    public void nextPlayer()
    {
       this.actualPlayer = this.players.get((this.players.indexOf(this.actualPlayer) + 1) % this.playersCount);
       this.actualPlayer.setCanMove(true);
    }
    
    /**
     * Returns name of actual game
     * @return Game name
     */
    public String getName()
    {
        return this.name;
    }
    
    /**
     * Returns count of players
     * @return Count of players
     */
    public int getCountOfPlayers()
    {
        return this.playersCount;
    }

    /**
     * Returns actual game board
     * @return Board of actual game
     */
    public Board getBoard()
    {
        return this.board;
    }

    /**
     * return actual player
     * @return Actual player
     */
    public Player getActualPlayer()
    {
        return this.actualPlayer;
    }
    
    /**
     * Generate array of players
     * @return Array of players
     */
    private ArrayList<Player> generatePlayers()
    {
        ArrayList<Player> players = new ArrayList<Player>();
        for (int i = 1; i <= this.playersCount; i++) {
            players.add(new Player(i, Player.getColor(i)));
        }
        
        return players;
    }
    
    /**
     * Returns card pack
     * @return Card pack
     */
    public CardPack getCardPack()
    {
        return this.cardPack;
    }
    
    /**
     * Returns list of players
     * @return List of players
     */
    public ArrayList<Player> getPlayers()
    {
        return this.players;
    }
}