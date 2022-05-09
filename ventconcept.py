#kivy libraries

from kivy.config import Config
Config.set('graphics', 'width', '1600')
Config.set('graphics', 'height', '900')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'window_icon', 'ventconcept.png')




# from kivy.resources import resource_add_path, resource_find
import kivy as kv
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.graphics import Ellipse, Line
from kivy.graphics import PushMatrix, Rotate, PopMatrix
from kivy.graphics.context_instructions import Color

from kivy.metrics import dp

from kivy.core.window import Window
Window.set_icon('ventconcept.png')

from kivy.lang import Builder


import os
import math
import subprocess
import json
import sys
import re
from random import randint
from datetime import datetime, timedelta


from ladybug.stat import STAT
from ladybug.ddy import DDY
from ladybug.dt import Date, DateTime
from ladybug.futil import write_to_file_by_name, nukedir, preparedir
from ladybug.epw import EPW
from ladybug.sql import SQLiteResult
from ladybug.datacollection import MonthlyCollection
from ladybug.header import Header
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.datatype.energyintensity import EnergyIntensity
from ladybug.datatype.temperature import Temperature
from ladybug.datacollection import BaseCollection
from ladybug_comfort.collection.adaptive import Adaptive
from ladybug_comfort.parameter.adaptive import AdaptiveParameter
from ladybug_comfort.adaptive import t_operative, \
    adaptive_comfort_ashrae55, adaptive_comfort_en15251, \
    cooling_effect_ashrae55, cooling_effect_en15251, \
    adaptive_comfort_conditioned
from ladybug_comfort.collection.base import ComfortCollection
from ladybug_geometry.geometry2d.pointvector import Point2D as Point2D_0
from ladybug_geometry.geometry2d.pointvector import Vector2D as Vector2D_0
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.polyface import Polyface3D
from ladybug_geometry.bounding import bounding_domain_x, bounding_domain_y, bounding_domain_z

from honeybee.config import folders
from honeybee.model import Model
from honeybee.typing import clean_and_id_ep_string
from honeybee.facetype import get_type_from_normal, Floor, Wall, RoofCeiling
from honeybee.face import Face
from honeybee.room import Room
from honeybee.aperture import Aperture
from honeybee.properties import FaceProperties
from honeybee.boundarycondition import boundary_conditions, Outdoors, Surface, Ground

from honeybee_energy.ventcool.opening import VentilationOpening
from honeybee_energy.material.opaque import EnergyMaterial
from honeybee_energy.material.glazing import EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.result.loadbalance import LoadBalance
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.run import run_idf, to_openstudio_osw, run_osw
from honeybee_energy.result.err import Err
from honeybee_energy.result.osw import OSW

from honeybee_energy.ventcool.afn import generate
from honeybee_energy.ventcool.opening import VentilationOpening
from honeybee_energy.ventcool.control import VentilationControl
from honeybee_energy.lib.schedules import schedule_by_identifier

from honeybee_energy.config import folders as energy_folders
from honeybee_energy.writer import energyplus_idf_version


from lbt_recipes.version import check_energyplus_version, check_openstudio_version, check_openstudio_return, check_energyplus_return



"""
try:
    from ladybug_rhino.config import conversion_to_meters, tolerance, angle_tolerance
    from ladybug_rhino.grasshopper import all_required_inputs, give_warning
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))
"""


# from garden.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# import matplotlib
# matplotlib.use('Kivy')
from vent_bounding import bounding_domain_x_y_length, bounding_domain_z_length, bounding_domain_x_length, bounding_domain_y_length
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.dates as dates

# os.chdir(sys._MEIPASS)

# List of all the output strings that will be requested
cool_out = 'Zone Ideal Loads Supply Air Total Cooling Energy'
heat_out = 'Zone Ideal Loads Supply Air Total Heating Energy'
light_out = 'Zone Lights Electricity Energy'
el_equip_out = 'Zone Electric Equipment Electricity Energy'
gas_equip_out = 'Zone Gas Equipment NaturalGas Energy'
shw_out = 'Water Use Equipment Heating Energy'
gl_el_equip_out = 'Zone Electric Equipment Total Heating Energy'
gl_gas_equip_out = 'Zone Gas Equipment Total Heating Energy'
gl1_shw_out = 'Water Use Equipment Zone Sensible Heat Gain Energy'
gl2_shw_out = 'Water Use Equipment Zone Latent Gain Energy'
oper_temp_output = 'Zone Operative Temperature'
air_temp_output = 'Zone Mean Air Temperature'
rad_temp_output = 'Zone Mean Radiant Temperature'
rel_humidity_output = 'Zone Air Relative Humidity'
energy_output = (cool_out, heat_out, light_out, el_equip_out, gas_equip_out, shw_out)


frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))


# def get_path():
#     if getattr(sys, 'frozen', False):
#             # we are running in a bundle
#             frozen = 'ever so'
#             bundle_dir = sys._MEIPASS
#     else:
#             # we are running in a normal Python environment
#             bundle_dir = os.path.dirname(os.path.abspath(__file__))
#             print(bundle_dir, "bundledir")
#     return bundle_dir



def window_north_south(box_0, north_south, percent):
    for i, face in enumerate(box_0.faces):
        try:
            if face.cardinal_direction() == north_south:
                if not face.geometry.has_holes:
                    sel_face = face

        except: # horizontal face, can be ignored
            pass

    sel_face.apertures_by_ratio(percent/100)
    return box_0

def window_north_south_spec(box_0, north_south, per_wid, per_hei, per_offset):
    for i, face in enumerate(box_0.faces):
        try:
            if face.cardinal_direction() == north_south:
                if not face.geometry.has_holes:
                    sel_face = face

        except: # horizontal face, can be ignored
            pass

    face_wid = bounding_domain_x_length([sel_face.geometry])
    win_wid = face_wid  * per_wid/100
    face_hei = bounding_domain_z_length([sel_face.geometry])
    win_hei = face_hei * per_hei/100
    total_dif = face_hei - win_hei
    off = total_dif * per_offset/100

    sel_face.apertures_by_width_height_rectangle(win_hei, win_wid, off, (win_wid +1), tolerance=0.01)

    return box_0


def remove_window(box_0, north_south):
    for i, face in enumerate(box_0.faces):
        print(face.apertures, "luxx", face.geometry.has_holes)
        try:
            print(face.cardinal_direction(), "cardinal_direction")
            if face.cardinal_direction() == north_south:
                # if not face.geometry.has_holes:
                sel_face = face
                sel_face.remove_apertures()

        except: # horizontal face, can be ignored
            pass

        


    return box_0


def interior_window_spec(box_0, box_1, per_wid, per_hei, per_offset): # remove exisitng interior windows and attribute new ones

    adj_faces = box_0.find_adjacency([box_0, box_1])
    ad_0 = adj_faces[0][0]
    ad_1 = adj_faces[0][1]
    ad_0.remove_apertures()
    ad_1.remove_apertures()

    ad_0._boundary_condition = boundary_conditions.by_name("Outdoors")
    ad_1._boundary_condition = boundary_conditions.by_name("Outdoors")

    face_wid = bounding_domain_x_length([ad_0.geometry])
    win_wid = face_wid * per_wid/100
    face_hei = bounding_domain_z_length([ad_0.geometry])
    win_hei = face_hei * per_hei/100
    total_dif = face_hei - win_hei
    off = total_dif * per_offset/100

    ad_0.apertures_by_width_height_rectangle(win_hei, win_wid, off, (win_wid +1), tolerance=0.01)



    face_1_aps = []
    cop_face_1_aps = []
    for ap in ad_0.apertures:
        face_1_aps.append(ap)

    for ap in face_1_aps:
        iden = ap.identifier+"_"+str(randint(0,150))
        geo = ap.geometry
        bound = ap.boundary_condition
        is_op = ap.is_operable
        new_ap = Aperture(iden, geo, bound, is_op)
        new_ap._display_name = ap.display_name
        new_ap._user_data = None if ap.user_data is None else ap.user_data.copy()
        ap._duplicate_child_shades(new_ap)
        new_ap._properties._duplicate_extension_attr(ap._properties)
        cop_face_1_aps.append(new_ap)


    ad_1.add_apertures(cop_face_1_aps)

    ad_0._boundary_condition = boundary_conditions.surface(ad_1)
    ad_1._boundary_condition = boundary_conditions.surface(ad_0)

    for i, ap in enumerate(ad_0.apertures):
        ap._boundary_condition = boundary_conditions.surface(ad_1.apertures[i], ad_0)
    for i, ap in enumerate(ad_1.apertures):
        ap._boundary_condition = boundary_conditions.surface(ad_0.apertures[i], ad_1)






def interior_window(box_0, box_1, percent, height): # remove exisitng interior windows and attribute new ones
    sill_height = 0.5 * ((height * 1.052) - height)
    adj_faces = box_0.find_adjacency([box_0, box_1])

    ad_0 = adj_faces[0][0]
    ad_1 = adj_faces[0][1]
    ad_0.remove_apertures()
    ad_1.remove_apertures()

    ad_0._boundary_condition = boundary_conditions.by_name("Outdoors")
    ad_1._boundary_condition = boundary_conditions.by_name("Outdoors")


    ad_0.apertures_by_ratio_rectangle(percent/100, height, sill_height, 1000)



    face_1_aps = []
    cop_face_1_aps = []
    for ap in ad_0.apertures:
        face_1_aps.append(ap)

    for ap in face_1_aps:
        iden = ap.identifier+"_"+str(randint(0,150))
        geo = ap.geometry
        bound = ap.boundary_condition
        is_op = ap.is_operable
        new_ap = Aperture(iden, geo, bound, is_op)
        new_ap._display_name = ap.display_name
        new_ap._user_data = None if ap.user_data is None else ap.user_data.copy()
        ap._duplicate_child_shades(new_ap)
        new_ap._properties._duplicate_extension_attr(ap._properties)
        cop_face_1_aps.append(new_ap)


    ad_1.add_apertures(cop_face_1_aps)


    ad_0._boundary_condition = boundary_conditions.surface(ad_1)
    ad_1._boundary_condition = boundary_conditions.surface(ad_0)

    for i, ap in enumerate(ad_0.apertures):
        ap._boundary_condition = boundary_conditions.surface(ad_1.apertures[i], ad_0)
    for i, ap in enumerate(ad_1.apertures):
        ap._boundary_condition = boundary_conditions.surface(ad_0.apertures[i], ad_1)





_heat_cop_ = None
_cool_cop_ = None
shades_ = None
_run = 2

gl_epw_file = None

tolerance = 0.005
angle_tolerance = 1

initial_room = None


# constructions
# construction type -> light or heavy



# light weight construction  materials

# insulation
ins_mat_name = clean_and_id_ep_string('OpaqueMaterial')
ins_mat_thickness = 0.36
ins_mat_conductivity = 0.049
ins_mat_density = 265
ins_mat_specific_heat = 836.3

ep_mat_insulation = EnergyMaterial(ins_mat_name, ins_mat_thickness, ins_mat_conductivity, ins_mat_density, ins_mat_specific_heat)


# gypsum board
gy_mat_name = clean_and_id_ep_string('OpaqueMaterial')
gy_mat_thickness = 0.016
gy_mat_conductivity = 0.16
gy_mat_density = 800
gy_mat_specific_heat = 1089

ep_mat_gypsum = EnergyMaterial(gy_mat_name, gy_mat_thickness, gy_mat_conductivity, gy_mat_density, gy_mat_specific_heat)


# heavy weight construction materials

# concrete
ins_mat_name = clean_and_id_ep_string('OpaqueMaterial')
ins_mat_thickness = 0.18
ins_mat_conductivity = 2.3
ins_mat_density = 2300
ins_mat_specific_heat = 1089

ep_mat_concrete = EnergyMaterial(ins_mat_name, ins_mat_thickness, ins_mat_conductivity, ins_mat_density, ins_mat_specific_heat)


# insulation
ins2_mat_name = clean_and_id_ep_string('OpaqueMaterial')
ins2_mat_thickness = 0.15
ins2_mat_conductivity = 0.049
ins2_mat_density = 265
ins2_mat_specific_heat = 836.3


ep_mat_insulation2 = EnergyMaterial(gy_mat_name, gy_mat_thickness, gy_mat_conductivity, gy_mat_density, gy_mat_specific_heat)

name_constr_light = clean_and_id_ep_string('OpaqueConstruction')
ep_constr_light = OpaqueConstruction(name_constr_light, [ep_mat_gypsum, ep_mat_insulation, ep_mat_gypsum])

name_constr_concr_ins = clean_and_id_ep_string('OpaqueConstruction')
ep_constr_concr_ins = OpaqueConstruction(name_constr_concr_ins, [ep_mat_insulation, ep_mat_concrete])

name_constr_concr = clean_and_id_ep_string('OpaqueConstruction')
ep_constr_concr = OpaqueConstruction(name_constr_concr, [ep_mat_concrete])

name_constr_light_ins = clean_and_id_ep_string('OpaqueConstruction')
ep_constr_light_ins = OpaqueConstruction(name_constr_concr, [ep_mat_gypsum, ep_mat_insulation2, ep_mat_gypsum])

gl_wall_constr = ep_constr_light
gl_roof_constr = ep_constr_light
gl_floor_constr = ep_constr_light
gl_int_wall_constr = ep_constr_light



# window 1 glazing material
window_mat1_name = clean_and_id_ep_string('WindowMaterial1')
window_u1_factor = 5.5
window_g1_factor = 0.8
gl_window1_mat = EnergyWindowMaterialSimpleGlazSys(window_mat1_name, window_u1_factor, window_g1_factor)

# window 1 glazing construction
window_constr1_name = clean_and_id_ep_string('WindowConstruction1')
gl_window_constr_1 = WindowConstruction(window_constr1_name, [gl_window1_mat])

# window 3 glazing material + thermal coating
window_mat3_name = clean_and_id_ep_string('WindowMaterial3e')
window_u3_factor = 0.8
window_g3_factor = 0.45
gl_window3_mat = EnergyWindowMaterialSimpleGlazSys(window_mat3_name, window_u3_factor, window_g3_factor)

# window 3 glazing construction + thermal coating
window_constr3_name = clean_and_id_ep_string('WindowConstruction3e')
gl_window_constr_3 = WindowConstruction(window_constr3_name, [gl_window3_mat])

# window 2 glazing material
window_mat2_name = clean_and_id_ep_string('WindowMaterial2')
window_u2_factor = 1.3
window_g2_factor = 0.7
gl_window2_mat = EnergyWindowMaterialSimpleGlazSys(window_mat2_name, window_u2_factor, window_g2_factor)

# window 2 glazing construction
window_constr2_name = clean_and_id_ep_string('WindowConstruction2')
gl_window_constr_2 = WindowConstruction(window_constr2_name, [gl_window2_mat])

# window 2 glazing material + thermal coating
window_mat2e_name = clean_and_id_ep_string('WindowMaterial')
window_u2e_factor = 1.3
window_g2e_factor = 0.6
gl_window2e_mat = EnergyWindowMaterialSimpleGlazSys(window_mat2e_name, window_u2e_factor, window_g2e_factor)

# window 3 glazing construction + thermal coating
window_constr2e_name = clean_and_id_ep_string('WindowConstruction')
gl_window_constr_2e = WindowConstruction(window_constr2e_name, [gl_window2e_mat])




gl_window_constr = gl_window_constr_3
############################################
# Global variables
# Geometry


# dim_list = []


gl_mode = "one_sided"

result_directory = os.path.join(os.getcwd(), "results")


# control and schedule parameters:
gl_max_out_temp = 25
gl_min_ind_temp = 18

# window opening parameters
gl_frac_area = 1.0 # for example hinged window
gl_frac_height = 1.0 # for example slided or hinged window
gl_discharge = 0.65 # completely unubstructed window without insect screen, not changeable, set for all cases
gl_is_operable = True

