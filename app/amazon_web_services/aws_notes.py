          |vCPUs|Mem(GB)|SSD Storage(GB)|
m3.xlarge	|4	  |15	    |2 x 40         |
m3.2xlarge|8	  |30	    |2 x 80         |



aws emr list-clusters
aws emr create-default-roles
aws emr list-steps --cluster-id myClusterID
--------
canonical user id is a longer string, and is required to grant s3 bucket access permissions.
-------
default aws EMR user is hadoop and hive logs are at 
/mnt/var/log/hive/user/hadoop/hive.log
--------
aws s3 ls s3://athena-examples/conversion/write-parquet-to-s3.q

--wildcard searches in path of objects is not supported but there is a work around using include and exclude flags
aws s3 cp /tmp/foo/ s3://bucket/ --recursive \
    --exclude "*" --include "*.jpg" --include "*.txt"

--------
Glue team? Supports only python. No support yet for JVM-based apps.

---------------------
RDS - table locks

aurora - lock handling mechanism.

cost

migration of RDS to aurora - 
snapshot - binlog replication to catch-up.

most of it is in snapshot. aurora is VPC.

------------------------------------------------------------------------------------------------
PINTEREST talk on - Scalable and Reliable Data Ingestion (Aug 28, 2017)
********************************************************************************
Singer logging agent -
    Simple logging mechanism
        Applications (eg - microservices) log events to disk
        Singer monitors file system events and writes to kafka.
    Performant
        Staged event driven architecture
        > 100 MBps

Loging completeness
    Singer Heartbeat
    Singer failure detection
    Logging completeness monioring and alerting
    Log auditing
------------------------------------------------------------------------------------------------
# to do a cat on aws s3, use `-` as the destination argument of copy. It will dump contents of file to STDOUT 
aws s3 cp s3://my_file.txt -

# to do a recursive listing 
aws s3 ls --recursive s3://krux-stats/marketing-performance-shared-config/success/2017-08-


------------------------------------------------------------------------------------------------
TODO - investigate athena? Not ready for production yet.

Kinesis - can SQl query and roll-ups on the fly. Built for write throughput.
12 streams = concurrent writes.
$21k/month. 
------------------------------------------------------------------------------------------------
dynamoDB - cannot store binary. has to be text.
writes are expensive ($$)

------------------------------------------------------------------------------------------------
DNS Limits
Each Amazon EC2 instance limits the number of packets that can be sent to the Amazon-provided DNS server to a maximum of 1024 packets per second per network interface. 
This limit cannot be increased. 
The number of DNS queries per second supported by the Amazon-provided DNS server varies by the type of query, the size of response, and the protocol in use. 
For more information and recommendations for a scalable DNS architecture, see the Hybrid Cloud DNS Solutions for Amazon VPC whitepaper.
------------------------------------------------------------------------------------------------
//stubbing out aws python cli boto3 library stubbing out requests to rest endpoints 
http://botocore.readthedocs.io/en/latest/reference/stubber.html


awslogs get /aws/sagemaker/TrainingJobs ${SAGEMAKER_JOB_ID} --profile 201643537510-data-engineers-prod -s2d > ${SAGEMAKER_JOB_ID}.txt

awslogs get /aws/sagemaker/TrainingJobs ${SAGEMAKER_JOB_ID} --profile 001550251112-data-engineers-staging -s2d > ${SAGEMAKER_JOB_ID}.txt

