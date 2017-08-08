package homework;

public class Signal {
	private final int id;
	private final Double initialFrequency;
	private Double currentFrequency;
	private final Double targetFrequency;

	/*
	 * Class wrapping signals. Each signal must have initial starting frequency
	 * and target final frequency at least 1 Hz.
	 */
	public Signal(int id, Double initialFrequency, Double targetFrequency)
			throws IllegalArgumentException {
		if ((initialFrequency < 1) || (targetFrequency < 1))
			throw new IllegalArgumentException(
					"Frequency must be at least 1 Hz");
		this.id = id;
		this.initialFrequency = initialFrequency;
		this.currentFrequency = initialFrequency;
		this.targetFrequency = targetFrequency;
	}

	public int getId() {
		return this.id;
	}

	public Double getInitialFrequency() {
		return this.initialFrequency;
	}

	public Double getFrequency() {
		return this.currentFrequency;
	}

	public Double getTargetFrequency() {
		return this.targetFrequency;
	}

	public void setFrequency(Double frequency) {
		this.currentFrequency = frequency;
	}
}
