﻿'''_5917.py

KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2123
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5915, _5916, _5911
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis(_5911.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2123.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6199.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6199.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_dynamic_analysis(self) -> 'List[_5915.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsDynamicAnalysis, constructor.new(_5915.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_dynamic_analysis(self) -> 'List[_5916.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesDynamicAnalysis, constructor.new(_5916.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis))
        return value
