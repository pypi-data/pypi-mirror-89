﻿'''_5572.py

TorqueConverterPumpSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2185
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6253
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5496
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'TorqueConverterPumpSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSingleMeshWhineAnalysis',)


class TorqueConverterPumpSingleMeshWhineAnalysis(_5496.CouplingHalfSingleMeshWhineAnalysis):
    '''TorqueConverterPumpSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2185.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6253.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6253.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
