# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from gm.pb import data_pb2 as gm_dot_pb_dot_data__pb2
from gm.pb import history_pb2 as gm_dot_pb_dot_history__pb2


class HistoryServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCurrentTicks = channel.unary_unary(
                '/history.api.HistoryService/GetCurrentTicks',
                request_serializer=gm_dot_pb_dot_history__pb2.GetCurrentTicksReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Ticks.FromString,
                )
        self.GetHistoryTicks = channel.unary_unary(
                '/history.api.HistoryService/GetHistoryTicks',
                request_serializer=gm_dot_pb_dot_history__pb2.GetHistoryTicksReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Ticks.FromString,
                )
        self.GetHistoryBars = channel.unary_unary(
                '/history.api.HistoryService/GetHistoryBars',
                request_serializer=gm_dot_pb_dot_history__pb2.GetHistoryBarsReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Bars.FromString,
                )
        self.GetHistoryTicksN = channel.unary_unary(
                '/history.api.HistoryService/GetHistoryTicksN',
                request_serializer=gm_dot_pb_dot_history__pb2.GetHistoryTicksNReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Ticks.FromString,
                )
        self.GetHistoryBarsN = channel.unary_unary(
                '/history.api.HistoryService/GetHistoryBarsN',
                request_serializer=gm_dot_pb_dot_history__pb2.GetHistoryBarsNReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_data__pb2.Bars.FromString,
                )
        self.GetBenchmarkReturn = channel.unary_unary(
                '/history.api.HistoryService/GetBenchmarkReturn',
                request_serializer=gm_dot_pb_dot_history__pb2.GetBenchmarkReturnReq.SerializeToString,
                response_deserializer=gm_dot_pb_dot_history__pb2.GetBenchmarkReturnRsp.FromString,
                )


class HistoryServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetCurrentTicks(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryTicks(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryBars(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryTicksN(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryBarsN(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBenchmarkReturn(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HistoryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCurrentTicks': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCurrentTicks,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetCurrentTicksReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Ticks.SerializeToString,
            ),
            'GetHistoryTicks': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryTicks,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetHistoryTicksReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Ticks.SerializeToString,
            ),
            'GetHistoryBars': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryBars,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetHistoryBarsReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Bars.SerializeToString,
            ),
            'GetHistoryTicksN': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryTicksN,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetHistoryTicksNReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Ticks.SerializeToString,
            ),
            'GetHistoryBarsN': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryBarsN,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetHistoryBarsNReq.FromString,
                    response_serializer=gm_dot_pb_dot_data__pb2.Bars.SerializeToString,
            ),
            'GetBenchmarkReturn': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBenchmarkReturn,
                    request_deserializer=gm_dot_pb_dot_history__pb2.GetBenchmarkReturnReq.FromString,
                    response_serializer=gm_dot_pb_dot_history__pb2.GetBenchmarkReturnRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'history.api.HistoryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HistoryService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetCurrentTicks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetCurrentTicks',
            gm_dot_pb_dot_history__pb2.GetCurrentTicksReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Ticks.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryTicks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetHistoryTicks',
            gm_dot_pb_dot_history__pb2.GetHistoryTicksReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Ticks.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryBars(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetHistoryBars',
            gm_dot_pb_dot_history__pb2.GetHistoryBarsReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Bars.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryTicksN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetHistoryTicksN',
            gm_dot_pb_dot_history__pb2.GetHistoryTicksNReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Ticks.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryBarsN(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetHistoryBarsN',
            gm_dot_pb_dot_history__pb2.GetHistoryBarsNReq.SerializeToString,
            gm_dot_pb_dot_data__pb2.Bars.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBenchmarkReturn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/history.api.HistoryService/GetBenchmarkReturn',
            gm_dot_pb_dot_history__pb2.GetBenchmarkReturnReq.SerializeToString,
            gm_dot_pb_dot_history__pb2.GetBenchmarkReturnRsp.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
