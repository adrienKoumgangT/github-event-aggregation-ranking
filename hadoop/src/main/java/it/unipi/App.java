package it.unipi;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {

        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "GHArchive Event Count");

        job.setJarByClass(GHArchiveEventCount.class);

        job.setMapperClass(EventCountMapper.class);
        job.setCombinerClass(EventCountReducer.class);
        job.setReducerClass(EventCountReducer.class);


        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);


    }
}
