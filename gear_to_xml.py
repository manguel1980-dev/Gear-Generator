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
# -------------------------------------------------------------------------------
#
# Reelases:
# 0.1: First Release
# ______________________________________________________________________________________

"""Generate xml format for gear data"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
from random import seed, random
# from gear_calc import createGearOutline

# axes position in vectors
x = 0
y = 1
# ----------------------

def synfigFormat(xmlR):
    """Return a xml format as required in synfig for the Element"""
    rough_string = ET.tostring(xmlR, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def guidGenerator(id):
    """generate id for guid"""
    randId = str(random())
    guidNumber = 'A' + randId[2:]
    L = len(guidNumber)

    for j in range(31 - L - len(str(id))):
        guidNumber += '0'
    guidNumber += 'A' + str(id)
    return guidNumber


def xml_support(canvasG, gearData, layer_desc='Gear Outline', rLocation=0):
    """"xml support"""

    layer = ET.SubElement(canvasG, 'layer', {'type' : 'outline',
                                            'active' : 'true',
                                            'exclude_from_rendering' : 'false',
                                            'version' : '0.3',
                                            'desc' : layer_desc})
    paramSub = ET.SubElement(layer,'param', {'name' : 'z_depth'})
    ET.SubElement(paramSub,'real', {'value' : '0.0000000000'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'amount'})
    ET.SubElement(paramSub, 'real', {'value': '1.0000000000'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'blend_method'})
    ET.SubElement(paramSub, 'integer', {'value' : '0'})
    paramSub = ET.SubElement(layer, 'param', {'name': 'color'})
    color = ET.SubElement(paramSub, 'color')
    r = ET.SubElement(color, 'r')
    r.text = '0.223529'
    g = ET.SubElement(color, 'g')
    g.text = '0.129412'
    b = ET.SubElement(color, 'b')
    b.text = '0.180392'
    a = ET.SubElement(color, 'a')
    a.text = '1.000000'
    paramSub = ET.SubElement(layer,'param', {'name' : 'origin'})
    vector = ET.SubElement(paramSub, 'vector')
    xx = ET.SubElement(vector,'x')
    xx.text = '0.0000000000'
    yy = ET.SubElement(vector,'y')
    yy.text = '0.0000000000'
    paramSub = ET.SubElement(layer,'param', {'name' : 'invert'})
    ET.SubElement(paramSub, 'bool', {'value' : 'false'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'antialias'})
    ET.SubElement(paramSub, 'bool', {'value' : 'true'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'feather'})
    ET.SubElement(paramSub, 'real', {'value' : '0.0000000000'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'blurtype'})
    ET.SubElement(paramSub, 'integer', {'value' : '1'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'winding_style'})
    ET.SubElement(paramSub, 'integer', {'value' : '0'})

    # filling spline
    paramSub = ET.SubElement(layer,'param', {'name' : 'bline'})
    bline = ET.SubElement(paramSub,'bline', {'type' : 'bline_point', 'loop' : 'true'})
    if rLocation == 0:
        for i in range(len(gearData)):
            if isinstance(gearData[i], list):
                guid = guidGenerator(i)
                entry = ET.SubElement(bline, 'entry')
                compositeSub = ET.SubElement(entry, 'composite', {'guid' : guid, 'type' : 'bline_point'})
                point = ET.SubElement(compositeSub, 'point')
                vectorSub = ET.SubElement(point, 'vector')
                xxSub = ET.SubElement(vectorSub, 'x')
                xxSub.text = str(gearData[i][x])
                yySub = ET.SubElement(vectorSub, 'y')
                yySub.text = str(gearData[i][y])
                width = ET.SubElement(compositeSub, 'width')
                ET.SubElement(width,'real', {'value' : '1.0000000000'})
                origin = ET.SubElement(compositeSub, 'origin')
                ET.SubElement(origin,'real', {'value' : '0.5000000000'})
                split = ET.SubElement(compositeSub, 'split')
                ET.SubElement(split,'bool', {'value' : 'false'})
                t1 = ET.SubElement(compositeSub, 't1')
                radial_composite = ET.SubElement(t1, 'radial_composite', {'type' : 'vector'})
                radius = ET.SubElement(radial_composite, 'radius')
                ET.SubElement(radius, 'real', {'value' : '0.0000000000'})
                theta = ET.SubElement(radial_composite, 'theta')
                ET.SubElement(theta, 'angle', {'value' : '0.000000'})
                t2 = ET.SubElement(compositeSub, 't2')
                radial_composite = ET.SubElement(t2, 'radial_composite', {'type' : 'vector'})
                radius = ET.SubElement(radial_composite, 'radius')
                ET.SubElement(radius, 'real', {'value' : '0.0000000000'})
                theta = ET.SubElement(radial_composite, 'theta')
                ET.SubElement(theta, 'angle', {'value' : '0.000000'})
                split_radius = ET.SubElement(compositeSub, 'split_radius')
                ET.SubElement(split_radius, 'bool', {'value' : 'true'})
                split_angle = ET.SubElement(compositeSub, 'split_angle')
                ET.SubElement(split_angle, 'bool', {'value' : 'true'})
            elif gearData[i] == 'A':
                pass
    else:
        for i in range(len(gearData)):
            if isinstance(gearData[i], list):
                guid = guidGenerator(rLocation + 2 + i)
                entry = ET.SubElement(bline, 'entry')
                compositeSub02 = ET.SubElement(entry, 'composite', {'guid': guid, 'type': 'bline_point'})
                point = ET.SubElement(compositeSub02, 'point')
                vectorSub02 = ET.SubElement(point, 'vector')
                xxSub02 = ET.SubElement(vectorSub02, 'x')
                xxSub02.text = str(gearData[i][0])
                yySub02 = ET.SubElement(vectorSub02, 'y')
                yySub02.text = str(gearData[i][1])
                width = ET.SubElement(compositeSub02, 'width')
                ET.SubElement(width, 'real', {'value': '1.0000000000'})
                origin = ET.SubElement(compositeSub02, 'origin')
                ET.SubElement(origin, 'real', {'value': '0.5000000000'})
                split = ET.SubElement(compositeSub02, 'split')
                ET.SubElement(split, 'bool', {'value': 'false'})
                t1 = ET.SubElement(compositeSub02, 't1')
                radial_composite = ET.SubElement(t1, 'radial_composite', {'type': 'vector'})
                radius = ET.SubElement(radial_composite, 'radius')
                ET.SubElement(radius, 'real', {'value': str(gearData[i][2])})
                theta = ET.SubElement(radial_composite, 'theta')
                ET.SubElement(theta, 'angle', {'value': str(gearData[i][3])})
                t2 = ET.SubElement(compositeSub02, 't2')
                radial_composite = ET.SubElement(t2, 'radial_composite', {'type': 'vector'})
                radius = ET.SubElement(radial_composite, 'radius')
                ET.SubElement(radius, 'real', {'value': str(gearData[i][2])})
                theta = ET.SubElement(radial_composite, 'theta')
                ET.SubElement(theta, 'angle', {'value': str(gearData[i][3])})
                split_radius = ET.SubElement(compositeSub02, 'split_radius')
                ET.SubElement(split_radius, 'bool', {'value': 'true'})
                split_angle = ET.SubElement(compositeSub02, 'split_angle')
                ET.SubElement(split_angle, 'bool', {'value': 'true'})

    paramSub = ET.SubElement(layer,'param', {'name' : 'width'})
    ET.SubElement(paramSub, 'real', {'value' : '0.0472440959'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'expand'})
    ET.SubElement(paramSub, 'real', {'value' : '0.0000000000'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'sharp_cusps'})
    ET.SubElement(paramSub, 'bool', {'value' : 'true'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'round_tip[0]'})
    ET.SubElement(paramSub, 'bool', {'value' : 'true'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'round_tip[1]'})
    ET.SubElement(paramSub, 'bool', {'value' : 'true'})
    paramSub = ET.SubElement(layer,'param', {'name' : 'homogeneous_width'})
    ET.SubElement(paramSub, 'bool', {'value' : 'true'})

    # xmlsupport = synfigFormat(layer)
    return layer