# simulation paramters
gl_period_type = "Hot Summer Day"
gl_an_period = AnalysisPeriod(8, 1, 0, 8, 31, 23)
# gl_runperiod = RunPeriod(Date(8, 1), Date(8, 31))
gl_startmonth = 8 
gl_startday = 1 
gl_endmonth = 8
gl_endday = 31

startdate = None # done
enddate = None # done

start_weekday = "Sunday" # write a function to get it automatically? # done
#gl_timestep = 4 # per hour # done, but change to 4 at minimum state (function)
gl_detailed = "low"


gl_terrain = "Urban"




fig = plt.figure("the_fig")
subplot_temp_0 = fig.add_subplot(1, 1, 1)

fig_1 = plt.figure("the_fig_1")
subplot_vent_0 = fig_1.add_subplot(1, 1, 1)

fig_2 = plt.figure()
subplot_temp_1 = fig_2.add_subplot(1, 1, 1)

fig_3 = plt.figure()
subplot_vent_1 = fig_3.add_subplot(1, 1, 1)

fig_4 = plt.figure()
subplot_temp_2 = fig_4.add_subplot(1, 1, 1)

fig_5 = plt.figure()
subplot_vent_2 = fig_5.add_subplot(1, 1, 1)







sql_ot = None
sql_at = None
sql_dc = None

sql_ot_1 = None
sql_at_1 = None
sql_dc_1 = None

sql_ot_2 = None
sql_at_2 = None
sql_dc_2 = None

sql_ou = None
sql_vt = None

gl_results = None


gl_pct_hot = None
gl_pct_cold = None
gl_total_h_hot = None
gl_total_h_cold = None
gl_pct_hot_1 = None
gl_pct_cold_1 = None
gl_total_h_hot_1 = None
gl_total_h_cold_1 = None
gl_pct_hot_2 = None
gl_pct_cold_2 = None
gl_total_h_hot_2 = None
gl_total_h_cold_2 = None









base_gl_room_0 = Room.from_box("room_0", 10, 10, 3, 0, Point3D(0, 0, 0))
base_gl_room_0 = window_north_south(base_gl_room_0, "North", 30)
base_gl_room_0 = window_north_south(base_gl_room_0, "South", 30)
gl_room_0 = base_gl_room_0
gl_room_1 = None
gl_room_2 = None

base_gl_room_0_at = Room.from_box("room_0_at", 10, 10, 3, 0, Point3D(0, 0, 0))
base_gl_room_0_at = window_north_south_spec(base_gl_room_0_at, "North", 30, 30, 10)
base_gl_room_0_at = window_north_south_spec(base_gl_room_0_at, "South", 30, 30, 90)
gl_room_0_at = base_gl_room_0_at
gl_room_1_at = None

base_gl_room_0_on = Room.from_box("room_0_on", 10, 10, 3, 0, Point3D(0, 0, 0))
base_gl_room_0_on = window_north_south(base_gl_room_0_on, "North", 30)
gl_room_0_on = base_gl_room_0_on
gl_room_1_at = None


########################################################################################
# specific globals (depending on single sided or cross ventilation template)

gl_template = "one_sided"

gl_north_0 = 0 
gl_north_1 = 0 # for cross ventilation template
gl_north_2 = 0 # for atrium template



def gl_room_construction_attributor(room_list):
    # room_list = [gl_room_0, gl_room_1, gl_room_2] if gl_room_2 is not None and gl_room_1 is not None else [gl_room_0, gl_room_1] if gl_room_1 is not None and gl_room_2 is None else [gl_room_0]
    for room in room_list:
        for face in room.faces:
            if isinstance(face.type, Floor):
                face.properties.energy.construction = gl_floor_constr
            elif isinstance(face.type, RoofCeiling):
                face.properties.energy.construction = gl_roof_constr
            else: # Wall:
                if isinstance(face.boundary_condition, Surface): # interior wall
                    face.properties.energy.construction = gl_int_wall_constr
                else: # isinstance(face.boundary_condition, Outdoor): # exterior wall
                    face.properties.energy.construction = gl_wall_constr
            for ap in face.apertures:
                ap.properties.energy.construction = gl_window_constr

def set_apertures_operable(room_list):
    for room in room_list:
        for face in room.faces:
            for ap in face.apertures:
                ap.is_operable = gl_is_operable

def set_afn_params(_model):
    leakage_tempaltes = {
        'excellent': 'Excellent',
        'medium': 'Medium',
        'verypoor': 'VeryPoor'
    }
    model = _model.duplicate()

    # set default properties for the leakage if they are not input
    leakage_template_ = None
    try:
        leakage = leakage_tempaltes[leakage_template_.lower()] \
            if leakage_template_ is not None else 'Medium'
    except KeyError:
        raise TypeError('leakage_template_ "{}" is not recognized. Choose from: '
                        'Excellent, Medium VeryPoor'.format(leakage_template_))
    use_room_infiltration = True # if leakage_template_ is None else False
    # pressure = _ref_pressure_ if _ref_pressure_ is not None else 101325
    pressure = 101325 # if _ref_pressure_ is None else _ref_pressure_
    # delta_pressure = _delta_pressure_ if _delta_pressure_ is not None else 4
    delta_pressure = 4 # if _delta_pressure_ is None else _delta_pressure_


    # generate the AFN leakage for all of the surfaces of the Model
    generate(model.rooms, leakage, use_room_infiltration, pressure, delta_pressure)

    # set up the Model-wide VentilationSimulationParameters for the AFN
    vent_sim_par = model.properties.energy.ventilation_simulation_control
    vent_sim_par.vent_control_type = 'MultiZoneWithoutDistribution'
    # if _long_axis_ is not None:  # assing this first so it's in the autocalculation
    #     vent_sim_par.long_axis_angle = _long_axis_
    model.properties.energy.autocalculate_ventilation_simulation_control()

    # set the properties used to approximate wind pressure coefficients

    
    vent_sim_par.building_type = 'LowRise' # if not _high_rise_ else 'HighRise'

    # if _aspect_ratio_ is not None:
    #     vent_sim_par.aspect_ratio = _aspect_ratio_
    #     vent_sim_par.long_axis_angle = _long_axis_
    report = model.properties.energy.ventilation_simulation_control

    return model


def ventilation_control(room_list):
    
    # set default values
    min_in_temp_ = gl_min_ind_temp
    max_in_temp_ = 100 
    min_out_temp_ = -100
    max_out_temp_ = gl_max_out_temp
    delta_temp_ = -100

    # get the schedule if it's just an identifier
    # if isinstance(_schedule_, str):

    _schedule_ = schedule_by_identifier("Always On")

    # create the VentilationControl object
    vent_cntrl = VentilationControl(
        min_in_temp_, max_in_temp_, min_out_temp_, max_out_temp_, delta_temp_, _schedule_)
    vent_cntrl_0 = vent_cntrl

    # loop through the rooms and assign the objects
    op_count = 0
    rooms = []
    for i, room_init in enumerate(room_list):
        room = room_init.duplicate()  # duplicate to avoid editing the input

        # assign the ventilation control for the windows
        room.properties.energy.window_vent_control = vent_cntrl_0

        vent_open = VentilationOpening(gl_frac_area, gl_frac_height, gl_discharge)

        # assign the cross ventilation
        cross_vent = None

        if cross_vent is None:
            # analyze  normals of room's apertures to test if cross vent is possible
            orient_angles = []
            for face in room.faces:
                for ap in face.apertures:
                    if ap.is_operable:
                        try:
                            orient_angles.append(ap.horizontal_orientation())
                        except ZeroDivisionError:
                            orient_angles.append(0)
            if len(orient_angles) != 0:
                orient_angles.sort()
                vent_open.wind_cross_vent = \
                    True if orient_angles[-1] - orient_angles[0] >= 90 else False
            else:
                vent_open.wind_cross_vent = False
        else:
            vent_open.wind_cross_vent = cross_vent
        vent_aps = room.properties.energy.assign_ventilation_opening(vent_open)
        rooms.append(room)
        op_count += len(vent_aps)

    # give a warning if no operable windows were found among the connected rooms
    if op_count == 0:
        print(
            'No operable Apertures were found among the connected _rooms.\n'
            'Make sure that you have set the is_operable property of Apertures to True.')

    return rooms






def solve_adjacency_at(overwrite=True):
    global gl_room_0_at
    global gl_room_1_at

    # print("here we are at adjacency method", bounding_domain_x_length([gl_room_0.geometry]), bounding_domain_x_length([gl_room_1.geometry]), bounding_domain_z_length([gl_room_0.geometry]), bounding_domain_z_length([gl_room_1.geometry]))
    if gl_room_1_at is not None:
        adj_rooms = [gl_room_0_at.duplicate(), gl_room_1_at.duplicate()] # duplicate the initial objects
    else:
        adj_rooms = [gl_room_0_at.duplicate()]


    # solve adjacnecy
    if overwrite:  # find adjscencies and re-assign them
        adj_aps = []
        adj_doors = []
        adj_faces = Room.find_adjacency(adj_rooms, tolerance)
        for face_pair in adj_faces:
            face_info = face_pair[0].set_adjacency(face_pair[1])
            adj_aps.extend(face_info['adjacent_apertures'])
            adj_doors.extend(face_info['adjacent_doors'])
        adj_info = {
            'adjacent_faces': adj_faces,
            'adjacent_apertures': adj_aps,
            'adjacent_doors': adj_doors
        }
    else:  # just solve for new adjacencies
        adj_info = Room.solve_adjacency(adj_rooms, tolerance)


    for adj_face in adj_info['adjacent_faces']:
        print('"{}" is adjacent to "{}"'.format(adj_face[0], adj_face[1]))





def solve_adjacency(overwrite=True):
    global gl_room_0
    global gl_room_1
    global gl_room_2
    
    if gl_room_2 is not None:
        adj_rooms = [gl_room_0.duplicate(), gl_room_1.duplicate(), gl_room_2.duplicate()] # duplicate the initial objects
    elif gl_room_2 is None and gl_room_1 is not None:
        adj_rooms = [gl_room_0.duplicate(), gl_room_1.duplicate()] # duplicate the initial objects
    else:
        adj_rooms = [gl_room_0.duplicate()]



    # solve adjacnecy
    if overwrite:  # find adjscencies and re-assign them
        adj_aps = []
        adj_doors = []
        adj_faces = Room.find_adjacency(adj_rooms, tolerance)
        for face_pair in adj_faces:
            face_info = face_pair[0].set_adjacency(face_pair[1])
            adj_aps.extend(face_info['adjacent_apertures'])
            adj_doors.extend(face_info['adjacent_doors'])
        adj_info = {
            'adjacent_faces': adj_faces,
            'adjacent_apertures': adj_aps,
            'adjacent_doors': adj_doors
        }
    else:  # just solve for new adjacencies
        adj_info = Room.solve_adjacency(adj_rooms, tolerance)


    for adj_face in adj_info['adjacent_apertures']:
        print('"{}" is adjacent to "{}"'.format(adj_face[0], adj_face[1]))




def cross_room_generator(identifier, length, width, height, z_add=None):

    if identifier == "room_0":
        origin_pt = Point3D(0, 0, 0)
        global gl_room_0
        gl_room_0 = Room.from_box(identifier, length, width, height, 0, origin_pt) # upper room
    elif identifier == "room_1":
        origin_pt = Point3D(0, 0-width, z_add) 
        global gl_room_1
        gl_room_1 = Room.from_box(identifier, length, width, height, 0, origin_pt) # middle room

    else: # == room_2
        origin_pt = Point3D(gl_room_1.geometry.min.x, 0-bounding_domain_y_length([gl_room_1.geometry])-width, gl_room_1.geometry.min.z + z_add)
        global gl_room_2
        gl_room_2 = Room.from_box(identifier, length, width, height, 0, origin_pt) # lower room

def cross_room_generator_at(identifier, length, width, height, z_add=None):
    if identifier == "room_0_at":
        origin_pt = Point3D(0, 0, 0)
        global gl_room_0_at
        gl_room_0_at = Room.from_box(identifier, length, width, height, 0, origin_pt) 
    elif identifier == "room_1_at":
        origin_pt = Point3D(0, 0-width, 0) 
        global gl_room_1_at
        gl_room_1_at = Room.from_box(identifier, length, width, height, 0, origin_pt) 
    else: # identifier == "room_0_on"
        origin_pt = Point3D(0, 0, 0) 
        global gl_room_0_on
        gl_room_0_on = Room.from_box(identifier, length, width, height, 0, origin_pt) 



def box_intersection(box_0, box_1):
    smaller = get_smaller_x_box(box_0, box_1)
    if smaller == "equal":
        return box_0, box_1

    for i, face in enumerate(box_0.faces):

        try:
            if face.cardinal_direction() == "South":
                if isinstance(face.boundary_condition, Surface):
                    pass
                else:
                    if smaller == "box_0":
                        small_face = face
                    else: # smaller == "box_1"
                        big_face = face
                    the_0_index = i

        except: # horizontal face, can be ignored
            pass

    for i, face in enumerate(box_1.faces):
        try:
            if face.cardinal_direction() == "North":

                if smaller == "box_0":
                    big_face = face
                else: # smaller == "box_1"
                    small_face = face
                the_1_index = i


        except: # horizontal faces
            pass

    vertice_list = []
    for v in small_face.vertices:

        if big_face.geometry._plane.distance_to_point(v) <= tolerance:
            vertice_list.append(v)


    small_face_3d = Face3D(vertice_list)


    big_face_clockwise = big_face.geometry.is_clockwise
    original_vertices = big_face.geometry.vertices
    original_plane = big_face.geometry.plane

    face_type = big_face.type
    face_bc = big_face.boundary_condition 
    face_identifier = big_face.identifier


    lb_face = Face3D.from_punched_geometry(big_face.geometry, [small_face_3d])
    lb_face = lb_face.remove_colinear_vertices(tolerance)

    hb_face = Face(face_identifier, lb_face, face_type, face_bc)

    small_face_flipped = Face(small_face.identifier, small_face_3d, small_face.type, small_face.boundary_condition)

    if smaller == "box_0":
        faces_1 = box_1.faces
        faces_1 = [hb_face if i == the_1_index else face for i, face in enumerate(faces_1)]
        faces_1.append(small_face_flipped)
        lb_faces_1 = [f.geometry for f in faces_1]
        
        try_solid = Polyface3D.from_faces(lb_faces_1, 0.01)
        print(try_solid.is_solid, "is solid or not")

        bx_ident = box_1.identifier
        box_1 = Room.from_polyface3d(bx_ident, try_solid)

    elif smaller == "box_1":
        faces_0 = box_0.faces
        faces_0 = [hb_face if i == the_0_index else face for i, face in enumerate(faces_0)]
        faces_0.append(small_face_flipped)
        lb_faces_0 = [f.geometry for f in faces_0]

        try_solid = Polyface3D.from_faces(lb_faces_0, 0.01)
        print(try_solid.is_solid, "is solid or not")
        box_ident = box_0.identifier
        box_0 = Room.from_polyface3d(box_ident, try_solid)

    return box_0, box_1



