import com.google.gson.JsonParser;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.DefaultConnectionKeepAliveStrategy;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.errors.WakeupException;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.opensearch.action.bulk.BulkRequest;
import org.opensearch.action.bulk.BulkResponse;
import org.opensearch.action.index.IndexRequest;
import org.opensearch.action.index.IndexResponse;
import org.opensearch.client.RequestOptions;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestHighLevelClient;
import org.opensearch.client.indices.CreateIndexRequest;
import org.opensearch.client.indices.GetIndexRequest;
import org.opensearch.common.xcontent.XContentType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.URI;
import java.time.Duration;
import java.util.Collection;
import java.util.Collections;
import java.util.Properties;

public class OpenSearchConsumer {
    public static RestHighLevelClient createOpenSearchClient() {
        String connString = "http://localhost:9200";
//        String connString = "https://c9p5mwld41:45zeygn9hy@kafka-course-2322630105.eu-west-1.bonsaisearch.net:443";

        // we build a URI from the connection string
        RestHighLevelClient restHighLevelClient;
        URI connUri = URI.create(connString);
        // extract login information if it exists
        String userInfo = connUri.getUserInfo();

        if (userInfo == null) {
            // REST client without security
            restHighLevelClient = new RestHighLevelClient(RestClient.builder(new HttpHost(connUri.getHost(), connUri.getPort(), "http")));

        } else {
            // REST client with security
            String[] auth = userInfo.split(":");

            CredentialsProvider cp = new BasicCredentialsProvider();
            cp.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(auth[0], auth[1]));

            restHighLevelClient = new RestHighLevelClient(
                    RestClient.builder(new HttpHost(connUri.getHost(), connUri.getPort(), connUri.getScheme()))
                            .setHttpClientConfigCallback(
                                    httpAsyncClientBuilder -> httpAsyncClientBuilder.setDefaultCredentialsProvider(cp)
                                            .setKeepAliveStrategy(new DefaultConnectionKeepAliveStrategy())));


        }

        return restHighLevelClient;
    }

    public static void main(String[] args) throws IOException {
        Logger logger = LoggerFactory.getLogger(OpenSearchConsumer.class.getSimpleName());


        String index = "wikimedia";
        String topic = "wikimedia.recentchange";

        RestHighLevelClient openSearchClient = createOpenSearchClient();
        // Create a Kafka client.
        KafkaConsumer<String, String> kafkaConsumer = createKafkaConsumer();

        // get a reference to the main thread
        final Thread mainThread = Thread.currentThread();
        // add the shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                logger.info("Detected a shutdown, let's exit by calling consumer.wakeup()...");
                kafkaConsumer.wakeup();

                // join the main thread to allow th eexecution of the code in the main thread
                try {
                    mainThread.join();
                } catch (InterruptedException e) {
//                    throw new RuntimeException(e);
                    e.printStackTrace();
                }
            }
        });

        try (openSearchClient; kafkaConsumer) {

            boolean indexExists = openSearchClient.indices().exists(new GetIndexRequest(index), RequestOptions.DEFAULT);

            if (!indexExists) {
                // we need to create an index on the open search if it doestn exist
                CreateIndexRequest createIndexRequest = new CreateIndexRequest(index);
                openSearchClient.indices().create(createIndexRequest, RequestOptions.DEFAULT);
                logger.info(("The Wikimedia index has been created!"));
            } else {
                logger.info("The Wikimedia index already exists");
            }

            // subscribe to consumer.
            kafkaConsumer.subscribe(Collections.singleton(topic));

            while (true) {
                ConsumerRecords<String, String> records = kafkaConsumer.poll(Duration.ofMillis(3000));
                int count = records.count();

                logger.info("Received " + count + " records(s)");

                BulkRequest bulkRequest = new BulkRequest();
                for (ConsumerRecord<String, String> record : records) {
                    // Unique ID configuration
                    // Strategy 1 - Defined an ID using Kafka record coordinates
//                    String id = record.topic() + "_" + record.partition() + "_" + record.offset();
                    // Strategy 2 - Use exiting ID from the data you are consuming
                    try {
                        String id = extractId(record);
                        // send the record into openSearch
                        IndexRequest indexRequest = new IndexRequest(index).source(record.value(), XContentType.JSON)
                                .id(id);

//                        IndexResponse response = openSearchClient.index(indexRequest, RequestOptions.DEFAULT);
                        bulkRequest.add(indexRequest);
//                        logger.info("Inserted data into OpenSearch, ID: " + response.getId());
                    } catch (Exception e) {

                    }

                }

                if (bulkRequest.numberOfActions() > 0) {
                    BulkResponse bulkResponse = openSearchClient.bulk(bulkRequest, RequestOptions.DEFAULT);
                    logger.info("Inserted " + bulkResponse.getItems().length + " record(s).");
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {

                    }
                    //commit offsets after the batch is consumed
                    kafkaConsumer.commitSync();
                    logger.info("Offsets have been committed!");
                }


            }

        } catch (WakeupException e) {
            logger.info("Consumer is starting to shut down");
        } catch (Exception e) {
            logger.error("Unexpected exception in the consumer", e);
        } finally {
            kafkaConsumer.close(); // close the consumer, this will also commit offset.
            logger.info("The Consumer will gracefully shut down");
        }
    }

    public static String extractId(ConsumerRecord<String, String> record) {
        String json = record.value();

        return JsonParser.parseString(json).getAsJsonObject().get("meta").getAsJsonObject().get("id").getAsString();
    }

    public static KafkaConsumer<String, String> createKafkaConsumer() {
        String bootstrapServers = "127.0.0.1:19092";
        String groupId = "consumer-opensearch-demo";
        // Create producer properties.
        Properties properties = new Properties();
        properties.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        properties.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        properties.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
        properties.setProperty(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");

        return new KafkaConsumer<String, String>(properties);
    }
}
