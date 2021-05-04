from aws_cdk import (
    core,
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets as targets
)

rate_table_name = "coincheck-rate-record-table"

class CoincheckRateRecorderStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create producer lambda function
        coincheck_rate_recorder_lambda = aws_lambda.Function(self, "coincheck_rate_recorder",
                                              runtime=aws_lambda.Runtime.PYTHON_3_8,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.asset("./lambda"))

        coincheck_rate_recorder_lambda.add_environment("TABLE_NAME", rate_table_name)

        # grant permission to lambda to read from demo table
        table = aws_dynamodb.Table.from_table_name(self, 'table', rate_table_name)
        table.grant_write_data(coincheck_rate_recorder_lambda)

        # Run every 1 minuts
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            schedule=aws_events.Schedule.rate(core.Duration.minutes(1)),
        )
        one_minute_rule.add_target(targets.LambdaFunction(coincheck_rate_recorder_lambda))