import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs. Path;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import java.util.StringTokenizer;
import java.io.IOException;

public class AverageData {
	public static class AverageDataMapper
		extends Mapper<Object, Text, Text, IntWritable> {
	private Text nameKey = new Text(); 
	private IntWritable useValue = new IntWritable();
	public void map(Object key, Text value, Context context)
		throws IOException, InterruptedException { 
	String line = value.toString();
	String[] parts = line.split("\t");
       	if (parts.length == 8) {
	       try {
			int numbers[];
			for (int i = 1; i <= 7; i++){
				numbers = 
			}
			String name = parts[0];
			IntWritable dailyUsage = parts[(1,2,3,4,5,6,7)];
		if (measurementType.equals("TMAX")) {
		       Float temperature = Float.parseFloat(parts[3]);
	       		yearKey.set(year);
			tempValue.set(temperature);
			context.write(yearKey, tempValue);
		}
	       }catch (NumberFormatException e) {
		       System.err.println("Ignoring Mlaformed Line: " +line);
	       }
	}
   }
}


public static class MaxTemperatureReducer
		extends Reducer<Text, FloatWritable, Text, FloatWritable> {
	private FloatWritable result = new FloatWritable();
	public void reduce(Text key, Iterable<FloatWritable> values, Context context)

		throws IOException, InterruptedException {

	Float maxValue = -100.0f;

	// Iterate through all temperatures for this year

	for (FloatWritable val: values) {

		maxValue = Math.max(maxValue, val.get());
	}
	result.set(maxValue);

	// Emit (Year, Max_Temperature)

	context.write(key, result);
	}
}



public static void main(String[] args) throws Exception {
    if (args. length != 2) {

	System.err.println("Usage: Internet Usage <input path output path>");

	System.exit(-1);
    }

	Configuration conf = new Configuration();
	Job job = Job.getInstance(conf, "Max Temperature Finder"); 
	// Set the main class for the job
    job.setJarByClass (MaxTemperature.class);
	// Set the Mapper class
	job.setMapperClass (MaxTemperatureMapper.class);

	// OPTIMIZATION

	// Set the Combiner class. For "max", we can reuse the Reducer
	// as a Combiner to reduce network traffic.
	job.setCombinerClass (MaxTemperatureReducer.class);
	// Set the Reducer class
	job.setReducerClass (MaxTemperatureReducer.class); 
	// Set the final output key and value types
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(FloatWritable.class);
	// Set the input and output paths from command-line arguments

	FileInputFormat.addInputPath(job, new Path(args [0]));

	FileOutputFormat.setOutputPath(job, new Path(args[1]));

	// Wait for the job to complete, and exit with 0 (success) or

	System.exit(job.waitForCompletion(true) ? 0: 1);
}
}
