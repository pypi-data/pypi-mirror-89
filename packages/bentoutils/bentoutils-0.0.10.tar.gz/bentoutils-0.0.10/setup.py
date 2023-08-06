import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='bentoutils',
    version='0.0.10',
    author='Mark Moloney',
    author_email='m4rkmo@gmail.com',
    description='Utilities for working with BentoML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/markmo/bentoutils',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'BentoML==0.9.2',
        'boto3',
        'click==7.1.2',
        'kubernetes==12.0.1',
        'PyYAML==5.3.1',
        'stringcase==1.2.0',
        'text-unidecode',
    ],
    entry_points='''
        [console_scripts]
        bentopack=bentoutils.cli:pack
        bentopacks3=bentoutils.cli:pack_from_s3
        get_kaniko_manifest=bentoutils.cli:get_kaniko_manifest
        get_knative_manifest=bentoutils.cli:get_knative_manifest
        get_route_manifest=bentoutils.cli:get_route_manifest
        get_saved_path=bentoutils.cli:get_saved_path
        first_bento_with_label=bentoutils.cli:first_bento_with_label
        containerize=bentoutils.cli:containerize
        deploy_to_knative=bentoutils.cli:deploy_to_knative
    ''',
    python_requires='>=3.6',
)
