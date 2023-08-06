﻿'''_3626.py

StraightBevelGearMeshParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1928
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6241
from mastapy.system_model.analyses_and_results.system_deflections import _2366
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3523
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'StraightBevelGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshParametricStudyTool',)


class StraightBevelGearMeshParametricStudyTool(_3523.BevelGearMeshParametricStudyTool):
    '''StraightBevelGearMeshParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1928.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1928.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6241.StraightBevelGearMeshLoadCase':
        '''StraightBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6241.StraightBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2366.StraightBevelGearMeshSystemDeflection]':
        '''List[StraightBevelGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2366.StraightBevelGearMeshSystemDeflection))
        return value
