from kubernetes import client
from gaas.games.defaults import (
    GameSpec, 
    Param, 
    ParamException, 
    ParamTypes
)

class CSGoGameSpec(GameSpec):

    id="csgo"
    name="Counter Strike: Global Offensive"
    params=[Param(
        id="SV_PASSWORD",
        type=ParamTypes.STRING,
        optional=True,
        name="Server Password",
        description="Password for the server",
    ), Param(
        id="RCON_PASSWORD",
        type=ParamTypes.STRING,
        name="Server Admin Password",
        description="Password for the RCON server",
    ),Param(
        id="MAP",
        type=ParamTypes.ARRAY,
        name="Map",
        description="Map the server will start on",
        elements=["de_vertigo","de_train","de_overpass","de_nuke","de_mirage","de_inferno","de_cache","de_dust2"]
    )]

    def get_param_constraints(self):
        return {
            "SV_PASSWORD": [(lambda v: len(v) > 5, "Password must be at least 4 characters.")],
            "RCON_PASSWORD": [(lambda v: len(v) > 10, "RCON Password must be at least 10 characters.")],
            "MAP": []
        }
    def make_deployment(self, params):
        env=[client.V1EnvVar(
                name=k,
                value=str(v)
        ) for k, v in params.items()]
        env.extend([client.V1EnvVar(
            name="LAN",
            value="1"
        )])
        return [client.V1Container(
            env=env,
            image= "registry.npf.dk/gaas-csgo:1570633345",
            name="csgo",
            resources=client.V1ResourceRequirements(
                limits={
                    "cpu": "4",
                    "memory": "32G"
                },
                requests={
                    "cpu": "2",
                    "memory": "16G"
                }
            ),
            ports=[client.V1ContainerPort(
                container_port=27015,
                protocol="UDP"
            ), client.V1ContainerPort(
                container_port=27020,
                protocol="UDP"
            ), client.V1ContainerPort(
                container_port=27015,
                protocol="TCP"
            ), client.V1ContainerPort(
                container_port=27020,
                protocol="TCP"
            )]
        )]

    def make_service(self, params):
        return [client.V1ServicePort(
                name="port1",
                port=27015,
                target_port=27015,
                protocol="UDP"
            ), client.V1ServicePort(
                name="port2",
                port=27020,
                target_port=27020,
                protocol="UDP"
            ),client.V1ServicePort(
                name="port3",
                port=27015,
                target_port=27015,
                protocol="TCP"
            ), client.V1ServicePort(
                name="port4",
                port=27020,
                target_port=27020,
                protocol="TCP"
            )]
