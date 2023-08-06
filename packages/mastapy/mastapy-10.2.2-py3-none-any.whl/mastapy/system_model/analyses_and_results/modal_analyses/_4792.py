﻿'''_4792.py

CylindricalPlanetGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2109
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2304
from mastapy.system_model.analyses_and_results.modal_analyses import _4790
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CylindricalPlanetGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearModalAnalysis',)


class CylindricalPlanetGearModalAnalysis(_4790.CylindricalGearModalAnalysis):
    '''CylindricalPlanetGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2109.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2109.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2304.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2304.CylindricalPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
