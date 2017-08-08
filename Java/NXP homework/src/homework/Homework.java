package homework;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.LinkedHashMap;

import org.json.JSONArray;
import org.json.JSONObject;

/*
 * Homework class is a main class responsible for creating objects.
 */
public class Homework {
	private final JSONObject inputData;
	private final String outputPath;
	private final ArrayList<Signal> signals;
	private final Apparatus apparatus;

	public Homework(String inputPath, String outputPath) throws Exception {
		this.outputPath = outputPath;
		try {
			// load input data from JSON file
			this.inputData = this.loadInputData(inputPath);
			this.signals = this.loadSignals(inputData);
			this.apparatus = this.loadApparatus(inputData);
		} catch (IOException e) {
			throw new Exception(
					"Input file handling failed. " + e.getMessage(), e);
		} catch (Exception e) {
			throw new Exception("Incorrect input data. " + e.getMessage(), e);
		}
	}

	public void run() throws Exception {
		String dataToFile = "";
		for (Signal signal : this.signals) {
			// get results for signal
			String path = this.apparatus.findBestConfiguration(signal);
			// print results to stdout
			System.out.println(path);
			dataToFile += path + "\n\n";
		}

		// print results to ouput file
		try (Writer writer = new BufferedWriter(new OutputStreamWriter(
				new FileOutputStream(this.outputPath), "utf-8"))) {
			writer.write(dataToFile);
		}
	}

	/*
	 * Load input data from json file.
	 */
	private JSONObject loadInputData(String filePath) throws IOException {
		String line = null;
		String text = "";
		FileReader fileReader = new FileReader(filePath);
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		// read the whole input file as a string and safely close file reader
		try {
			while ((line = bufferedReader.readLine()) != null) {
				text += line + "\n";
			}
		} finally {
			bufferedReader.close();
		}

		// parse the string to JSON object
		JSONObject data = new JSONObject(text);
		return data;
	}

	/*
	 * Load signals from json array of signals.
	 */
	private ArrayList<Signal> loadSignals(JSONObject data) {
		ArrayList<Signal> sigs = new ArrayList<Signal>();
		JSONArray sigsData = data.getJSONArray("signals");
		for (Object sigData : sigsData) {
			JSONObject sigJson = new JSONObject(sigData.toString());
			Signal sig = new Signal(sigJson.getInt("id"),
					sigJson.getDouble("initHz"), sigJson.getDouble("targetHz"));
			sigs.add(sig);
		}

		return sigs;
	}

	/*
	 * Load devices from json file.
	 */
	private Apparatus loadApparatus(JSONObject data) throws Exception {
		ArrayList<Device> deviceList = new ArrayList<Device>();
		JSONArray apparatusData = data.getJSONArray("devices");
		// keep previous device reference to assign a follower later
		Device lastDevice = null;
		for (Object deviceData : apparatusData) {
			JSONObject deviceDataJson = new JSONObject(deviceData.toString());
			// create devices, start with nested layer 0 = not nested
			Device device = this.loadDevice(deviceDataJson, 0);
			deviceList.add(device);

			// assign following device, so devices are linked together
			if (lastDevice != null) {
				lastDevice.setNextDevice(device);
			}
			lastDevice = device;
		}
		lastDevice.setNextDevice(null);

		Apparatus apparatus = new Apparatus(deviceList);
		return apparatus;
	}

	/*
	 * Creates device objects derived from Device class.
	 */
	private Device loadDevice(JSONObject deviceData, int nestedLayer)
			throws Exception {
		Device device;
		int deviceId = deviceData.getInt("id");
		String deviceType = deviceData.getString("device");
		// based on device type create Device class inherited devices
		switch (deviceType) {
		case "multiplexer":
			JSONArray muxInputsData = deviceData.getJSONArray("inputs");
			LinkedHashMap<Integer, Device> inputs = new LinkedHashMap<Integer, Device>();

			// recursively create all devices connected to mux inputs
			for (Object muxInputData : muxInputsData) {
				JSONObject muxinputDataJson = new JSONObject(
						muxInputData.toString());
				Device dev = this.loadDevice(muxinputDataJson, nestedLayer + 1);
				inputs.put(dev.getId(), dev);
			}
			// assign nested levels to mux for more readable output later
			// e.g. mux1 connected to mux2's input connected to mux3 = 2 levels
			device = new Multiplexer(deviceId, inputs);
			if (nestedLayer > 0) {
				((Multiplexer) device).setNestedLevel(nestedLayer);
			}
			break;
		case "divider":
			device = new Divider(deviceId, deviceData.getDouble("modifier"));
			break;
		case "multiplier":
			device = new Multiplier(deviceId, deviceData.getDouble("modifier"));
			break;
		case "none":
			device = new Cable(deviceId);
			break;
		default:
			throw new Exception("Unknown device type: " + deviceType);
		}

		return device;
	}

}
