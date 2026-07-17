from flask import Flask, request, make_response
from flask_cors import CORS
from flask_restx import Api
from config.settings import Config
from database import init_db
from config.logger import setup_logger
import logging


logger = setup_logger('app')

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes and origins
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "HEAD", "DELETE", "OPTIONS"],
        allow_headers=[
            'Content-Type',
            'Access-Control-Allow-Origin',
            'X-Requested-With',
            'Accept',
            'Origin',
            'Access-Control-Request-method',
            'Access-Control-Request-Headers',
            'Authorization',
            'App-Alert',
            'X-Total-Count',
            'File',
            'Filename',
            'X-File-Name',
            'Cache-Control'
        ],
        expose_headers=[
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Credentials',
            'Authorization',
            'app-alert',
            'app-alert-type',
            'X-Total-Count',
            'Filename'
        ]
    )

    # Configure Flask logging
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    # Log startup
    logger.info("Starting YARN Cluster Management API")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"YARN RM URL: {Config.YARN_RM_URL}")

    # Configure Flask
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize database
    try:
        init_db(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    # Create API with Swagger
    api = Api(
        app,
        version='1.0',
        title='YARN Cluster Management API',
        description='REST API for managing Hadoop/Spark jobs on YARN cluster',
        doc='/docs',
        prefix='/api'
    )

    # Register namespaces
    try:
        from namespaces.cluster.namespace import cluster_ns
        from namespaces.applications.namespace import applications_ns
        from namespaces.jobs.namespace import jobs_ns
        from namespaces.nodes.namespace import nodes_ns

        api.add_namespace(cluster_ns)
        api.add_namespace(applications_ns)
        api.add_namespace(jobs_ns)
        api.add_namespace(nodes_ns)

        logger.info("All namespaces registered successfully")
    except Exception as e:
        logger.error(f"Failed to register namespaces: {e}")
        raise


    # Add request logging middleware
    @app.before_request
    def log_request_info():
        logger.debug(f"Request: {request.method} {request.url}")
        if request.is_json:
            logger.debug(f"Request Body: {request.get_json(silent=True)}")

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,Accept")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS,PATCH")
            response.headers.add("Access-Control-Max-Age", "3600")
            return response, 200

    @app.after_request
    def log_response_info(response):
        logger.debug(f"Response: {response.status} {response.status_code}")
        return response


    @app.after_request
    def add_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, HEAD, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] =  'Content-Type, Access-Control-Allow-Origin, X-Requested-With, Accept, Origin, Access-Control-Request-method, Access-Control-Request-Headers, Authorization, App-Alert, X-Total-Count, File, Filename, X-File-Name, Cache-Control'
        return response


    # Add error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 error: {error}")
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        return {'error': 'Internal server error'}, 500



    return app


if __name__ == '__main__':
    try:
        application = create_app()
        logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
        application.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        raise
