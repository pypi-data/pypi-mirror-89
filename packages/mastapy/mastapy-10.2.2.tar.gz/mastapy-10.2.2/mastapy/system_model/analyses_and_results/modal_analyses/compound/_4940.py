﻿'''_4940.py

FaceGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2110
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4796
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4944
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FaceGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundModalAnalysis',)


class FaceGearCompoundModalAnalysis(_4944.GearCompoundModalAnalysis):
    '''FaceGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2110.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4796.FaceGearModalAnalysis]':
        '''List[FaceGearModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4796.FaceGearModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4796.FaceGearModalAnalysis]':
        '''List[FaceGearModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4796.FaceGearModalAnalysis))
        return value
