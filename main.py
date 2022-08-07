#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports.k8s import KubeNamespace, ObjectMeta


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        KubeNamespace(
            self,
            id="test-namespace",
            metadata=ObjectMeta(name="test"),
        )
        # define resources here


app = App()
MyChart(app, "basic-cdk8s-example")

app.synth()