def remove_intersections(box_0, north_south):
    nor_sou_list = []
    for i, face in enumerate(box_0.faces):
        try:
            if face.cardinal_direction() == north_south:
                face._boundary_condition = boundary_conditions.by_name("Outdoors")
                nor_sou_list.append(face.geometry)
                

        except: # horizontal face, can be ignored
            pass


    lb_f = [face.geometry for face in box_0.faces]

    new_f = []
    new_i = []

    sel_f = None
    for i, f in enumerate(lb_f):
        if len(f.vertices) > 4:
            sel_f = i

    if sel_f is not None:
        if lb_f[sel_f] in nor_sou_list:
            pass
        else:
            return box_0
    else:
        return box_0

    for i, f in enumerate(lb_f):
        if i != sel_f:
            if f.plane.is_coplanar_tolerance(lb_f[sel_f].plane, 0.005, 0.005):
                pass
            else:
                new_f.append(box_0.faces[i])
            
        else:
            face = Face3D(lb_f[sel_f].boundary, lb_f[sel_f].plane)
            hb_f = Face(box_0.faces[i].identifier, face, box_0.faces[i].type, box_0.faces[i].boundary_condition)
            new_f.append(hb_f)

    # room_prop = box_0.properties

    box_0 = Room(box_0.identifier, new_f, tolerance)

    return box_0





def get_smaller_x_box (box_0, box_1):
    if bounding_domain_x_length([box_0.geometry]) < bounding_domain_x_length([box_1.geometry]):
        return "box_0"
    elif bounding_domain_x_length([box_0.geometry]) == bounding_domain_x_length([box_1.geometry]):
        return "equal"
    else:
        return "box_1"




def serialize_data(data_dicts):
    """Reserialize a list of MonthlyCollection dictionaries."""
    return [MonthlyCollection.from_dict(data) for data in data_dicts]


def stat_file_solver(period_type):

    localepw = gl_epw_file
    localpath = localepw.rsplit("\\", 1)[0]
    directory = os.listdir(localpath) #'[0:-4] +"\\")
    found_stat = False
    for file in directory:
        if file.endswith(".stat"):
            found_stat = True
            stat_obj = STAT(os.path.join(localpath, file))
            nonetype = type(None)
            print(period_type)
            if period_type == "Hot Summer Week":
                try:
                    RunPeriod.from_analysis_period(stat_obj.extreme_hot_week)
                    return stat_obj.extreme_hot_week
                except:
                    PeriodErrorPopup.title = "Warning"
                    PeriodErrorPopup.error_warning = "The chosen simulation period is not available for the loaded weather data."
                    PeriodErrorPopup().open()
                    return
            elif period_type == "Typical Summer Week":
                try:
                    runper = RunPeriod.from_analysis_period(stat_obj.typical_summer_week)
                    return stat_obj.typical_summer_week
                
                except:
                    PeriodErrorPopup.title = "Warning"
                    PeriodErrorPopup.error_warning = "The chosen simulation period is not available for the loaded weather data."
                    PeriodErrorPopup().open()
                    return
            else:
                pass
    if found_stat is False:
        PeriodErrorPopup.title = "Warning"
        PeriodErrorPopup.error_warning = "No .stat file was found in the folder of the .epw. \n \
            The .stat file is necessary for if you select the simulation period: \n \
            hot summer week or typical summer week. If you don't have a .stat file, \n \
            choose a costum simulation period or the hot summer day."
        PeriodErrorPopup().open()
        return
            


def ep_glazing_maker(window_type):
    if window_type == "Triple + thermal coating":
        return gl_window_constr_3
    elif window_type == "Double Glazing":
        return gl_window_constr_2
    elif window_type == "Single Glazing":
        return gl_window_constr_1
    else: 
        return gl_window_constr_2e



def ep_constr_maker(srf_type, heavy_light, val):
    srf_list = ["int_floorconstr", "int_wallconstr"]
    if srf_type in srf_list:
        if heavy_light == "light":
            return ep_constr_light_ins
        else:
            return ep_constr_concr
    else:
        if heavy_light == "light":
            change_mat = ep_constr_light.materials[1]
            new_r = 1 / val
            differ_r = new_r - ep_constr_light.r_value # check this
            old_mat_r = change_mat.r_value
            new_mat_r = old_mat_r + differ_r
            new_thick = change_mat.conductivity * new_mat_r
            change_mat_dup = change_mat.duplicate()
            change_mat_dup.thickness = new_thick
            return OpaqueConstruction(name_constr_light, [ep_mat_gypsum, change_mat_dup, ep_mat_gypsum])
        else:
            change_mat = ep_constr_concr_ins.materials[0]
            new_r = 1 / val
            differ_r = new_r - ep_constr_concr_ins.r_value # check this
            old_mat_r = change_mat.r_value
            new_mat_r = old_mat_r + differ_r
            new_thick = change_mat.conductivity * new_mat_r
            change_mat_dup = change_mat.duplicate()
            change_mat_dup.thickness = new_thick
            return OpaqueConstruction(name_constr_light, [change_mat_dup, ep_mat_concrete])
    
def adaptive_comfort(_out_temp, _air_temp, _mrt_, _air_speed_ = None):
    adapt_par_ = AdaptiveParameter(False) # set to en15251 (European standard) by default # should add an option to toggle between Ashrae and en15251, still not implemented in this version


    def extract_collections(input_list):
        """Process inputs into collections and floats."""
        defaults = [None, None, _air_temp, 0.1]
        data_colls = []
        for i, input in enumerate(input_list):
            if input is None:
                input_list[i] = defaults[i]
            elif isinstance(input, BaseCollection):
                data_colls.append(input)
            else:
                try:
                    input_list[i] = float(input)
                except ValueError as e:
                    raise TypeError('input {} is not valid. Expected float or '
                                    'DataCollection. Got {}'.format(input, type(input)))
        return input_list, data_colls


    # Process inputs and assign defaults.
    input_list = [_out_temp, _air_temp, _mrt_, _air_speed_]
    input, data_colls = extract_collections(input_list)
    adapt_par = adapt_par_ or AdaptiveParameter()
    adapt_par.set_neutral_offset_from_comfort_class(2) # set to building class 2 according to DIN EN 15251
    if data_colls == []:
        # The inputs are all individual values.
        prevail_temp = input[0]
        to = t_operative(input[1], float(input[2]))
        
        # Determine the ralationship to the neutral temperature
        if adapt_par.conditioning != 0:
            comf_result = adaptive_comfort_conditioned(prevail_temp, to,
                adapt_par.conditioning, adapt_par.standard)
        elif adapt_par.ashrae55_or_en15251 is True:
            comf_result = adaptive_comfort_ashrae55(prevail_temp, to)
        else:
            comf_result = adaptive_comfort_en15251(prevail_temp, to)
        
        # Determine the cooling effect
        if adapt_par.discrete_or_continuous_air_speed is True:
            ce = cooling_effect_ashrae55(input[3], to)
        else:
            ce = cooling_effect_en15251(input[3], to)
        
        # Output results
        neutral_temp = comf_result['t_comf']
        deg_neutral = comf_result['deg_comf']
        comfort = adapt_par.is_comfortable(comf_result, ce)
        condition = adapt_par.thermal_condition(comf_result, ce)
    else:
        # The inputs include Data Collections.
        if not isinstance(_air_temp, BaseCollection):
            _air_temp = data_colls[0].get_aligned_collection(
                float(_air_temp), Temperature(), 'C')



        comf_obj = Adaptive.from_air_and_rad_temp(_out_temp, _air_temp, _mrt_,
                                                 _air_speed_, adapt_par)
        
        prevail_temp = comf_obj.prevailing_outdoor_temperature
        neutral_temp = comf_obj.neutral_temperature
        deg_neutral = comf_obj.degrees_from_neutral
        comfort = comf_obj.is_comfortable
        condition = comf_obj.thermal_condition

    return deg_neutral, comf_obj



##############################################################################
# Kivy  classes
Builder.load_file('ventconcept.kv')


class PeriodErrorPopup(Popup):
    error_warning = StringProperty("No text")

class UPopup(Popup):
    thewarning = StringProperty("No")

class UvaluePopup(Popup):
    error = StringProperty("No text")
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class PopupEpw(Popup):
    load = ObjectProperty()
    def get_path(self):
        path = os.path.join(os.getcwd(), 'epw_files')
        return path
    def deactivated_but(self, selected):
        if selected == []:
            return True 
        else:
            if selected[0][-4:] == ".epw":
                return False 
            else: 
                return True


class PopupPeriod(Popup):

    month30 = ["April", "June", "September", "November"]
    febplusdays = ["29", "30", "31"]

    def spinner_clicked(self, value, typ):
        if typ == "sm" or "em":
            self.day_count(value, typ)
        else: print(value) #important to have this one to call "value" in cases where typ is not sm or em
        run_var_update(value, typ)

    def day_count(self, value, typ):
        if typ == "sm":
            if value in self.month30:
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                if self.ids.spinnerSD.text == "31":
                    self.ids.spinnerSD.text = "30"
            elif value == "February":
                if self.ids.spinnerSD.text in self.febplusdays:
                    self.ids.spinnerSD.text = "28"
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
            else:
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        if typ == "em":
            if value in self.month30:
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                if self.ids.spinnerED.text == "31":
                    self.ids.spinnerED.text = "30"
            elif value == "February":
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
                if self.ids.spinnerED.text in self.febplusdays:
                    self.ids.spinnerED.text = "28"
            else:
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]



class PopupConstr(Popup):
    wall_constr = StringProperty("light")
    roof_constr = StringProperty("light")
    gr_floor_constr = StringProperty("light")
    int_floor_constr = StringProperty("light")
    int_wall_constr = StringProperty("light")

    wall_constr_group = StringProperty("wallconstr")
    roof_constr_group = StringProperty("roofconstr")
    floor_constr_group = StringProperty("floorconstr")
    int_floor_constr_group = StringProperty("int_floorconstr")
    int_wall_constr_group = StringProperty("int_wallconstr")

    wall_constr_u = NumericProperty(0.13)
    roof_constr_u = NumericProperty(0.13)
    gr_floor_constr_u = NumericProperty(0.13)

    u_popup = ObjectProperty(UPopup())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)      

    def set_red_color(self, y):
        self.ids[y].foreground_color = (1, 0, 0.2, 1)

    def set_black_color(self, text, y):
        self.ids[y].foreground_color = (0, 0, 0, 1)
        self.ids[y].text = str(float(text))


    def glazing_type (self, value):
        global gl_window_constr
        gl_window_constr = ep_glazing_maker(value)

    def set_u_stand(self, construction):
        if construction == "wallconstr":
            self.wall_constr_u = 0.13
        elif construction == "roofconstr":
            self.roof_constr_u = 0.13
        else:
            self.floor_constr_u = 0.13       


    def manage_constr(self, construction, boolean, u_val, id_value=None):
        if u_val == None:
            pass
        else:
            try:
                u_val = float(u_val)
            except:
                self.set_u_stand(construction)
                self.u_popup.thewarning = "Input must be a number. Use the point (.) instead of comma (,) for decimals."
                self.u_popup.open()
                print("hiiii2")
                return


            if float(u_val) <= 0 or float(u_val) > 4:

                self.set_u_stand(construction)

                # UValueErrorPopup.error_warning = "U-Value must between 0 and 4.0."
                self.u_popup.thewarning = "U-Value must be higher than 0.0 and smaller than 4.0."
                self.u_popup.open()

                return

        if construction == "wallconstr":
            if u_val == None:
                u_val = self.wall_constr_u
            else:
                self.wall_constr_u = float(u_val)

            if boolean == True:
                self.wall_constr = "light"
            elif boolean == False:
                self.wall_constr = "heavy"
            else: # boolean == None
                pass
            global gl_wall_constr
            gl_wall_constr = ep_constr_maker(construction, self.wall_constr, float(u_val))
        elif construction == "roofconstr":
            if u_val == None:
                u_val = self.roof_constr_u
            else:
                self.roof_constr_u = float(u_val)

            if boolean == True:
                self.roof_constr = "light"
            elif boolean == False:
                self.roof_constr = "heavy"
            else: # boolean == None
                pass

            global gl_roof_constr
            gl_roof_constr = ep_constr_maker(construction, self.roof_constr, float(u_val))
        elif construction == "floorconstr":
            if u_val == None:
                u_val = self.gr_floor_constr_u
            else:
                self.gr_floor_constr_u = float(u_val)

            if boolean == True:
                self.gr_floor_constr = "light"
            elif boolean == False:
                self.gr_floor_constr = "heavy"
            else: # boolean == None
                pass

            global gl_floor_constr
            gl_floor_constr = ep_constr_maker(construction, self.gr_floor_constr, float(u_val))
        elif construction == "int_wallconstr":
            if boolean == True:
                self.int_wall_constr = "light"
            elif boolean == False:
                self.int_wall_constr = "heavy"
            else: # boolean == None
                pass

            global gl_int_wall_constr
            gl_int_wall_constr = ep_constr_maker(construction, self.int_wall_constr, None)
        else:
            if boolean == True:
                self.int_floor_constr = "light"
            elif boolean == False:
                self.int_floor_constr = "heavy"
            else: # boolean == None
                pass

            global gl_int_floor_constr
            gl_int_floor_constr = ep_constr_maker(construction, self.int_floor_constr, None)
                
        if id_value is not None:
            self.set_black_color(u_val, id_value)
        

class ScreenLayout_2(BoxLayout):
    pass
class ScreenTogLayout_2(BoxLayout):
    room_result_button = StringProperty("room1")
    def room_result_button_set(self, text):
        self.room_result_button = text

class ScrMng_2(ScreenManager):
    pass

class ScreenLayout(BoxLayout):
    pass

class ScrMng(ScreenManager):
    pass

class Screen1(Screen):
    text_0_len = StringProperty("10.0")
    text_0_wid = StringProperty("10.0")
    text_0_hei = StringProperty("3.0")

    rec_0_len = NumericProperty(200)
    rec_0_wid = NumericProperty(200)
    rec_0_hei = NumericProperty(60)


    length_0 = 10 
    width_0 = 10 
    height_0 = 3


    window_0_rat = NumericProperty(30.0)



    scale_factor = NumericProperty(20)
    canvas_scale = NumericProperty(1)


    compass_angle = NumericProperty(0)


    image_url = StringProperty("images/box_house.png")


    popup_general = PeriodErrorPopup()
    popup_general.title = "Warning"
    popup_general.error_warning = "Only numbers are allowed as input. \n Also, use (.) instead of (,) for decimals."

    popup_number_limit = PeriodErrorPopup()
    popup_number_limit.title = "Warning"
    popup_number_limit.error_warning = "The room lenght, width or height must be higher than 0.2 m and smaller than 300 m."


    popup_percent_ctrl_2 = PeriodErrorPopup()
    popup_percent_ctrl_2.title = "Warning"
    popup_percent_ctrl_2.error_warning = "The window percent-to-wall must be higher than 2 % and smaller than 98 %."


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def set_red_color(self, y):
        self.ids[y].foreground_color = (1, 0, 0.2, 1)

    def set_black_color(self, text, y):
        self.ids[y].foreground_color = (0, 0, 0, 1)
        self.ids[y].text = str(float(text))


    def slide_angle(self, *args):
        value = float(args[1])
        global gl_north_0
        gl_north_0 = value
        self.compass_angle = value


    def create_box_room(self, dimension, width_height, id_value=None):

        global gl_room_0_on

        try:
            dimension = float(dimension)
        except:
            self.popup_general.open()
            return


        if dimension < 0.2 or dimension > 300:
            self.popup_number_limit.open()
            return  

        if width_height == "width":
            self.width_0 = dimension
        elif width_height == "length":
            self.length_0 = dimension
        else: # width_height == "height":
            self.height_0 = dimension


        cross_room_generator_at("room_0_on", self.length_0, self.width_0, self.height_0)

        for face in gl_room_0_on.faces:
            if isinstance(face.type, Floor):
                self.rec_0_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                self.rec_0_len = bounding_domain_x_length([face.geometry]) * self.scale_factor
        self.rec_0_hei = self.height_0 * self.scale_factor


        gl_room_0_on = window_north_south(gl_room_0_on, "North", self.window_0_rat)
        
        self.self_canvas_dim()

        if id_value is not None:
            self.set_black_color(dimension, id_value)


    def self_canvas_dim(self):

        total_length = bounding_domain_x_length([gl_room_0_on.geometry])
        total_width = bounding_domain_y_length([gl_room_0_on.geometry])
        max_dim = total_length if total_length > total_width else total_width

        if max_dim > 20:
            self.canvas_scale = 20 / max_dim
        else:
            self.canvas_scale = 1



    def window_setter(self, percent, typ, id_value = None):

        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return

        if percent < 5 or percent > 95:
            self.popup_percent_ctrl_2.open()
            return

        global gl_room_0_on
        self.window_0_rat = percent

        gl_room_0_on = remove_window(gl_room_0_on, "North")
        gl_room_0_on = window_north_south(gl_room_0_on, "North", percent)

        if id_value is not None:
            self.set_black_color(percent, id_value)




