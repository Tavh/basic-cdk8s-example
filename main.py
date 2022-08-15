#!/usr/bin/env python
from typing import Dict
from constructs import Construct
from cdk8s import App, Chart
from imports.k8s import KubeNamespace, ObjectMeta
from imports.k8s import (
    Container,
    ContainerPort,
    CrossVersionObjectReferenceV2Beta2,
    DeploymentSpec,
    EnvVar,
    HorizontalPodAutoscalerSpecV2Beta2,
    IntOrString,
    KubeDeployment,
    KubeHorizontalPodAutoscalerV2Beta2,
    KubeNamespace,
    KubeService,
    LabelSelector,
    LocalObjectReference,
    MetricSpecV2Beta2,
    MetricTargetV2Beta2,
    ObjectMeta,
    PodSpec,
    PodTemplateSpec,
    Quantity,
    ResourceMetricSourceV2Beta2,
    ResourceRequirements,
    ServicePort,
    ServiceSpec,
)
from charts.span_search_chart import SpanSearchChart
from cdk8s_image import Image

def _convert_resources(resources: Dict[str, str]) -> Dict[str, Quantity]:
    return {key: Quantity.from_string(value) for key, value in resources.items()}


service_name = "span-search"
service_port = 5000

app = App()

image = Image(scope=app, id="image", registry="tavh", name="span-search", dir="../SpanSearch")

env_vars = [
    EnvVar(name="PORT", value=f"{service_port}"),
]

SpanSearchChart(
    scope=app, 
    id="basic-cdk8s-example", 
    service_name="span-search",
    service_port=service_port,
    service_image=image,
    limits=_convert_resources({"cpu": "500m", "memory": "0.3Gi"}),
    requests=_convert_resources({"cpu": "250m", "memory": "0.1Gi"}),
    env_vars=env_vars,
)

app.synth()

