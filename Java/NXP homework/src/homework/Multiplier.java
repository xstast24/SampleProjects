package homework;

public class Multiplier extends Device implements Conductive {
	private final Double modifier;

	/*
	 * Multiplier can lead a signal and multiply its frequency by
	 * Multiplier.modifier, which has to be at least 1.0 (otherwise it would be
	 * a divider).
	 */
	public Multiplier(int id, Double modifier) throws IllegalArgumentException {
		super(id, Device.Type.MULTIPLIER);

		if (modifier < 1)
			throw new IllegalArgumentException(
					"Multiplier's modifier must be at least 1 or greater");
		this.modifier = modifier;
	}

	public Double getModifierValue() {
		return this.modifier;
	}

	@Override
	public Double leadSignal(Signal signal) {
		Double resultFreq = signal.getFrequency() * this.modifier;
		signal.setFrequency(resultFreq);
		return resultFreq;
	}
}