class Screen2(Screen):
    text_0 = StringProperty("10.0")
    text_1 = StringProperty("10.0")


    rec_0_len = NumericProperty(200)
    rec_0_wid = NumericProperty(200)
    rec_1_len = NumericProperty(0)
    rec_1_wid = NumericProperty(0)
    rec_2_len = NumericProperty(0)
    rec_2_wid = NumericProperty(0)


    length_0 = 10 
    length_1 = None
    length_2 = None

    width_0 = 10 
    width_1 = None 
    width_2 = None


    all_height = 3 # default hight is set to 3 meters
    adapted_height_1 = None


    window_0_rat = NumericProperty(30.0) 
    window_1_rat = NumericProperty(30.0) 
    window_2_rat = NumericProperty(30.0)
    window_3_rat = NumericProperty(30.0)

    int_window_0_rat = NumericProperty(20.0)
    int_window_1_rat = NumericProperty(20.0)

    scale_factor = NumericProperty(20)
    canvas_scale = NumericProperty(1)



    disabled_0 = BooleanProperty(False)
    disabled_1 = BooleanProperty(True)
    disabled_2 = BooleanProperty(True)

    dis_but_0 = BooleanProperty(False)
    dis_but_1 = BooleanProperty(True)

    compass_angle = NumericProperty(0)

    toggle0 = NumericProperty(1)
    toggle_lr0 = StringProperty("l")



    r_m_l_1 = NumericProperty(0)
    r_m_l_2 = NumericProperty(0)

    rml_1_type = "l"
    rml_2_type = "l"

    z_add_1 = None
    # others
    image_url = StringProperty("images/box_house.png")


    popup_general = PeriodErrorPopup()
    popup_general.title = "Warning"
    popup_general.error_warning = "Only numbers are allowed as input. \n Also, use (.) instead of (,) for decimals."

    popup_number_limit = PeriodErrorPopup()
    popup_number_limit.title = "Warning"
    popup_number_limit.error_warning = "The room lenght, width or height must be higher than 0.2 m and smaller than 300 m."

    popup_ratio_limit = PeriodErrorPopup()
    popup_ratio_limit.title = "Warning"
    popup_ratio_limit.error_warning = "The window to wall percentage must be higher than 5% and smaller than 95%."



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def placeholder(self):
        pass
    def set_red_color(self, y):
        self.ids[y].foreground_color = (1, 0, 0.2, 1)

    def set_black_color(self, text, y):
        self.ids[y].foreground_color = (0, 0, 0, 1)
        self.ids[y].text = str(float(text))


    def slide_angle(self, *args):
        value = float(args[1])
        global gl_north_1
        gl_north_1 = value
        self.compass_angle = value


    def heihgt_at(self, box_0_len, box_1_len, hei):
        if box_0_len < box_1_len:
            adapted_h = hei + 0.04
            z_add = -0.02
        elif box_0_len == box_1_len:
            adapted_h = hei
            z_add = 0
        else: 
            adapted_h = hei - 0.04
            z_add = 0.02
        return adapted_h, z_add


    def create_box_room(self, dimension, width_height, room_index, id_value=None, mod_text=True):

        global gl_room_0
        global gl_room_1
        global gl_room_2


        if isinstance(dimension, list):
            try:
                dimension = [float(i) for i in dimension]
            except:
                self.popup_general.open()
                return
        else:
            try:
                dimension = float(dimension)
            except:
                self.popup_general.open()
                return

        if isinstance(dimension, list):
            for it in dimension:
                if it < 0.2 or it > 300:
                    self.popup_number_limit.open()
                    return                    
        else:
            if dimension < 0.2 or dimension > 300:
                self.popup_number_limit.open()
                return  


        if room_index == 0:
            if width_height == "width":
                self.width_0 = dimension
            elif width_height == "length":
                self.length_0 = dimension
            elif width_height == "height":
                self.all_height = dimension
            else: # "both"
                self.length_0 = dimension[0]
                self.width_0 = dimension[1]

            cross_room_generator("room_0", self.length_0, self.width_0, self.all_height)
 
            for face in gl_room_0.faces:
                if isinstance(face.type, Floor):
                    self.rec_0_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                    self.rec_0_len = bounding_domain_x_length([face.geometry]) * self.scale_factor


            gl_room_0 = window_north_south(gl_room_0, "North", self.window_0_rat)
            gl_room_0 = window_north_south(gl_room_0, "South", self.window_1_rat)
            
            self.self_canvas_dim(0)


        elif room_index == 1:
            if width_height == "width":
                self.width_1 = dimension
            elif width_height == "length":
                self.length_1 = dimension

            else: # "both"
                self.length_1 = dimension[0]
                self.width_1 = dimension[1]

                
                self.disabled_0 = True
                self.disabled_1 = False
                # self.dis_but_0 = True
                self.dis_but_1 = False
                if mod_text:
                    self.ids.textlen_1.text = str(self.rec_0_len/self.scale_factor)
                    self.ids.textwid_1.text = str(10.0)
                    self.ids.text_inrat_0.text = str(self.int_window_0_rat)
                    self.ids.text_rat_2.text = str(self.window_2_rat)
                    self.ids.room1_big.text = "Room 2"

            self.adapted_height_1, self.z_add_1 = self.heihgt_at(self.length_0, self.length_1, self.all_height)

            cross_room_generator("room_1", self.length_1, self.width_1, self.adapted_height_1, self.z_add_1)
            # print(gl_room_0.geometry.min.x, "min_x", gl_room_0.geometry.max.x, "max_x", gl_room_0.geometry.min.y, "min_y", gl_room_0.geometry.max.y, "max_y",gl_room_1.geometry.min.x, "min_x", gl_room_1.geometry.max.x, "max_x", gl_room_1.geometry.min.y, "min_y", gl_room_1.geometry.max.y, "max_y", "createroom1_first", "HHHHHHHHHHHHHHHHHHHHH")
            for face in gl_room_1.faces:
                if isinstance(face.type, Floor):
                    self.rec_1_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                    self.rec_1_len = bounding_domain_x_length([face.geometry]) * self.scale_factor

            self.self_canvas_dim(1)
            
            gl_room_1.move(self.align(self.rml_1_type, gl_room_0, gl_room_1, "0_1"))  
            gl_room_0 = remove_intersections(gl_room_0, "South")
            gl_room_0 = remove_window(gl_room_0, "South")

            gl_room_0, gl_room_1 = box_intersection(gl_room_0, gl_room_1)
            gl_room_1 = window_north_south(gl_room_1, "South", self.window_2_rat)

            solve_adjacency() # solves adjacencies of all existing rooms

            interior_window(gl_room_0, gl_room_1, self.int_window_0_rat, self.all_height*0.95)


        else: # room_index == 2
            if width_height == "width":
                self.width_2 = dimension
            elif width_height == "length":
                self.length_2 = dimension

            else: # "both"
                self.length_2 = dimension[0]
                self.width_2 = dimension[1]

                self.disabled_0 = True
                self.disabled_1 = True
                self.disabled_2 = False
                self.dis_but_0 = True
                if mod_text:
                    self.ids.textlen_2.text = str(self.rec_1_len/self.scale_factor)
                    self.ids.textwid_2.text = str(10.0)
                    self.ids.text_inrat_1.text = str(self.int_window_1_rat)
                    self.ids.text_rat_3.text = str(self.window_3_rat)
                    self.ids.room2_big.text = "Room 3"

            adapted_height_2, z_add = self.heihgt_at(self.length_1, self.length_2, self.adapted_height_1)            

            cross_room_generator("room_2", self.length_2, self.width_2, adapted_height_2, z_add)

            for face in gl_room_2.faces:
                if isinstance(face.type, Floor):
                    self.rec_2_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                    self.rec_2_len = bounding_domain_x_length([face.geometry]) * self.scale_factor

            self.self_canvas_dim(2)
            gl_room_2.move(self.align(self.rml_2_type, gl_room_1, gl_room_2, "1_2"))  

            gl_room_1 = remove_intersections(gl_room_1, "South")
            gl_room_1 = remove_window(gl_room_1, "South")

            gl_room_1, gl_room_2 = box_intersection(gl_room_1, gl_room_2)


            gl_room_2 = window_north_south(gl_room_2, "South", self.window_3_rat)

            interior_window(gl_room_0, gl_room_1, self.int_window_0_rat, self.all_height*0.95) # because originals got deleted in gl_room_1, easiest way is to call method again :/
            interior_window(gl_room_1, gl_room_2, self.int_window_1_rat, self.all_height*0.95)
            solve_adjacency() # solves adjacencies of all existing rooms

        if id_value is not None:
            self.set_black_color(dimension, id_value)
           

    def remove_box_room(self, ind):
        global gl_room_0
        global gl_room_1
        global gl_room_2

        if ind == 1:
            self.rec_1_len = 0
            self.rec_1_wid = 0
            self.adapted_height_1 = None
            self.disabled_0 = False
            self.disabled_1 = True
            self.dis_but_1 = True
            self.ids.textlen_1.text = " "
            self.ids.textwid_1.text = " "
            self.ids.text_inrat_0.text = " "
            self.ids.text_rat_2.text = " "
            self.ids.room1_big.text = " "
            self.rml_1_type = "l"

            gl_room_1 = None
            gl_room_0 = remove_intersections(gl_room_0, "South")
            gl_room_0 = remove_window(gl_room_0, "South")
            gl_room_0 = window_north_south(gl_room_0, "South", 30)
            solve_adjacency()

            self.self_canvas_dim(0)

        elif ind == 2:
            self.rec_2_len = 0
            self.rec_2_wid = 0
            self.disabled_1 = False
            self.disabled_2 = True
            self.dis_but_0 = False
            self.ids.textlen_2.text = " "
            self.ids.textwid_2.text = " "
            self.ids.text_inrat_1.text = " "
            self.ids.text_rat_3.text = " "
            self.ids.room2_big.text = " "
            self.rml_2_type = "l"

            gl_room_2 = None
            gl_room_1 = remove_intersections(gl_room_1, "South")
            gl_room_1 = remove_window(gl_room_1, "South")
            gl_room_1 = window_north_south(gl_room_1, "South", 30)
            solve_adjacency()

            self.self_canvas_dim(1)


    def remove_and_add_rml(self, rml, ind):
        global gl_room_0
        global gl_room_1
        global gl_room_2
        if ind == "0_1":
            self.rml_1_type = rml
            gl_room_1.move(self.align(self.rml_1_type, gl_room_0, gl_room_1, "0_1"))

            gl_room_1 = None
            gl_room_0 = remove_intersections(gl_room_0, "South")
            gl_room_0 = remove_window(gl_room_0, "South")
            gl_room_0 = window_north_south_spec(gl_room_0, "South", 30, 30, 50)
            solve_adjacency()
            self.create_box_room([self.length_1, self.width_1], "both", 1, mod_text=False)

        else: #ind == "1_2":
            self.rml_2_type = rml
            gl_room_2.move(self.align(self.rml_2_type, gl_room_1, gl_room_2, "1_2"))

            gl_room_2 = None
            gl_room_1 = remove_intersections(gl_room_1, "South")
            gl_room_1 = remove_window(gl_room_1, "South")
            gl_room_1 = window_north_south_spec(gl_room_1, "South", 30, 30, 50)
            solve_adjacency()
            self.create_box_room([self.length_2, self.width_2], "both", 2, mod_text=False)


    def self_canvas_dim(self, ind):
        if ind == 0:
            total_length = bounding_domain_x_length([gl_room_0.geometry])
            total_width = bounding_domain_y_length([gl_room_0.geometry])
            max_dim = total_length if total_length > total_width else total_width

            if max_dim > 20:
                self.canvas_scale = 20 / max_dim
            else:
                self.canvas_scale = 1


        elif ind == 1:
            total_length = bounding_domain_x_length([gl_room_0.geometry, gl_room_1.geometry])
            total_width = bounding_domain_y_length([gl_room_0.geometry, gl_room_1.geometry])
            max_dim = total_length if total_length > total_width else total_width

            if max_dim > 20:
                self.canvas_scale = 20 / max_dim
            else:
                self.canvas_scale = 1

        else: # ind == 2
            total_length = bounding_domain_x_length([gl_room_0.geometry, gl_room_1.geometry, gl_room_2.geometry])
            total_width = bounding_domain_y_length([gl_room_0.geometry, gl_room_1.geometry, gl_room_2.geometry])
            max_dim = total_length if total_length > total_width else total_width

            if max_dim > 20:
                self.canvas_scale = 20 / max_dim
            else:
                self.canvas_scale = 1


    """deactivated due to issue of deleted windows at some times - remove_and_add_rml was created instead, this method deletes room 1/2 and recreates it then
    def align_et_al(self, r_m_l, ind):
        global gl_room_0
        global gl_room_1
        global gl_room_2


        if ind == "0_1":
            self.adapted_height_1, self.z_add_1 = self.heihgt_at(self.length_0, self.length_1, self.all_height)

            cross_room_generator("room_1", bounding_domain_x_length([gl_room_1.geometry]), bounding_domain_y_length([gl_room_1.geometry]), self.adapted_height_1, self.z_add_1)

            gl_room_0 = remove_intersections(gl_room_0, "South")
            gl_room_1.move(self.align(r_m_l, gl_room_0, gl_room_1, ind))  

            gl_room_0 = remove_window(gl_room_0, "South")


            gl_room_1 = window_north_south(gl_room_1, "South", self.window_2_rat)
            for face in gl_room_0:
                for ap in face.apertures:
                    print(ap.geometry.area, "area room 0")
            for face in gl_room_1:
                for ap in face.apertures:
                    print(ap.geometry.area, "area room 1")

            gl_room_0, gl_room_1 = box_intersection(gl_room_0, gl_room_1)

            solve_adjacency() # solves adjacencies of all existing rooms
            interior_window(gl_room_0, gl_room_1, self.int_window_0_rat, self.all_height*0.95)



        elif ind == "1_2":
            self.adapted_height_2, z_add = self.heihgt_at(self.length_1, self.length_2, self.adapted_height_1)

            cross_room_generator("room_2", bounding_domain_x_length([gl_room_2.geometry]), bounding_domain_y_length([gl_room_2.geometry]), self.adapted_height_2, z_add)
            
            gl_room_1 = remove_intersections(gl_room_1, "South")
            gl_room_2.move(self.align(r_m_l, gl_room_1, gl_room_2, ind))  
            
            gl_room_1 = remove_window(gl_room_1, "South")
            
            gl_room_2 = window_north_south(gl_room_2, "South", self.window_3_rat)
            gl_room_1, gl_room_2 = box_intersection(gl_room_1, gl_room_2)
            for face in gl_room_0:
                for ap in face.apertures:
                    print(ap.geometry.area, "area room 0")
            for face in gl_room_1:
                for ap in face.apertures:
                    print(ap.geometry.area, "area room 1")
            for face in gl_room_2:
                for ap in face.apertures:
                    print(ap.geometry.area, "area room 2")

            interior_window(gl_room_0, gl_room_1, self.int_window_0_rat, self.all_height*0.95) # because originals got deleted in gl_room_1, easiest way is to call method again :/
            
            interior_window(gl_room_1, gl_room_2, self.int_window_1_rat, self.all_height*0.95)   
            solve_adjacency() # solves adjacencies of all existing rooms
    """


    def align(self, r_m_l, box_0, box_1, ind):
        if r_m_l == "l":
            if get_smaller_x_box(box_0, box_1) == "box_1":
                x_add_add = +0.02
            elif get_smaller_x_box(box_0, box_1) == "box_0":
                x_add_add = -0.02
            else: 
                x_add_add = 0
            x_add = box_0.geometry.min.x - box_1.geometry.min.x + x_add_add
        elif r_m_l == "r":
            if get_smaller_x_box(box_0, box_1) == "box_1":
                x_add_add = -0.02
            elif get_smaller_x_box(box_0, box_1) == "box_0":
                x_add_add = +0.02
            else: 
                x_add_add = 0
            # x_add = + (bounding_domain_x_length([box_1.geometry]) - bounding_domain_x_length([box_0.geometry])) + x_add_add
            x_add = box_0.geometry.max.x - box_1.geometry.max.x + x_add_add
        else: # r_m_l == "m"
            if get_smaller_x_box(box_0, box_1) == "equal":
                x_add = 0
            else:
                x_add = (box_0.geometry.max.x - box_0.geometry.min.x)*0.5 - (box_1.geometry.max.x - box_1.geometry.min.x)*0.5 


        if ind == "0_1":
            if r_m_l == "l":
                self.r_m_l_1 = 0
                self.rml_1_type = "l"
            elif r_m_l == "r":
                self.r_m_l_1 = (self.rec_1_len - self.rec_0_len)  # * self.canvas_scale
                self.rml_1_type = "r"
            else: # r_m_l == "m"
                self.r_m_l_1 = 0.5 * (self.rec_1_len - self.rec_0_len)  # * self.canvas_scale
                self.rml_1_type = "m"

        else: # ind == "1_2":
            if r_m_l == "l":
                self.r_m_l_2 = 0
                self.rml_2_type = "l"
            elif r_m_l == "r":
                self.r_m_l_2 = (self.rec_2_len - self.rec_1_len)  # * self.canvas_scale
                self.rml_2_type = "r"
            else: # r_m_l == "m"
                self.r_m_l_2 = 0.5 * (self.rec_2_len - self.rec_1_len)  # * self.canvas_scale
                self.rml_2_type = "m"

        return Vector3D(x_add, 0, 0)



    def window_setter(self, ind, percent, id_value = None):

        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return

        if percent < 2 or percent > 98:
            self.popup_ratio_limit.open()
            return

        global gl_room_0
        global gl_room_1
        global gl_room_2

        if ind == 0:
            gl_room_0 = remove_window(gl_room_0, "North")
            gl_room_0 = window_north_south(gl_room_0, "North", percent)
            self.window_0_rat = percent
        elif ind == 1:
            gl_room_0 = remove_window(gl_room_0, "South")
            gl_room_0 = window_north_south(gl_room_0, "South", percent)
            self.window_1_rat = percent
        elif ind == 2:
            gl_room_1 = remove_window(gl_room_1, "South")
            gl_room_1 = window_north_south(gl_room_1, "South", percent)
            self.window_2_rat = percent      
        else: # ind == 3:
            gl_room_2 = remove_window(gl_room_2, "South")
            gl_room_2 = window_north_south(gl_room_2, "South", percent)
            self.window_3_rat = percent

        if id_value is not None:
            self.set_black_color(percent, id_value)

    def interior_window_setter(self, ind, percent, id_value = None):
        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return

        if percent < 2 or percent > 98:
            self.popup_ratio_limit.open()
            return

        percent = float(percent)
        global gl_room_0
        global gl_room_1
        global gl_room_2

        if ind == 0:
            interior_window(gl_room_0, gl_room_1, percent, self.all_height*0.95)
            self.int_window_0_rat = percent
        else: # ind == 1:
            interior_window(gl_room_1, gl_room_2, percent, self.all_height*0.95)
            self.int_window_1_rat = percent

        if id_value is not None:
            self.set_black_color(percent, id_value)



