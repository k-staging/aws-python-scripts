### このスクリプトについて  

EC2,RDS,ELB(ALB),ElastiCache,Route53,S3の一覧を表示する  


### 必要なもの  

python2.7環境でboto3をインストール  

```
pip install boto3  
```

.bashrcなどにcredentialsのpathを追記  

```
export AWS_CONFIG_FILE=~/.aws/credentials  
```


### 使い方  
基本的に```python スクリプト名 [profile]```で動く  
ec2_describe.pyのみname_tagを指定可能  

```
python alb_describe.py [profile]  
python ec2_describe.py [profile] [name_tag]  
python ec2_event_describe.py [profile]  
python elasticache_describe.py [profile]  
python elasticache_event_describe.py [profile]  
python elb_describe.py [profile]  
python iam_role_describe.py [profile]  
python iam_user_describe.py [profile]  
python kinesis_describe.py [profile]  
python rds_describe.py [profile]  
python rds_event_describe.py [profile]  
python route53_describe.py [profile]  
python s3_describe.py [profile]  
```

複数profileで実行したい場合は、all_profile_describe.pyを使う  
引数にはスクリプト名を渡す  

```
python all_profile_describe.py ec2_describe.py
```
