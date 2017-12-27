#!/usr/bin/python3
# -*-coding: utf-8 -*

import Simulator.DIPMSimulator as DipmSim
import Simulator.SCPMSimulator as ScpmSim
import tools.Archivist as Archivist
import tools.Display as Display

sim = None
# model = 'dipm'
# model = 'scpm'

models = ['dipm', 'scpm']

for model in models:
    config = 'configs/'
    results = 'results/'
    export = 'img_export/'
    if model == 'dipm':
        sim = DipmSim.DIPMSimulator()
        config += 'config_dipm_exp2.p'
        results += 'results_dipm_exp2.p'
        export += model + '_exp2'
    elif model == 'scpm':
        sim = ScpmSim.SCPMSimulator()
        config += 'config_scpm_exp2.p'
        results += 'results_scpm_exp1.p'
        export += model + '_exp2'

    sim.init_and_load_config(config)
    sim.run_sim(results)
    data = Archivist.load(results)

    Display.flexible_display_or_save(data['gpi_outputs'], model, export, [0, 1], data['salience'], 0.05)
