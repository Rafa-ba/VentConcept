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


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask


_default_inputs = {   'bsdfs': None,
    'grid_name': None,
    'octree_file': None,
    'params_folder': '__params',
    'radiance_parameters': '-aa 0.1 -ad 2048 -ar 64',
    'sensor_count': 200,
    'sensor_grid': None,
    'simulation_folder': '.'}


class MergeResults(QueenbeeTask):
    """Merge several files with similar starting name into one."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def name(self):
        return self._input_params['grid_name']

    @property
    def extension(self):
        return '.res'

    @property
    def folder(self):
        value = pathlib.Path('results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance grid merge input_folder grid  {extension} --name {name}'.format(extension=self.extension, name=self.name)

    def requires(self):
        return {'RayTracing': RayTracing(_input_params=self._input_params)}

    def output(self):
        return {
            'result_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '../../results/{name}.res'.format(name=self.name)).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'input_folder', 'from': self.folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result-file', 'from': '{name}{extension}'.format(name=self.name, extension=self.extension),
                'to': pathlib.Path(self.execution_folder, '../../results/{name}.res'.format(name=self.name)).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class RayTracingLoop(QueenbeeTask):
    """Run ray-tracing and post-process the results for a skyview simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    fixed_radiance_parameters = luigi.Parameter(default='-I -ab 1 -h')

    @property
    def grid(self):
        value = pathlib.Path(self.input()['SplitGrid']['output_folder'].path, self.item['path'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def scene_file(self):
        value = pathlib.Path(self._input_params['octree_file'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdf_folder(self):
        try:
            pathlib.Path(self._input_params['bsdfs'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['bsdfs'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'results').resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance raytrace daylight-factor scene.oct grid.pts --rad-params "{radiance_parameters}" --rad-params-locked "{fixed_radiance_parameters}" --output grid.res'.format(radiance_parameters=self.radiance_parameters, fixed_radiance_parameters=self.fixed_radiance_parameters)

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'result': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'grid', 'to': 'grid.pts', 'from': self.grid, 'optional': False},
            {'name': 'scene_file', 'to': 'scene.oct', 'from': self.scene_file, 'optional': False},
            {'name': 'bsdf_folder', 'to': 'model/bsdf', 'from': self.bsdf_folder, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'result', 'from': 'grid.res',
                'to': pathlib.Path(self.execution_folder, '{item_name}.res'.format(item_name=self.item['name'])).resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class RayTracing(luigi.Task):
    """Run ray-tracing and post-process the results for a skyview simulation."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def grids_list(self):
        value = pathlib.Path(self.input()['SplitGrid']['grids_list'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.grids_list)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['SplitGrid']['grids_list'].path).as_posix()

    def run(self):
        yield [RayTracingLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'ray_tracing.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'SplitGrid': SplitGrid(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'ray_tracing.done').resolve().as_posix())
        }


class SplitGrid(QueenbeeTask):
    """Split a single sensor grid file into multiple smaller grids."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sensor_count(self):
        return self._input_params['sensor_count']

    @property
    def input_grid(self):
        value = pathlib.Path(self._input_params['sensor_grid'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance grid split grid.pts {sensor_count} --folder output --log-file output/grids_info.json'.format(sensor_count=self.sensor_count)

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'sub_grids').resolve().as_posix()
            ),
            'grids_list': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output/grids_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_grid', 'to': 'grid.pts', 'from': self.input_grid, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output',
                'to': pathlib.Path(self.execution_folder, 'sub_grids').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'grids-list', 'from': 'output/grids_info.json', 'to': pathlib.Path(self.params_folder, 'output/grids_info.json').resolve().as_posix()}]


class _SkyViewRayTracing_236d9e12Orchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [MergeResults(_input_params=self.input_values)]
