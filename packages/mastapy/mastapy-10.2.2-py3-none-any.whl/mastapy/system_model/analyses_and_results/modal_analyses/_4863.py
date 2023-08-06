﻿'''_4863.py

SynchroniserSleeveModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2183
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6248
from mastapy.system_model.analyses_and_results.system_deflections import _2373
from mastapy.system_model.analyses_and_results.modal_analyses import _4862
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'SynchroniserSleeveModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveModalAnalysis',)


class SynchroniserSleeveModalAnalysis(_4862.SynchroniserPartModalAnalysis):
    '''SynchroniserSleeveModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2183.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2183.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6248.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6248.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2373.SynchroniserSleeveSystemDeflection':
        '''SynchroniserSleeveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2373.SynchroniserSleeveSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
