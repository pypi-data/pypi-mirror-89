#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from irff.plot.reax_plot import plbo
# from irff.plot import reax_pldd,reax_plbd
from irff.irff import IRFF
from irff.irff_np import IRFF_NP
from ase.io import read,write
import numpy as np
from ase.io.trajectory import Trajectory,TrajectoryWriter
import matplotlib.pyplot as plt


def e(traj='siesta.traj',batch_size=50,nn=True):
    ffield = 'ffield.json' if nn else 'ffield'
    images = Trajectory(traj)
    atoms  = images[0]
    e,e_ = [],[]
    eb,el,eo,eu = [],[],[],[]
    ea,ep,etc = [],[],[]
    et,ef    = [],[]
    ev,eh,ec = [],[],[]

    eb_,el_,eo_,eu_ = [],[],[],[]
    ea_,ep_,etc_ = [],[],[]
    et_,ef_    = [],[]
    ev_,eh_,ec_ = [],[],[]

    ir = IRFF(atoms=atoms,
              libfile='ffield.json',
              rcut=None,
              nn=True,
              autograd=False)

    for i,atoms in enumerate(images):
        ir.calculate(atoms)
        e.append(ir.E)
        eb.append(ir.Ebond.numpy())
        el.append(ir.Elone.numpy())
        eo.append(ir.Eover.numpy())
        eu.append(ir.Eunder.numpy())
        ea.append(ir.Eang.numpy())
        ep.append(ir.Epen.numpy())
        et.append(ir.Etor.numpy())
        ef.append(ir.Efcon.numpy())
        etc.append(ir.Etcon.numpy())
        ev.append(ir.Evdw.numpy())
        eh.append(ir.Ehb.numpy())
        ec.append(ir.Ecoul.numpy())

    ir_ = IRFF_NP(atoms=atoms,
                  libfile='ffield.json',
                  rcut=None,
                  nn=True)

    for i,atoms in enumerate(images):
        ir_.calculate(atoms)
        e_.append(ir_.E)
        eb_.append(ir_.Ebond)
        el_.append(ir_.Elone)
        eo_.append(ir_.Eover)
        eu_.append(ir_.Eunder)
        ea_.append(ir_.Eang)
        ep_.append(ir_.Epen)
        et_.append(ir_.Etor)
        ef_.append(ir_.Efcon)
        etc_.append(ir_.Etcon)
        ev_.append(ir_.Evdw)
        eh_.append(ir_.Ehb)
        ec_.append(ir_.Ecoul)

    e_irffnp = {'Energy':e,'Ebond':eb,'Eunger':eu,'Eover':eo,'Eang':ea,'Epen':ep,
              'Elone':el,
              'Etcon':etc,'Etor':et,'Efcon':ef,'Evdw':ev,'Ecoul':ec,'Ehbond':eh}
    e_irff = {'Energy':e_,'Ebond':eb_,'Eunger':eu_,'Eover':eo_,'Eang':ea_,'Epen':ep_,
              'Elone':el_,
              'Etcon':etc_,'Etor':et_,'Efcon':ef_,'Evdw':ev_,'Ecoul':ec_,'Ehbond':eh_}

    for key in e_irffnp:
        plt.figure()   
        plt.ylabel('%s (eV)' %key)
        plt.xlabel('Step')

        plt.plot(e_irffnp[key],alpha=0.01,
                 linestyle='-.',marker='o',markerfacecolor='none',
                 markeredgewidth=1,markeredgecolor='b',markersize=4,
                 color='blue',label='IRFF_NP')
        plt.plot(e_irff[key],alpha=0.01,
                 linestyle=':',marker='^',markerfacecolor='none',
                 markeredgewidth=1,markeredgecolor='red',markersize=4,
                 color='red',label='IRFF')
        plt.legend(loc='best',edgecolor='yellowgreen') # lower left upper right
        plt.savefig('%s.eps' %key) 
        plt.close() 

e('opt.traj')

