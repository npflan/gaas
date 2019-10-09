#################
# imports ####
#################
import uuid
import ipaddress
from . import servers_blueprint
from flask import request
from kubernetes import client
from gaas.games.enabled import get_game_by_id
import json
from datetime import datetime, timedelta, timezone
import humanfriendly

################
# routes ####
################

@servers_blueprint.route('/list')
def list_servers():
    u_ip = request.remote_addr
    services = client.CoreV1Api().list_service_for_all_namespaces(
    watch=False,
    label_selector="app=gaas"
    )
    deployments = client.AppsV1Api().list_deployment_for_all_namespaces(
        watch=False,
        label_selector="app=gaas"
    )
    pods = client.CoreV1Api().list_pod_for_all_namespaces(
        watch=False,
        label_selector="app=gaas"
    )
    servers={}
    for service in services.items:
        try:
            uid=service.metadata.labels["server"]
            candelete=False
            game=service.metadata.labels["game"]
            servers[uid] = {
            "uid":service.metadata.labels["server"],
            "game": game,
            "ports": [
                "{}/{}".format(port.protocol, port.port)
                for port in service.spec.ports
                ]
            }
        except KeyError as e:
            pass
        
    for deploy in deployments.items:
        try:
            uid=deploy.metadata.labels["server"]
            if uid not in servers:
                continue
            if deploy.metadata.labels["creator"] == u_ip:
                servers[uid]["candelete"] = "yes"
            for container in deploy.spec.template.spec.containers:
                if container.env:
                    servers[uid]["env"]={
                        env.name: env.value
                        for env in container.env
                    }
        except KeyError as e:
            pass

    for pod in pods.items:
        try:
            uid=pod.metadata.labels["server"]
            if uid not in servers:
                continue
            if pod.status.container_statuses == None:
                continue
            servers[uid]["ip"] = pod.status.pod_ip
            servers[uid]['run_time'] = format_time(pod.status.start_time)
            servers[uid]["pods"]=[{
                "ready": status.ready,
                "image": status.image,
                "restart_count": status.restart_count,
                "state": status.state.waiting.reason if status.state.waiting is not None else None,
            } for status in pod.status.container_statuses]
        except (KeyError) as e:
            pass
    return json.dumps(servers)

@servers_blueprint.route('/delete', methods=['post'])
def delete():
    uid = request.json['uid']
    ip = request.remote_addr
    deployment = client.AppsV1Api().read_namespaced_deployment_status(
        name="gaas-{}".format(uid),
        namespace="gaas",
    )
    if deployment.metadata.labels["creator"] != ip:
        raise Exception("You did not create this job")
    client.AppsV1Api().delete_namespaced_deployment(
        name="gaas-{}".format(uid),
        namespace="gaas",
    )
    client.CoreV1Api().delete_namespaced_service(
        name="gaas-{}".format(uid),
        namespace="gaas",
    )
    return "ok", 204

@servers_blueprint.route('/add', methods=['POST'])
def add_servers():

    if count_servers():
        return "You can't have more than 3 servers", 403
    game_id = request.json['game_id']
    params = request.json['parms']
    u_ip = request.remote_addr

    game=get_game_by_id(game_id)
    try:
        game.validate_params(params, game)
    except Exception as e:
        return str(e), 404
    
    
    uid=uuid.uuid4().hex[:12]
    name="gaas-{}".format(uid)
    labels={
        "app": "gaas",
        "game": game_id,
        "server": uid,
        "creator": u_ip,
    }
    metadata=client.V1ObjectMeta(
        labels=labels,
        name=name,
    )
    ip_ext=alloc_ip()
    extra_env=[client.V1EnvVar(
        name="IP_ALLOC",
        value=ip_ext
    ), client.V1EnvVar(
        name="IP_CREATOR",
        value=u_ip
    )]
    containers = game.make_deployment(params)
    for container in containers:
        if container.env:
            container.env.extend(extra_env)
        else:
            container.env = extra_env
        if not container.resources:
            container.resources=client.V1ResourceRequirements(
                limits={
                    "cpu": "2",
                    "memory": "1G"
                },
                requests={
                    "cpu": "1",
                    "memory": "1G"
                }
            )
    deployment=client.V1Deployment(
            spec=client.V1DeploymentSpec(
                replicas=1,
                strategy=client.AppsV1beta1DeploymentStrategy(
                    rolling_update=client.AppsV1beta1RollingUpdateDeployment(
                        max_surge=0,
                        max_unavailable=1
                    )
                ),
                selector=client.V1LabelSelector(
                    match_labels=labels,
                ),
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=containers,
                        termination_grace_period_seconds=0,
                        affinity=client.V1Affinity(
                            node_affinity=client.V1NodeAffinity(
                                required_during_scheduling_ignored_during_execution=client.V1NodeSelector(
                                    node_selector_terms=[
                                        client.V1NodeSelectorTerm(
                                            match_expressions=[
                                                client.V1NodeSelectorRequirement(
                                                    key="kubernetes.io/role",
                                                    operator="NotIn",
                                                    values=["shared"]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
                    )
                )
            )
    )
    service=client.V1Service(
        spec=client.V1ServiceSpec(
            type="ClusterIP",
            selector=labels,
            ports=game.make_service(params),
        )
    )
    deployment.metadata=metadata
    deployment.spec.template.metadata=metadata
    service.metadata=metadata
    
    client.AppsV1Api().create_namespaced_deployment(
        namespace="gaas",
        body=deployment,
    )

    service_resp = client.CoreV1Api().create_namespaced_service(
        namespace="gaas",
        body=service,
    )
    return {"uid": uid, "ip": u_ip}

@servers_blueprint.errorhandler(500)
def internal_error(error):
    return "Sorry an error has happend in the cloud", 500

def alloc_ip():
    EXTERNAL_PREFIX = "10.96.0.0/14"
    space=ipaddress.ip_network(EXTERNAL_PREFIX)
    reserved=[]
    services = client.CoreV1Api().list_service_for_all_namespaces(watch=False)
    for service in services.items:
        if service.spec.external_i_ps:
            reserved.extend(service.spec.external_i_ps)
    for ip in space:
        if str(ip) not in reserved:
            return str(ip)
    raise Exception("Cluster ran out of available IPs")

def count_servers():
    ip = request.remote_addr
    deployments = client.AppsV1Api().list_deployment_for_all_namespaces(
        watch=False,
        label_selector="creator={}".format(ip)
    )
    if len(deployments.items) > 2:
        return True

def format_time(start):
    age = datetime.now(timezone.utc) - start
    hours, remainder = divmod(age.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if minutes > 0:
        if hours > 0:
            if hours == 1:
                return '{} hour and {} min'.format(int(hours), int(minutes))
            else: 
                return '{} hours and {} min'.format(int(hours), int(minutes))
        else:
            return '{} min and {} sec'.format(int(minutes), int(seconds))
    else:
        return '{} sec'.format(int(seconds))
