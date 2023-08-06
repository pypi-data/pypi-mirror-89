﻿'''_5391.py

KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2123
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6199
from mastapy.system_model.analyses_and_results.system_deflections import _2328
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5389, _5390, _5385
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis(_5385.KlingelnbergCycloPalloidConicalGearSetGearWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2328.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2328.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5389.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5389.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_gear_whine_analysis(self) -> 'List[_5389.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsGearWhineAnalysis, constructor.new(_5389.KlingelnbergCycloPalloidSpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5390.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5390.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_gear_whine_analysis(self) -> 'List[_5390.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesGearWhineAnalysis, constructor.new(_5390.KlingelnbergCycloPalloidSpiralBevelGearMeshGearWhineAnalysis))
        return value
