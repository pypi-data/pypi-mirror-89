﻿'''_3826.py

HypoidGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2117
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6187
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3825, _3824, _3772
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'HypoidGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetModalAnalysesAtStiffnesses',)


class HypoidGearSetModalAnalysesAtStiffnesses(_3772.AGMAGleasonConicalGearSetModalAnalysesAtStiffnesses):
    '''HypoidGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2117.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6187.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6187.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_modal_analyses_at_stiffnesses(self) -> 'List[_3825.HypoidGearModalAnalysesAtStiffnesses]':
        '''List[HypoidGearModalAnalysesAtStiffnesses]: 'HypoidGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsModalAnalysesAtStiffnesses, constructor.new(_3825.HypoidGearModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_3824.HypoidGearMeshModalAnalysesAtStiffnesses]':
        '''List[HypoidGearMeshModalAnalysesAtStiffnesses]: 'HypoidMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesModalAnalysesAtStiffnesses, constructor.new(_3824.HypoidGearMeshModalAnalysesAtStiffnesses))
        return value
