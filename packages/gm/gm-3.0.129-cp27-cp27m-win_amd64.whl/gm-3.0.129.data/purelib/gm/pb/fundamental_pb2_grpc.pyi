from typing import Any, Optional

class FundamentalServiceStub:
    GetFundamentals: Any = ...
    GetFundamentalsN: Any = ...
    GetInstrumentInfos: Any = ...
    GetFuzzyMatchInstrumentInfos: Any = ...
    GetInstruments: Any = ...
    GetHistoryInstruments: Any = ...
    GetConstituents: Any = ...
    GetSector: Any = ...
    GetIndustry: Any = ...
    GetConcept: Any = ...
    GetTradingDates: Any = ...
    GetPreviousTradingDate: Any = ...
    GetNextTradingDate: Any = ...
    GetTradingTimes: Any = ...
    GetDividends: Any = ...
    GetDividendsSnapshot: Any = ...
    GetContinuousContracts: Any = ...
    GetOptionsByUnderlying: Any = ...
    def __init__(self, channel: Any) -> None: ...

class FundamentalServiceServicer:
    def GetFundamentals(self, request: Any, context: Any) -> None: ...
    def GetFundamentalsN(self, request: Any, context: Any) -> None: ...
    def GetInstrumentInfos(self, request: Any, context: Any) -> None: ...
    def GetFuzzyMatchInstrumentInfos(self, request: Any, context: Any) -> None: ...
    def GetInstruments(self, request: Any, context: Any) -> None: ...
    def GetHistoryInstruments(self, request: Any, context: Any) -> None: ...
    def GetConstituents(self, request: Any, context: Any) -> None: ...
    def GetSector(self, request: Any, context: Any) -> None: ...
    def GetIndustry(self, request: Any, context: Any) -> None: ...
    def GetConcept(self, request: Any, context: Any) -> None: ...
    def GetTradingDates(self, request: Any, context: Any) -> None: ...
    def GetPreviousTradingDate(self, request: Any, context: Any) -> None: ...
    def GetNextTradingDate(self, request: Any, context: Any) -> None: ...
    def GetTradingTimes(self, request: Any, context: Any) -> None: ...
    def GetDividends(self, request: Any, context: Any) -> None: ...
    def GetDividendsSnapshot(self, request: Any, context: Any) -> None: ...
    def GetContinuousContracts(self, request: Any, context: Any) -> None: ...
    def GetOptionsByUnderlying(self, request: Any, context: Any) -> None: ...

def add_FundamentalServiceServicer_to_server(servicer: Any, server: Any) -> None: ...

class FundamentalService:
    @staticmethod
    def GetFundamentals(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetFundamentalsN(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetInstrumentInfos(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetFuzzyMatchInstrumentInfos(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetInstruments(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetHistoryInstruments(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetConstituents(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetSector(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetIndustry(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetConcept(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetTradingDates(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetPreviousTradingDate(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetNextTradingDate(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetTradingTimes(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetDividends(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetDividendsSnapshot(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetContinuousContracts(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
    @staticmethod
    def GetOptionsByUnderlying(request: Any, target: Any, options: Any = ..., channel_credentials: Optional[Any] = ..., call_credentials: Optional[Any] = ..., compression: Optional[Any] = ..., wait_for_ready: Optional[Any] = ..., timeout: Optional[Any] = ..., metadata: Optional[Any] = ...): ...
