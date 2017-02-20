
package Labyrinth.events;

public class NewGameListener 
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
