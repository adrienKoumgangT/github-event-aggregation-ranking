package it.unipi;
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.codehaus.jettison.json.JSONObject;


public class EventCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

        // reuse Hadoop's Writable objects
        private final Text reducerKey = new Text();
        private final static IntWritable one = new IntWritable(1);

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            //String line = value.toString();

            try {

                JSONObject jsonl = new JSONObject(value.toString());

                String eventType = jsonl.getString("type");
                String createdAt = jsonl.getString("created_at");

                JSONObject repo = jsonl.getJSONObject("repo");
                long repoId = repo.getLong("id");

                String compositeKey = repoId + "," + createdAt + "," + eventType;

                reducerKey.set(compositeKey);
                context.write(reducerKey, one);

            } catch (Exception e) {
                // Skip bad or incomplete JSON lines
            }
        }
}
