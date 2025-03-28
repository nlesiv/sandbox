import org.apache.kafka.clients.producer.Callback;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class ProducerDemoKeysWithCallback {

    private static final Logger log = LoggerFactory.getLogger(ProducerDemoKeysWithCallback.class);

    public static void main(String[] args) {
        log.info("hello world");

        // Create producer properties
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "localhost:19092");

//        properties.setProperty("security.protocol", "SASL_SSL");
        properties.setProperty("key.serializer", StringSerializer.class.getName());
        properties.setProperty("value.serializer", StringSerializer.class.getName());

//        properties.setProperty("batch.size", "400");

        // Dont do this in prod!
//        properties.setProperty("partitioner.class", RoundRobinPartitioner.class.getName());

        // Create the producer
        KafkaProducer<String, String> producer = new KafkaProducer<>(properties);

        for (int j = 0; j < 2; ++j) {


            // Create a producer record
            for (int i = 0; i < 10; ++i) {
                String topic = "demo_java";
                String key = "id_" + i;
                String value = "hello world " + i;
                ProducerRecord<String, String> producerRecord = new ProducerRecord<>(
                        topic, key, value
                );
                send(producer, producerRecord);
            }

        }

        // send data


        // flush and close the producer - send all data and block untill done -- synchronous
        producer.flush();

        producer.close();
    }

    public static void send(KafkaProducer<String, String> producer, ProducerRecord<String, String> record) {
        producer.send(record, new Callback() {
            @Override
            public void onCompletion(RecordMetadata recordMetadata, Exception e) {
                // Executed every time a record is succesfully sent or an exceptoin is thrown
                if (e == null) {
                    // the record was succesfully sent.
                    log.info("Received new metadata \n" +
                            "key: " + record.key() + "\n" +
                            "Topic: " + recordMetadata.topic() + "\n" +
                            "Partition: " + recordMetadata.partition() + "\n" +
                            "Offset: " + recordMetadata.offset() + "\n" +
                            "Timestamp: " + recordMetadata.timestamp()
                    );
                } else {
                    log.error("error while producing", e);
                }
            }
        });
    }
}
