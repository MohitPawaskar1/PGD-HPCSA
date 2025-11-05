import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class Transaction {

    public static class TransactionMapper extends Mapper<Object, Text, Text, IntWritable> {
        private Text item = new Text();
        private IntWritable itemCount = new IntWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split("\t");

            // Assuming odd indices are items and the following even index is count
            for (int i = 1; i < parts.length; i += 2) {
                String currentItem = parts[i];
                int currentCount = Integer.parseInt(parts[i + 1]);
                item.set(currentItem);
                itemCount.set(currentCount);
                context.write(item, itemCount);
            }
        }
    }

    public static class TransactionReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        private int grandTotal = 0;

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            grandTotal += sum;  // Accumulate grand total
            context.write(key, result);
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            // After all reduce calls, write the grand total
            context.write(new Text("Grand Total"), new IntWritable(grandTotal));
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: Transaction <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "transaction count");
        job.setJarByClass(Transaction.class);
        job.setMapperClass(TransactionMapper.class);
        job.setCombinerClass(TransactionReducer.class);
        job.setReducerClass(TransactionReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

