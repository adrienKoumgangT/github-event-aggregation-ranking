import subprocess
import json
import time
import uuid
import threading
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List
import logging

import requests

from models.cluster_models import ClusterInfo, ClusterMetrics, ClusterApplication, ClusterStatItem, ClusterAppAttempt, \
    ClusterAppContainer, ClusterNode, ClusterNewApplication, ClusterAppSubmit
from src.config.settings import Config



logger = logging.getLogger(__name__)


class ResourcesOrchestrator:
    def __init__(self):
        self.rm_url = f"{Config.YARN_RM_URL}/ws/v1/cluster"

    def cluster_info(self) -> ClusterInfo | Dict[str, Any]:
        """The cluster information resource provides overall information about the cluster."""
        url = f"{self.rm_url}/info"
        msg_log = f"Cluster info ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"Cluster info ({self.rm_url}): {r.text}")
                return ClusterInfo.from_dict(r.json().get('clusterInfo'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_metrics(self) -> ClusterMetrics | Dict[str, Any]:
        """The cluster metrics resource provides some overall metrics about the cluster."""
        url = f"{self.rm_url}/metrics"
        msg_log = f"Cluster metrics ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterMetrics.from_dict(r.json().get('clusterMetrics'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"Cluster metrics ({self.rm_url}): {e}")
            return {'status_code': 500, 'error': e}

    def cluster_scheduler(self) -> Dict[str, Any]:
        """A scheduler resource contains information about the current scheduler configured in a cluster.
        It currently supports the Fifo, Capacity and Fair Scheduler.
        You will get different information depending on which scheduler is configured so be sure to look at the type information."""
        url = f"{self.rm_url}/scheduler"
        msg_log = f"Cluster scheduler ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return r.json().get('scheduler', {}).get('schedulerInfo')
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_apps(self) -> List[ClusterApplication] | Dict[str, Any]:
        """With the Applications API, you can obtain a collection of resources, each of which represents an application.
        When you run a GET operation on this resource, you obtain a collection of Application Objects."""
        url = f"{self.rm_url}/apps"
        msg_log = f"Cluster apps ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                print(r.json().get('apps').get('app'))
                return [ClusterApplication.from_dict(a) for a in r.json().get('apps').get('app')]
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_app_statistics(self) -> List[ClusterStatItem] | Dict[str, Any]:
        """With the Application Statistics API, you can obtain a collection of triples, each of which contains the application type,
        the application state and the number of applications of this type and this state in ResourceManager context.
        Note that with the performance concern, we currently only support at most one applicationType per query.
        We may support multiple applicationTypes per query as well as more statistics in the future.
        When you run a GET operation on this resource, you obtain a collection of statItem objects."""
        url = f"{self.rm_url}/appstatistics"
        msg_log = f"Cluster app statistics ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return [ClusterStatItem.from_dict(a) for a in r.json().get('appStatInfo').get('statItem')]
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_app(self, app_id: str) -> ClusterApplication | Dict[str, Any]:
        """An application resource contains information about a particular application that was submitted to a cluster."""
        url = f"{self.rm_url}/apps/{app_id}"
        msg_log = f"Cluster app ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(f"{self.rm_url}/apps/{app_id}")
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterApplication.from_dict(r.json().get('app'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_app_attempts(self, app_id: str) -> List[ClusterAppAttempt] | Dict[str, Any]:
        """With the application attempts API, you can obtain a collection of resources that represent an application attempt.
        When you run a GET operation on this resource, you obtain a collection of App Attempt Objects."""
        url = f"{self.rm_url}/apps/{app_id}/appattempts"
        msg_log = f"Cluster app attempts ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return [ClusterAppAttempt.from_dict(a) for a in r.json().get('appAttempts').get('appAttempt')]
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_app_attempt_containers(self, app_id: str, attempt_id: str) -> List[ClusterAppContainer] | Dict[str, Any]:
        """With Containers for an Application Attempt API you can obtain the list of containers, which belongs to an Application Attempt."""
        url = f"{self.rm_url}/apps/{app_id}/appattempts/{attempt_id}/containers"
        msg_log = f"Cluster app attempt containers ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return [ClusterAppContainer.from_dict(a) for a in r.json().get('containers').get('container')]
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    def cluster_app_attempt_container(self, app_id: str, attempt_id: str, container_id) -> ClusterAppContainer | Dict[str, Any]:
        """With Specific Container for an Application Attempt API you can obtain information about a specific container,
        which belongs to an Application Attempt and selected by the container id."""
        url = f"{self.rm_url}/apps/{app_id}/appattempts/{attempt_id}/containers/{container_id}"
        msg_log = f"Cluster app attempt container ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterAppContainer.from_dict(r.json().get('container'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # Cluster Nodes API

    def cluster_nodes(self) -> ClusterNode | Dict[str, Any]:
        """With the Nodes API, you can obtain a collection of resources, each of which represents a node.
        When you run a GET operation on this resource, you obtain a collection of Node Objects."""
        url = f"{self.rm_url}/nodes"
        msg_log = f"Cluster nodes ({url})"
        logger.info(f"Cluster nodes ({self.rm_url})")
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterNode.from_dict(r.json().get('node'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # Cluster Node API

    def cluster_node(self, node_id: str) -> List[ClusterNode] | Dict[str, Any]:
        """A node resource contains information about a node in the cluster."""
        url = f"{self.rm_url}/nodes/{node_id}"
        msg_log = f"Cluster node ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return [ClusterNode.from_dict(n) for n in r.json().get('nodes').get('node')]
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # --- Cluster Writeable APIs ---

    # The setions below refer to APIs which allow to create and modify applications.
    # These APIs are currently in alpha and may change in the future.

    # Cluster New Application API

    def cluster_new_application(self) -> ClusterNewApplication | Dict[str, Any]:
        """With the New Application API, you can obtain an application-id which can then be used as part of the Cluster Submit Applications API to submit applications.
        The response also includes the maximum resource capabilities available on the cluster.

        This feature is currently in the alpha stage and may change in the future."""
        url = f"{self.rm_url}/apps/new-application"
        msg_log = f"Cluster new application ({url})"
        logger.info(msg_log)
        try:
            r = requests.post(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterNewApplication.from_dict(r.json())
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # Cluster Submit Application

    def cluster_submit_application(self, app_submit: ClusterAppSubmit) -> Dict[str, Any]:
        """The Submit Applications API can be used to submit applications.
        In case of submitting applications, you must first obtain an application-id using the Cluster New Application API.
        The application-id must be part of the request body.
        The response contains a URL to the application page which can be used to track the state and progress of your application."""
        url = f"{self.rm_url}/apps"
        msg_log = f"Cluster submit applications ({url})"
        logger.info(msg_log)
        try:
            r = requests.post(url, json=app_submit.to_dict())
            if r.status_code == 202:
                logger.info(f"{msg_log}: App submitted successfully")
                return {'status_code': r.status_code, 'msg': 'App submitted successfully'}
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}



if __name__ == '__main__':
    res = ResourcesOrchestrator()

    print("Cluster info:")
    ci = res.cluster_info()
    if isinstance(ci, ClusterInfo):
        print(ci.to_dict())
    print()

    print("Cluster metrics:")
    cm = res.cluster_metrics()
    if isinstance(cm, ClusterMetrics):
        print(cm.to_dict())
    print()

    print("Cluster apps:")
    ca_list = res.cluster_apps()
    for ca in ca_list:
        if isinstance(ca, ClusterApplication):
            print(ca.to_dict())
    print()

    print("Cluster app statistics:")
    cas_list = res.cluster_app_statistics()
    for cas in cas_list:
        if isinstance(cas, ClusterStatItem):
            print(cas.to_dict())
    print()

    app__id = "application_1782248356725_0001"
    print("Cluster app id:", app__id)
    app = res.cluster_app(app__id)
    if isinstance(app, ClusterApplication):
        print(app.to_dict())
    print()

