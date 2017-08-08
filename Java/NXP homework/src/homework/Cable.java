package homework;

public class Cable extends Device implements Conductive {

	/*
	 * Cable serving to purpose of leading a signal where no signal modifiers
	 * are present. Does not modify the signal.
	 */
	public Cable(int id) {
		super(id, Device.Type.CABLE);
	}

	@Override
	public Double leadSignal(Signal signal) {
		return signal.getFrequency();
	}

}
