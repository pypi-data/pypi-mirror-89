﻿'''_4162.py

ComponentCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4212
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ComponentCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundModalAnalysesAtSpeeds',)


class ComponentCompoundModalAnalysesAtSpeeds(_4212.PartCompoundModalAnalysesAtSpeeds):
    '''ComponentCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
