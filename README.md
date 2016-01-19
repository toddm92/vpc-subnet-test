### VPC AZ Subnet Test

It's not uncommon in older AWS accounts (i.e. with EC2-Classic) to come across a "depreciated zone" where VPC subnets are not permitted.
This Python script tests creating a VPC subnet in each availability-zone for every AWS region.

**Requirements:**

* Tested w/ python version 2.7 / boto version 2.34
* A valid profile in `~/.aws/config` or `${AWS_CONFIG_FILE}` with the appropriate API keys

**Usage:**

```
subnet-test.py -p <profile>
```

**Output:**

```
./subnet-test.py -p eng

Testing VPC subnet creation in all availabe zones..

Region: us-east-1
Attempting us-east-1a ..success!
Attempting us-east-1b ..failed!
Value (us-east-1b) for parameter availabilityZone is invalid. Subnets can currently only be created in the following availability zones: us-east-1a, us-east-1c, us-east-1d, us-east-1e. 

Attempting us-east-1c ..success!
Attempting us-east-1d ..success!
Attempting us-east-1e ..success!

Cleaning up ..done!

Region: ap-northeast-1
Attempting ap-northeast-1a ..failed!
Value (ap-northeast-1a) for parameter availabilityZone is invalid. Subnets can currently only be created in the following availability zones: ap-northeast-1b, ap-northeast-1c. 

Attempting ap-northeast-1b ..success!
Attempting ap-northeast-1c ..success!

Cleaning up ..done!

Region: eu-west-1
Attempting eu-west-1a ..success!
Attempting eu-west-1b ..success!
Attempting eu-west-1c ..success!

Cleaning up ..done!

Region: ap-southeast-1
Attempting ap-southeast-1a ..success!
Attempting ap-southeast-1b ..success!

Cleaning up ..done!

Region: ap-southeast-2
Attempting ap-southeast-2a ..success!
Attempting ap-southeast-2b ..success!

Cleaning up ..done!

Region: us-west-2
Attempting us-west-2a ..success!
Attempting us-west-2b ..success!
Attempting us-west-2c ..success!

Cleaning up ..done!

Region: us-west-1
Attempting us-west-1b ..success!
Attempting us-west-1c ..success!

Cleaning up ..done!

Region: eu-central-1
Attempting eu-central-1a ..success!
Attempting eu-central-1b ..success!

Cleaning up ..done!

Region: sa-east-1
Attempting sa-east-1a ..success!
Attempting sa-east-1b ..success!
Attempting sa-east-1c ..success!

Cleaning up ..done!

Testing complete.
```

**To Do:**

- [x] Clean up verbose output
- [x] Create dynamic regions array
- [x] Make profile an argument
