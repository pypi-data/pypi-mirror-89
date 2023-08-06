#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from os import system, getcwd, chdir,listdir
from os.path import isfile # exists
from irff.irff_np import IRFF_NP
import argh
import argparse
import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from ase.io.trajectory import Trajectory,TrajectoryWriter
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read
import tensorflow as tf



colors = ['darkviolet','darkcyan','fuchsia','chartreuse',
          'midnightblue','red','deeppink','agua','blue',
          'cornflowerblue','orangered','lime','magenta',
          'mediumturquoise','aqua','cyan','deepskyblue',
          'firebrick','mediumslateblue','khaki','gold','k']

# p    = self.atoms.get_momenta()
# self.atoms.set_momenta(p)

def opt2md(traj='opt.traj'):
    images = Trajectory(traj)
    tframe = len(images)
    
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 rcut=None,
                 nn=True)

    cell = images[0].get_cell()
    his = TrajectoryWriter('md.traj',mode='w')
    for i,atoms in enumerate(images):
        if i >=11:
           break
        atoms.set_cell(cell)
        ir.calculate(atoms)
        calc = SinglePointCalculator(atoms,energy=ir.E)
        atoms.set_calculator(calc)
        his.write(atoms=atoms)
    his.close()


if __name__ == '__main__':
   ''' use commond like ./bp.py <t> to run it
       pb:   plot bo uncorrected 
       t:   train the whole net
   '''
   opt2md()


