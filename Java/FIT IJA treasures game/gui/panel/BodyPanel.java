/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Labyrinth.gui.panel;

import Labyrinth.gui.GameWindow;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import javax.swing.JPanel;

/**
 *
 * @author budry
 */
public class BodyPanel extends JPanel
{
    /**
     * Create body panel
     * @param window Actual game window
     */
    public BodyPanel(GameWindow window)
    {
        setLayout(new GridBagLayout());

        GridBagConstraints gc1 = new GridBagConstraints();
        
        gc1.gridx = 0;
        gc1.gridy = 1;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new YCordsPanel(window), gc1);
        
        gc1.gridx = 1;
        gc1.gridy = 0;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new XCordsPanel(window), gc1);
        
        gc1.gridx = 1;
        gc1.gridy = 1;
        gc1.anchor = GridBagConstraints.WEST;
        gc1.fill = GridBagConstraints.VERTICAL;
        add(new BoardPanel(), gc1);
    }
}
