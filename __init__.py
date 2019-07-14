from airflow.plugins_manager import AirflowPlugin
from redshift_plugin.operators.s3_to_redshift_operator import S3ToRedshiftOperator
from redshift_plugin.operators.redshift_to_s3_operator import RedshiftToS3CustomTransfer
from redshift_plugin.operators.redshift_to_druid_operator import RedshiftToDruidOperator
from redshift_plugin.macros.redshift_auth import redshift_auth


class S3ToRedshiftPlugin(AirflowPlugin):
    name = "redshift_plugin"
    operators = [
        S3ToRedshiftOperator,
        RedshiftToS3CustomTransfer,
        RedshiftToDruidOperator,
    ]
    # Leave in for explicitness
    hooks = []
    executors = []
    macros = [redshift_auth]
    admin_views = []
    flask_blueprints = []
    menu_links = []
