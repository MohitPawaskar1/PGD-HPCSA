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

import javax.naming.Context;

import java.io.IOException;


// Odd - Item, Even - Count

public class Transaction {
	public static class TransactionMapper
		extends Mapper<Object, Text, Text, IntWritable> {
	private Text Item = new Text(); 
	private IntWritable ItemCount = new IntWritable();
	public void map(Object key, Text value, Context context)
		throws IOException, InterruptedException { 
	String line = value.toString();
	String[] parts = line.split("\t");
	for (int i = 1; i < parts.length; i += 2){
		String currentitem = parts[i];
		int currentcount = Integer.parseInt(parts[i+1]);
	Item.set(currentitem);
	ItemCount.set(currentcount);
	context.write(Item, ItemCount);
		}
	}
}



public static class TransactionReducer
		extends Reducer<Text, IntWritable, Text, IntWritable> {
	private IntWritable result = new IntWritable();
	private int Grand_Total = 0;
	public void reduce(Text key, Iterable<IntWritable> values, Context context)

		throws IOException, InterruptedException {

	int sum = 0;
	for (IntWritable val: values) {

		sum += val.get();
		this.Grand_Total += sum;
	}
	result.set(sum);

	// Emit (Year, Max_Temperature)

	context.write(key, result);

	}

	@Override
	protected void cleanup(Context context) throws IOException, InterruptedException{
		result.set(this.Grand_Total);
		context.write(new Text("Grand_Total: "),result);
	}


		}

public static void main(String[] args) throws Exception {
    if (args. length != 2) {

	System.err.println("Usage: Item Counter <input path output path");

	System.exit(-1);
    }

	Configuration conf = new Configuration();
	Job job = Job.getInstance(conf, "Item Total Count Finder"); 
    job.setJarByClass (Transaction.class);
	job.setMapperClass (TransactionMapper.class);
	job.setCombinerClass (TransactionReducer.class);
	job.setReducerClass (TransactionReducer.class); 
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(IntWritable.class);
	FileInputFormat.addInputPath(job, new Path(args [0]));
	FileOutputFormat.setOutputPath(job, new Path(args[1]));
	System.exit(job.waitForCompletion(true) ? 0: 1);
}
}
