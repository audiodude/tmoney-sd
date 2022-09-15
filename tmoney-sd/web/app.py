import boto3
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
  s3 = boto3.client('s3')
  resp = s3.list_objects(Bucket='tmoney-sd', Delimiter='/')
  all_prefixes = []
  for obj in resp.get('CommonPrefixes'):
    all_prefixes.append(obj.get('Prefix'))

  urls = []
  for prefix in all_prefixes:
    response = s3.generate_presigned_url('get_object',
                                         Params={
                                             'Bucket': 'tmoney-sd',
                                             'Key': f'{prefix}grid-0000.png'
                                         },
                                         ExpiresIn=3600)
    urls.append(response)
  return urls