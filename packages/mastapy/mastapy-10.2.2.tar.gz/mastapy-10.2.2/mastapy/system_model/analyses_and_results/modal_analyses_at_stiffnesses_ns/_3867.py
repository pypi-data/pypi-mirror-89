﻿'''_3867.py

SpringDamperModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2177
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6235
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3805
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'SpringDamperModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperModalAnalysesAtStiffnesses',)


class SpringDamperModalAnalysesAtStiffnesses(_3805.CouplingModalAnalysesAtStiffnesses):
    '''SpringDamperModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2177.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6235.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6235.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
