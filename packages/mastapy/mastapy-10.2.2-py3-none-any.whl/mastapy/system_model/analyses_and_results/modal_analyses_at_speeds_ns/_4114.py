﻿'''_4114.py

StabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4086
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _6548
from mastapy._internal.python_net import python_net_import

_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StabilityAnalysis',)


class StabilityAnalysis(_6548.StaticLoadAnalysisCase):
    '''StabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analyses_at_speeds_options(self) -> '_4086.ModalAnalysesAtSpeedsOptions':
        '''ModalAnalysesAtSpeedsOptions: 'ModalAnalysesAtSpeedsOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4086.ModalAnalysesAtSpeedsOptions)(self.wrapped.ModalAnalysesAtSpeedsOptions) if self.wrapped.ModalAnalysesAtSpeedsOptions else None
