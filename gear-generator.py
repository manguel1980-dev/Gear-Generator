#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:         Gear Generator
# Purpose:      Just for fun
#
# Author:       Manuel Astros
# Email:        manuel.astros1980@gmail.com
# Web:          https://sites.google.com/view/interpolation/home
#
# Created:     25/06/2021
# Copyright:   (c) astros 2021
# Licence:     MIT
# Based on:    Gear Drawing with Bézier Curves (https://www.arc.id.au/GearDrawing.html)
#-------------------------------------------------------------------------------
#
# Reelases:
# 0.1: First Release
#______________________________________________________________________________________

import os
import sys
import xml.etree.ElementTree as ET
from gear_calc import createGearOutline, createIntGearOutline
from gear_to_xml import g_to_xml, synfigFormat
#import tkinter as tk

def read_filename(f_name):
    # Read input file
    i_file = open(f_name, 'r')
    fileName = i_file.name
    i_file.close()
    return fileName


def gear_generator(format_g):
    address = format_g.find("./param/canvas/layer[@desc='Internal']/param/canvas/layer/param/[@name='text']/string")
    internal = address.text

    address = format_g.find("./param/canvas/layer[@desc='Pitch Diameter']/param/canvas/layer/param/[@name='text']/string")
    pitch_diameter_mm = float(address.text)
    pitch_diameter_unit = pitch_diameter_mm/(127/6)

    address = format_g.find("./param/canvas/layer[@desc='Teeth Number']/param/canvas/layer/param/[@name='text']/string")
    teeth_number= int(address.text)

    address = format_g.find("./param/canvas/layer[@desc='Pressure Angle']/param/canvas/layer/param/[@name='text']/string")
    pressure_angle = float(address.text)

    address = format_g.find("./param/canvas/layer[@desc='Diameter']/param/canvas/layer/param/[@name='text']/string")
    diameter_mm = float(address.text)
    radius_mm = diameter_mm/2
    radius_unit = radius_mm/(127/6)

    module = pitch_diameter_unit/teeth_number

    if internal == 'yes':
        gear_calc = createIntGearOutline(module, teeth_number, pressure_angle, radius_unit)
        radius_type = 'Outline Rim'
    elif internal == 'no' or internal == None:
        gear_calc = createGearOutline(module, teeth_number, pressure_angle, radius_unit)
        radius_type = 'Shaft'
    group_name = 'Gear'
    gear_xml = g_to_xml(gear_calc, group_name, radius_type)

    return gear_xml



def process(f_name):
    # Read input file
    fileName = read_filename(f_name)
    #    fileName = 'Intento-format-03-T.sif'
    tree = ET.parse(fileName)
    root = tree.getroot()
    formatG = root.find("layer[@desc='Gear Format']")
    format_path = os.path.join(os.path.dirname(sys.argv[0]), 'Format')

    if os.path.isfile('Gear'):
        format_tree = ET.parse('Gear')
        addToFile = format_tree.getroot()
        os.remove('Gear')
    elif formatG == None:
        format_tree = ET.parse(format_path)
        addToFile = format_tree.getroot()
    else:
        root.remove(formatG)
        addToFile = gear_generator(formatG)

    root.append(addToFile)
    root = synfigFormat(root)
    tree.write(fileName)


if len(sys.argv) < 2:
    sys.exit()
else:
    process(sys.argv[1])
