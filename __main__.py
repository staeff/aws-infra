import pulumi
import pulumi_aws as aws

size = "t2.micro"

# Create a new vpc
vpc = aws.ec2.Vpc("ec2-vpc", cidr_block="10.0.0.0/16")

public_subnet = aws.ec2.Subnet(
    "ec2-public-subnet",
    cidr_block="10.0.101.0/24",
    tags={"Name": "ec2-public"},
    vpc_id=vpc.id,
)

# Create Internet Gateway
igw = aws.ec2.InternetGateway(
    "ec2-igw",
    vpc_id=vpc.id,
)

# Create Route Table
route_table = aws.ec2.RouteTable(
    "ec2-route-table",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
)

rt_assoc = aws.ec2.RouteTableAssociation(
    "ec2-rta", route_table_id=route_table.id, subnet_id=public_subnet.id
)

#  create a security group for the EC2 instance that allows HTTP traffic to port 80
sg = aws.ec2.SecurityGroup(
    "ec2-http-sg",
    description="Allow HTTP traffic to EC2 instance",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    vpc_id=vpc.id,
)

# use an Amazon AMI for our EC2 instance
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[aws.GetAmiFilterArgs(name="name", values=["amzn-ami-hvm-*"])],
)

user_data = """
#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

ec2_instance = aws.ec2.Instance(
    "ec2-tutorial",
    instance_type=size,
    vpc_security_group_ids=[sg.id],
    ami=ami.id,
    user_data=user_data,
    subnet_id=public_subnet.id,
    associate_public_ip_address=True,
)

pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("public_dns", ec2_instance.public_dns)
