﻿'''_3809.py

CVTPulleyModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2165
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3853
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'CVTPulleyModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyModalAnalysesAtStiffnesses',)


class CVTPulleyModalAnalysesAtStiffnesses(_3853.PulleyModalAnalysesAtStiffnesses):
    '''CVTPulleyModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2165.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2165.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
