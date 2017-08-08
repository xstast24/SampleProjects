package homework;

/*
 * Class wrapping all devices connected to the frequency
 * modifying apparatus.
 */
public class Device {
	private final int id;
	private final Type type;
	protected Device nextDevice;

	public Device(int id, Type deviceType) {
		this.id = id;
		this.type = deviceType;
	}

	public enum Type {
		CABLE, MULTIPLEXER, DIVIDER, MULTIPLIER
	}

	public int getId() {
		return this.id;
	}

	public Type getType() {
		return this.type;
	}

	public Device getNextDevice() {
		return this.nextDevice;
	}

	public void setNextDevice(Device nextDevice) {
		this.nextDevice = nextDevice;
	}
}
