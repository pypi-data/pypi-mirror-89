'''_3272.py

AssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2081, _2120
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3139
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3273, _3275, _3278, _3284,
    _3285, _3286, _3291, _3296,
    _3306, _3308, _3310, _3314,
    _3320, _3321, _3322, _3329,
    _3336, _3339, _3340, _3341,
    _3343, _3345, _3350, _3351,
    _3352, _3361, _3354, _3356,
    _3360, _3366, _3367, _3372,
    _3375, _3378, _3382, _3386,
    _3390, _3393, _3265
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponse',)


class AssemblyCompoundSteadyStateSynchronousResponse(_3265.AbstractAssemblyCompoundSteadyStateSynchronousResponse):
    '''AssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2081.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2081.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3139.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3139.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3139.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3139.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def bearings(self) -> 'List[_3273.BearingCompoundSteadyStateSynchronousResponse]':
        '''List[BearingCompoundSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3273.BearingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3275.BeltDriveCompoundSteadyStateSynchronousResponse]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3275.BeltDriveCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3278.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3278.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3284.BoltCompoundSteadyStateSynchronousResponse]':
        '''List[BoltCompoundSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3284.BoltCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3285.BoltedJointCompoundSteadyStateSynchronousResponse]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3285.BoltedJointCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3286.ClutchCompoundSteadyStateSynchronousResponse]':
        '''List[ClutchCompoundSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3286.ClutchCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3291.ConceptCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3291.ConceptCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3296.ConceptGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3296.ConceptGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3306.CVTCompoundSteadyStateSynchronousResponse]':
        '''List[CVTCompoundSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3306.CVTCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3308.CycloidalAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponse]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3308.CycloidalAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3310.CycloidalDiscCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponse]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3310.CycloidalDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3314.CylindricalGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3314.CylindricalGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3320.FaceGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3320.FaceGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def fe_parts(self) -> 'List[_3321.FEPartCompoundSteadyStateSynchronousResponse]':
        '''List[FEPartCompoundSteadyStateSynchronousResponse]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3321.FEPartCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3322.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3322.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3329.HypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3329.HypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3336.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3336.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3339.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3339.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3340.MassDiscCompoundSteadyStateSynchronousResponse]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3340.MassDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3341.MeasurementComponentCompoundSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3341.MeasurementComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3343.OilSealCompoundSteadyStateSynchronousResponse]':
        '''List[OilSealCompoundSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3343.OilSealCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3345.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3345.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3350.PlanetCarrierCompoundSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3350.PlanetCarrierCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3351.PointLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3351.PointLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3352.PowerLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3352.PowerLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3361.ShaftHubConnectionCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3361.ShaftHubConnectionCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def ring_pins(self) -> 'List[_3354.RingPinsCompoundSteadyStateSynchronousResponse]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponse]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3354.RingPinsCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3356.RollingRingAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3356.RollingRingAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3360.ShaftCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftCompoundSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3360.ShaftCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3366.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3366.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3367.SpringDamperCompoundSteadyStateSynchronousResponse]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3367.SpringDamperCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3372.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3372.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3375.StraightBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3375.StraightBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3378.SynchroniserCompoundSteadyStateSynchronousResponse]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3378.SynchroniserCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3382.TorqueConverterCompoundSteadyStateSynchronousResponse]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3382.TorqueConverterCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3386.UnbalancedMassCompoundSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3386.UnbalancedMassCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3390.WormGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3390.WormGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3393.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3393.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value
