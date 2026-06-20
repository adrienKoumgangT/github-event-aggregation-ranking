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

        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "GHArchive Event Count");

        job.setJarByClass(App.class);

        job.setMapperClass(EventCountMapper.class);
        job.setCombinerClass(EventCountReducer.class);
        job.setReducerClass(EventCountReducer.class);


        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        //System.exit(job.waitForCompletion(true) ? 0 : 1);
        if (job.waitForCompletion(true)) {
            Configuration conf2 = new Configuration();
            conf2.setInt("top.n.value", 5); // defauly N

            Job job2 = Job.getInstance(conf2, "GHArchive Top N Events");
            job2.setJarByClass(App.class);

            job2.setMapperClass(TopEventsMapper.class);
            job2.setReducerClass(TopEventsReducer.class);

            job2.setOutputKeyClass(Text.class);
            job2.setOutputValueClass(Text.class);

            FileInputFormat.addInputPath(job2, new Path(args[1]));
            FileOutputFormat.setOutputPath(job2, new Path(args[2]));

            System.exit(job2.waitForCompletion(true) ? 0 : 1);
        }


    }
}