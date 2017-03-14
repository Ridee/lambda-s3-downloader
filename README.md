S3 Downloader
=============

I have realized that a lot of times we spend a lot of time downloading and
uploading stuff to S3. I have created this simple lambda to help you out.

Using this lambda is way faster and cheaper than creating an EC2 machine for
downloading it and then uploading it to S3.

How to deploy
-------------

First, installing requirements.txt should give you a valid working
environment.

Then, `invoke prepare` will install and pack all the dependencies in a .zip
that you can upload to Lambda.


How to invoke
-------------

Basically it accepts a JSON. For now it is only http/s to S3, and the format
is the following. Featuring boto3

```
from boto3 import Session
session = Session()

url = 'http://google.es/'
bucket = 'test'
key = 'test.html'

lambda_client = session.client('lambda')
lambda_client.invoke(
  FunctionName='S3Downloader',
  InvocationType='Event',
  Payload=json.dumps({
    'source': {
      'url': url,
    },
    'destiny': {
      'bucket': bucket,
      'key': s3_key,
    },
  })
)
```
