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
    KubeIngress,
    IngressSpec,
    IngressRule,
    IngressBackend,
    HttpIngressRuleValue,
    HttpIngressPath,
    IngressServiceBackend,
    ServiceBackendPort,
)
from cdk8s_image import Image


class SpanSearchChart(Chart):
    def __init__(
        self, 
        scope: Construct, 
        id: str,
        service_name: str,
        service_port: int,
        service_image: Image,
        limits: Dict[str, Quantity],
        requests: Dict[str, Quantity],
        env_vars: list[EnvVar],
        ):
        super().__init__(scope, id)
        
        namespace = KubeNamespace(
            self,
            id="namespace",
            metadata=ObjectMeta(name=service_name),
        )

        labels = {"app": service_name}

        deployment = KubeDeployment(
            self,
            "deployment",
            metadata=ObjectMeta(
                name=service_name,
                namespace=namespace.name,
            ),
            spec=DeploymentSpec(
                selector=LabelSelector(match_labels=labels),
                template=PodTemplateSpec(
                    metadata=ObjectMeta(labels=labels),
                    spec=PodSpec(
                        containers=[
                            Container(
                                name=service_name,
                                image=service_image.url,
                                env=env_vars,
                                ports=[ContainerPort(container_port=service_port)],
                                resources=ResourceRequirements(
                                    limits=limits,
                                    requests=requests
                                ),
                            )
                        ],
                    ),
                ),
            ),
        )

        service = KubeService(
            self,
            "service",
            metadata=ObjectMeta(name=service_name, namespace=namespace.name),
            spec=ServiceSpec(
                selector=labels,
                ports=[
                    ServicePort(
                        port=5000,
                        name="span-search",
                        target_port=IntOrString.from_number(service_port),
                    )
                ],
            ),
        )

        ingress = KubeIngress(
            self, 
            "ingress",
            spec=IngressSpec(
                ingress_class_name="nginx",
                default_backend=IngressBackend(                                        
                    service=IngressServiceBackend(
                        name="span-search",
                        port=ServiceBackendPort(number=service_port)
                    )
                ),
                rules=[
                    IngressRule(                
                        http=HttpIngressRuleValue(
                            paths=[
                                HttpIngressPath(
                                    path_type="Prefix",
                                    path="/",
                                    backend=IngressBackend(                                        
                                        service=IngressServiceBackend(
                                            name="span-search",
                                            port=ServiceBackendPort(number=service_port)
                                        )
                                    )
                                )
                            ],
                           
                        )
                    )
                ]
            )
        )
    
        
        deployment.add_dependency(namespace)
        service.add_dependency(deployment)
        ingress.add_dependency(service)