class Screen3(Screen):
    text_0_len = StringProperty("10.0")
    text_0_wid = StringProperty("10.0")
    text_0_hei = StringProperty("3.0")
    text_0_off = StringProperty("0.0")

    rec_0_len = NumericProperty(200)
    rec_0_wid = NumericProperty(200)
    rec_0_hei = NumericProperty(60)
    rec_1_len = NumericProperty(0)
    rec_1_wid = NumericProperty(0)
    rec_1_hei = NumericProperty(0)


    length_0 = 10 
    length_1 = None

    width_0 = 10 
    width_1 = None

    height_0 = 3
    height_1 = None 

    offset_0 = 0


    window_0_rat_wid = NumericProperty(30.0)
    window_1_rat_wid = NumericProperty(30.0)
    window_2_rat_wid = NumericProperty(30.0)
    window_0_rat_hei = NumericProperty(30.0)
    window_1_rat_hei = NumericProperty(30.0)
    window_2_rat_hei = NumericProperty(15.0)
    window_0_offs = NumericProperty(10.0)
    window_1_offs = NumericProperty(90.0)
    window_2_offs = NumericProperty(90.0)

    int_window_0_rat_wid = NumericProperty(20.0)
    int_window_0_rat_hei = NumericProperty(30.0)
    int_window_0_offs = NumericProperty(90.0)

    scale_factor = NumericProperty(20)
    canvas_scale = NumericProperty(1)
    canvas_hei_scale = NumericProperty(1)
    new_hei = NumericProperty(0)

    compass_angle = NumericProperty(0)

    disabled_0 = BooleanProperty(False)
    disabled_1 = BooleanProperty(True)
    disabled_2 = BooleanProperty(True)

    dis_but_0 = BooleanProperty(False)
    dis_but_1 = BooleanProperty(True)



    r_m_l_1 = NumericProperty(0)

    rml_1_type = "l"


    image_url = StringProperty("images/box_house.png")


    popup_general = PeriodErrorPopup()
    popup_general.title = "Warning"
    popup_general.error_warning = "Only numbers are allowed as input. \n Also, use (.) instead of (,) for decimals."

    popup_number_limit = PeriodErrorPopup()
    popup_number_limit.title = "Warning"
    popup_number_limit.error_warning = "The room lenght, width or height must be higher than 0.2 m and smaller than 300 m."

    popup_percent_ctrl = PeriodErrorPopup()
    popup_percent_ctrl.title = "Warning"
    popup_percent_ctrl.error_warning = "The offset from Room 1 to Room 2 (Atrium) must be between 0 % and 100 %."

    popup_percent_ctrl_2 = PeriodErrorPopup()
    popup_percent_ctrl_2.title = "Warning"
    popup_percent_ctrl_2.error_warning = "The window percent-to-wall must be higher than 2 % and smaller than 98 %."

    popup_percent_ctrl_3 = PeriodErrorPopup()
    popup_percent_ctrl_3.title = "Warning"
    popup_percent_ctrl_3.error_warning = "The window offset must be higher than 2 % (aligned to bottom) \n \
        and smaller than 98 % (aligned to top)."

    popup_ratio_limit = PeriodErrorPopup()
    popup_ratio_limit.title = "Warning"
    popup_ratio_limit.error_warning = "The height offset in percent can be between 0 % (stick to the buttom of the atrium) and \n 100 % (Room 1 ceiling aligned to atrium ceiling)"

    popup_dim_control = PeriodErrorPopup()
    popup_dim_control.title = "Warning"
    popup_dim_control.error_warning = "The atrium length and height must be taller \n than the length and height of Room 1."



    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def set_red_color(self, y):
        self.ids[y].foreground_color = (1, 0, 0.2, 1)

    def set_black_color(self, text, y):
        self.ids[y].foreground_color = (0, 0, 0, 1)
        self.ids[y].text = str(float(text))


    def slide_angle(self, *args):
        value = float(args[1])
        global gl_north_2
        gl_north_2 = value
        self.compass_angle = value


    def heihgt_at(self, box_0_len, box_1_len):
        if box_0_len == box_1_len:
            self.height_1 = hei + 0.04
            z_add = -0.02
        else: 
            z_add = 0
        


    def create_box_room(self, dimension, width_height, room_index, id_value=None, mod_text=True):

        global gl_room_0_at
        global gl_room_1_at

        if isinstance(dimension, list):
            try:
                dimension = [float(i) for i in dimension]
            except:
                self.popup_general.open()
                return
        else:
            try:
                dimension = float(dimension)
            except:
                self.popup_general.open()
                return

        if isinstance(dimension, list):
            for it in dimension:
                if it < 0.2 or it > 300:
                    self.popup_number_limit.open()
                    return                    
        else:
            if dimension < 0.2 or dimension > 300:
                self.popup_number_limit.open()
                return  


        if room_index == 0:
            if width_height == "width":
                self.width_0 = dimension
            elif width_height == "length":
                self.length_0 = dimension
            elif width_height == "height":
                self.height_0 = dimension
            else: # "both"
                self.length_0 = dimension[0]
                self.width_0 = dimension[1]

            cross_room_generator_at("room_0_at", self.length_0, self.width_0, self.height_0)
 
            for face in gl_room_0_at.faces:
                if isinstance(face.type, Floor):
                    self.rec_0_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                    self.rec_0_len = bounding_domain_x_length([face.geometry]) * self.scale_factor
            self.rec_0_hei = self.height_0 * self.scale_factor


            gl_room_0_at = window_north_south_spec(gl_room_0_at, "North", self.window_0_rat_wid, self.window_0_rat_hei, self.window_0_offs)
            gl_room_0_at = window_north_south_spec(gl_room_0_at, "South", self.window_1_rat_wid, self.window_1_rat_hei, self.window_1_offs)
            
            self.self_canvas_dim(0)
            self.self_canvas_dim_height(0)


        else: # room_index == 1:
            if width_height == "width":
                self.width_1 = dimension
            elif width_height == "length":
                self.length_1 = dimension
            elif width_height == "height":
                self.height_1 = dimension
            else: # "all three"
                self.length_1 = dimension[0]
                self.width_1 = dimension[1]
                self.height_1 = dimension[2]

                
                self.disabled_0 = True
                self.disabled_1 = False
                # self.dis_but_0 = True
                self.dis_but_1 = False
                if mod_text:
                    self.ids.textlen_1.text = str(float(self.length_0 * 2))
                    self.ids.textwid_1.text = str(10.0)
                    self.ids.texthei_1.text = str(float(self.height_0 * 2))


                    self.ids.int_window_0_wid.text = str(float(self.int_window_0_rat_wid))
                    self.ids.int_window_0_hei.text = str(float(self.int_window_0_rat_hei))
                    self.ids.int_window_0_offs.text = str(float(self.int_window_0_offs))
                    self.ids.window_2_wid.text = str(float(self.window_2_rat_wid))
                    self.ids.window_2_hei.text = str(float(self.window_2_rat_hei))
                    self.ids.window_2_offs.text = str(float(self.window_2_offs))

                    self.ids.room1_big.text = "Atrium/ \nRoom 2"


            if self.check_and_adapt_height() is False:
                self.popup_dim_control.open()
                return

            cross_room_generator_at("room_1_at", self.length_1, self.width_1, self.height_1)

            for face in gl_room_1_at.faces:
                if isinstance(face.type, Floor):
                    self.rec_1_wid = bounding_domain_y_length([face.geometry]) * self.scale_factor
                    self.rec_1_len = bounding_domain_x_length([face.geometry]) * self.scale_factor
            self.rec_1_hei = self.height_1 * self.scale_factor

            self.self_canvas_dim(1)
            self.self_canvas_dim_height(1)

            gl_room_0_at.move(self.z_adjust(self.offset_0)) ####new

            gl_room_1_at.move(self.align(self.rml_1_type, gl_room_0_at, gl_room_1_at))

            gl_room_0_at = remove_intersections(gl_room_0_at, "South")

            gl_room_0 = remove_window(gl_room_0_at, "South")

            gl_room_0_at, gl_room_1_at = box_intersection(gl_room_0_at, gl_room_1_at)

            gl_room_1_at = window_north_south_spec(gl_room_1_at, "South", self.window_2_rat_wid, self.window_2_rat_hei, self.window_2_offs)

            solve_adjacency_at() # solves adjacencies of all existing rooms

            interior_window_spec(gl_room_0_at, gl_room_1_at, self.int_window_0_rat_wid, self.int_window_0_rat_hei, self.int_window_0_offs)


        if id_value is not None:
            self.set_black_color(dimension, id_value)
        

    def check_and_adapt_height(self):
        if self.height_0 <= self.height_1 and self.length_0 <= self.length_1:
            pass
        else:
            return False
        if self.height_0 >= (self.height_1 - 0.04):
            self.height_1 = self.height_1 + 0.04
        if self.length_0 >= (self.length_1 - 0.04):
            self.length_1 = self.length_1 + 0.04
        return True

    def z_adjust(self, percent):
        self.offset_0 = percent
        # adding safety space
        if percent < 2:
            add = +0.02
        elif percent > 98:
            add = -0.02
        else:
            add = 0

        total_z = self.height_1 - self.height_0
        current_z = gl_room_0_at.geometry.min.z

        new_hei = total_z * (percent/100)
        self.new_hei = new_hei
        dif_z = new_hei - current_z + add
 
        return Vector3D(0, 0, dif_z)
 
    def remove_and_add(self, percent, id_value):
        global gl_room_0_at
        global gl_room_1_at

        self.offset_0 = float(percent)

        gl_room_1_at = None
        gl_room_0_at = remove_intersections(gl_room_0_at, "South")
        gl_room_0_at = remove_window(gl_room_0_at, "South")
        gl_room_0_at = window_north_south_spec(gl_room_0_at, "South", 30, 30, 50)
        solve_adjacency_at()

        self.create_box_room([self.length_1, self.width_1, self.height_1], "all", 1, mod_text=False)

        if id_value is not None:
            self.set_black_color(percent, id_value)

    def remove_and_add_rml(self, rml):
        global gl_room_0_at
        global gl_room_1_at

        self.rml_1_type = rml
        gl_room_1_at.move(self.align(self.rml_1_type, gl_room_0_at, gl_room_1_at))

        gl_room_1_at = None
        gl_room_0_at = remove_intersections(gl_room_0_at, "South")
        gl_room_0_at = remove_window(gl_room_0_at, "South")
        gl_room_0_at = window_north_south_spec(gl_room_0_at, "South", 30, 30, 50)
        solve_adjacency_at()

        self.create_box_room([self.length_1, self.width_1, self.height_1], "all", 1, mod_text=False)


    def remove_box_room(self):
        global gl_room_0_at
        global gl_room_1_at

        self.rec_1_len = 0
        self.rec_1_wid = 0
        self.rec_1_hei = 0
        self.new_hei = 0
        self.adapted_height_1 = None
        self.disabled_0 = False
        self.disabled_1 = True
        self.dis_but_1 = True
        self.ids.textlen_1.text = " "
        self.ids.textwid_1.text = " "
        self.ids.texthei_1.text = " "
        self.ids.int_window_0_wid.text = " "
        self.ids.int_window_0_hei.text = " "
        self.ids.int_window_0_offs.text = " "
        self.ids.window_2_wid.text = " "
        self.ids.window_2_hei.text = " "
        self.ids.window_2_offs.text = " "
        self.rml_1_type = "l"
        gl_room_1_at = None
        gl_room_0_at = remove_intersections(gl_room_0_at, "South")
        gl_room_0_at = remove_window(gl_room_0_at, "South")
        gl_room_0_at = window_north_south_spec(gl_room_0_at, "South", 30, 30, 50)
        solve_adjacency_at()

        self.self_canvas_dim(0)
        self.self_canvas_dim_height(0)



    def self_canvas_dim(self, ind):
        if ind == 0:
            total_length = bounding_domain_x_length([gl_room_0_at.geometry])
            total_width = bounding_domain_y_length([gl_room_0_at.geometry])
            max_dim = total_length if total_length > total_width else total_width

        else: # ind == 1:
            total_length = bounding_domain_x_length([gl_room_0_at.geometry, gl_room_1_at.geometry])
            total_width = bounding_domain_y_length([gl_room_0_at.geometry, gl_room_1_at.geometry])
            max_dim = total_length if total_length > total_width else total_width

        if max_dim > 20:
            self.canvas_scale = 20 / max_dim
        else:
            self.canvas_scale = 1

    def self_canvas_dim_height(self, ind):
        if ind == 0:
            total_height = bounding_domain_z_length([gl_room_0_at.geometry])
            total_width = bounding_domain_y_length([gl_room_0_at.geometry])

        else: # ind == 1:
            total_height = bounding_domain_z_length([gl_room_1_at.geometry])
            total_width = bounding_domain_y_length([gl_room_0_at.geometry, gl_room_1_at.geometry])

        if (total_height - 10)  > (total_width - 30):
            if total_height > 11:
                self.canvas_hei_scale = 11 / total_height
            else:
                self.canvas_hei_scale = 1
        else:
            if total_width > 20:
                self.canvas_hei_scale = 20 / total_width
            else:
                self.canvas_hei_scale = 1


    """ deactivated due to issue of deleted windows at some times - remove_and_add was created instead, this method deletes room 1 and recreates it
    def align_z_al(self, percent, id_value):
        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return

        if percent < 0 or percent > 100:
            self.popup_percent_ctrl.open()
            return  


        global gl_room_0_at
        global gl_room_1_at

        for face in gl_room_0_at.faces:


        gl_room_0_at.move(self.z_adjust(percent))

        gl_room_0_at = remove_intersections(gl_room_0_at, "South")

        gl_room_0_at = remove_window(gl_room_0_at, "South")
        gl_room_0_at = remove_window(gl_room_0_at, "North")
        gl_room_1_at = remove_window(gl_room_1_at, "North")
        gl_room_1_at = remove_window(gl_room_1_at, "South")

        # solve_adjacency_at()

        gl_room_0_at = window_north_south_spec(gl_room_0_at, "North", self.window_0_rat_wid, self.window_0_rat_hei, self.window_0_offs)
        gl_room_1_at = window_north_south_spec(gl_room_1_at, "South", self.window_1_rat_wid, self.window_1_rat_hei, self.window_1_offs)

        gl_room_0_at, gl_room_1_at = box_intersection(gl_room_0_at, gl_room_1_at)

        solve_adjacency_at() # solves adjacencies of all existing rooms

        interior_window_spec(gl_room_0_at, gl_room_1_at, self.int_window_0_rat_wid, self.int_window_0_rat_hei, self.int_window_0_offs)

        if id_value is not None:
            self.set_black_color(percent, id_value)
    """

    """  deactivated due to issue of deleted windows at some times - remove_and_add_rml was created instead, this method deletes room 1 and recreates it
    def align_et_al(self, r_m_l):
        global gl_room_0_at
        global gl_room_1_at
        
        cross_room_generator_at("room_1_at", self.length_1, self.width_1, self.height_1)

        gl_room_0_at = remove_intersections(gl_room_0_at, "South")

        gl_room_0_at.move(self.z_adjust(self.offset_0)) # always update to z position
        gl_room_1_at.move(self.align(r_m_l, gl_room_0_at, gl_room_1_at))

        gl_room_0_at = remove_window(gl_room_0_at, "South")


        gl_room_1_at = remove_window(gl_room_1_at, "North")

        gl_room_0_at, gl_room_1_at = box_intersection(gl_room_0_at, gl_room_1_at)

        solve_adjacency_at() # solves adjacencies of all existing rooms
        interior_window_spec(gl_room_0_at, gl_room_1_at, self.int_window_0_rat_wid, self.int_window_0_rat_hei, self.int_window_0_offs)
    """

    def align(self, r_m_l, box_0, box_1):
        if r_m_l == "l":

            if get_smaller_x_box(box_0, box_1) == "box_0":
                x_add_add = -0.02

            x_add = box_0.geometry.min.x - box_1.geometry.min.x + x_add_add
        elif r_m_l == "r":
            if get_smaller_x_box(box_0, box_1) == "box_0":
                x_add_add = +0.02

            # x_add = + (bounding_domain_x_length([box_1.geometry]) - bounding_domain_x_length([box_0.geometry])) + x_add_add
            x_add = box_0.geometry.max.x - box_1.geometry.max.x + x_add_add
        else: # r_m_l == "m"
            if get_smaller_x_box(box_0, box_1) == "equal":
                x_add = 0
            else:
                x_add = (box_0.geometry.max.x - box_0.geometry.min.x)*0.5 - (box_1.geometry.max.x - box_1.geometry.min.x)*0.5 


        if r_m_l == "l":
            self.r_m_l_1 = 0
            self.rml_1_type = "l"
        elif r_m_l == "r":
            self.r_m_l_1 = (self.rec_1_len - self.rec_0_len)  # * self.canvas_scale
            self.rml_1_type = "r"
        else: # r_m_l == "m"
            self.r_m_l_1 = 0.5 * (self.rec_1_len - self.rec_0_len)  # * self.canvas_scale
            self.rml_1_type = "m"


        return Vector3D(x_add, 0, 0)



    def window_setter(self, ind, percent, typ, id_value = None):

        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return
        if typ == "offset":
            if percent < 2 or percent > 98:
                self.popup_percent_ctrl_3.open()
                return
        else:
            if percent < 2 or percent > 98:
                self.popup_percent_ctrl_2.open()
                return

        global gl_room_0_at
        global gl_room_1_at


        if ind == 0:
            if typ == "height":
                height = percent
                width = self.window_0_rat_wid
                offset = self.window_0_offs
                self.window_0_rat_hei = percent
            elif typ == "width":
                height = self.window_0_rat_hei
                width = percent
                offset = self.window_0_offs
                self.window_0_rat_wid = percent
            else: # offset
                offset = percent
                height = self.window_0_rat_hei
                width = self.window_0_rat_wid
                self.window_0_offs = percent

        elif ind == 1:
            if typ == "height":
                height = percent
                width = self.window_1_rat_wid
                offset = self.window_1_offs
                self.window_1_rat_hei = percent
            elif typ == "width":
                height = self.window_1_rat_hei
                width = percent
                offset = self.window_1_offs
                self.window_1_rat_wid = percent
            else: # offset
                offset = percent
                height = self.window_1_rat_hei
                width = self.window_1_rat_wid
                self.window_1_offs = percent

        else: # ind == 2
            if typ == "height":
                height = percent
                width = self.window_2_rat_wid
                offset = self.window_2_offs
                self.window_2_rat_hei = percent
            elif typ == "width":
                height = self.window_2_rat_hei
                width = percent
                offset = self.window_2_offs
                self.window_2_rat_wid = percent
            else: # offset
                offset = percent
                height = self.window_2_rat_hei
                width = self.window_2_rat_wid
                self.window_2_offs = percent

        if ind == 0:
            gl_room_0_at = remove_window(gl_room_0_at, "North")
            gl_room_0_at = window_north_south_spec(gl_room_0_at, "North", width, height, offset)

        elif ind == 1:
            gl_room_0_at = remove_window(gl_room_0_at, "South")
            gl_room_0_at = window_north_south_spec(gl_room_0_at, "South", width, height, offset)

        else: # ind == 2:
            gl_room_1_at = remove_window(gl_room_1_at, "South")
            gl_room_1_at = window_north_south_spec(gl_room_1_at, "South", width, height, offset)
   

        if id_value is not None:
            self.set_black_color(percent, id_value)

    def interior_window_setter(self, percent, typ, id_value = None):
        try:
            percent = float(percent)
        except:
            self.popup_general.open()
            return

        if typ == "offset":
            if percent < 2 or percent > 98:
                self.popup_percent_ctrl_3.open()
                return
        else:
            if percent < 2 or percent > 98:
                self.popup_percent_ctrl_2.open()
                return
        global gl_room_0_at
        global gl_room_1_at

        if typ == "height":
            height = percent
            width = self.int_window_0_rat_wid
            offset = self.int_window_0_offs
            self.int_window_0_rat_hei = percent
        elif typ == "width":
            height = self.int_window_0_rat_hei
            width = percent
            offset = self.int_window_0_offs
            self.int_window_0_rat_wid = percent
        else: # offset
            height = self.int_window_0_rat_hei
            width = self.int_window_0_rat_wid
            offset = percent
            self.int_window_0_offs = percent

        interior_window_spec(gl_room_0_at, gl_room_1_at, width, height, offset)

        if id_value is not None:
            self.set_black_color(percent, id_value)


