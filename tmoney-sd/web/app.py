import boto3
import flask

app = flask.Flask(__name__)


def read_contents(s3_resource, bucket, key):
  obj = s3_resource.Object(bucket, key)
  return obj.get()['Body'].read().decode('utf-8').strip()


def gen_url(s3, key):
  return s3.generate_presigned_url('get_object',
                                   Params={
                                       'Bucket': 'tmoney-sd',
                                       'Key': key,
                                   },
                                   ExpiresIn=3600)


@app.route('/')
def index():
  s3 = boto3.client('s3')
  s3_resource = boto3.resource('s3')
  resp = s3.list_objects(Bucket='tmoney-sd', Delimiter='/')
  all_prefixes = []
  for obj in resp.get('CommonPrefixes'):
    all_prefixes.append(obj.get('Prefix'))

  galleries = []
  for prefix in all_prefixes:
    url = gen_url(s3, f'{prefix}grid-0000.png')

    prompt_key = f'{prefix}prompt.txt'
    prompt = read_contents(s3_resource, 'tmoney-sd', prompt_key)

    galleries.append({'url': url, 'prompt': prompt, 'id': prefix.strip('/')})

  return flask.render_template('index.html.jinja2', galleries=galleries)


@app.route('/gallery/<gallery_id>')
def show_gallery(gallery_id):
  s3 = boto3.client('s3')
  s3_resource = boto3.resource('s3')

  items = [{
      'url': gen_url(s3, f'{gallery_id}/samples/{i:05}.png')
  } for i in range(6)]
  return flask.render_template('show_gallery.html.jinja2',
                               items=items,
                               prompt=read_contents(s3_resource, 'tmoney-sd',
                                                    f'{gallery_id}/prompt.txt'))
