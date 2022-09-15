import boto3
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
  s3 = boto3.client('s3')
  s3_resource = boto3.resource('s3')
  resp = s3.list_objects(Bucket='tmoney-sd', Delimiter='/')
  all_prefixes = []
  for obj in resp.get('CommonPrefixes'):
    all_prefixes.append(obj.get('Prefix'))

  galleries = []
  for prefix in all_prefixes:
    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': 'tmoney-sd',
                                        'Key': f'{prefix}grid-0000.png'
                                    },
                                    ExpiresIn=3600)

    prompt_key = f'{prefix}prompt.txt'
    obj = s3_resource.Object('tmoney-sd', prompt_key)
    prompt = obj.get()['Body'].read().decode('utf-8').strip()

    galleries.append({'url': url, 'prompt': prompt})

  return flask.render_template('index.html.jinja2', galleries=galleries)