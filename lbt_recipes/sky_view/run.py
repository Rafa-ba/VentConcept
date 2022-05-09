"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    chris: chris@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import sys
import luigi
import os
import time
import pathlib
from multiprocessing import freeze_support
from queenbee_local import local_scheduler, _copy_artifacts, update_params, parse_input_args, LOGS_CONFIG

import flow.main as sky_view_workerbee


_recipe_default_inputs = {   'cloudy_sky': 'uniform',
    'grid_filter': '*',
    'model': None,
    'radiance_parameters': '-aa 0.1 -ad 2048 -ar 64',
    'sensor_count': 200}


class LetSkyViewFly(luigi.WrapperTask):
    # global parameters
    _input_params = luigi.DictParameter()

    def requires(self):
        yield [sky_view_workerbee._Main_236d9e12Orchestrator(_input_params=self._input_params)]


def start(project_folder, user_values, workers):
    freeze_support()

    input_params = update_params(_recipe_default_inputs, user_values)

    if 'simulation_folder' not in input_params or not input_params['simulation_folder']:
        if 'simulation_id' not in input_params or not input_params['simulation_id']:
            simulation_id = 'sky_view_%d' % int(round(time.time(), 2) * 100)
        else:
            simulation_id = input_params['simulation_id']

        simulation_folder = pathlib.Path(project_folder, simulation_id).as_posix()
        input_params['simulation_folder'] = simulation_folder
    else:
        simulation_folder = input_params['simulation_folder']

    # copy project folder content to simulation folder
    artifacts = ['model']
    optional_artifacts = []
    for artifact in artifacts:
        value = input_params[artifact]
        if value is None:
            if artifact in optional_artifacts:
                continue
            raise ValueError('None value for required artifact input: %s' % artifact)
        from_ = pathlib.Path(project_folder, input_params[artifact]).resolve().as_posix()
        to_ = pathlib.Path(simulation_folder, input_params[artifact]).resolve().as_posix()
        _copy_artifacts(from_, to_)

    # set up logs
    log_folder = pathlib.Path(simulation_folder, '__logs__')
    log_folder.mkdir(exist_ok=True)
    cfg_file = pathlib.Path(simulation_folder, '__logs__', 'logs.cfg')
    log_file = pathlib.Path(simulation_folder, '__logs__', 'logs.log').as_posix()
    with cfg_file.open('w') as lf:
        lf.write(LOGS_CONFIG.replace('WORKFLOW.LOG', log_file))

    luigi.build(
        [LetSkyViewFly(_input_params=input_params)],
        local_scheduler=local_scheduler(),
        workers=workers,
        logging_conf_file=cfg_file.as_posix()
    )


if __name__ == '__main__':
    project_folder, user_values, workers = parse_input_args(sys.argv)
    start(project_folder, user_values, workers)
