#!/usr/bin/python3
# -*-coding: utf-8 -*

import pickle


def config_dipm1_generator():
    conf = {}
    # weights
    conf.update({'wcs1': 1.0})
    conf.update({'wcs2': 1.0})
    conf.update({'wsd2_gpe': 1.0})
    conf.update({'wgpe_stn': 1.0})
    conf.update({'wsd1_gpi': 1.0})
    conf.update({'stn_gpi': 1.0})

    # threshold
    conf.update({'theta_d1': 0.2})
    conf.update({'theta_d2': 0.2})
    conf.update({'theta_gpe': -0.2})
    conf.update({'theta_stn': -0.25})
    conf.update({'theta_gpi': -0.2})

    # slope parameter
    conf.update({'m': 1.0})
    # activation rate
    conf.update({'k': 25.0})
    # time increment
    conf.update({'dt': 1.0})

    serialize_config(conf, '../configs/dipm1.p')


def config_sim1_generator():
    config1 = {}
    name = 'sim1'
    dipms_conf = {
        0: None,
        1: None,
        2: None
    }
    nb_of_runs = 5
    time_interval = 1.0
    channels = 3
    salience = {
        0: [0.0, 0.4, 0.4, 0.6, 0.4],
        1: [0.0, 0.0, 0.6, 0.6, 0.6],
        2: [0.0 for i in range(0, 5)]
    }

    config1.update({'name': name})
    config1.update({'dipms_conf': dipms_conf})
    config1.update({'nb_of_runs': nb_of_runs})
    config1.update({'time_interval': time_interval})
    config1.update({'channels': channels})
    config1.update({'salience': salience})

    serialize_config(config1, '../configs/sim1.p')


def serialize_config(config: dict, file_name: str):
    # Using pickle's serialization to keep int keys as int
    with open(file_name, 'wb') as results_file:
        pickle.dump(config, results_file)
    results_file.close()


config_sim1_generator()
config_dipm1_generator()