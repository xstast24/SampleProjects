package homework;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

/**
 * NXP Recruit Qualification Task (Filip Stastny) (JavaSE-1.7+)
 * 
 * Usage instructions: Application loads data from JSON file and saves results
 * to a regular text file, plus prints them to stdout. Parameter -i <inputFile>
 * (compulsory), -o <outputFile> (optional). JSON file should compose of two
 * arrays: 'signals' and 'devices'. Signals array should define id (integer),
 * initial and target frequency (double) for each signal. Devices keeps array of
 * devices, each specified by id, device type and signal modifier for 'divider',
 * 'multiplier' or array with devices connected to inputs for 'multiplexer'. If
 * there is no device connected to mux input, use 'none' for device field.
 * Multiplexers can be nested by will (mux1 connected to mux2 input -> mux3
 * input, etc.). Example JSON files can be found in ./examples/ where
 * 'input_task.json' is the example specified in NXP task. In ./lib/ folder are
 * located libraries used to parse JSON, params, etc.
 * 
 * Signals are processed by the apparatus (all connected devices) and the best
 * possible combination should be found. Prints output with 1 Hz precision.
 * Sections: muxs' configuration, device list and final signal frequency [Hz].
 * 
 * Known bugs: recursive refactoring for mux nesting messed up output mux config
 * and device list. Signal frequency should be calculated correctly.
 */
public class Main {
	private static String inputPath;
	private static String outputPath;

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		Main.parseArgs(args);
		try {
			Homework homework = new Homework(Main.inputPath, Main.outputPath);
			homework.run();
		} catch (Exception e) {
			System.out.println("Error occurred:\n" + e.getMessage());
			throw e; // TODO System.exit(1)
		}
	}

	private static void parseArgs(String[] args) {
		Options options = new Options();

		Option optInput = new Option("i", "input", true,
				"Path to json file with input data");
		optInput.setRequired(true);
		options.addOption(optInput);

		Option optOutput = new Option("o", "output", true,
				"Path to output file (optional)");
		optOutput.setRequired(true);
		options.addOption(optOutput);

		CommandLineParser parser = new DefaultParser();
		HelpFormatter formatter = new HelpFormatter();
		CommandLine cmd;

		try {
			cmd = parser.parse(options, args);
		} catch (ParseException e) {
			System.out.println(e.getMessage());
			formatter.printHelp("homework", options);
			System.exit(2);
			return;
		}

		inputPath = cmd.getOptionValue("input");
		outputPath = cmd.getOptionValue("output");
	}
}
