# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from p2pfl.communication.protocols.edge.proto import edge_node_pb2 as edge__node__pb2


class NodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MainStream = channel.stream_stream(
                '/edge_node.Node/MainStream',
                request_serializer=edge__node__pb2.EdgeMessage.SerializeToString,
                response_deserializer=edge__node__pb2.EdgeMessage.FromString,
                )


class NodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MainStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MainStream': grpc.stream_stream_rpc_method_handler(
                    servicer.MainStream,
                    request_deserializer=edge__node__pb2.EdgeMessage.FromString,
                    response_serializer=edge__node__pb2.EdgeMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'edge_node.Node', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Node(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MainStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/edge_node.Node/MainStream',
            edge__node__pb2.EdgeMessage.SerializeToString,
            edge__node__pb2.EdgeMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
