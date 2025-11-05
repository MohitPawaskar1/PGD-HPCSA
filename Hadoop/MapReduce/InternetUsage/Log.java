import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.fs. Path;
import org.apache.hadoop.mapreduce.Mapper;
import java.util.StringTokenizer;
import java.io.IOException;

public class Log {
	public static class LogMapper
		extends Mapper<Object, Text, Text, FloatWritable> {
	private Text username = new Text(); 
	private FloatWritable avg = new FloatWritable();
	public void map(Object key, Text value, Context context)
		throws IOException, InterruptedException { 
	String line = value.toString();
	String[] words = line.split("\t");
			username.set(words[0]);
			// Integer avg;
			int i = 1, sum = 0;
			while (i < 8) {
				sum += Integer.parseInt(words[i]);
				i++;
			}
			avg.set(sum/7.0f);
			if (avg.get() >= 5){
				context.write(username, avg);
			}
		}
	}



public static void main(String[] args) throws Exception {
	Configuration conf = new Configuration();
	Job job = Job.getInstance(conf, "Internet Log Monitor"); 
    job.setJarByClass (Log.class);
	job.setMapperClass (LogMapper.class);
	job.setNumReduceTasks(0);
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(FloatWritable.class);
	FileInputFormat.addInputPath(job, new Path(args [0]));
	FileOutputFormat.setOutputPath(job, new Path(args[1]));
	System.exit(job.waitForCompletion(true) ? 0: 1);
}
}