def prepare_plot_temp(subpl):
    subpl.set_xlabel('Simulated Time Span')
    subpl.set_ylabel("Temperature in C°")
    subpl.set_title('Temperature', y=1.0, pad=-14)     
    subpl.xaxis_date()
    subpl.grid('on') 
def prepare_plot_vent(subpl):
    subpl.set_xlabel('Simulated Time Span')
    subpl.set_ylabel("Air Changes per Hour (ACH)")
    subpl.set_title('Ventilation (ACH refers to volume of all rooms together)', y=1.0, pad=-14)
    subpl.xaxis_date()
    subpl.grid('on')
def extract_sql(sql):
    datetime_x = lb_datetime_to_datetime(sql.datetimes)
    sql_x = dates.date2num(datetime_x)
    sql_y = list(sql.values)
    return sql_x, sql_y
def extract_sql_y(sql):
    sql_y = list(sql.values)
    return sql_y


class Screen4(Screen):
    figureagg_temp = ObjectProperty()
    figureagg_ach = ObjectProperty()
    legend = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_results(self):
        if sql_ot is None:
            PeriodErrorPopup.error_warning = "No simulation was found. Make sure you run a simulation \nunder the Simulation Tap, before loading the results."
            PeriodErrorPopup().open()
            return


        sql_x_ot, sql_y_ot = extract_sql(sql_ot)
        subplot_temp_0.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at)
        subplot_temp_0.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_0.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        if self.legend is False:
            lgd = subplot_temp_0.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')
            self.legend = True

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_0.plot(sql_x_vt, sql_y_vt, color="b")


        layout = self.ids.resultlayout
        layout_1 = self.ids.percent_hot_layout

        try:
            layout.remove_widget(self.figureagg_temp)
        except:
            pass
        try:
            layout.remove_widget(self.figureagg_ach)
        except:
            pass

        self.figureagg_temp = FigureCanvasKivyAgg(fig)
        self.figureagg_ach = FigureCanvasKivyAgg(fig_1)

        layout.add_widget(self.figureagg_temp)
        layout.add_widget(self.figureagg_ach)

        self.ids.label_resume.text = "Resume Room 1: "
        self.ids.label_hot.text = str(round(gl_pct_hot,2)) +" %: too Hot"
        #self.ids.label_cold.text = str(round(gl_pct_cold, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot) +" h: too Hot"
        #self.ids.label_cold_hours.text = str(gl_total_h_cold) +" h: too Cold"

        self.ids.label_results_0.text = " "


    def clear_anterior_graphs(self):
        if sql_ot is None:
            PeriodErrorPopup.error_warning = "No simulation was found. Make sure you run a simulation \nunder the Simulation Tap, before loading the results."
            PeriodErrorPopup().open()
            return
        global subplot_temp_0
        global subplot_vent_0

        fig.clf()
        fig_1.clf()


        subplot_temp_0 = fig.add_subplot(1, 1, 1)
        prepare_plot_temp(subplot_temp_0)

        sql_x_ot, sql_y_ot = extract_sql(sql_ot)
        subplot_temp_0.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at)
        subplot_temp_0.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_0.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        lgd = subplot_temp_0.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')


        subplot_vent_0 = fig_1.add_subplot(1, 1, 1)
        prepare_plot_vent(subplot_vent_0)

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_0.plot(sql_x_vt, sql_y_vt, color="b")

        fig.canvas.draw_idle()
        fig_1.canvas.draw_idle()

        self.ids.label_resume.text = "Resume Room 1: "
        self.ids.label_hot.text = str(round(gl_pct_hot,2)) +" %: too Hot"
        #self.ids.label_cold.text = str(round(gl_pct_cold, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot) +" h: too Hot"
        #self.ids.label_cold_hours.text = str(gl_total_h_cold) +" h: too Cold"

        self.ids.label_results_0.text = " "


class Screen5(Screen):
    figureagg_temp = ObjectProperty()
    figureagg_ach = ObjectProperty()
    legend = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_results(self):
        if sql_ot_1 is None:
            PeriodErrorPopup.error_warning = "No simulation for Room 2 was found. Maybe your model only has one Room \nor no simulation at all was done. In this case run the simulation \nunder the simulation tab."
            PeriodErrorPopup().open()
            try:
                layout.remove_widget(self.figureagg_temp)
            except:
                pass
            try:
                layout.remove_widget(self.figureagg_ach)
            except:
                pass
            self.ids.label_resume.text = " "
            self.ids.label_hot.text = " "
            #self.ids.label_cold.text = " "
            self.ids.label_hot_hours.text = " "
            #self.ids.label_cold_hours.text = " "

            self.ids.label_results_1.text = " "
            return


        sql_x_ot, sql_y_ot = extract_sql(sql_ot_1)
        subplot_temp_1.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at_1)
        subplot_temp_1.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_1.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        if self.legend is False:
            lgd = subplot_temp_1.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')
            self.legend = True

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_1.plot(sql_x_vt, sql_y_vt, color="b")


        layout = self.ids.resultlayout
        layout_1 = self.ids.percent_hot_layout

        try:
            layout.remove_widget(self.figureagg_temp)
        except:
            pass
        try:
            layout.remove_widget(self.figureagg_ach)
        except:
            pass

        self.figureagg_temp = FigureCanvasKivyAgg(fig_2)
        self.figureagg_ach = FigureCanvasKivyAgg(fig_3)

        layout.add_widget(self.figureagg_temp)
        layout.add_widget(self.figureagg_ach)

        self.ids.label_resume.text = "Resume Room 2: "
        self.ids.label_hot.text = str(round(gl_pct_hot_1,2)) +" %: too Hot"
        # self.ids.label_cold.text = str(round(gl_pct_cold_1, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot_1) +" h: too Hot"
        # self.ids.label_cold_hours.text = str(gl_total_h_cold_1) +" h: too Cold"

        self.ids.label_results_1.text = " "


    def clear_anterior_graphs(self):
        if sql_ot_1 is None:
            PeriodErrorPopup.error_warning = "No simulation for Room 2 was found. Maybe your model only has one Room \nor no simulation at all was done. In this case run the simulation \nunder the simulation tab."
            PeriodErrorPopup().open()
            try:
                layout.remove_widget(self.figureagg_temp)
            except:
                pass
            try:
                layout.remove_widget(self.figureagg_ach)
            except:
                pass
            self.ids.label_resume.text = " "
            self.ids.label_hot.text = " "
            #self.ids.label_cold.text = " "
            self.ids.label_hot_hours.text = " "
            #self.ids.label_cold_hours.text = " "

            self.ids.label_results_1.text = " "
            return

        global subplot_temp_1
        global subplot_vent_1

        fig_2.clf()
        fig_3.clf()


        subplot_temp_1 = fig_2.add_subplot(1, 1, 1)
        prepare_plot_temp(subplot_temp_1)

        sql_x_ot, sql_y_ot = extract_sql(sql_ot_1)
        subplot_temp_1.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at_1)
        subplot_temp_1.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_1.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        lgd = subplot_temp_1.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')


        subplot_vent_1 = fig_3.add_subplot(1, 1, 1)
        prepare_plot_vent(subplot_vent_1)

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_1.plot(sql_x_vt, sql_y_vt, color="b")

        fig_2.canvas.draw_idle()
        fig_3.canvas.draw_idle()

        self.ids.label_resume.text = "Resume Room 2: "
        self.ids.label_hot.text = str(round(gl_pct_hot_1,2)) +" %: too Hot"
        # self.ids.label_cold.text = str(round(gl_pct_cold_1, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot_1) +" h: too Hot"
        # self.ids.label_cold_hours.text = str(gl_total_h_cold_1) +" h: too Cold"

        self.ids.label_results_1.text = " "


