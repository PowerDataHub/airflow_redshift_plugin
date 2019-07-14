from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook

from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults


class RedshiftToDruidOperator(BaseOperator):
    """
    Unloads a Redshift table to S3 and load into apache druid

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

    """

    template_fields = (
        "s3_bucket",
        "s3_key",
        "schema",
        "table",
        "sql",
        "druid_ingest_spec",
    )
    template_ext = (".sql",)
    ui_color = "#fff7e6"

    @apply_defaults
    def __init__(
        self,
        s3_bucket,
        s3_key,
        schema,
        table,
        sql=None,
        druid_ingest_spec=None,
        unload_options=tuple(),
        include_header=False,
        autocommit=False,
        aws_conn_id="aws_default",
        redshift_conn_id="postgres_default",
        druid_conn_id="druid_ingest_default",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.redshift_conn_id = redshift_conn_id
        self.druid_conn_id = druid_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.schema = schema
        self.table = table
        self.sql = sql
        self.druid_ingest_spec = druid_ingest_spec
        self.unload_options = unload_options
        self.autocommit = autocommit
        self.include_header = include_header

        self.pg_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.s3_hook = S3Hook(aws_conn_id=self.aws_conn_id)

        if self.include_header and "PARALLEL OFF" not in [
            uo.upper().strip() for uo in unload_options
        ]:
            self.unload_options = list(unload_options) + ["PARALLEL OFF"]

    def execute(self, context):
        self.unload()

    def unload(self):
        credentials = self.s3_hook.get_credentials()
        unload_options = "\n\t\t\t".join(self.unload_options)

        if self.include_header:
            self.log.info("Retrieving headers from %s.%s...", self.schema, self.table)

            columns_query = """ SELECT column_name
                                    FROM information_schema.columns
                                    WHERE table_schema = '{schema}'
                                    AND   table_name = '{table}'
                                    ORDER BY ordinal_position
                            """.format(
                schema=self.schema, table=self.table
            )

            cursor = self.pg_hook.get_conn().cursor()
            cursor.execute(columns_query)
            rows = cursor.fetchall()
            columns = [row[0] for row in rows]

            column_names = ", ".join("{0}".format(c) for c in columns)
            column_headers = ", ".join("\\'{0}\\'".format(c) for c in columns)
            column_castings = ", ".join(
                "CAST({0} AS text) AS {0}".format(c) for c in columns
            )

            select_query = """SELECT {column_names} FROM
                                    (SELECT 2 sort_order, {column_castings}
                                     FROM {schema}.{table}
                                    UNION ALL
                                    SELECT 1 sort_order, {column_headers})
                                 ORDER BY sort_order""".format(
                column_names=column_names,
                column_castings=column_castings,
                column_headers=column_headers,
                schema=self.schema,
                table=self.table,
            )
        else:
            if self.sql:
                select_query = self.sql
            else:
                select_query = "SELECT * FROM {schema}.{table}".format(
                    schema=self.schema, table=self.table
                )

        unload_query = """
                    UNLOAD ('{select_query}')
                    TO 's3://{s3_bucket}/{s3_key}/{table}_'
                    with credentials
                    'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'
                    {unload_options};
                    """.format(
            select_query=select_query,
            table=self.table,
            s3_bucket=self.s3_bucket,
            s3_key=self.s3_key,
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
            unload_options=unload_options,
        )

        self.log.info("Executing UNLOAD command...")
        self.pg_hook.run(unload_query, self.autocommit)
        self.log.info("UNLOAD command complete...")
