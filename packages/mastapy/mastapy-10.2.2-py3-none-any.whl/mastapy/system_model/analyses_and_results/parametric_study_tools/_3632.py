﻿'''_3632.py

SynchroniserParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2179
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6246
from mastapy.system_model.analyses_and_results.system_deflections import _2374
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3616
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SynchroniserParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserParametricStudyTool',)


class SynchroniserParametricStudyTool(_3616.SpecialisedAssemblyParametricStudyTool):
    '''SynchroniserParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2179.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2179.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6246.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6246.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2374.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2374.SynchroniserSystemDeflection))
        return value
