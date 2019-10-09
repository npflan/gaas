from kubernetes import client
from gaas.games.defaults import (
    GameSpec,
    Param,
    ParamException,
    ParamTypes
)

class TeeWorldsGameSpec(GameSpec):

    id="teeworld"
    name="TeeWorlds"

    params=[Param(
        id="RCON_PASSWORD",
        type=ParamTypes.STRING,
        name="Server Admin Password",
        description="Password for the RCON server",
    ),Param(
        id="SERVER_NAME",
        type=ParamTypes.STRING,
        name="Server Name",
        optional=True,
        description="The game server name ",
    ),Param(
        id="MAP",
        type=ParamTypes.ARRAY,
        name="Map",
        description="Map the server will start on",
        elements=["ctf1","ctf2","ctf3","ct3","ct4","ct5","ct6","ct7","ct8","dm1","dm2","dm3","dm6","dm7","dm8","dm9","lms1"]
    )]

    def get_param_constraints(self):
        return {
            "RCON_PASSWORD": [(lambda v: len(v) > 10, "RCON Password must be at least 10 characters.")],
            "SERVER_NAME": [(lambda v: len(v) > 4, "RCON Password must be at least 4 characters.")],
            "MAP": [],
        }

    def make_deployment(self, params):
        env=[client.V1EnvVar(
                name=k,
                value=str(v)
        ) for k, v in params.items()]
        env.extend([client.V1EnvVar(
            name="PORT",
            value="8303"
        )])
        return [client.V1Container(
            env=env,
            image="cytram/teeworlds",
            image_pull_policy="Always",
            name="teeworld",
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
                container_port=8303,
                protocol="UDP"
            )]
        )]

    def make_service(self, params):
        return [client.V1ServicePort(
            name="port1",
            port=8303,
            target_port=8303,
            protocol="UDP"
        )]