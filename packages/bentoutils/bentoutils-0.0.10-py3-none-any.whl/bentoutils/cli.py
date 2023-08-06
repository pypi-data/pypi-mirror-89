import os
import sys

import boto3
import click
from bentoml.utils.lazy_loader import LazyLoader
from botocore.client import Config

from bentoutils.kubeutil import from_yaml
from bentoutils.print_kaniko_manifest import camel_to_kebab, gen_manifest as gen_kaniko_manifest
from bentoutils.print_knative_manifest import gen_manifest as gen_knative_manifest
from bentoutils.print_route_manifest import gen_manifest as gen_route_manifest

yatai_proto = LazyLoader('yatai_proto', globals(), 'bentoml.yatai.proto')


@click.command()
@click.option('--module', help='fully qualified module name containing service to package')
@click.option('--clz', help='class name of service to package')
@click.option('--name', help='model name')
@click.option('--path', help='directory path of pretrained model')
def pack(module, clz, name, path, labels=None, opts=None):
    if labels is None:
        labels = {}

    if opts is None:
        opts = {}

    # Create a service instance
    svc = get_instance(module, clz)

    # Package the pretrained model artifact
    svc.pack(name, path, opts)

    # Save the service to the model registry for serving
    saved_path = svc.save(labels=labels)

    #print('Saved model to ' + saved_path)
    click.echo(saved_path)


def get_instance(module_name, class_name):
    module = __import__(module_name)
    class_ = getattr(module, class_name)
    return class_()


@click.command()
@click.option('--module', help='fully qualified module name containing service to package')
@click.option('--clz', help='class name of service to package')
@click.option('--name', help='model name')
@click.option('--bucket', help='bucket name of pretrained model')
@click.option('--path', help='directory path of pretrained model')
def pack_from_s3(module, clz, name, bucket, path, labels=None, opts=None):
    s3 = boto3.resource('s3',
        endpoint_url=os.environ['S3_ENDPOINT_URL'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

    def download_directory(bucket_name, directory, local_directory=None):
        if local_directory is None:
            local_directory = os.path.join('/tmp', bucket_name, directory)

        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=directory):
            target = os.path.join(local_directory, os.path.relpath(obj.key, directory))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    tmp_path = '/tmp/{}/{}'.format(bucket, path)

    if not os.path.exists(tmp_path):
        download_directory(bucket, path)

    if labels is None:
        labels = {}

    if opts is None:
        opts = {}

    # Create a service instance
    svc = get_instance(module, clz)

    # Package the pretrained model artifact
    svc.pack(name, tmp_path, opts)

    # Save the service to the model registry for serving
    saved_path = svc.save(labels=labels)

    #print('Saved model to ' + saved_path)
    click.echo(saved_path)


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--path', help="path to saved artifacts")
@click.option('--registry', help="private registry in 'host:port' format")
def get_kaniko_manifest(bento, path, registry):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    click.echo(gen_kaniko_manifest(name, pod_name, version, path, registry))


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--registry', help="private registry in 'host:port' format")
def get_knative_manifest(bento, registry):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    click.echo(gen_knative_manifest(pod_name, version, registry))


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--currev', help="current knative revision name")
@click.option('--newrev', help="new knative revision name")
@click.option('--percent', help="percent to route to new revision")
def get_route_manifest(bento, cur_rev, new_rev, percent):
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    pod_name = camel_to_kebab(name)
    click.echo(gen_route_manifest(pod_name, cur_rev, new_rev, percent))


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
def get_saved_path(bento):
    # Get saved path
    if ':' in bento:
        name, version = bento.split(':')
    else:
        name = bento
        version = 'latest'

    yatai_client = get_default_yatai_client()
    result = yatai_client.repository.get(name, version)
    if result.status.status_code != yatai_proto.status_pb2.Status.OK:
        error_code, error_message = status_pb_to_error_code_and_message(result.status)
        click.echo(f'{error_code}:{error_message}')
        sys.exit(1)
    
    click.echo(result.bento.uri.uri)


@click.command()
@click.option('--labels', help="labels to find bento")
def first_bento_with_label(labels):
    yatai_client = get_default_yatai_client()
    result = yatai_client.repository.list(labels=labels)
    if result.status.status_code != yatai_proto.status_pb2.Status.OK:
        error_code, error_message = status_pb_to_error_code_and_message(result.status)
        click.echo(f'{error_code}:{error_message}')
        sys.exit(1)
    
    if len(result) == 0:
        return None

    bento = result[0]
    click.echo(f'{bento.name}:{bento.version}')


@click.command()
@click.option('--bento', help="bento name in 'name:version' format")
@click.option('--registry', help="private registry in 'host:port' format")
def containerize(bento, registry):
    saved_path = get_saved_path(bento)
    manifest = get_kaniko_manifest(bento, saved_path, registry)
    from_yaml(manifest)


@click.command()
@click.option('--bento', help='bento service name')
@click.option('--registry', help='registry name')
def deploy_to_knative(bento, registry):
    saved_path = get_saved_path(bento)
    manifest = get_knative_manifest(bento, saved_path, registry)
    from_yaml(manifest)

    # Build Docker image
    # client = docker.from_env()
    # tag = f'{registry}/{name}:{version}'
    # client.images.build(path=saved_path, tag=tag)
    # for line in client.push(tag, stream=True, decode=True):
    #     print(line)

    
    # Generate KNative manifest
    # output_dir = tempfile.TemporaryDirectory(dir='/tmp')
    # root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # resources_dir = os.path.join(root_dir, 'templates/knative')
    # env = Environment(loader=FileSystemLoader(resources_dir))
    # template = env.get_template('service.yaml')
    # svc_name = stringcase.spinalcase(name)
    # yaml_file = os.path.join(output_dir, 'service.yaml')
    # template.stream(name=svc_name, registry=registry).dump(yaml_file)

    # # Deploy to KNative
    # from_yaml(yaml_file)

    # # Cleanup
    # output_dir.cleanup()


def get_default_yatai_client():
    from bentoml.yatai.client import YataiClient

    return YataiClient()


# This function assumes the status is not status.OK
def status_pb_to_error_code_and_message(pb_status) -> (int, str):
    from bentoml.yatai.proto import status_pb2

    assert pb_status.status_code != status_pb2.Status.OK
    error_code = status_pb2.Status.Code.Name(pb_status.status_code)
    error_message = pb_status.error_message
    return error_code, error_message
