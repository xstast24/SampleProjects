package homework;

import java.util.ArrayList;

import org.javatuples.Triplet;

/*
 * Apparatus class keeps reference to devices. Devices are linked to their
 * followers, so only the first layer is needed here. Apparatus can search
 * recursively through devices for the best path for given signals.
 */
public class Apparatus {
	private final ArrayList<Device> devices;

	public Apparatus(ArrayList<Device> devices) {
		this.devices = devices;
	}

	public ArrayList<Device> getDevicesList() {
		return this.devices;
	}

	/*
	 * Find best multiplexer settings and device sequence for given signal.
	 * Return multiplexers configuration, device sequence and final frequency.
	 */
	public String findBestConfiguration(Signal signal) {
		// create section headers for output
		String config = String.format(
				"Signal %1$d - multiplexer configuration:\n", signal.getId());
		String path = String.format("Signal %1$d - device list\n",
				signal.getId());

		// begin with the first device and recursively search through all
		// possible paths for given signal signal.
		Device device = this.devices.get(0);
		Triplet<String, String, Double> result = recursivePathSearch(signal,
				device);

		// format results to one string for output
		config += result.getValue0();
		path += result.getValue1();
		String outputFreq = String.format("Output frequency: %1$.0f\n",
				result.getValue2());
		return config + path + outputFreq;
	}

	/*
	 * Recursively try to lead signal through all possible paths through all
	 * devices and return the configuration that leads to frequency closest to
	 * target signal frequency.
	 */
	private Triplet<String, String, Double> recursivePathSearch(Signal signal,
			Device device) {
		Double targetFreq = signal.getTargetFrequency();
		Integer bestInputId = null;
		Triplet<String, String, Double> currentBest = null;
		String config = "";
		String path = "";

		// lead signal through devices, for multiplexors recurse inputs
		while (device != null) {
			switch (device.getType()) {
			case CABLE:
				((Cable) device).leadSignal(signal);
				break;
			case DIVIDER:
				((Divider) device).leadSignal(signal);
				path += String.format("Divider by %1$.2f\n",
						((Divider) device).getModifierValue());
				break;
			case MULTIPLEXER:
				Double tmpFreq = signal.getFrequency();
				for (Integer inputId : ((Multiplexer) device).inputs.keySet()) {
					// restore valid frequency for this layer
					signal.setFrequency(tmpFreq);
					// call path search for all inputs
					Triplet<String, String, Double> tmpResult = this
							.recursivePathSearch(signal,
									((Multiplexer) device).inputs.get(inputId));
					// save temporary best value
					if (currentBest == null) {
						currentBest = tmpResult;
						bestInputId = inputId;
					} else {
						if (Math.abs(targetFreq - tmpResult.getValue2()) < Math
								.abs(targetFreq - currentBest.getValue2())) {
							currentBest = tmpResult;
							bestInputId = inputId;
						}
					}
				}
				// save mux configuration
				config += this.getMuxConfigLabel(device, bestInputId);
				config += currentBest.getValue0();
				path += currentBest.getValue1();
				break;
			case MULTIPLIER:
				((Multiplier) device).leadSignal(signal);
				path += String.format("Multiplier by %1$.2f\n",
						((Multiplier) device).getModifierValue());
				break;
			default:
				break;

			}
			device = device.getNextDevice();
		}

		// load data from the best found value
		Double bestFreq = signal.getFrequency();
		if (currentBest != null) {
			bestFreq = currentBest.getValue2();
		}

		return new Triplet<String, String, Double>(config, path, bestFreq);
	}

	/*
	 * Create a string label for mux configuration. For nested multiplexers add
	 * number of parentheses depending on the nested level.
	 */
	private String getMuxConfigLabel(Device mux, Integer activeInputId) {
		int nestedLevel = ((Multiplexer) mux).getNestedLevel();
		String label = String.format("Mux %1$d input %2$d",
				((Multiplexer) mux).getId(), activeInputId);
		// nested level were counted when created the apparatus and devices
		if (nestedLevel > 0) {
			for (int i = 0; nestedLevel > i; i++) {
				label = "(" + label + ")";
			}
		}
		return label + "\n";
	}
}
