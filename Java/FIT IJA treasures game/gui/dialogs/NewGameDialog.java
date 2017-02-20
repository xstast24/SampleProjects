
package Labyrinth.gui.dialogs;

import Labyrinth.Game;
import Labyrinth.events.GameListener;
import Labyrinth.events.NewGameListener;
import Labyrinth.gui.GameWindow;
import Labyrinth.gui.buttons.CloseDialogButton;
import java.awt.BorderLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

/**
 * New game dialog
 * Select game name and count of players
 * @author Ondřej Záruba (xzarub06)
 * @author Filip Štastný (xstast24)
 */
public class NewGameDialog extends JDialog implements ActionListener
{
    private JTextField gameNameInput;
    private JComboBox countOfPlayersBox;
    private JComboBox gameSizeBox;

    public NewGameDialog()
    {
        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints cs = new GridBagConstraints();

        cs.fill = GridBagConstraints.HORIZONTAL;

        JLabel newGameLabel = new JLabel("Game name: ");
        cs.gridx = 0;
        cs.gridy = 0;
        cs.gridwidth = 1;
        panel.add(newGameLabel, cs);

        this.gameNameInput = new JTextField(20);
        cs.gridx = 1;
        cs.gridy = 0;
        cs.gridwidth = 2;
        panel.add(this.gameNameInput, cs);

        JLabel playersCountLabel = new JLabel("Conut of players: ");
        cs.gridx = 0;
        cs.gridy = 1;
        cs.gridwidth = 1;
        panel.add(playersCountLabel, cs);

        DefaultComboBoxModel countOfPlayersModel = new DefaultComboBoxModel();

        countOfPlayersModel.addElement("2");
        countOfPlayersModel.addElement("3");
        countOfPlayersModel.addElement("4");

        this.countOfPlayersBox = new JComboBox(countOfPlayersModel);
        countOfPlayersBox.setSelectedIndex(0);

        JScrollPane fruitListScrollPane = new JScrollPane(this.countOfPlayersBox);
        cs.gridx = 1;
        cs.gridy = 1;
        cs.gridwidth = 2;
        panel.add(fruitListScrollPane, cs);

        JLabel gameSizeLabel = new JLabel("Game size:");
        cs.gridx = 0;
        cs.gridy = 2;
        cs.gridwidth = 2;
        panel.add(gameSizeLabel, cs);

        DefaultComboBoxModel gameSizeModel = new DefaultComboBoxModel();

        gameSizeModel.addElement("5");
        gameSizeModel.addElement("7");
        gameSizeModel.addElement("9");
        gameSizeModel.addElement("11");

        this.gameSizeBox = new JComboBox(gameSizeModel);
        gameSizeBox.setSelectedIndex(1);

        JScrollPane gameSizeScrollPane = new JScrollPane(this.gameSizeBox);
        cs.gridx = 1;
        cs.gridy = 2;
        cs.gridwidth = 2;
        panel.add(gameSizeScrollPane, cs);


        JButton createGameButton = new JButton("Create a new game");
        createGameButton.addActionListener(this);

        JPanel bp = new JPanel();

        bp.add(createGameButton);
        bp.add(new CloseDialogButton(this));
        panel.setBorder(new EmptyBorder(10, 10, 10, 10));

        getContentPane().add(panel, BorderLayout.CENTER);
        getContentPane().add(bp, BorderLayout.PAGE_END);

        pack();
        setResizable(false);
        setLocationRelativeTo(GameWindow.getInstance());
    }

    /**
     * Open dialog
     */
    public void open()
    {
        pack();
        setVisible(true);
    }

    /**
     * Create a new Game
     * @param e Action event
     */
    public void actionPerformed(ActionEvent e)
    {
        String gameName = this.gameNameInput.getText();
        if (gameName.isEmpty()) {
            JOptionPane.showMessageDialog(null, "You must fill game name");
        } else {
            int playersCount = Integer.parseInt(this.countOfPlayersBox.getSelectedItem().toString());
            int size = Integer.parseInt(this.gameSizeBox.getSelectedItem().toString());
            Game.createGame(gameName, playersCount, size);
            GameListener.getInstance().emit();
            NewGameListener.getInstance().emit();
            dispose();
        }   
    }
}
