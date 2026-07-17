from flask_restx import Namespace, Resource, reqparse
from .models import node_model, resource_utilization_model, total_resource_model, node_health_model, \
    node_health_item_model
from .service import NodeService

nodes_ns = Namespace(
    'nodes',
    description='Node management and monitoring operations'
)

# Register models
nodes_ns.models[node_model.name] = node_model
nodes_ns.models[resource_utilization_model.name] = resource_utilization_model
nodes_ns.models[total_resource_model.name] = total_resource_model
nodes_ns.models[node_health_model.name] = node_health_model
nodes_ns.models[node_health_item_model.name] = node_health_item_model

# Request parser for filtering nodes
node_filter_parser = reqparse.RequestParser()
node_filter_parser.add_argument('state', type=str, help='Filter by node state (RUNNING, UNHEALTHY, etc.)')
node_filter_parser.add_argument('rack', type=str, help='Filter by rack name')


@nodes_ns.route('/')
class NodeListResource(Resource):

    @nodes_ns.doc('list_nodes')
    @nodes_ns.expect(node_filter_parser)
    @nodes_ns.marshal_list_with(node_model)
    @nodes_ns.response(200, 'Success')
    @nodes_ns.response(500, 'Internal Server Error')
    def get(self):
        """List all nodes in the cluster"""
        args = node_filter_parser.parse_args()
        nodes = NodeService.get_all_nodes()

        # Apply filters if provided
        if args.get('state'):
            nodes = [n for n in nodes if n.get('state', '').upper() == args['state'].upper()]
        if args.get('rack'):
            nodes = [n for n in nodes if n.get('rack', '') == args['rack']]

        return nodes


@nodes_ns.route('/statistics')
class NodeStatisticsResource(Resource):

    @nodes_ns.doc('get_node_statistics')
    @nodes_ns.response(200, 'Success')
    @nodes_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get node statistics and aggregate information"""
        return NodeService.get_node_statistics()


@nodes_ns.route('/<string:node_id>')
@nodes_ns.param('node_id', 'The node identifier')
class NodeDetailResource(Resource):

    @nodes_ns.doc('get_node')
    @nodes_ns.marshal_with(node_model)
    @nodes_ns.response(200, 'Success')
    @nodes_ns.response(404, 'Node not found')
    @nodes_ns.response(500, 'Internal Server Error')
    def get(self, node_id):
        """Get specific node details"""
        node = NodeService.get_node(node_id)
        if not node or isinstance(node, dict):
            nodes_ns.abort(404, f"Node {node_id} not found")
        return node


@nodes_ns.route('/<string:node_id>/utilization')
@nodes_ns.param('node_id', 'The node identifier')
class NodeUtilizationResource(Resource):

    @nodes_ns.doc('get_node_utilization')
    @nodes_ns.response(200, 'Success')
    @nodes_ns.response(404, 'Node not found')
    @nodes_ns.response(500, 'Internal Server Error')
    def get(self, node_id):
        """Get resource utilization for a specific node"""
        utilization = NodeService.get_node_resource_utilization(node_id)
        if not utilization or 'error' in utilization:
            nodes_ns.abort(404, f"Node {node_id} not found")
        return utilization


@nodes_ns.route('/health')
class NodeHealthResource(Resource):

    @nodes_ns.doc('get_nodes_health')
    @nodes_ns.marshal_with(node_health_model)
    @nodes_ns.response(200, 'Success')
    @nodes_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get health status of all nodes"""
        nodes = NodeService.get_all_nodes()

        def get_health_status(state: str) -> str:
            """Map node state to health status"""
            healthy_states = ['RUNNING', 'NEW']
            unhealthy_states = ['UNHEALTHY', 'LOST', 'REBOOTED']

            if state in healthy_states:
                return 'Healthy'
            elif state in unhealthy_states:
                return 'Unhealthy'
            else:
                return state

        health_summary = {
            'total': len(nodes),
            'healthy': len([n for n in nodes if n.state in ['RUNNING', 'NEW']]),
            'unhealthy': len([n for n in nodes if n.state in ['UNHEALTHY', 'LOST', 'REBOOTED']]),
            'lost': len([n for n in nodes if n.state == 'LOST']),
            'decommissioned': len([n for n in nodes if n.state == 'DECOMMISSIONED']),
            'nodes': [
                {
                    'id': n.id,
                    'hostname': n.nodeHostName,
                    'state': n.state,
                    'healthStatus': get_health_status(n.state),
                    'lastHealthUpdate': n.lastHealthUpdate
                }
                for n in nodes
            ]
        }

        return health_summary