def g_to_xml(gearData, group_name, shaft_or_outline=None):
    """function to create xml format for gear data"""
    rLoc = gearData.index('R')
    canvasG = ET.Element('canvas')
    layerG = ET.SubElement(canvasG, 'layer', {'type' : 'group',
                                            'active' : 'true',
                                            'exclude_from_rendering' : 'false',
                                            'version' : '0.3',
                                            'desc' : group_name})

    param = ET.SubElement(layerG, 'param', {'name' : 'z_depth'})
    ET.SubElement(param,'real', {'value' : '0.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'amount'})
    ET.SubElement(param, 'real', {'value': '1.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'blend_method'})
    ET.SubElement(param, 'integer', {'value' : '0', 'static' : 'true'})
    param = ET.SubElement(layerG,'param', {'name' : 'origin'})
    vector = ET.SubElement(param, 'vector')
    xx = ET.SubElement(vector,'x')
    xx.text = '0.0000000000'
    yy = ET.SubElement(vector,'y')
    yy.text = '0.0000000000'

    param = ET.SubElement(layerG,'param', {'name' : 'transformation'})
    composite = ET.SubElement(param, 'composite', {'type' : 'transformation'})
    offset = ET.SubElement(composite, 'offset')
    vector = ET.SubElement(offset, 'vector')
    xx = ET.SubElement(vector,'x')
    xx.text = '0.0000000000'
    yy = ET.SubElement(vector,'y')
    yy.text = '0.0000000000'
    angle = ET.SubElement(composite, 'angle')
    ET.SubElement(angle, 'angle', {'value': '0.000000'})
    skew_angle = ET.SubElement(composite, 'skew_angle')
    ET.SubElement(skew_angle, 'angle', {'value': '0.000000'})
    scale = ET.SubElement(composite, 'scale')
    vector = ET.SubElement(scale, 'vector')
    xx = ET.SubElement(vector,'x')
    xx.text = '1.0000000000'
    yy = ET.SubElement(vector,'y')
    yy.text = '1.0000000000'

    param = ET.SubElement(layerG,'param', {'name' : 'canvas'})
    canvas = ET.SubElement(param,'canvas')

    xml_support(canvas, gearData[:rLoc])
    if shaft_or_outline != None and gearData[rLoc + 1] != 0:
        xml_support(canvas, gearData[rLoc:], shaft_or_outline, rLoc)

    param = ET.SubElement(layerG,'param', {'name' : 'time_dilation'})
    ET.SubElement(param,'real', {'value' : '1.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'time_offset'})
    ET.SubElement(param,'time', {'value' : '0s'})
    param = ET.SubElement(layerG,'param', {'name' : 'children_lock'})
    ET.SubElement(param,'bool', {'value' : 'false'})
    param = ET.SubElement(layerG,'param', {'name' : 'outline_grow'})
    ET.SubElement(param,'real', {'value' : '0.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'z_range'})
    ET.SubElement(param,'bool', {'value' : 'false', 'static' : 'true'})
    param = ET.SubElement(layerG,'param', {'name' : 'z_range_position'})
    ET.SubElement(param,'real', {'value' : '0.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'z_range_depth'})
    ET.SubElement(param,'real', {'value' : '0.0000000000'})
    param = ET.SubElement(layerG,'param', {'name' : 'z_range_blur'})
    ET.SubElement(param,'real', {'value' : '0.0000000000'})

    xml_gear = synfigFormat(layerG)
    return layerG



# -----------------------Pueba-------------------------------------

# folder = 'Gear'
#
# # da = ['M',[1.02,-.03], [3.004, 8.08], 'M', 2, -8, 0, [-7.25,.002],[1,1]]
# da = createGearOutline(.15, 40, 20, 12)
# aa = g_to_xml(da, folder, 'shaft')
# print(aa)



# -----------------------Pueba-------------------------------------