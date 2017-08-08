package homework;

import java.util.LinkedHashMap;

/*
 * Multiplexer can have 0 or more inputs and exactly 1 (paralel)
 * device connected to each input. Multiplexers can be connected to
 * another multiplexers' inputs and be nested that way (serial).
 *   
 */
public class Multiplexer extends Device {
	protected final LinkedHashMap<Integer, Device> inputs;
	private int nestedLevel = 0;

	/*
	 * Multiplexer keeps reference to objects connected to its inputs. Setting a
	 * nested level is used only for purpose of creating a readable output.
	 */
	public Multiplexer(int id, LinkedHashMap<Integer, Device> inputs) {
		super(id, Device.Type.MULTIPLEXER);

		this.inputs = inputs;
	}

	public Boolean isNested() {
		return this.nestedLevel > 0;
	}

	public int getNestedLevel() {
		return this.nestedLevel;
	}

	public void setNestedLevel(int level) {
		this.nestedLevel = level;
	}

	public Device getDeviceByInput(Integer inputId) {
		return this.inputs.get(inputId);
	}

	@Override
	public void setNextDevice(Device device) {
		this.nextDevice = device;
		for (Integer inputId : this.inputs.keySet()) {
			this.inputs.get(inputId).setNextDevice(device);
		}
	}
}
