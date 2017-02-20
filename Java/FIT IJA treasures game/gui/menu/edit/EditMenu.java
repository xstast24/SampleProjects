
package Labyrinth.gui.menu.edit;

import javax.swing.JMenu;

/**
 * Game menu
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class EditMenu extends JMenu
{
    /**
     * Create edit menu
     */
    public EditMenu()
    {
        setText("Edit");
        add(new UndoItem());
    }
}
