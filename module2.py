#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      astro
#
# Created:     25/06/2021
# Copyright:   (c) astro 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
#from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from gear_calc import createGearOutline
from gear_to_xml import g_to_xml, synfigFormat
import sys

# fileName = 'Intento-format-03-T.sif'
# tree = ET.parse(fileName)
# root = tree.getroot()
#
# folder = 'Gear'
# da = createGearOutline(.15, 20, 20, 5)
# aa = g_to_xml(da, folder, 'shaft')
# root.append(aa)
# root = synfigFormat(root)
# tree.write('Intento-format-03-T.sif')


i_file = open('Format', 'r')
fileName = i_file.name
i_file.close()

i_target = open('','w')
