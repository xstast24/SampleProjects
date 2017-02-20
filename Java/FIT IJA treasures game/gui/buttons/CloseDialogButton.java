
package Labyrinth.gui.buttons;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JDialog;

/**
 * Universal close button for all dialogs
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class CloseDialogButton extends JButton implements ActionListener
{
    private JDialog dialog;
 
    /**
     * @param dialog Any dialog
     */
    public CloseDialogButton(JDialog dialog)
    {
        this.dialog = dialog;
        setText("Close");
        addActionListener(this);
    }

    /**
     * Close dialog
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e) 
    {
        this.dialog.dispose();
    }
}
