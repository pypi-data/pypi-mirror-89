﻿'''_3866.py

SpringDamperHalfModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2178
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6234
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3804
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'SpringDamperHalfModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfModalAnalysesAtStiffnesses',)


class SpringDamperHalfModalAnalysesAtStiffnesses(_3804.CouplingHalfModalAnalysesAtStiffnesses):
    '''SpringDamperHalfModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2178.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2178.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6234.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6234.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
