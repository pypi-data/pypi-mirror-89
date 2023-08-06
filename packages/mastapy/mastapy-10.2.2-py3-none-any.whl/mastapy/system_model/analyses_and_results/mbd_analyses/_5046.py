﻿'''_5046.py

ConceptGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2104
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6129
from mastapy.system_model.analyses_and_results.mbd_analyses import _5045, _5044, _5071
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ConceptGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetMultiBodyDynamicsAnalysis',)


class ConceptGearSetMultiBodyDynamicsAnalysis(_5071.GearSetMultiBodyDynamicsAnalysis):
    '''ConceptGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2104.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2104.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6129.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6129.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5045.ConceptGearMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5045.ConceptGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_gears_multi_body_dynamics_analysis(self) -> 'List[_5045.ConceptGearMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearMultiBodyDynamicsAnalysis]: 'ConceptGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsMultiBodyDynamicsAnalysis, constructor.new(_5045.ConceptGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_meshes_multi_body_dynamics_analysis(self) -> 'List[_5044.ConceptGearMeshMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearMeshMultiBodyDynamicsAnalysis]: 'ConceptMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesMultiBodyDynamicsAnalysis, constructor.new(_5044.ConceptGearMeshMultiBodyDynamicsAnalysis))
        return value
