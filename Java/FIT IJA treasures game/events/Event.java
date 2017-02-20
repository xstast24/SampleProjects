/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Labyrinth.events;

import java.util.Observable;

/**
 *
 * @author budry
 */
public class Event extends Observable
{
    public void emit() 
    {	
        setChanged();
        notifyObservers();
    }
}
