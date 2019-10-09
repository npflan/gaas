from kubernetes import client
from gaas.games.defaults import (
    GameSpec,
    Param,
    ParamException,
    ParamTypes
)

class Cod4xGameSpec(GameSpec):

    id="cod4x"
    name="Call of Duty 4: Modern Warfare X Mod"
    
    params=[Param(
        id="RCON_PASSWORD",
        type=ParamTypes.STRING,
        name="Server Admin Password",
        description="Password for the RCON server",
    ),Param(
        id="GAME_TYPE",
        type=ParamTypes.ARRAY,
        name="Game Type",
        description="Which game the game will run",
        elements=["sd","sab","snd","tdm","koth","dm","all"]
    )]

    def get_param_constraints(self):
        return {
            "RCON_PASSWORD": [(lambda v: len(v) > 10, "RCON Password must be at least 10 characters.")],
            "GAME_TYPE": []
        }

    def make_deployment(self, params):
        return [client.V1Container(
            image="cytram/gaas-factorio",
            image_pull_policy="Always",
            name="cod4x",
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
            port=3074,
            target_port=3074,
            protocol="UDP"
        )]