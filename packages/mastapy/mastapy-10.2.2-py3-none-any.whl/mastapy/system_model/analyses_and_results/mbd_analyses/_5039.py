﻿'''_5039.py

CoaxialConnectionMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1873
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6122
from mastapy.system_model.analyses_and_results.mbd_analyses import _5117
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CoaxialConnectionMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionMultiBodyDynamicsAnalysis',)


class CoaxialConnectionMultiBodyDynamicsAnalysis(_5117.ShaftToMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''CoaxialConnectionMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1873.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1873.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6122.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6122.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
