# aws-cli-ec2-plugin
Basic AWS CLI extension for fetching data related to EC2 instances using tag keys.

## Installation 
From GitHub
```shell
python -m pip install git+https://github.com/pyToshka/aws-cli-ec2-plugin.git

```
Local installation

```shell
git clone https://github.com/pyToshka/aws-cli-ec2-plugin.git
cd aws-cli-ec2-plugin
pip install .
```

## Configuration 

For enabling the plugin:
```shell

aws configure set plugins.ec2info awsec2info    

```
## Options
```text

Options:
  --tag TEXT                                            Tag name  [required]
  --output [json|plain|table]                           Output format for received information
  --attribute [name|type|state|private_ip|public_ip]    Get single attribute
  --region TEXT                                         AWS region name. Default us-east-1
```
## Simple output 

### Text

```shell
aws ec2info --tag Name --region us-west-2
```
output
```text
------
name: test
type: t3.large
state: stopped
private_ip: 127.0.0.1
public_ip: None
------

```
### Json

```shell
aws ec2info --tag Name --output json --region us-west-2 
```
output
```text
{
        "name": "test",
        "private_ip": "127.0.0.1",
        "public_ip": null,
        "state": "stopped",
        "type": "t3.large"
    }
]

```

### Table

```shell
aws ec2info --tag Name --output table --region us-west-2 
```
output
```text
name      | type      | state   | private_ip    | public_ip     
--------- | --------- | ------- | ------------- | --------------
test      | t3.large  | stopped | 127.0.0.      |   

```

Enjoy
