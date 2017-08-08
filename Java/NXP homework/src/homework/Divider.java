package homework;

public class Divider extends Device implements Conductive {
	private final Double modifier;

	/*
	 * Divider can lead a signal and divide its frequency by Divider.modifier
	 * value, which has to be at least 1 (otherwise it would be a multiplier).
	 */
	public Divider(int id, Double modifier) throws IllegalArgumentException {
		super(id, Device.Type.DIVIDER);

		if (modifier < 1)
			throw new IllegalArgumentException(
					"Divider's modifier must be at least 1 or greater");
		this.modifier = modifier;
	}

	/*
	 * Return a modifier, which is the number used for division.
	 */
	public Double getModifierValue() {
		return this.modifier;
	}

	@Override
	public Double leadSignal(Signal signal) {
		Double resultFreq = signal.getFrequency() / this.modifier;
		signal.setFrequency(resultFreq);
		return resultFreq;
	}
}
