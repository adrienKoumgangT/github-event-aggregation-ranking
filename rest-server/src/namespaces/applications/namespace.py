from flask_restx import Namespace, Resource
from .models import (
    application_model, app_statistics_model, app_attempt_model,
    container_model, submit_application_model, application_state_model, am_container_spec_model, resource_request_model,
    resource_capability_model, resource_information_model, resource_informations_model, execution_type_request_model,
    resource_usage_model, resource_usages_by_partition_model, resource_info_model, application_timeout_model,
    resource_seconds_map_entry_model, application_summary_model
)
from .service import ApplicationService

applications_ns = Namespace(
    'applications',
    description='Application management operations'
)

# Register models
applications_ns.models[application_model.name] = application_model
applications_ns.models[application_summary_model.name] = application_summary_model
applications_ns.models[resource_request_model.name] = resource_request_model
applications_ns.models[resource_capability_model.name] = resource_capability_model
applications_ns.models[resource_information_model.name] = resource_information_model
applications_ns.models[resource_informations_model.name] = resource_informations_model
applications_ns.models[execution_type_request_model.name] = execution_type_request_model
applications_ns.models[resource_usage_model.name] = resource_usage_model
applications_ns.models[resource_usages_by_partition_model.name] = resource_usages_by_partition_model
applications_ns.models[resource_info_model.name] = resource_info_model
applications_ns.models[application_timeout_model.name] = application_timeout_model
applications_ns.models[resource_seconds_map_entry_model.name] = resource_seconds_map_entry_model
applications_ns.models[app_statistics_model.name] = app_statistics_model
applications_ns.models[app_attempt_model.name] = app_attempt_model
applications_ns.models[container_model.name] = container_model
applications_ns.models[am_container_spec_model.name] = am_container_spec_model
applications_ns.models[submit_application_model.name] = submit_application_model
applications_ns.models[application_state_model.name] = application_state_model


@applications_ns.route('/')
class ApplicationListResource(Resource):

    @applications_ns.doc('list_applications')
    @applications_ns.marshal_list_with(application_summary_model)
    @applications_ns.response(200, 'Success')
    def get(self):
        """List all applications"""
        return ApplicationService.get_all_applications()


@applications_ns.route('/<string:app_id>')
@applications_ns.param('app_id', 'The application identifier')
class ApplicationDetailResource(Resource):

    @applications_ns.doc('get_application')
    @applications_ns.marshal_with(application_model)
    @applications_ns.response(200, 'Success')
    @applications_ns.response(404, 'Application not found')
    def get(self, app_id):
        """Get application details"""
        return ApplicationService.get_application(app_id)


@applications_ns.route('/<string:app_id>/state')
@applications_ns.param('app_id', 'The application identifier')
class ApplicationStateResource(Resource):

    @applications_ns.doc('get_application_state')
    @applications_ns.marshal_with(application_state_model)
    def get(self, app_id):
        """Get application state"""
        return ApplicationService.get_application_state(app_id)

    @applications_ns.doc('kill_application')
    @applications_ns.expect(application_state_model)
    @applications_ns.marshal_with(application_state_model)
    def put(self, app_id):
        """Kill an application"""
        return ApplicationService.kill_application(app_id)


@applications_ns.route('/<string:app_id>/attempts')
@applications_ns.param('app_id', 'The application identifier')
class AppAttemptsResource(Resource):

    @applications_ns.doc('get_app_attempts')
    @applications_ns.marshal_list_with(app_attempt_model)
    def get(self, app_id):
        """Get application attempts"""
        return ApplicationService.get_app_attempts(app_id)


@applications_ns.route('/statistics')
class AppStatisticsResource(Resource):

    @applications_ns.doc('get_app_statistics')
    @applications_ns.marshal_list_with(app_statistics_model)
    def get(self):
        """Get application statistics"""
        return ApplicationService.get_app_statistics()


@applications_ns.route('/submit')
class SubmitApplicationResource(Resource):

    @applications_ns.doc('submit_application')
    @applications_ns.expect(submit_application_model)
    @applications_ns.response(202, 'Application submitted')
    def post(self):
        """Submit a new application"""
        return ApplicationService.submit_application(applications_ns.payload)
