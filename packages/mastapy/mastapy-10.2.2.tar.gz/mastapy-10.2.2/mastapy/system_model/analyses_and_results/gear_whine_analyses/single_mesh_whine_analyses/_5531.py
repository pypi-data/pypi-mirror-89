'''_5531.py

ModalAnalysisForWhine
'''


from mastapy.system_model.analyses_and_results.modal_analyses import _4823, _4820
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_FOR_WHINE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ModalAnalysisForWhine')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisForWhine',)


class ModalAnalysisForWhine(_4820.ModalAnalysis):
    '''ModalAnalysisForWhine

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_FOR_WHINE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisForWhine.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_settings(self) -> '_4823.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4823.ModalAnalysisOptions)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None
