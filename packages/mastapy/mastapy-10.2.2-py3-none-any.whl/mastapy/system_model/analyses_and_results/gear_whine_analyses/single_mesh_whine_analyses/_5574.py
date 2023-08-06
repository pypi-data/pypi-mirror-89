﻿'''_5574.py

TorqueConverterTurbineSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2187
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6254
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5496
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'TorqueConverterTurbineSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineSingleMeshWhineAnalysis',)


class TorqueConverterTurbineSingleMeshWhineAnalysis(_5496.CouplingHalfSingleMeshWhineAnalysis):
    '''TorqueConverterTurbineSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2187.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6254.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6254.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
