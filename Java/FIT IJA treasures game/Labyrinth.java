
package Labyrinth;

import Labyrinth.gui.GameGUI;

/**
 * Core game class
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class Labyrinth 
{
    /**
     * Start game
     * @param args Input arguments
     */
    public static void main(String[] args)
    {
        GameGUI gameGUI = new GameGUI();
        gameGUI.create();
    }
}
