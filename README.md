# Amazon Selling Partners API

Amazon is deprecating the MWS API in favor of a [new](https://github.com/amzn/selling-partner-api-docs/blob/main/guides/en-US/developer-guide/SellingPartnerApiDeveloperGuide.md#Self-authorization). The new APIs are published as Swagger [specifications](https://github.com/amzn/selling-partner-api-models/tree/main/models) along with language-specific [implementations](https://github.com/amzn/selling-partner-api-models/tree/main/clients) for request signing. This repository wraps both of those with a Maven build and a `git submodule` to allow easy publishing to jitpack.io.

### Usage:

Add the repository:
```
  <repositories>
    <repository>
      <id>jitpack.io</id>
      <url>https://jitpack.io</url>
    </repository>
  </repositories>
```

Add the dependency:
```
    <dependency>
      <groupId>com.github.kdunn926</groupId>
      <artifactId>sellingpartnerapi-aa-java</artifactId>
      <version>v1.7</version>
    </dependency>
```

Code ([source](https://github.com/amzn/selling-partner-api-docs/blob/main/guides/en-US/developer-guide/SellingPartnerApiDeveloperGuide.md#connecting-to-the-selling-partner-api-using-a-generated-java-sdk)):
```
import com.amazon.SellingPartnerAPIAA.AWSAuthenticationCredentials;
import com.amazon.SellingPartnerAPIAA.AWSAuthenticationCredentialsProvider;
import com.amazon.SellingPartnerAPIAA.LWAAuthorizationCredentials;


AWSAuthenticationCredentials awsAuthenticationCredentials=AWSAuthenticationCredentials.builder()
  .accessKeyId("myAccessKeyId")
  .secretKey("mySecretId")
  .region("us-east-1")
  .build();

AWSAuthenticationCredentialsProvider awsAuthenticationCredentialsProvider=AWSAuthenticationCredentialsProvider.builder()
  .roleArn("myroleARN")
  .roleSessionName("myrolesessioname")
  .build();

LWAAuthorizationCredentials lwaAuthorizationCredentials = LWAAuthorizationCredentials.builder()
  .clientId("myClientId")
  .clientSecret("myClientSecret")
  .endpoint("https://api.amazon.com/auth/o2/token")
  .build();

SellersApi sellersApi = new SellersApi.Builder()
  .awsAuthenticationCredentials(awsAuthenticationCredentials)
  .awsAuthenticationCredentialsProvider(awsAuthenticationCredentialsProvider)
  .lwaAuthorizationCredentials(lwaAuthorizationCredentials)
  .endpoint("https://sellingpartnerapi-na.amazon.com")
  .build();
```
