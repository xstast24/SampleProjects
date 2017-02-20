
package Labyrinth.gui;

import Labyrinth.Game;
import Labyrinth.PlayerCoordinator;
import Labyrinth.Stone;
import Labyrinth.gui.menu.MenuBar;
import Labyrinth.gui.panel.EndGamePanel;
import Labyrinth.gui.panel.GamePanel;
import Labyrinth.events.GameListener;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;
import java.awt.event.KeyEvent;
import java.util.Observable;
import java.util.Observer;
import javax.swing.JFrame;
import javax.swing.JOptionPane;

/**
 * Game window
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GameWindow extends JFrame implements Observer, java.awt.event.KeyListener
{
    private static GameWindow instance;
    private boolean isPressed = false;
    
    /**
     * Create a new window
     */
    public GameWindow()
    {
        addKeyListener(this);
        setTitle("Labyrinth");
        setLayout(new FlowLayout());
        
        MenuBar menuBar = new MenuBar();
        setJMenuBar(menuBar);
        
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setPreferredSize(this.getWindowDimension());
        
        GameListener.getInstance().addObserver(this);
    }
    
    public static GameWindow getInstance()
    {
        return instance;
    }
    
    public static GameWindow create()
    {
        instance = new GameWindow();
        
        return instance;
    }
    
    /**
     * Returns screen size
     * @return screen dimensions
     */
    private Dimension getWindowDimension()
    {
        GraphicsDevice gd = GraphicsEnvironment.getLocalGraphicsEnvironment().getDefaultScreenDevice();
        
        return new Dimension(gd.getDisplayMode().getWidth(), gd.getDisplayMode().getHeight());
    }
    
    /**
     * Update game window in depends on Game menu
     * @param o Observable object
     * @param arg Game object
     */
    public void update(Observable o, Object arg)
    {
        getContentPane().removeAll();
        if (Game.isEnd()) {
            getContentPane().add(new EndGamePanel());
        } else {
            if (Game.getActualGame() != null) {
                getContentPane().add(new GamePanel(this));
            }
        }
        revalidate();
        repaint();
    }
    
    /**
     * Run action after key press
     * @param e Key event
     */
    public void keyPressed(KeyEvent e)
    {
        if (!this.isPressed && Game.getActualGame() != null && e.getKeyCode() >= 37 && e.getKeyCode() <= 40) {
            if (Game.getActualGame().getActualPlayer().getActualCard() == null) {
                JOptionPane.showMessageDialog(null, "You must first select card from card pack");
            } else {
                this.isPressed = true;
                if (PlayerCoordinator.move(this.translateKey(e))) {
                    GameListener.getInstance().emit();
                }
            }
        }
    }

    /**
     * Set is pressed to false
     * @param e Key event
     */
    public void keyReleased(KeyEvent e)
    {
        if (Game.getActualGame() != null && e.getKeyCode() >= 37 && e.getKeyCode() <= 40) {
            this.isPressed = false;
        }        
    }
    
    public void keyTyped(KeyEvent e) {}
    
    /**
     * Translate pressed key to Stone CANGO type
     * @param e Key event
     * @return Stone CANGO type
     */
    private Stone.CANGO translateKey(KeyEvent e)
    {
        if (e.getKeyCode() == 37) {
            return Stone.CANGO.LEFT;
        } else if (e.getKeyCode() == 38) {
            return Stone.CANGO.UP;
        } else if (e.getKeyCode() == 39) {
            return Stone.CANGO.RIGHT;
        } else {
            return Stone.CANGO.DOWN;
        }
    }
}
