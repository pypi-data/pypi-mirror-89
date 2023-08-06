﻿'''_4054.py

CVTPulleyModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2165
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4099
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CVTPulleyModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyModalAnalysesAtSpeeds',)


class CVTPulleyModalAnalysesAtSpeeds(_4099.PulleyModalAnalysesAtSpeeds):
    '''CVTPulleyModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2165.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2165.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
