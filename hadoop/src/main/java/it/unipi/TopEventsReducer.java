package it.unipi;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Map;
import java.util.Collections;
import java.util.Comparator;

public class TopEventsReducer extends Reducer<Text, Text, Text, Text>
{
    private int n = 5; // top n events
    private Text finalValue = new Text();

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        // retrieve the N values
        this.n = context.getConfiguration().getInt("top.n.value", 5);
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        // Local map to accumulate global totals for each event type on this day
        HashMap<String, Integer> eventTotals = new HashMap<>();

        // Accumulate the totals per eventTyoe for this day
        for (Text val : values) {
            String[] data = val.toString().split(",");
            if (data.length == 2) {
                String eventType = data[0];
                int count = Integer.parseInt(data[1]);

                // Sum up counts across all repositories for this specific event type
                eventTotals.put(eventType, eventTotals.getOrDefault(eventType, 0) + count);
            }
        }

        // Map entries to a List so we can sort them
        ArrayList<Map.Entry<String, Integer>> sortedEvents = new ArrayList<>(eventTotals.entrySet());

        // Sort the list in descending order based on the total counts
        Collections.sort(sortedEvents, new Comparator<Map.Entry<String, Integer>>() {
            @Override
            public int compare(Map.Entry<String, Integer> e1, Map.Entry<String, Integer> e2) {
                return e2.getValue().compareTo(e1.getValue()); // Descending sort
            }
        });

        // Output the Top N elements for this day
        int limit = Math.min(n, sortedEvents.size());
        for (int i = 0; i < limit; i++) {
            Map.Entry<String, Integer> entry = sortedEvents.get(i);

            // Format: Rank#_EventType,TotalCount (e.g., "1_PushEvent,54201")
            String rankAndEvent = (i + 1) + "_" + entry.getKey();
            finalValue.set(rankAndEvent + "," + entry.getValue());

            context.write(key, finalValue); // Outputs: Key (Timestamp) \t Value (Rank_Event,Count)
        }
    }
}

