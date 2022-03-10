# Provision an EC2 instance with Pulumi

Official Tutorial: https://www.pulumi.com/registry/packages/aws/how-to-guides/ec2-webserver/
A blog post with more details whats actually been done on the aws end: https://www.learnaws.org/2021/06/19/pulumi-python-ec2/

## Pulumi

A few commands used with the example

```
$ pulumi preview
$ pulumi up
$ pulumi stack
$ pulumi stack ls
$ pulumi stack output public_dns
$ pulumi stack output public_ip
$ curl $(pulumi stack output public_ip)
$ pulumi destroy
```

## AWS


## Todo

* `ec2_instance.public_dns` is empty with the code of the second tutorial, but worked with the first
* Opening the instance in the browser didn't work somehow, the `curl` command instead works?!?
