﻿'''_5087.py

KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2121
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6196
from mastapy.system_model.analyses_and_results.mbd_analyses import _5086, _5085, _5084
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis(_5084.KlingelnbergCycloPalloidConicalGearSetMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2121.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6196.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6196.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5086.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5086.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_multi_body_dynamics_analysis(self) -> 'List[_5086.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsMultiBodyDynamicsAnalysis, constructor.new(_5086.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_multi_body_dynamics_analysis(self) -> 'List[_5085.KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesMultiBodyDynamicsAnalysis, constructor.new(_5085.KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis))
        return value