class Screen6(Screen):
    figureagg_temp = ObjectProperty()
    figureagg_ach = ObjectProperty()
    legend = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_results(self):
        layout = self.ids.resultlayout
        layout_1 = self.ids.percent_hot_layout

        if sql_ot_2 is None:
            PeriodErrorPopup.error_warning = "No simulation for Room 3 was found. Maybe your model only has one Room \nor no simulation at all was done. In this case run the simulation \nunder the simulation tab."
            PeriodErrorPopup().open()
            try:
                layout.remove_widget(self.figureagg_temp)
            except:
                pass
            try:
                layout.remove_widget(self.figureagg_ach)
            except:
                pass
            self.ids.label_resume.text = " "
            self.ids.label_hot.text = " "
            # self.ids.label_cold.text = " "
            self.ids.label_hot_hours.text = " "
            # self.ids.label_cold_hours.text = " "

            self.ids.label_results_2.text = " "
            return


        sql_x_ot, sql_y_ot = extract_sql(sql_ot_2)
        subplot_temp_2.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at_2)
        subplot_temp_2.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_2.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        if self.legend is False:
            lgd = subplot_temp_2.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')
            self.legend = True

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_2.plot(sql_x_vt, sql_y_vt, color="b")


        layout = self.ids.resultlayout
        layout_1 = self.ids.percent_hot_layout

        try:
            layout.remove_widget(self.figureagg_temp)
        except:
            pass
        try:
            layout.remove_widget(self.figureagg_ach)
        except:
            pass

        self.figureagg_temp = FigureCanvasKivyAgg(fig_4)
        self.figureagg_ach = FigureCanvasKivyAgg(fig_5)

        layout.add_widget(self.figureagg_temp)
        layout.add_widget(self.figureagg_ach)

        self.ids.label_resume.text = "Resume Room 3: "
        self.ids.label_hot.text = str(round(gl_pct_hot_2,2)) +" %: too Hot"
        # self.ids.label_cold.text = str(round(gl_pct_cold_2, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot_2) +" h: too Hot"
        # self.ids.label_cold_hours.text = str(gl_total_h_cold_2) +" h: too Cold"

        self.ids.label_results_2.text = " "


    def clear_anterior_graphs(self):
        layout = self.ids.resultlayout
        layout_1 = self.ids.percent_hot_layout
        if sql_ot_2 is None:
            PeriodErrorPopup.error_warning = "No simulation for Room 3 was found. Maybe your model only has one Room \nor no simulation at all was done. In this case run the simulation \nunder the simulation tab."
            PeriodErrorPopup().open()
            try:
                layout.remove_widget(self.figureagg_temp)
            except:
                pass
            try:
                layout.remove_widget(self.figureagg_ach)
            except:
                pass
            self.ids.label_resume.text = " "
            self.ids.label_hot.text = " "
            # self.ids.label_cold.text = " "
            self.ids.label_hot_hours.text = " "
            # self.ids.label_cold_hours.text = " "

            self.ids.label_results_2.text = " "
            return

        global subplot_temp_2
        global subplot_vent_2

        fig_4.clf()
        fig_5.clf()


        subplot_temp_2 = fig_4.add_subplot(1, 1, 1)
        prepare_plot_temp(subplot_temp_2)

        sql_x_ot, sql_y_ot = extract_sql(sql_ot_2)
        subplot_temp_2.plot(sql_x_ot, sql_y_ot, label="Indoor Operative Temp.", color="r")

        sql_x_at, sql_y_at = extract_sql(sql_at_2)
        subplot_temp_2.plot(sql_x_at, sql_y_at, label="Indoor Air Temp.", color="k")

        sql_x_ou, sql_y_ou = extract_sql(sql_ou)
        subplot_temp_2.plot(sql_x_ou, sql_y_ou, label="Outdoor Air Temp.", color="y")

        lgd = subplot_temp_2.legend(bbox_to_anchor=(0.9, 1.0), loc='upper left')


        subplot_vent_2 = fig_5.add_subplot(1, 1, 1)
        prepare_plot_vent(subplot_vent_2)

        if sql_vt is not None:
            sql_x_vt = sql_x_ot
            sql_y_vt = extract_sql_y(sql_vt)
            subplot_vent_2.plot(sql_x_vt, sql_y_vt, color="b")

        fig_4.canvas.draw_idle()
        fig_5.canvas.draw_idle()

        self.ids.label_resume.text = "Resume Room 3: "
        self.ids.label_hot.text = str(round(gl_pct_hot_2,2)) +" %: too Hot"
        # self.ids.label_cold.text = str(round(gl_pct_cold_2, 2)) +" %: too Cold"
        self.ids.label_hot_hours.text = str(gl_total_h_hot_2) +" h: too Hot"
        # self.ids.label_cold_hours.text = str(gl_total_h_cold_2) +" h: too Cold"

        self.ids.label_results_2.text = " "






class MyLayout(BoxLayout):

    #label_ang_text = ObjectProperty()

    dactivated_activated_color = ListProperty([])

    # epw popup related properties
    epw_path = StringProperty(" ")
    epw_popup = ObjectProperty(None)

    period_popup = ObjectProperty(PopupPeriod())



    constr_popup = PopupConstr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_red_color(self, y):
        self.ids[y].foreground_color = (1, 0, 0.2, 1)

    def set_black_color(self, text, y):
        self.ids[y].foreground_color = (0, 0, 0, 1)
        self.ids[y].text = str(float(text))

    def const_popup_open(self):

        const_popup = self.constr_popup
        const_popup.open()

    def aperture_set(self, way):
        global gl_frac_area
        global gl_frac_height
        global gl_is_operable
        if way == "Closed":
            # selected_hb.apertures[0].is_operable = False
            gl_is_operable = False
        else:
            # selected_hb.apertures[0].is_operable = True
            if way == "Hinged":
                gl_is_operable = True
                gl_frac_area = 1
                gl_frac_height = 1
            elif way == "Slided":
                gl_is_operable = True
                gl_frac_area = 0.5
                gl_frac_height = 1
            else: # tilted window
                gl_is_operable = True
                gl_frac_area = 0.2
                gl_frac_height = 0.5


    def set_point_set(self, value, typ, id_value):
        value = float(value)
        global gl_max_out_temp
        global gl_min_ind_temp
        if typ == "max_out":
            gl_max_out_temp = value
        else: #  typ == "min_ind"
            gl_min_ind_temp = value

        self.set_black_color(value, id_value)


    def period_setter(self, value):
        global gl_period_type
        gl_period_type = value



    def period_popup_open(self):
        self.period_popup.open()

    def epw_popup_open(self):
        self.epw_popup = PopupEpw(load=self.load_epw)
        self.epw_popup.open()

    def load_epw(self, selected):
        self.epw_popup.dismiss()
        path = str(selected[0])
        epw_path_update(path)
        
        if len(path) > 100:
            epw_path_laststr = "\\...\\  ..." + path[-85:]
        else:
            epw_path_laststr = path
        self.epw_path = epw_path_laststr



    def template_set(self, value):
        global gl_template
        gl_template = value
        # if gl_epw_file is None:
        #     PeriodErrorPopup.title = "Notification"
        #     PeriodErrorPopup.error_warning = "You are changing the template. Simulation will only be \nexecuted for the chosen/current template."
        #     PeriodErrorPopup().open()



    def spinner_clicked_ter(self, value):
        global gl_terrain
        print(value) #important to have this one to call "value" in cases where typ is not sm or em
        if value == "Seaside":
            value = "Ocean"
        gl_terrain = value

    def spinner_clicked(self, value, typ):
        if typ == "sm" or "em":
            self.day_count(value, typ)
        else: print(value) #important to have this one to call "value" in cases where typ is not sm or em
        run_var_update(value, typ)

    def day_count(self, value, typ):
        if typ == "sm":
            if value in self.month30:
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                if self.ids.spinnerSD.text == "31":
                    self.ids.spinnerSD.text = "30"
            elif value == "February":
                if self.ids.spinnerSD.text in self.febplusdays:
                    self.ids.spinnerSD.text = "28"
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
            else:
                self.ids.spinnerSD.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        if typ == "em":
            if value in self.month30:
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                if self.ids.spinnerED.text == "31":
                    self.ids.spinnerED.text = "30"
            elif value == "February":
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28"]
                if self.ids.spinnerED.text in self.febplusdays:
                    self.ids.spinnerED.text = "28"
            else:
                self.ids.spinnerED.values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

    def slide_timestep(self, *args):
        global gl_detailed
        if self.ids.detailslider.value == 0:
            self.detailtext.text = "low (usually sufficient)"
            gl_detailed = "low"
        elif self.ids.detailslider.value == 1:
            self.detailtext.text = "medium"
            gl_detailed = "medium"
        else:
            self.detailtext.text = "high"
            gl_detailed = "high"



    def reset_simulation_was_run(self):
        self.ids.simulationwasrun.text = " "
    def run_simulation(self):
        runit()




class Mainapp(App):
    def build(self):
        self.title = "VentConcept 1.0"
        self.icon = "ventconcept.png"
        return MyLayout()
    # def on_start(self, **kwargs):
    #     screen1 = self.root.ids.sclay.ids.screenm.get_screen('screen1')
    #     screen1.rectangle_create()





def epw_path_update(path):
    global gl_epw_file
    gl_epw_file = path

def run_var_update(variable, typ):
    global gl_startmonth
    global gl_startday 
    global gl_endmonth
    global gl_endday
    if typ == "sd":
        gl_startday = int(variable)
        if gl_startmonth is not None:
            startdate_update()
    elif typ == "sm":
        gl_startmonth = month_name_number(variable)
        if gl_startday is not None:
            startdate_update()
    elif typ == "ed":
        gl_endday = int(variable)
        if gl_endmonth is not None:
            enddate_update()
    elif typ == "em":
        gl_endmonth = month_name_number(variable)
        if gl_endday is not None:
            enddate_update()
    elif typ == "wd":
        start_weekday = variable
    else:
        pass

def startdate_update():
    global startdate
    startdate = Date(gl_startmonth, gl_startday)


def enddate_update():
    global enddate
    enddate = Date(gl_endmonth, gl_endday)


def month_name_number(month):
    month_name_lst = ["January", "February", "March", "April", "May","June", "July", "August", "September", "October", "November", "December"]
    for x, mo in enumerate(month_name_lst):
        if mo == month:
            mo = x + 1 
            return mo





def month_aligner(total_ind):
    months_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(len(months_day)):
        if total_ind < sum(months_day[0:i]):
            m = i if i != 0 else 12
            return m, total_ind - sum(months_day[0:i-1])+1


def face_wit_hole(min_face, max_face):
    max_face._holes = None
    max_face._holes = [min_face.vertices]
    new_face = max_face
    return new_face

def energy_plus_run(_model, directory, _sim_par_, _epw_file, sch_directory):
    # create the strings for simulation paramters and model
    ver_str = energyplus_idf_version() if energy_folders.energyplus_version \
        is not None else energyplus_idf_version(compatibe_ep_version)
    sim_par_str = _sim_par_.to_idf()
    model_str = _model.to.idf(_model, schedule_directory=sch_directory)
    idf_str = '\n\n'.join([ver_str, sim_par_str, model_str])


    # write the final string into an IDF
    idf = os.path.join(directory, 'in.idf')
    write_to_file_by_name(directory, 'in.idf', idf_str, True)

    # run the IDF through EnergyPlus
    silent = True if _run == 1 else False
    sql, zsz, rdd, html, err = run_idf(idf, gl_epw_file, silent=silent)
    return sql, zsz, rdd, html, err



def afn_run_os(_model, directory, _sim_par_, _epw_file, sch_directory):

    check_openstudio_version()

    _model = _model.duplicate()
    # remove colinear vertices using the Model tolerance to avoid E+ tolerance issues
    for room in _model.rooms:
        room.remove_colinear_vertices_envelope(_model.tolerance)
    # auto-assign stories if there are none since most OpenStudio measures need these
    if len(_model.stories) == 0:
        _model.assign_stories_by_floor_height()
    # scale the model if the units are not meters
    if _model.units != 'Meters':
        _model.convert_to_units('Meters')

    # # delete any existing files in the directory and prepare it for simulation
    # nukedir(directory, True)
    preparedir(directory)
    preparedir(sch_directory)

    # write the model parameter JSONs
    model_dict = _model.to_dict(triangulate_sub_faces=True)
    model_json = os.path.join(directory, '.hbjson')
    with open(model_json, 'w') as fp:
        json.dump(model_dict, fp)

    # write the simulation parameter JSONs
    sim_par_dict = _sim_par_.to_dict()
    sim_par_json = os.path.join(directory, 'simulation_parameter.json')
    with open(sim_par_json, 'w') as fp:
        json.dump(sim_par_dict, fp)

    # process any measures input to the component
    measures = None 

    # collect the two jsons for output and write out the osw file
    jsons = [model_json, sim_par_json]
    osw = to_openstudio_osw(
        directory, model_json, sim_par_json, additional_measures=measures,
        epw_file=_epw_file, schedule_directory=sch_directory)
    run_ = 3
    # run the measure to translate the model JSON to an openstudio measure
    silent = True if run_ == 3 else False
    # if run_ > 0 and not no_report_meas:  # everything must run with OS CLI
    #     osm, idf = run_osw(osw, measures_only=False, silent=silent)
    #     sql, zsz, rdd, html, err = output_energyplus_files(os.path.dirname(idf))
    if run_ > 0:  # no reporting measure; simulate separately from measure application
        osm, idf = run_osw(osw, silent=silent)
        # # process the additional strings
        # if add_str_ != [] and add_str_[0] is not None and idf is not None:
        #     add_str = '\n'.join(add_str_)
        #     with open(idf, "a") as idf_file:
        #         idf_file.write(add_str)
        if idf is None:  # measures failed to run correctly; parse out.osw
            print("error in Openstudiorun")
            log_osw = OSW(os.path.join(directory, 'out.osw'))
            for error, tb in zip(log_osw.errors, log_osw.error_tracebacks):
                if 'Cannot create a surface' in error:
                    error = 'Your Rhino Model units system is: {}\n'.format(error)
                print(tb)
                raise Exception(error)
        if run_ in (1, 3):  # run the resulting idf throught EnergyPlus
            sql, zsz, rdd, html, err = run_idf(idf, _epw_file, silent=silent)
            return sql, zsz, rdd, html, err



def lb_datetime_to_datetime(lb_datetime):
    new_datetime_list = []
    for time in lb_datetime:
        new_datetime = datetime(time.year, time.month, time.day, time.hour)
        new_datetime_list.append(new_datetime)
    return(new_datetime_list)



