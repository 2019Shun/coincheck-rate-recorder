#!/usr/bin/env python3

from aws_cdk import core

from coincheck_rate_recorder.coincheck_rate_recorder_stack import CoincheckRateRecorderStack


app = core.App()
CoincheckRateRecorderStack(app, "CoincheckRateRecorderStack", env={"region": "ap-northeast-1"})

app.synth()
