[![Maintained by Powerdatahub.com](https://img.shields.io/badge/maintained%20by-powerdatahub.com-%235849a6.svg?style=for-the-badge)](https://powerdatahub.com/?ref=repo_aws_airflow) [![Tested with Apache Airflow 1.10.3](https://img.shields.io/badge/Tested%20with%20Apache%20Airflow-1.10.3-5849a6.svg?style=for-the-badge)](https://github.com/apache/airflow/)

# Airflow Plugin - Redshift

Move data from [Amazon Redshift](https://aws.amazon.com/pt/redshift/) to other sources like Amazon S3, Apache Druid and more

## Operators

### RedshiftToDruidOperator

Executes an UNLOAD command to s3 and load into Apache Druid

### RedshiftToS3CustomOperador

Executes an UNLOAD command to s3 as a CSV with headers

### S3ToRedshiftOperator

Executes an COPY command to load a S3 file into Redshift

---
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)
