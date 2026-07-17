package it.unipi;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class App
{
    public static void main( String[] args ) throws Exception
    {
        // check number of args
        if (args.length != 4) {
            System.err.println("Error: Wrong number of arguments provided.");
            System.err.println("Usage: hadoop jar <jar_name>.jar it.unipi.App <top_n> <input_path> <intermediate_path> <final_output_path>");
            System.exit(1);
        }

        Configuration conf = new Configuration();
        // conf.setInt("top.n.value", Integer.parseInt(args[0]));

        Job job = Job.getInstance(conf, "GHArchive Event Count");

        job.setJarByClass(App.class);

        job.setMapperClass(EventCountMapper.class);
        job.setCombinerClass(EventCountReducer.class);
        job.setReducerClass(EventCountReducer.class);


        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[1]));
        FileOutputFormat.setOutputPath(job, new Path(args[2]));

        //System.exit(job.waitForCompletion(true) ? 0 : 1);

        boolean job1Success = job.waitForCompletion(true);
        if (!job1Success) { System.exit(1); }

        else {
            Configuration conf2 = new Configuration();
            conf2.setInt("top.n.value", Integer.parseInt(args[0])); // use the same N value

            Job job2 = Job.getInstance(conf2, "GHArchive Top N Events");
            job2.setJarByClass(App.class);

            job2.setMapperClass(TopEventsMapper.class);
            job2.setReducerClass(TopEventsReducer.class);

            job2.setOutputKeyClass(Text.class);
            job2.setOutputValueClass(Text.class);

            FileInputFormat.addInputPath(job2, new Path(args[2] + "/part*"));
            FileOutputFormat.setOutputPath(job2, new Path(args[3]));

            System.exit(job2.waitForCompletion(true) ? 0 : 1);
        }


    }
}