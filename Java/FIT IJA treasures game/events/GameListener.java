
package Labyrinth.events;

/**
 * Observe for Game
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class GameListener
{
    private static Event event;
    
    public static Event getInstance()
    {
        if (event == null) {
            event = new Event();
        }
        
        return event;
    }
}
