package it.unipi;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;

public class TopEventsMapper extends Mapper<LongWritable, Text, Text, Text> {
    private Text outputKey = new Text();
    private Text outputValue = new Text();

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // Convert line to string: "repoId,createdAt,eventType count"
        String line = value.toString().trim();

        // Split by one or more spaces to separate Job 1's key from value
        String[] parts = line.split("\\s+");
        if (parts.length != 2) return; // to skip incorrect rowa

        String compositeKey = parts[0].trim(); // repoId, created_at, eventType
        String count = parts[1].trim(); // count

        // Split composit key by coma
        String[] tokens = compositeKey.split(",");
        if (tokens.length == 3) {
            String date = tokens[1].trim();
            String eventType = tokens[2].trim();

            // group by date ofcreation
            outputKey.set(date);

            // Pass event type and count together as a text string (e.g., "PushEvent,10")
            outputValue.set(eventType + "," + count);

            context.write(outputKey, outputValue);
        }
    }

}

