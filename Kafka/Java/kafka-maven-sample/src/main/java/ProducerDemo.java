import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class ProducerDemo {

    private static final Logger log = LoggerFactory.getLogger(ProducerDemo.class);
    public static void main(String[] args) {
        log.info("hello world");

        // Create producer properties
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "localhost:19092");

//        properties.setProperty("security.protocol", "SASL_SSL");
        properties.setProperty("key.serializer", StringSerializer.class.getName());
        properties.setProperty("value.serializer", StringSerializer.class.getName());


        // Create the producer
        KafkaProducer<String, String> producer = new KafkaProducer<>(properties);

        // Create a producer record
        ProducerRecord<String, String> producerRecord = new ProducerRecord<>(
            "demo_java", "I am a Kafka Producer!"
        );
        // send data
        producer.send(producerRecord);

        // flush and close the producer - send all data and block untill done -- synchronous
        producer.flush();

        producer.close();
    }
}
