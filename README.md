### このスクリプトについて  

EC2,RDS,ELB,ElastiCacheのインスタンス一覧を表示します。  

### 必要なもの  

```
pip install boto3
```

### 使い方  

```
python ec2_describe.py [awsのprofile名]  
python rds_describe.py [awsのprofile名]  
python elb_describe.py [awsのprofile名]  
python alb_describe.py [awsのprofile名]  
python elasticache_describe.py [awsのprofile名]  
```

