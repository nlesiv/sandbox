/*
 Maven Dependency If Using Maven

<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
    <version>2.x.x</version>
</dependency>

*/

import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class UploadFileToS3 {

    public static void main(String[] args) {
        // Specify your S3 bucket and file path
        String bucketName = "your-s3-bucket-name";
        String filePath = "path/to/your/file.txt";

        // Create an S3 client
        S3Client s3Client = S3Client.builder()
                .region(Region.US_EAST_1) // Replace with your desired region
                .credentialsProvider(DefaultCredentialsProvider.create())
                .build();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8))) {
            // Read file content line by line
            String line;
            while ((line = reader.readLine()) != null) {
                // Convert each line to UTF-8
                byte[] utf8Bytes = line.getBytes(StandardCharsets.UTF_8);

                // Upload the UTF-8 encoded content to S3
                s3Client.putObject(PutObjectRequest.builder()
                        .bucket(bucketName)
                        .key("destination/path/in/s3/file.txt") // Replace with your desired S3 destination path
                        .build(), () -> new ByteArrayInputStream(utf8Bytes));
            }

            System.out.println("File uploaded to S3 successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

