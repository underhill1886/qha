#!/usr/bin/env python3

import numpy
from lazy_property import LazyProperty

import qha.multi_configurations.same_phonon_dos as same_phonon_dos
from qha.calculator.utils import is_all_same
from qha.utils.units import QHAUnits
from .diverse_phdos import DiversePhDOSHelmholtzFreeEnergyCalculator

# TODO: move to other places

units = QHAUnits()


class IdenticalPhDOSHelmholtzFreeEnergyCalculator(DiversePhDOSHelmholtzFreeEnergyCalculator):
    def validate(self):
        super().validate()
        self.validate_is_configuration_same()

    def validate_is_configuration_same(self):
        self.validate_is_q_weights_same()
        self.validate_is_volumes_same()
        self.validate_is_frequencies_same()

    def validate_is_q_weights_same(self):
        if not is_all_same(self.all_q_weights):
            raise RuntimeError('q-weights for different configurations are different!')

    def validate_is_volumes_same(self):
        if not is_all_same(self.all_volumes.magnitude):
            raise RuntimeError('Volumes for different configurations are different!')

    def validate_is_frequencies_same(self):
        print(self.all_volumes.magnitude)
        raise NotImplementedError()

    def calculate_helmholtz_free_energy(self):
        self._helmholtz_free_energies = numpy.array([
            same_phonon_dos.FreeEnergy(
                temperature,
                self.degeneracies,
                self.q_weights,
                self.static_energies,
                self.volumes,
                self.frequencies,
                self.settings['static_only'],
                self.settings['order']
            ).free_energies()
            for temperature in self.temperatures().magnitude
        ])

    @LazyProperty
    def q_weights(self):
        return self.all_q_weights[0]

    @LazyProperty
    @units.wraps(units.Hz, None)
    def frequencies(self):
        return self.all_frequencies[0]

    @LazyProperty
    @units.wraps(units.bohr ** 3, None)
    def volumes(self):
        return self.all_volumes[0]

    @LazyProperty
    @units.wraps(units.Hz, None)
    def static_energies(self):
        return self.all_static_energies[0]