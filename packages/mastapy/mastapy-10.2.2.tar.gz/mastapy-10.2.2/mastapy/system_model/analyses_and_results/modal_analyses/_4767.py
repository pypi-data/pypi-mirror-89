﻿'''_4767.py

ClutchHalfModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2157
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6120
from mastapy.system_model.analyses_and_results.system_deflections import _2272
from mastapy.system_model.analyses_and_results.modal_analyses import _4784
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ClutchHalfModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfModalAnalysis',)


class ClutchHalfModalAnalysis(_4784.CouplingHalfModalAnalysis):
    '''ClutchHalfModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2157.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2157.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6120.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6120.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2272.ClutchHalfSystemDeflection':
        '''ClutchHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.ClutchHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
