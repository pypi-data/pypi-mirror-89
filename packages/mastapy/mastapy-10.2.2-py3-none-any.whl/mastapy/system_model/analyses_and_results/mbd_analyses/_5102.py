﻿'''_5102.py

PartToPartShearCouplingMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2166
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6210
from mastapy.system_model.analyses_and_results.mbd_analyses import _5054
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PartToPartShearCouplingMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingMultiBodyDynamicsAnalysis',)


class PartToPartShearCouplingMultiBodyDynamicsAnalysis(_5054.CouplingMultiBodyDynamicsAnalysis):
    '''PartToPartShearCouplingMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2166.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6210.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6210.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
