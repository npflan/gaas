from kubernetes import client
from gaas.games.defaults import (
    GameSpec,
    Param,
    ParamException,
    ParamTypes
)

class FactorioGameSpec(GameSpec):

    id="factorio"
    name="Factorio"

    def make_deployment(self, params):
        return [client.V1Container(
            image="cytram/gaas-factorio",
            image_pull_policy="Always",
            name="factorio",
            resources=client.V1ResourceRequirements(
                limits={
                    "cpu": "2",
                    "memory": "10G"
                },
                requests={
                    "cpu": "1",
                    "memory": "5G"
                }
            ),
            ports=[client.V1ContainerPort(
                container_port=34197,
                protocol="UDP"
            )]
        )]

    def make_service(self, params):
        return [client.V1ServicePort(
            name="port1",
            port=34197,
            target_port=34197,
            protocol="UDP"
        )]