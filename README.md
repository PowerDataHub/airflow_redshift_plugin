[![Maintained by Powerdatahub.com](https://img.shields.io/badge/maintained%20by-powerdatahub.com-%235849a6.svg?style=for-the-badge)](https://powerdatahub.com/?ref=repo_aws_airflow) [![Tested with Apache Airflow 1.10.3](https://img.shields.io/badge/Tested%20with%20Apache%20Airflow-1.10.3-5849a6.svg?style=for-the-badge)](https://github.com/apache/airflow/)

# Airflow Plugin - Redshift

Move data from [Amazon Redshift](https://aws.amazon.com/pt/redshift/) to other sources like Amazon S3, Apache Druid and more

## Operators

### RedshiftToDruidOperator

Executes an UNLOAD command to s3 and load into Apache Druid

```
    :param s3_bucket: reference to a specific S3 bucket
    :type s3_bucket: str
    :param s3_key: reference to a specific S3 key
    :type s3_key: str
    :param schema: reference to a specific schema in redshift database
    :type schema: str
    :param table: reference to a specific table in redshift database
    :type table: str
    :param sql: Custom SQL statement to execute
    :type sql: str
    :param druid_ingest_spec: druid ingestion json spec
    :type druid_ingest_spec: json
    :param unload_options: reference to a list of UNLOAD options
    :type unload_options: list
    :param include_header: Should include headers in the final file?
    :type include_header: bool
    :param autocommit: if True perform autocommit
    :type autocommit: bool
    :param aws_conn_id: reference to a specific S3 connection
    :type aws_conn_id: str
    :param redshift_conn_id: reference to a specific redshift database
    :type redshift_conn_id: str
    :param druid_conn_id: reference to a specific Druid overlord connection
    :type druid_conn_id: str
```
### RedshiftToS3CustomOperador

Executes an UNLOAD command to s3 as a CSV with headers

### S3ToRedshiftOperator

Executes an COPY command to load a S3 file into Redshift

---
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)
