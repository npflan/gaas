from kubernetes import client, config
from datetime import datetime, timedelta, timezone
import humanfriendly

try:
    config.load_incluster_config()
except Exception:
    config.load_kube_config()


pods = client.CoreV1Api().list_pod_for_all_namespaces(
        watch=False,
        label_selector="app=gaas"
    )

for pod in pods.items:
    start = pod.status.start_time
    age = datetime.now(timezone.utc) - start
    hours, remainder = divmod(age.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if minutes > 0:
        print('{} min and {} sec'.format(int(minutes), int(seconds)))
        if hours > 0:
            print('{} hour and {} min'.format(int(hours), int(minutes)))

servers={}

#for pod in pods.items:
#        try:
#            uid=pod.metadata.labels["server"]
#            if uid not in servers:
#                continue
#            servers[uid]["ip"] = pod.status.pod_ip
#            servers[uid]["pods"]=[{
#                "ready": status.ready,
#                "image": status.image,
#                "restart_count": status.restart_count,
#                "state": status.state.waiting.reason if status.state.waiting is not None else None,
#            } for status in pod.status.container_statuses]
#        except KeyError as e:
#            pass
#
#
#print(servers)
