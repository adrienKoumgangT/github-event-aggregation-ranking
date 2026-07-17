from typing import Dict, Any, List
import time

import requests

from config.logger import get_logger
from namespaces.applications.models import Application, StatItem, AppAttempt, AppContainer, ClusterNewApplication, \
    ClusterAppSubmit, AppStateResponse, KillAppRequest, AppState
from namespaces.cluster.models import ClusterInfo, ClusterMetrics
from namespaces.nodes.models import ClusterNode
from src.config.settings import Config

logger = get_logger(__name__)


class YarnClient:
    rm_url = f"{Config.YARN_RM_URL}/ws/v1/cluster"

    # Cluster Information APIs

    @classmethod
    def cluster_info(cls) -> ClusterInfo | Dict[str, Any]:
        """The cluster information resource provides overall information about the cluster."""
        url = f"{cls.rm_url}/info"
        msg_log = f"Cluster info ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return ClusterInfo.from_dict(r.json().get('clusterInfo'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_metrics(cls) -> ClusterMetrics | Dict[str, Any]:
        """The cluster metrics resource provides some overall metrics about the cluster."""
        url = f"{cls.rm_url}/metrics"
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
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_scheduler(cls) -> Dict[str, Any]:
        """A scheduler resource contains information about the current scheduler configured in a cluster.
        It currently supports the Fifo, Capacity and Fair Scheduler.
        You will get different information depending on which scheduler is configured so be sure to look at the type information."""
        url = f"{cls.rm_url}/scheduler"
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

    # Cluster Applications APIs

    @classmethod
    def cluster_apps(cls) -> List[Application] | Dict[str, Any]:
        """With the Applications API, you can obtain a collection of resources, each of which represents an application.
        When you run a GET operation on this resource, you obtain a collection of Application Objects."""
        url = f"{cls.rm_url}/apps"
        msg_log = f"Cluster apps ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                apps_data = r.json().get('apps', {}).get('app', [])
                if apps_data:
                    return [Application.from_dict(a) for a in apps_data]
                else:
                    return []
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_app_statistics(cls) -> List[StatItem] | Dict[str, Any]:
        """With the Application Statistics API, you can obtain a collection of triples, each of which contains the application type,
        the application state and the number of applications of this type and this state in ResourceManager context.
        Note that with the performance concern, we currently only support at most one applicationType per query.
        We may support multiple applicationTypes per query as well as more statistics in the future.
        When you run a GET operation on this resource, you obtain a collection of statItem objects."""
        url = f"{cls.rm_url}/appstatistics"
        msg_log = f"Cluster app statistics ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                stat_items = r.json().get('appStatInfo', {}).get('statItem', [])
                if stat_items:
                    return [StatItem.from_dict(a) for a in stat_items]
                else:
                    return []
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_app(cls, app_id: str) -> Application | Dict[str, Any]:
        """An application resource contains information about a particular application that was submitted to a cluster."""
        url = f"{cls.rm_url}/apps/{app_id}"
        msg_log = f"Cluster app ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return Application.from_dict(r.json().get('app'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_app_attempts(cls, app_id: str) -> List[AppAttempt] | Dict[str, Any]:
        """With the application attempts API, you can obtain a collection of resources that represent an application attempt.
        When you run a GET operation on this resource, you obtain a collection of App Attempt Objects."""
        url = f"{cls.rm_url}/apps/{app_id}/appattempts"
        msg_log = f"Cluster app attempts ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                attempts = r.json().get('appAttempts', {}).get('appAttempt', [])
                if attempts:
                    return [AppAttempt.from_dict(a) for a in attempts]
                else:
                    return []
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_app_attempt_containers(cls, app_id: str, attempt_id: str) -> List[AppContainer] | Dict[str, Any]:
        """With Containers for an Application Attempt API you can obtain the list of containers, which belongs to an Application Attempt."""
        url = f"{cls.rm_url}/apps/{app_id}/appattempts/{attempt_id}/containers"
        msg_log = f"Cluster app attempt containers ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                containers = r.json().get('containers', {}).get('container', [])
                if containers:
                    return [AppContainer.from_dict(c) for c in containers]
                else:
                    return []
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    @classmethod
    def cluster_app_attempt_container(cls, app_id: str, attempt_id: str, container_id: str) -> AppContainer | Dict[str, Any]:
        """With Specific Container for an Application Attempt API you can obtain information about a specific container,
        which belongs to an Application Attempt and selected by the container id."""
        url = f"{cls.rm_url}/apps/{app_id}/appattempts/{attempt_id}/containers/{container_id}"
        msg_log = f"Cluster app attempt container ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                return AppContainer.from_dict(r.json().get('container'))
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # Cluster Nodes APIs

    @classmethod
    def cluster_nodes(cls) -> List[ClusterNode] | Dict[str, Any]:
        """With the Nodes API, you can obtain a collection of resources, each of which represents a node.
        When you run a GET operation on this resource, you obtain a collection of Node Objects."""
        url = f"{cls.rm_url}/nodes"
        msg_log = f"Cluster nodes ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                logger.info(f"{msg_log}: {r.text}")
                nodes = r.json().get('nodes', {}).get('node', [])
                if nodes:
                    # Always return dicts
                    return [ClusterNode.from_dict(n) for n in nodes]
                else:
                    return []
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': str(e)}

    @classmethod
    def cluster_node(cls, node_id: str) -> ClusterNode | Dict[str, Any]:
        """A node resource contains information about a node in the cluster."""
        url = f"{cls.rm_url}/nodes/{node_id}"
        msg_log = f"Cluster node ({url})"
        logger.info(msg_log)
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

    # Cluster Writeable APIs (Alpha)

    # --- New Application API ---

    @classmethod
    def cluster_new_application(cls) -> ClusterNewApplication | Dict[str, Any]:
        """With the New Application API, you can obtain an application-id which can then be used as part of
        the Cluster Submit Applications API to submit applications.
        The response also includes the maximum resource capabilities available on the cluster.

        This feature is currently in the alpha stage and may change in the future."""
        url = f"{cls.rm_url}/apps/new-application"
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

    # --- Submit Application API ---

    @classmethod
    def cluster_submit_application(cls, app_submit: ClusterAppSubmit) -> Dict[str, Any]:
        """The Submit Applications API can be used to submit applications.
        In case of submitting applications, you must first obtain an application-id using the Cluster New Application API.
        The application-id must be part of the request body.
        The response contains a URL to the application page which can be used to track the state and progress of your application."""
        url = f"{cls.rm_url}/apps"
        msg_log = f"Cluster submit applications ({url})"
        logger.info(msg_log)
        try:
            r = requests.post(url, json=app_submit.to_dict())
            if r.status_code == 202:
                logger.info(f"{msg_log}: App submitted successfully")
                return {
                    'status_code': r.status_code,
                    'msg': 'App submitted successfully',
                    'location': r.headers.get('Location')
                }
            else:
                logger.error(f"{msg_log}: status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': e}

    # --- Application State APIs ---

    @classmethod
    def get_application_state(cls, app_id: str) -> Dict[str, Any]:
        """
        Get the state of a submitted application.

        With the application state API, you can query the state of a submitted app.

        Args:
            app_id: The application ID (e.g., application_1399397633663_0003)

        Returns:
            Dictionary containing the application state or error information
        """
        url = f"{cls.rm_url}/apps/{app_id}/state"
        msg_log = f"Get application state ({url})"
        logger.info(msg_log)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                state_data = r.json()
                state_response = AppStateResponse.from_dict(state_data)
                logger.info(f"{msg_log}: Application state retrieved successfully - {state_response.state.value}")
                return {
                    'status_code': r.status_code,
                    'msg': 'Application state retrieved successfully',
                    'state': state_response.state.value
                }
            else:
                logger.error(f"{msg_log}: Failed with status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}
        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': str(e)}

    @classmethod
    def kill_application(cls, app_id: str) -> Dict[str, Any]:
        """
        Kill a running application by modifying its state to KILLED.

        To perform the PUT operation, authentication has to be setup for the RM web services.
        In addition, you must be authorized to kill the app. Currently you can only change the
        state to "KILLED"; an attempt to change the state to any other results in a 400 error response.

        When you carry out a successful PUT, the initial response may be a 202. You can confirm
        that the app is killed by repeating the PUT request until you get a 200, querying the
        state using the GET method or querying for app information and checking the state.

        Args:
            app_id: The application ID (e.g., application_1399397633663_0003)

        Returns:
            Dictionary containing the result of the kill operation or error information
        """
        url = f"{cls.rm_url}/apps/{app_id}/state"
        msg_log = f"Kill application ({url})"
        logger.info(msg_log)

        kill_request = KillAppRequest()

        try:
            r = requests.put(url, json=kill_request.to_dict())

            if r.status_code == 200:
                # Application is confirmed killed
                state_data = r.json()
                state_response = AppStateResponse.from_dict(state_data)
                logger.info(f"{msg_log}: Application killed successfully - State: {state_response.state.value}")
                return {
                    'status_code': r.status_code,
                    'msg': 'Application killed successfully',
                    'state': state_response.state.value
                }
            elif r.status_code == 202:
                # Application kill initiated but not yet completed
                state_data = r.json()
                state_response = AppStateResponse.from_dict(state_data)
                logger.info(f"{msg_log}: Kill request accepted, application state: {state_response.state.value}")
                return {
                    'status_code': r.status_code,
                    'msg': 'Kill request accepted, application may still be running',
                    'state': state_response.state.value
                }
            elif r.status_code == 400:
                logger.error(f"{msg_log}: Bad request - Only 'KILLED' is allowed as a target state")
                return {
                    'status_code': r.status_code,
                    'error': 'Bad request - Only KILLED state is allowed',
                    'response': r.text
                }
            elif r.status_code == 403:
                logger.error(f"{msg_log}: Unauthorized - Authentication required")
                return {
                    'status_code': r.status_code,
                    'error': 'Unauthorized - Authentication filter must be setup'
                }
            else:
                logger.error(f"{msg_log}: Failed with status code: {r.status_code}")
                return {'status_code': r.status_code, 'error': r.text}

        except Exception as e:
            logger.error(f"{msg_log}: {e}")
            return {'status_code': 500, 'error': str(e)}

    @classmethod
    def kill_application_with_retry(cls, app_id: str, max_retries: int = 5, retry_delay: float = 1.0) -> Dict[str, Any]:
        """
        Kill an application with automatic retry until confirmed killed.

        This method handles the initial 202 response by automatically retrying the
        PUT request until a 200 response is received (confirmed killed) or max retries reached.

        Args:
            app_id: The application ID (e.g., application_1399397633663_0003)
            max_retries: Maximum number of retry attempts (default: 5)
            retry_delay: Delay between retries in seconds (default: 1.0)

        Returns:
            Dictionary containing the final result of the kill operation
        """
        msg_log = f"Kill application with retry for {app_id}"
        logger.info(msg_log)

        result = {}
        for attempt in range(max_retries):
            result = cls.kill_application(app_id)

            if result['status_code'] == 200:
                logger.info(f"{msg_log}: Application confirmed killed after {attempt + 1} attempt(s)")
                return result
            elif result['status_code'] == 202:
                logger.info(f"{msg_log}: Attempt {attempt + 1}/{max_retries} - Application not yet killed, retrying...")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                continue
            else:
                # Error occurred (400, 403, etc.)
                logger.error(f"{msg_log}: Error occurred during kill attempt {attempt + 1}")
                return result

        logger.warning(f"{msg_log}: Max retries reached, application may still be running")
        return {
            'status_code': 202,
            'msg': f'Max retries ({max_retries}) reached. Application may still be running. Verify state manually.',
            'state': result.get('state', 'UNKNOWN')
        }

    # Application State Utility Methods

    @classmethod
    def is_application_running(cls, app_id: str) -> bool:
        """
        Check if an application is still running.

        Args:
            app_id: The application ID

        Returns:
            True if the application is in a running state, False otherwise
        """
        result = cls.get_application_state(app_id)
        if result['status_code'] == 200:
            running_states = [
                AppState.NEW,
                AppState.NEW_SAVING,
                AppState.SUBMITTED,
                AppState.ACCEPTED,
                AppState.RUNNING
            ]
            return AppState(result['state']) in running_states
        return False

    @classmethod
    def is_application_finished(cls, app_id: str) -> bool:
        """
        Check if an application has finished (successfully or not).

        Args:
            app_id: The application ID

        Returns:
            True if the application is in a final state, False otherwise
        """
        result = cls.get_application_state(app_id)
        if result['status_code'] == 200:
            final_states = [
                AppState.FINISHED,
                AppState.FAILED,
                AppState.KILLED
            ]
            return AppState(result['state']) in final_states
        return False

    @classmethod
    def wait_for_application_state(cls, app_id: str, target_states: List[AppState],
                                   timeout: int = 60, check_interval: float = 1.0) -> Dict[str, Any]:
        """
        Wait for an application to reach a specific state.

        Args:
            app_id: The application ID
            target_states: List of target states to wait for
                          (e.g., [AppState.FINISHED, AppState.FAILED, AppState.KILLED])
            timeout: Maximum time to wait in seconds (default: 60)
            check_interval: Time between state checks in seconds (default: 1.0)

        Returns:
            Dictionary with the final state information
        """
        msg_log = f"Wait for application {app_id}"
        logger.info(f"{msg_log}: Waiting for states: {[s.value for s in target_states]}")

        start_time = time.time()
        result = {}

        while time.time() - start_time < timeout:
            result = cls.get_application_state(app_id)

            if result['status_code'] == 200:
                current_state = AppState(result['state'])
                logger.info(f"{msg_log}: Current state: {current_state.value}")

                if current_state in target_states:
                    logger.info(f"{msg_log}: Reached target state: {current_state.value}")
                    return result
            else:
                logger.error(f"{msg_log}: Failed to get state")
                return result

            time.sleep(check_interval)

        elapsed_time = time.time() - start_time
        logger.warning(f"{msg_log}: Timeout after {elapsed_time:.2f} seconds")
        return {
            'status_code': 408,
            'error': f'Timeout waiting for application to reach states: {[s.value for s in target_states]}',
            'state': result.get('state', 'UNKNOWN') if 'result' in locals() else 'UNKNOWN'
        }

    @classmethod
    def submit_and_wait(cls, app_submit: ClusterAppSubmit,
                        timeout: int = 300,
                        check_interval: float = 5.0) -> Dict[str, Any]:
        """
        Submit an application and wait for it to complete.

        Args:
            app_submit: The application submission details
            timeout: Maximum time to wait in seconds (default: 300)
            check_interval: Time between state checks in seconds (default: 5.0)

        Returns:
            Dictionary with the final application status
        """
        # Get new application ID first if not provided
        if not app_submit.application_id:
            new_app_result = cls.cluster_new_application()
            if isinstance(new_app_result, dict) and 'error' in new_app_result:
                return new_app_result
            app_submit.application_id = new_app_result.application_id

        # Submit the application
        submit_result = cls.cluster_submit_application(app_submit)
        if submit_result['status_code'] != 202:
            return submit_result

        app_id = app_submit.application_id
        logger.info(f"Application {app_id} submitted, waiting for completion...")

        # Wait for final state
        final_states = [AppState.FINISHED, AppState.FAILED, AppState.KILLED]
        result = cls.wait_for_application_state(
            app_id,
            target_states=final_states,
            timeout=timeout,
            check_interval=check_interval
        )

        return result

    @classmethod
    def kill_and_wait(cls, app_id: str, timeout: int = 60, check_interval: float = 1.0) -> Dict[str, Any]:
        """
        Kill an application and wait for it to be killed.

        Args:
            app_id: The application ID
            timeout: Maximum time to wait in seconds (default: 60)
            check_interval: Time between state checks in seconds (default: 1.0)

        Returns:
            Dictionary with the final application status
        """
        # Send kill request
        kill_result = cls.kill_application(app_id)
        if kill_result['status_code'] not in [200, 202]:
            return kill_result

        # Wait for killed state
        return cls.wait_for_application_state(
            app_id,
            target_states=[AppState.KILLED],
            timeout=timeout,
            check_interval=check_interval
        )

