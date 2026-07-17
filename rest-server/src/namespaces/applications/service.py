from typing import Dict, Any, List

from config.logger import get_logger
from namespaces.applications.models import AMContainerSpec, Resource, ClusterAppSubmit
from services.yarn_client import YarnClient


logger = get_logger(__name__)


class ApplicationService:

    @staticmethod
    def get_all_applications() -> List[Dict[str, Any]]:
        """Get all applications from YARN"""
        try:
            result = YarnClient.cluster_apps()
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"Failed to get applications: {result.get('error')}")
                return []
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error getting applications: {e}")
            return []

    @staticmethod
    def get_application(app_id: str) -> Dict[str, Any]:
        """Get specific application details"""
        try:
            result = YarnClient.cluster_app(app_id)
            if isinstance(result, dict):
                if 'error' in result:
                    logger.error(f"Failed to get application {app_id}: {result.get('error')}")
                return result
            return result.__dict__ if hasattr(result, '__dict__') else result
        except Exception as e:
            logger.error(f"Error getting application {app_id}: {e}")
            return {'error': str(e)}

    @staticmethod
    def get_application_state(app_id: str) -> Dict[str, Any]:
        """Get application state"""
        try:
            result = YarnClient.get_application_state(app_id)
            return result
        except Exception as e:
            logger.error(f"Error getting application state {app_id}: {e}")
            return {'error': str(e), 'state': 'UNKNOWN'}

    @staticmethod
    def kill_application(app_id: str) -> Dict[str, Any]:
        """Kill an application"""
        try:
            # First try to kill with retry
            result = YarnClient.kill_application_with_retry(app_id, max_retries=3, retry_delay=2.0)
            return result
        except Exception as e:
            logger.error(f"Error killing application {app_id}: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def get_app_attempts(app_id: str) -> List[Dict[str, Any]]:
        """Get application attempts"""
        try:
            result = YarnClient.cluster_app_attempts(app_id)
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"Failed to get app attempts for {app_id}: {result.get('error')}")
                return []
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error getting app attempts for {app_id}: {e}")
            return []

    @staticmethod
    def get_app_statistics() -> List[Dict[str, Any]]:
        """Get application statistics"""
        try:
            result = YarnClient.cluster_app_statistics()
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"Failed to get app statistics: {result.get('error')}")
                return []
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error getting app statistics: {e}")
            return []

    @staticmethod
    def submit_application(data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new application"""
        try:
            # First get a new application ID
            new_app = YarnClient.cluster_new_application()
            if isinstance(new_app, dict) and 'error' in new_app:
                return {'error': 'Failed to get new application ID', 'status_code': 500}

            application_id = new_app.application_id if hasattr(new_app, 'application_id') else new_app.get('application-id')

            # Create AM Container Spec
            am_spec_data = data.get('amContainerSpec', {})
            am_spec = AMContainerSpec(
                local_resources=am_spec_data.get('localResources', {}),
                environment=am_spec_data.get('environment', {}),
                commands=am_spec_data.get('commands', []),
                service_data=am_spec_data.get('serviceData', {}),
                credentials=am_spec_data.get('credentials'),
                application_acls=am_spec_data.get('applicationAcls', {})
            )

            # Create resource
            resource = Resource(
                memory=data.get('memory', 1024),
                vCores=data.get('vCores', 1)
            )

            # Create application submission
            app_submit = ClusterAppSubmit(
                application_id=application_id,
                application_name=data.get('applicationName', 'default-app'),
                queue=data.get('queue', 'default'),
                priority=data.get('priority', 0),
                am_container_spec=am_spec,
                unmanaged_am=False,
                max_app_attempts=data.get('maxAppAttempts', 2),
                resource=resource,
                application_type=data.get('applicationType', 'YARN'),
                keep_containers_across_application_attempts=False,
                application_tags=data.get('applicationTags', []),
                log_aggregation_context=data.get('logAggregationContext'),
                attempt_failures_validity_interval=data.get('attemptFailuresValidityInterval'),
                reservation_id=data.get('reservationId'),
                am_black_listing_requests=data.get('amBlackListingRequests')
            )

            # Submit the application
            result = YarnClient.cluster_submit_application(app_submit)

            if result.get('status_code') == 202:
                return {
                    'message': 'Application submitted successfully',
                    'applicationId': application_id,
                    'status': 'SUBMITTED'
                }
            else:
                return {
                    'error': result.get('error', 'Failed to submit application'),
                    'status_code': result.get('status_code', 500)
                }

        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def get_app_containers(app_id: str, attempt_id: str) -> List[Dict[str, Any]]:
        """Get containers for an application attempt"""
        try:
            result = YarnClient.cluster_app_attempt_containers(app_id, attempt_id)
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"Failed to get containers for {app_id}/{attempt_id}: {result.get('error')}")
                return []
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error getting containers for {app_id}/{attempt_id}: {e}")
            return []

    @staticmethod
    def get_container_details(app_id: str, attempt_id: str, container_id: str) -> Dict[str, Any]:
        """Get specific container details"""
        try:
            result = YarnClient.cluster_app_attempt_container(app_id, attempt_id, container_id)
            return result.__dict__ if hasattr(result, '__dict__') else result
        except Exception as e:
            logger.error(f"Error getting container {container_id}: {e}")
            return {'error': str(e)}
