﻿'''_5098.py

OilSealMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2050
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6205
from mastapy.system_model.analyses_and_results.mbd_analyses import _5051
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'OilSealMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealMultiBodyDynamicsAnalysis',)


class OilSealMultiBodyDynamicsAnalysis(_5051.ConnectorMultiBodyDynamicsAnalysis):
    '''OilSealMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2050.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2050.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6205.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[OilSealMultiBodyDynamicsAnalysis]':
        '''List[OilSealMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(OilSealMultiBodyDynamicsAnalysis))
        return value
