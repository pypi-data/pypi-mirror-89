# -*- coding: utf-8 -*-
"""Generating the training data.

This script generates the training data according to the config specifications.

Example
-------
To run this script, pass in the desired config file as argument::

    $ generate baobab/configs/tdlmc_diagonal_config.py --n_data 1000

"""

import os, sys
import random
import argparse
from ast import literal_eval
from types import SimpleNamespace
from tqdm import tqdm
import numpy as np
import pandas as pd
# Lenstronomy modules
import lenstronomy
print("Lenstronomy path being used: {:s}".format(lenstronomy.__path__[0]))
from lenstronomy.LensModel.lens_model import LensModel
from lenstronomy.LightModel.light_model import LightModel
from lenstronomy.PointSource.point_source import PointSource
import lenstronomy.Util.util as util
# Baobab modules
from baobab.configs import BaobabConfig
import baobab.bnn_priors as bnn_priors
from baobab.sim_utils import get_PSF_model, Imager, metadata_utils

def parse_args():
    """Parse command-line arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('existing_config', help='path to Baobab config file used to generate the existing dataset')
    parser.add_argument('modified_config', help='path to Baobab config file path for the new dataset')
    args = parser.parse_args()
    # sys.argv rerouting for setuptools entry point
    if args is None:
        args = SimpleNamespace()
        args.config = sys.argv[0]
        args.n_data = sys.argv[1]
    return args

def main():
    args = parse_args()
    old_cfg = BaobabConfig.from_file(args.existing_config)
    cfg = BaobabConfig.from_file(args.modified_config)
    # Seed for reproducibility
    np.random.seed(cfg.seed)
    random.seed(cfg.seed)
    # Create data directory
    load_dir = old_cfg.out_dir
    save_dir = cfg.out_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print("Destination folder path: {:s}".format(save_dir))
        print("Log path: {:s}".format(cfg.log_path))
        cfg.export_log()
    else:
        raise OSError("Destination folder already exists.")
    # Instantiate PSF models
    psf_models = instantiate_PSF_models(cfg.psf, cfg.instrument.pixel_scale)
    n_psf = len(psf_models)
    # Instantiate density models
    kwargs_model = dict(
                    lens_model_list=[cfg.bnn_omega.lens_mass.profile, cfg.bnn_omega.external_shear.profile],
                    source_light_model_list=[cfg.bnn_omega.src_light.profile],
                    )       
    lens_mass_model = LensModel(lens_model_list=kwargs_model['lens_model_list'])
    src_light_model = LightModel(light_model_list=kwargs_model['source_light_model_list'])
    if 'lens_light' in cfg.components:
        kwargs_model['lens_light_model_list'] = [cfg.bnn_omega.lens_light.profile]
        lens_light_model = LightModel(light_model_list=kwargs_model['lens_light_model_list'])
    else:
        lens_light_model = None
    if 'agn_light' in cfg.components:
        kwargs_model['point_source_model_list'] = [cfg.bnn_omega.agn_light.profile]
        ps_model = PointSource(point_source_type_list=kwargs_model['point_source_model_list'], fixed_magnification_list=[False])
    else:
        ps_model = None
    # Instantiate Imager object
    if cfg.bnn_omega.kinematics.calculate_vel_disp or cfg.bnn_omega.time_delays.calculate_time_delays:
        for_cosmography = True
    else:
        for_cosmography = False
    imager = Imager(cfg.components, lens_mass_model, src_light_model, lens_light_model=lens_light_model, ps_model=ps_model, kwargs_numerics=cfg.numerics, min_magnification=0.0, for_cosmography=for_cosmography, magnification_frac_err=cfg.bnn_omega.magnification.frac_error_sigma)
    # Initialize BNN prior
    if for_cosmography:
        kwargs_lens_eq_solver = {'min_distance': 0.05, 'search_window': cfg.instrument.pixel_scale*cfg.image.num_pix, 'num_iter_max': 100}
        bnn_prior = getattr(bnn_priors, cfg.bnn_prior_class)(cfg.bnn_omega, cfg.components, kwargs_lens_eq_solver)
    else:
        kwargs_lens_eq_solver = {}
        bnn_prior = getattr(bnn_priors, cfg.bnn_prior_class)(cfg.bnn_omega, cfg.components)
    # Initialize empty metadata dataframe
    metadata_load_path = os.path.join(load_dir, 'metadata.csv')
    metadata = pd.read_csv(metadata_load_path, index_col=None)
    metadata_path = os.path.join(save_dir, 'metadata.csv')
    metadata['measured_magnification'] = [[]]*cfg.n_data
    current_idx = 0 # running idx of dataset
    pbar = tqdm(total=cfg.n_data)
    while current_idx < cfg.n_data:
        metadata_row = metadata.iloc[current_idx]
        # TODO: instead of sampling, read in the params
        kwargs_lens_mass = metadata_utils.get_kwargs_lens_mass(metadata_row)
        kwargs_lens_light = metadata_utils.get_kwargs_lens_light(metadata_row)
        kwargs_src_light = metadata_utils.get_kwargs_src_light(metadata_row)
        kwargs_ps = metadata_utils.get_kwargs_ps(metadata_row)
        sample = dict(
                      lens_mass=kwargs_lens_mass[0],
                      external_shear=kwargs_lens_mass[1],
                      lens_light=kwargs_lens_light[0],
                      src_light=kwargs_src_light[0],
                      agn_light=kwargs_ps[0],
                      misc=dict(
                                x_image=literal_eval(metadata_row['x_image']), 
                                y_image=literal_eval(metadata_row['y_image']),
                                )
                      )
        # Set detector and observation conditions 
        kwargs_detector = util.merge_dicts(cfg.instrument, cfg.bandpass, cfg.observation)
        psf_model = get_PSF_model(psf_models, n_psf, current_idx)
        kwargs_detector.update(seeing=cfg.psf.fwhm, psf_type=cfg.psf.type, kernel_point_source=psf_model, background_noise=0.0)
        # Generate the image
        img, img_features = imager.generate_image(sample, cfg.image.num_pix, kwargs_detector)
        if img is None: # select on stats computed while rendering the image
            continue
        # Save image file
        img_filename = 'X_{0:07d}.npy'.format(current_idx)
        img_path = os.path.join(save_dir, img_filename)
        np.save(img_path, img)
        # Save labels
        if 'agn_light' in cfg.components:
            metadata.at[current_idx, 'measured_magnification'] = img_features['measured_magnification'].tolist()
        metadata.loc[current_idx, 'total_magnification'] = img_features['total_magnification'].tolist()
        # Update progress
        current_idx += 1
        pbar.update(1)
    # Export to csv
    metadata.to_csv(metadata_path, index=None)
    pbar.close()
    
if __name__ == '__main__':
    main()
