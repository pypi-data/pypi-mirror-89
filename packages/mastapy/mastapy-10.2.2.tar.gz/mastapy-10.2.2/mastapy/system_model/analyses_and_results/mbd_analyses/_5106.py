﻿'''_5106.py

PointLoadMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2055
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6217
from mastapy.system_model.analyses_and_results.mbd_analyses import _5145
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PointLoadMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadMultiBodyDynamicsAnalysis',)


class PointLoadMultiBodyDynamicsAnalysis(_5145.VirtualComponentMultiBodyDynamicsAnalysis):
    '''PointLoadMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2055.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2055.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6217.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6217.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
