﻿'''_4432.py

FaceGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4430, _4431, _4436
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4310
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'FaceGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundModalAnalysisAtAStiffness',)


class FaceGearSetCompoundModalAnalysisAtAStiffness(_4436.GearSetCompoundModalAnalysisAtAStiffness):
    '''FaceGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2111.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2111.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4430.FaceGearCompoundModalAnalysisAtAStiffness]':
        '''List[FaceGearCompoundModalAnalysisAtAStiffness]: 'FaceGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundModalAnalysisAtAStiffness, constructor.new(_4430.FaceGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def face_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4431.FaceGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[FaceGearMeshCompoundModalAnalysisAtAStiffness]: 'FaceMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_4431.FaceGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4310.FaceGearSetModalAnalysisAtAStiffness]':
        '''List[FaceGearSetModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4310.FaceGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4310.FaceGearSetModalAnalysisAtAStiffness]':
        '''List[FaceGearSetModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4310.FaceGearSetModalAnalysisAtAStiffness))
        return value
