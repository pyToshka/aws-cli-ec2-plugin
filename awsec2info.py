import logging
from awscli.customizations.commands import BasicCommand
import ast
import pprint
import boto3

import json

LOG = logging.getLogger(__name__)


def pprint_json(json_array, sort=True, indents=4):
    if isinstance(json_array, str):
        print(json.dumps(json.loads(json_array), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_array, sort_keys=sort, indent=indents))
    return None


def pprint_table(my_dict, col_list=None):
    """
    :param my_dict:
    :param col_list:
    """
    if not col_list:
        col_list = list(my_dict[0].keys() if my_dict else [])
    my_list = [col_list]  # 1st row = header
    for item in my_dict:
        my_list.append(
            [str(item[col] if item[col] is not None else "") for col in col_list]
        )
    col_size = [max(map(len, col)) for col in zip(*my_list)]
    format_str = " | ".join(["{{:<{}}}".format(i) for i in col_size])
    my_list.insert(1, ["-" * i for i in col_size])  # Seperating line
    for item in my_list:
        print(format_str.format(*item))


def get_aws_info(tag, region="us-east-1", output="plain", attribute=None):
    """Getting information about EC2 instance based on tag name"""
    if region is None:
        region = "us-east-1"
    print(
        f"Retrieving information for ec2 instance based on input parameters tag - {tag}, region {region} and attribute {attribute} output format is {output}"
    )
    ec2 = boto3.resource("ec2", region_name=region)
    instances = {}
    instances_list = []
    name = ""
    for instance in ec2.instances.all():
        if instance.tags is None:
            continue
        for tags in instance.tags:
            if "Name" in tags["Key"]:
                name = tags["Value"]
            if tags["Key"] == tag:
                try:
                    public_ip = instance.public_ip_address
                except AttributeError:
                    public_ip = "None"
                try:
                    private_ip = instance.private_ip_address
                except AttributeError:
                    private_ip = "None"
                instances[instance.id] = {
                    "name": name,
                    "type": instance.instance_type,
                    "state": instance.state["Name"],
                    "private_ip": private_ip,
                    "public_ip": public_ip,
                }
    if attribute:
        for instance_id, instance in instances.items():
            print(ast.literal_eval(pprint.pformat(instance[attribute])))
    if output == "json" and not attribute:
        for instance_id, instance in instances.items():
            instances_list.append(instance)
        pprint_json(instances_list)

    elif output == "table" and not attribute:
        for instance_id, instance in instances.items():
            instances_list.append(instance)
        pprint_table(instances_list)
    else:
        if attribute:
            pass

        else:
            attributes = ["name", "type", "state", "private_ip", "public_ip"]
            for instance_id, instance in instances.items():
                for key in attributes:
                    print("{0}: {1}".format(key, instance[key]))
                print("------")


class Ec2InfoPluginError(Exception):
    pass


def awscli_initialize(cli):
    cli.register("building-command-table.main", inject_commands)


def inject_commands(command_table, session, **kwargs):
    command_table["ec2info"] = Ec2InfoPlugin(session)


class Ec2InfoPlugin(BasicCommand):
    NAME = "ec2info"
    DESCRIPTION = "Retrieving information about EC2 instances based on tag key"
    SYNOPSIS = "aws ec2info [--tag TAG --output [json|plain|table] --attribute [name|type|state|private_ip|public_ip]]"
    ARG_TABLE = [
        {"name": "tag", "required": True, "help_text": "Tag name"},
        {
            "name": "output",
            "required": False,
            "default": "plain",
            "help_text": "Output format for received information. Accept json|plain|table",
        },
        {
            "name": "attribute",
            "required": False,
            "help_text": "Get single attribute. Accept [name|type|state|private_ip|public_ip]",
        },
    ]
    UPDATE = False

    def _run_main(self, args, parsed_globals):
        """Run the command and report success."""
        logging.basicConfig(level=logging.INFO)
        for handler in logging.root.handlers:
            handler.addFilter(logging.Filter(__name__))
        self._call(args, parsed_globals)

        return 0

    def _call(self, options, parsed_globals):
        """Run the command."""
        get_aws_info(
            tag=options.tag,
            region=parsed_globals.region,
            output=parsed_globals.output,
            attribute=options.attribute,
        )