##if all_required_inputs(ghenv.Component) and _run:
def runit():
    # check the presence of energyplus and check that the version is compatible
    check_energyplus_version()

    if gl_epw_file is None:
        PeriodErrorPopup.error_warning = "No weather file was loaded. Load an EPW file first."
        PeriodErrorPopup().open()
        return

    if gl_template == "one_sided":
        room_list = [gl_room_0_on]
        # construction attribution is implemented already, but should be updated to new way, solution as cross-ventilation
        north = gl_north_0
    elif gl_template == "cross_ventilation":
        room_list = [gl_room_0, gl_room_1, gl_room_2] if gl_room_2 is not None and gl_room_1 is not None else [gl_room_0, gl_room_1] if gl_room_1 is not None and gl_room_2 is None else [gl_room_0]
    
        north = gl_north_1
    else: # gl_template == "chimney_ventilation"
        room_list = [gl_room_0_at, gl_room_1_at] if gl_room_1_at is not None else [gl_room_0]
        north = gl_north_2


    gl_room_construction_attributor(room_list) # assign construction to all rooms
    set_apertures_operable(room_list) # set apertures to operable if not set to closed
    room_list = ventilation_control(room_list) # assign type of opening (hinged, slided, tilt) to windows



    global gl_an_period

    if gl_period_type == "Costum Period":
        gl_an_period = AnalysisPeriod(gl_startmonth, gl_startday, 0, gl_endmonth, gl_endday, 23, 1)
        ana_per = gl_an_period
        runper = RunPeriod.from_analysis_period(ana_per)

    elif gl_period_type == "Hot Summer Day":

        epw_data = EPW(gl_epw_file)
        dry_bulb_temperature = epw_data.dry_bulb_temperature
        dry_bulb_day_dic = dry_bulb_temperature.group_by_day()

        all_year_day_vals = []
        for key in dry_bulb_day_dic:
            value = dry_bulb_day_dic[key]
            all_year_day_vals.append((sum(value)/len(value)) + (max(value)*2))

        max_temp_ind = all_year_day_vals.index(max(all_year_day_vals))

        aligned_date = month_aligner(max_temp_ind)
        aligned_date_plus = month_aligner(max_temp_ind+1)
        ddy_date = DateTime(aligned_date[0], aligned_date[1])
        ddy_date_1 = DateTime(aligned_date_plus[0], aligned_date_plus[1])
        ana_per = AnalysisPeriod(aligned_date[0], aligned_date[1], 0, aligned_date_plus[0], aligned_date_plus[1], 23, 1)
        runper = RunPeriod.from_analysis_period(ana_per)
    else: 
        ana_per = stat_file_solver(gl_period_type)
        runper = RunPeriod.from_analysis_period(ana_per)
        # if isinstance(runper, str):
        #     # this warning should not be linked here, it should directly check if epw was loaded or not!
        #     PeriodErrorPopup.error_warning = runper
        #     PeriodErrorPopup().open()

        #     return



    _model = Model('simulation', room_list, orphaned_shades=shades_,
           tolerance=tolerance, angle_tolerance=angle_tolerance)



    floor_area = _model.floor_area
    assert floor_area != 0, 'Connected _rooms have no floors with which to compute EUI.'
    #floor_area = floor_area * conversion_to_meters() ** 2
    # mults = [rm.multiplier for rm in sim_room_prop]
    # mults = None if all(mul == 1 for mul in mults) else mults

    # process the simulation folder name and the directory
    clean_name = re.sub(r'[^.A-Za-z0-9_-]', '_', _model.display_name)

    directory = os.path.join(result_directory, clean_name, 'eneryplus')



    # directory = os.path.join(folders.default_simulation_folder, _model.identifier)
    sch_directory = os.path.join(directory, 'schedules')
    nukedir(directory)  # delete any existing files in the directory


    _sim_par_ = SimulationParameter()
    _sim_par_.run_period = runper
    _sim_par_.terrain_type = gl_terrain


    _sim_par_.shadow_calculation.calculation_update_method = 'Periodic'
    _sim_par_.shadow_calculation.calculation_frequency = 30
    _sim_par_.shadow_calculation.maximum_figures = 15000
    _sim_par_.output.add_zone_energy_use()
    _sim_par_.output.reporting_frequency = 'Hourly'
    _sim_par_.output.add_comfort_metrics()
    _sim_par_.north_angle = north

    if gl_detailed == "low":
        _sim_par_.timestep = 4
        _sim_par_.shadow_calculation.calculation_method = 'PolygonClipping'
        _sim_par_.shadow_calculation.solar_distribution = 'FullExteriorWithReflections'
    elif gl_detailed == "medium":
        _sim_par_.timestep = 10
        _sim_par_.shadow_calculation.calculation_method = 'PolygonClipping'
        _sim_par_.shadow_calculation.solar_distribution = 'FullExteriorWithReflections'
    else:
        _sim_par_.timestep = 30
        _sim_par_.shadow_calculation.calculation_method = 'PixelCounting'
        _sim_par_.shadow_calculation.solar_distribution = 'FullInteriorAndExteriorWithReflections'



    # choose whether to use E+ or OS for the simulation, if OS is not found always E+ is used, but cross ventilation effects are not displayes as well as no Air Flow Networks can be considered
    # RECENT VERSION IS ONLY COMPATIBLE TO OPENSTUDIO NOT ENERGYPLUS (AS OTHERWISE POTENTIALLY CONFUSING)
    tryout = False
    if check_openstudio_return() is True : # Openstudio is installed and found on the pc
        if tryout is True: # gl_template == "one_sided": # no afn calculation
            _sim_par_.output.add_output("Zone Ventilation Air Change Rate")
            _sim_par_.output.add_output("Zone Infiltration Air Change Rate")
            _sim_par_.output.add_output("Zone Mechanical Ventilation Air Changes per Hour")
        else:
            _sim_par_.output.add_output("AFN Zone Infiltration Volume")
            _sim_par_.output.add_output("AFN Zone Infiltration Air Change Rate")
            _sim_par_.output.add_output("AFN Zone Mixing Volume")
            _model = set_afn_params(_model) # CREATE AFN MODEL -- ONLY IF OPENSTUDIO IS INSTALLED 

        sql, zsz, rdd, html, err = afn_run_os(_model, directory, _sim_par_, gl_epw_file, sch_directory)

    else:
        PeriodErrorPopup.title = "Warning"
        PeriodErrorPopup.error_warning = "No compatible Openstudio version was found on the PC. \nInstall Openstudio version 3.2.0 or higher, or the \nOpenstudio app version 1.2.0 or higher. "
        PeriodErrorPopup().open()
        return        

    """
    else: # Openstudio was not found on the pc
        if check_energyplus_return() is False:
            PeriodErrorPopup.title = "Warning"
            PeriodErrorPopup.error_warning = "No compatible Openstudio or EnergyPlus version \n was found on the PC. \nInstall Openstudio version 3.2.0 or higher, or the \nOpenstudio app version 1.2.0 or higher. \nElsewise you can install a new version of EnergyPlus, also Openstudio is recommended. \n As Simulations without Openstudio might not be as \nprecise in Crossventilation and \nChimney Ventilation mode. Wind and buoyancy effects \nare better taken into account with Openstudio. \n(Air Flow Network method)"
            PeriodErrorPopup().open()
            return
        else:
            if gl_template != "one_sided":
                PeriodErrorPopup.title = "Warning"         
                PeriodErrorPopup.error_warning = "Openstudio should be used for cross-ventilation or \nchimney effect ventilation cases to consider more accurate air flows. \n(Air Flow Network -AFN- method) \nBut no Openstudio version was found on the Pc, so the less \naccurate standard EnergyPlus simulation method is used."
                PeriodErrorPopup().open()
                # directory = os.path.join(folders.default_simulation_folder, _model.identifier)
                directory = os.path.join(result_directory, _model.identifier)
                sch_directory = os.path.join(directory, 'schedules')
                #nukedir(directory)  # delete any existing files in the directory
            _sim_par_.output.add_output("Zone Ventilation Air Change Rate")
            _sim_par_.output.add_output("Zone Infiltration Air Change Rate")
            _sim_par_.output.add_output("Zone Mechanical Ventilation Air Changes per Hour")
            print(_model, type(_model), "the type of the model haha")
            print(_model, type(sch_directory), "the type of the schedule haha")
            sql, zsz, rdd, html, err = energy_plus_run(_model, directory, _sim_par_, gl_epw_file, sch_directory)
    """


    if html is None and err is not None:  # something went wrong; parse the errors
        err_obj = Err(err)
        print(err_obj.file_contents)
        for error in err_obj.fatal_errors:
            raise Exception(error)

    # parse the result sql and get the monthly data collections
    if os.name == 'nt':  # we are on windows; use IronPython like usual
        sql_obj = SQLiteResult(sql)
        cool_init = sql_obj.data_collections_by_output_name(cool_out)
        heat_init = sql_obj.data_collections_by_output_name(heat_out)
        # light_init = sql_obj.data_collections_by_output_name(light_out)
        # elec_equip_init = sql_obj.data_collections_by_output_name(el_equip_out)
        # gas_equip_init = sql_obj.data_collections_by_output_name(gas_equip_out)
        # shw_init = sql_obj.data_collections_by_output_name(shw_out)

        # adding comfort metrics!
        oper_temp = sql_obj.data_collections_by_output_name(oper_temp_output)
        air_temp = sql_obj.data_collections_by_output_name(air_temp_output)
        rad_temp = sql_obj.data_collections_by_output_name(rad_temp_output)
        rel_humidity = sql_obj.data_collections_by_output_name(rel_humidity_output)

        # experimental
        flow_rate = sql_obj.data_collections_by_output_name("Zone Ventilation Air Change Rate")
        inf_rate = sql_obj.data_collections_by_output_name("Zone Infiltration Air Change Rate")

        # afn_volume = sql_obj.data_collections_by_output_name("AFN Zone Infiltration Volume")
        afn_inf_rate = sql_obj.data_collections_by_output_name("AFN Zone Infiltration Air Change Rate")
        # mech_flow_rate = sql_obj.data_collections_by_output_name("AFN Zone Mixing Volume")



        total_rate = flow_rate + inf_rate + afn_inf_rate


        global sql_ot
        global sql_at
        global sql_ou
        global sql_dc

        global sql_ot_1
        global sql_at_1
        global sql_ou_1
        global sql_dc_1

        global sql_ot_2
        global sql_at_2
        global sql_ou_2
        global sql_dc_2

        global sql_vt


        global gl_pct_hot
        global gl_pct_cold
        global gl_total_h_hot
        global gl_total_h_cold
        global gl_pct_hot_1
        global gl_pct_cold_1
        global gl_total_h_hot_1
        global gl_total_h_cold_1
        global gl_pct_hot_2
        global gl_pct_cold_2
        global gl_total_h_hot_2
        global gl_total_h_cold_2


        epw_data = EPW(gl_epw_file)
        dry_bulb_temperature = epw_data.dry_bulb_temperature
        dry_bulb_temperature_fil = dry_bulb_temperature.filter_by_analysis_period(ana_per)

        sql_ou = dry_bulb_temperature_fil


        sql_ot = oper_temp[0]
        sql_at = air_temp[0]
        dc_temp, comf_obj = adaptive_comfort(dry_bulb_temperature, air_temp[0], rad_temp[0])

        gl_total_h_hot = comf_obj.total_h_hot
        gl_total_h_cold = comf_obj.total_h_cold
        gl_pct_hot = comf_obj.percent_hot
        gl_pct_cold = comf_obj.percent_cold
        gl_pct_neutral = comf_obj.percent_neutral

        if len(total_rate) > 0:
            sql_vt = total_rate[0]
        else:
            sql_vt = None

        # print(sql_vt, "ventilation values", sql_vt.values, sql_vt.header, sql_vt.header.metadata)
        if len(oper_temp) > 1:
            sql_ot_1 = oper_temp[1]
            sql_at_1 = air_temp[1]
            dc_temp_1, comf_obj_1 = adaptive_comfort(dry_bulb_temperature, air_temp[1], rad_temp[1])

            gl_total_h_hot_1 = comf_obj_1.total_h_hot
            gl_total_h_cold_1 = comf_obj_1.total_h_cold
            gl_pct_hot_1 = comf_obj_1.percent_hot
            gl_pct_cold_1 = comf_obj_1.percent_cold
            gl_pct_neutral_1 = comf_obj_1.percent_neutral

            v0 = room_list[0].geometry.volume
            v1 = room_list[1].geometry.volume

            sql_vt_0_n = total_rate[0]*v0
            sql_vt_1_n = total_rate[1]*v1
            sql_vt = (sql_vt_0_n + sql_vt_1_n) / (v0+v1)

        else:
            sql_ot_1 = None
            sql_at_1 = None
            comf_obj_1 = None

            gl_total_h_hot_1 = None
            gl_total_h_cold_1 = None
            gl_pct_hot_1 = None
            gl_pct_cold_1 = None
            gl_pct_neutral_1 = None


        if len(oper_temp) > 2:
            sql_ot_2 = oper_temp[2]
            sql_at_2 = air_temp[2]
            dc_temp_2, comf_obj_2 = adaptive_comfort(dry_bulb_temperature, air_temp[2], rad_temp[2])

            gl_total_h_hot_2 = comf_obj_2.total_h_hot
            gl_total_h_cold_2 = comf_obj_2.total_h_cold
            gl_pct_hot_2 = comf_obj_2.percent_hot
            gl_pct_cold_2 = comf_obj_2.percent_cold
            gl_pct_neutral_2 = comf_obj_2.percent_neutral


            v0 = room_list[0].geometry.volume
            v1 = room_list[1].geometry.volume
            v2 = room_list[2].geometry.volume

            sql_vt_0_n = total_rate[0]*v0
            sql_vt_1_n = total_rate[1]*v1
            sql_vt_2_n = total_rate[2]*v2
            sql_vt = (sql_vt_0_n + sql_vt_1_n + sql_vt_2_n) / (v0+v1+v2)

        else:
            sql_ot_2 = None
            sql_at_2 = None
            comf_obj_2 = None

            gl_total_h_hot_2 = None
            gl_total_h_cold_2 = None
            gl_pct_hot_2 = None
            gl_pct_cold_2 = None
            gl_pct_neutral_2 = None


        prepare_plot_temp(subplot_temp_0)
        prepare_plot_vent(subplot_vent_0)
        prepare_plot_temp(subplot_temp_1)
        prepare_plot_vent(subplot_vent_1)
        prepare_plot_temp(subplot_temp_2)
        prepare_plot_vent(subplot_vent_2)





        warntext = "! New Simulation was run, load the results !"

        scr4 = App.get_running_app().root.ids.sclay_2.ids.screenm_2.get_screen('screen4').ids.label_results_0
        scr4.text = warntext

        scr5 = App.get_running_app().root.ids.sclay_2.ids.screenm_2.get_screen('screen5').ids.label_results_1
        scr5.text = warntext

        scr6 = App.get_running_app().root.ids.sclay_2.ids.screenm_2.get_screen('screen6').ids.label_results_2
        scr6.text = warntext

        App.get_running_app().root.ids.simulationwasrun.text = "Simulation has finished - \ngo to the Results tab."



    # must still be changed for mac (new output strings)
    else:  # we are on Mac; sqlite3 module doesn't work in Mac IronPython
        # Execute the honybee CLI to obtain the results via CPython
        cmds = [folders.python_exe_path, '-m', 'honeybee_energy', 'result',
                'data-by-outputs', sql]
        for outp in energy_output:
            cmds.append('["{}"]'.format(outp))
        process = subprocess.Popen(cmds, stdout=subprocess.PIPE)
        stdout = process.communicate()
        data_coll_dicts = json.loads(stdout[0])
        cool_init = serialize_data(data_coll_dicts[0])
        heat_init = serialize_data(data_coll_dicts[1])
        light_init = serialize_data(data_coll_dicts[2])
        elec_equip_init = serialize_data(data_coll_dicts[3])
        gas_equip_init = serialize_data(data_coll_dicts[4])
        shw_init = serialize_data(data_coll_dicts[5])




if __name__ == "__main__":
    Mainapp().run()






