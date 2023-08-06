# ssmbotocredentialprovider
Credential provider to present ssm creds in /root/.aws/credentials to other users
of the system.

## Dependencies

This depends upon devices which were provisioned via iotdeviceprovisioner
and have a properly configured /AWSIoT directory with a certificate, private key, and metadata.json file created.


## Using

```python
import ssmbotocredentialprovider.AWS

session = ssmbotocredentialprovider.AWS.get_boto3_session(region_name="us-east-2")

s3_client = session.client('s3')
s3_client.list_buckets()
```

## Using the metadata server - method 1 with docker bridge networks

docker build -t metadata-server metadata-container

```
docker network create --driver bridge metadata_network --subnet 169.254.169.0/16

# adjust arguments appropriately if you want to use this as a service
docker run --restart unless-stopped --detach --net=metadata_network \
    --ip=169.254.169.254 metadata-server:latest
```

## Using the metadata server - method 2 with ip tables

### Configure iptables

```
/usr/sbin/iptables -t nat -A OUTPUT -p tcp -d 169.254.169.254 --dport 80 -j DNAT --to-destination 127.0.0.1:51680
/usr/sbin/iptables -t nat -A OUTPUT -p tcp -d 169.254.170.2   --dport 80 -j DNAT --to-destination 127.0.0.1:51680
```

if you have docker

```
/usr/sbin/iptables -t nat -I PREROUTING -p tcp -d 169.254.169.254 --dport 80 -j REDIRECT --to-ports 51680 -i docker0
/usr/sbin/iptables -t nat -I PREROUTING -p tcp -d 169.254.170.2 --dport 80 -j REDIRECT --to-ports 51680 -i docker0
```

### Start the server

Create a script/service which runs this:
```
python /usr/local/bin/fakemetadata-server.py
```

### Use your aws tools

Example:

```
aws s3 ls s3://
```


