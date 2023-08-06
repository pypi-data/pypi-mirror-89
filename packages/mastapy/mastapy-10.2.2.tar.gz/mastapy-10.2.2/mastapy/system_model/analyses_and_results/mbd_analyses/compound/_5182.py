﻿'''_5182.py

ComponentCompoundMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5232
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ComponentCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundMultiBodyDynamicsAnalysis',)


class ComponentCompoundMultiBodyDynamicsAnalysis(_5232.PartCompoundMultiBodyDynamicsAnalysis):
    '''ComponentCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
