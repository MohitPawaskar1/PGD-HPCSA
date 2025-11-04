import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Rating {

    public static class RatingMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {
        private Text movieID = new Text();
        private DoubleWritable rating = new DoubleWritable();

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split("\t");
            if (parts.length == 4) {
                try {
                    String movie_id = parts[1];
                    double rate_val = Double.parseDouble(parts[2]);
                    movieID.set(movie_id);
                    rating.set(rate_val);
                    context.write(movieID, rating);
                } catch (NumberFormatException e) {
                    System.err.println("Ignoring Malformed Line: " + line);
                }
            }
        }
    }

    public static class AverageRatingReducer extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {
        private DoubleWritable result = new DoubleWritable();

        public void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
            double total_sum = 0.0;
            int total_count = 0;
            for (DoubleWritable val : values) {
                total_sum += val.get();
                total_count++;
            }
            double Average = total_sum / total_count;
            result.set(Average);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: Rating <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Average Movie Rating Finder");
        job.setJarByClass(Rating.class);
        job.setMapperClass(RatingMapper.class);
        job.setCombinerClass(AverageRatingReducer.class);
        job.setReducerClass(AverageRatingReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

