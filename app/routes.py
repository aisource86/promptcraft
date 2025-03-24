from flask import Blueprint, request, jsonify
import grpc
from grpc.service_pb2_grpc import MyServiceStub
from grpc.service_pb2 import Request as GrpcRequest

main = Blueprint('main', __name__)

@main.route('/grpc-message', methods=['POST'])
def grpc_message():
    data = request.json
    name = data.get('name', 'Unknown')

    # Connect to gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = MyServiceStub(channel)
        grpc_request = GrpcRequest(name=name)
        grpc_response = stub.GetMessage(grpc_request)

    return jsonify({"message": grpc_response.message})
