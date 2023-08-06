'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1915 import AdvancedTimeSteppingAnalysisForModulationModeViewOptions
    from ._1916 import ModalContributionViewOptions
