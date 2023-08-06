'''_2418.py

BoltCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2270
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2424
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BoltCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundSystemDeflection',)


class BoltCompoundSystemDeflection(_2424.ComponentCompoundSystemDeflection):
    '''BoltCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2270.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2270.BoltSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2270.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2270.BoltSystemDeflection))
        return value
