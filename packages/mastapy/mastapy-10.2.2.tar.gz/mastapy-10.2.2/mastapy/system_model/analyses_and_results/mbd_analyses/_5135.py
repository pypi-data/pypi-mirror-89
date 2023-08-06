﻿'''_5135.py

SynchroniserMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2179
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6246
from mastapy.system_model.analyses_and_results.mbd_analyses import _5119
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SynchroniserMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserMultiBodyDynamicsAnalysis',)


class SynchroniserMultiBodyDynamicsAnalysis(_5119.SpecialisedAssemblyMultiBodyDynamicsAnalysis):
    '''SynchroniserMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserMultiBodyDynamicsAnalysis.TYPE'):
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
