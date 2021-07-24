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

from math import cos, sin, tan, pi, radians, atan, asin, acos, sqrt, pow

# axes position in vectors:
x = 0
y = 1
# ----------------------

"""   * involuteBezCoeff
   *
   * Calculation of Bezier coefficients for
   * Higuchi et al. approximation to an involute.
   * ref: YNU Digital Eng Lab Memorandum 05-1
   *
   * Parameters:
   * module - sets the size of teeth (see gear design texts)
   * numTeeth - number of teeth on the gear
   * pressure angle - angle in degrees, usually 14.5 or 20
   * order - the order of the Bezier curve to be fitted [3, 4, 5, ..]
   * fstart - fraction of distance along tooth profile to start
   * fstop - fraction of distance along profile to stop"""


def involuteBezCoeff(module, numTeeh, pressAngle=20, order = 3, fstart=0.01, fstop=1):
    # pitch circle radius
    Rpitch = module*numTeeh/2
    # pressure angle. By default = 20°
    phi = pressAngle
    # base circle radius
    Rb = Rpitch*cos(radians(phi))
    # addendum radius (outer radius)
    Ra = Rpitch + module
    # order of Bezier approximation. By default = 3
    p = order
    # involute angle at addendum
    ta = sqrt(pow(Ra,2)-pow(Rb,2))/Rb
    # By default = 0.01
    start = fstart
    # By default = 1
    stop = fstop
    bzCoeffs = []

    def chebyExpnCoeffs(j, func):
        # any suitable number much larger than  (N>>p)
        N = 50
        c = 0
        cc = 0
        for k in range(1, N+1):
            cc = func(cos(pi*(k-0.5)/N)) * cos(pi*j*(k-0.5)/N)
            c += cc
        return 2*c/N

    def chebyPolyCoeff(p, func):
        coeffs = [0 for i in range(p+1)]
        fnCoeff = [0 for i in range(p+1)]
        T = [[0 for j in range(p + 1)] for i in range(2)]
        T[0][0] = 1
        T[1][1] = 1
        # now generate the Chebyshev polynomial coefficient using
        # formula T(k+1) = 2xT(k) - T(k-1) which yields
        # T = [ [ 1,  0,  0,  0,  0,  0],    // T0(x) =  +1
        #       [ 0,  1,  0,  0,  0,  0],    // T1(x) =   0  +x
        #       [-1,  0,  2,  0,  0,  0],    // T2(x) =  -1  0  +2xx
        #       [ 0, -3,  0,  4,  0,  0],    // T3(x) =   0 -3x    0   +4xxx
        #       [ 1,  0, -8,  0,  8,  0],    // T4(x) =  +1  0  -8xx       0  +8xxxx
        #       [ 0,  5,  0,-20,  0, 16]],    // T5(x) =   0  5x    0  -20xxx       0  +16xxxxx
        for k in range(1, p+1):
            T.append([0, 0, 0, 0])
            for j in range(len(T[k])-1):
                T[k+1][j+1] = 2*T[k][j]
            for j in range(len(T[k-1])):
                T[k+1][j] -= T[k-1][j]

        # convert the chebyshev function series into a simple polynomial
        # and collect like terms, out T polynomial coefficients
        for k in range(p+1):
            fnCoeff[k] = chebyExpnCoeffs(k, func)
            coeffs[k] = 0
        for k in range(p+1):
            # loop thru powers of x
            for pwr in range(p+1):
                coeffs[pwr] += fnCoeff[k]*T[k][pwr]
        # fix the 0th coeff
        coeffs[0] -= chebyExpnCoeffs(0, func)/2
        return coeffs

    # Equation of involute using the Bezier parameter t as variable
    def involuteXbez(t):
        # map t (0 <= t <= 1) onto x (where -1 <= x <= 1)
        x = t*2-1
        # map theta (where ts <= theta <= te) from x (-1 <=x <= 1)
        theta = x*(te-ts)/2 + (ts + te)/2
        return Rb*(cos(theta)+theta*sin(theta))

    def involuteYbez(t):
        # map t (0 <= t <= 1) onto x (where -1 <= x <= 1)
        x = t*2-1
        # map theta (where ts <= theta <= te) from x (-1 <=x <= 1)
        theta = x*(te-ts)/2 + (ts + te)/2
        return Rb*(sin(theta)-theta*cos(theta))

    def binom(n, k):
        coeff = 1
        for i in range(n-k+1, n+1):
            coeff *= i
        for i in range(1, k+1):
            coeff /= i
        return coeff

    def bezCoeff(i, func):
        # generate the polynomial coeffs in one go
        bc = 0
        polyCoeffs = chebyPolyCoeff(p, func)
        for j in range(i+1):
            bc += binom(i, j)*polyCoeffs[j]/binom(p, j)
        return bc

    if(fstart < stop):
        start = fstart

    # involute angle, theta, at end of approx
    te = sqrt(stop)*ta
    # involute angle, theta, at start of approx
    ts = sqrt(start)*ta
    # calc Bezier coeffs
    for i in range(p+1):
        bcoeff = [0,0]
        bcoeff[x] = bezCoeff(i, involuteXbez)
        bcoeff[y] = bezCoeff(i, involuteYbez)
        bzCoeffs.append(bcoeff)
    return bzCoeffs



#--------------------------
#
# Support Functions
#
#---------------------------

# Rotate pt {x: , y: } by rads radians about origin
#---------------------------------------------------
def rotate(pt, rads):
    sinA = sin(rads)
    cosA = cos(rads)
    return([pt[x]*cosA - pt[y]*sinA,
            pt[x]*sinA + pt[y]*cosA])


# Convert polar coords to cartesian
#------------------------------------------
def toCartesian(radius, angle):
    return([radius*cos(angle),
            radius*sin(angle)])


# Generate invoulte angle as a function of  radius R
# Rb: base circle radius
#-------------------------------------------
def getInvolutePolar(Rb, R):
    return ((sqrt(pow(R,2) - pow(Rb,2))/Rb)-acos(Rb/R))


# Displace pt {x: , y: } by X or Y disrtance about origin
#---------------------------------------------------
def displace(pt, distX, distY):
    return[pt[x]+ distX, pt[y]+distY]


"""
genGearToothData
Creates an array of drawing commands and their coordinates
to draw a single spur gear tooth based on a circle
involute using the metric gear standards. Pseudo SVG path
data array is returned. Each coord is an object {x: , y: }
suitable for rotation by later processing if required.
m : module in milimeter
z: number of tooth adimensional
phi: pressure angle in degrees
"""
def genGearToothData(m, z, phi=20):
    addendum = m
    dedendum = 1.25*m
    toothHeight = dedendum - addendum
    # Rpitch : pitch circle radius
    Rpitch = z*m/2
    # Rb: involute base circle radius. By default 20°
    Rb = Rpitch*cos(radians(phi))
    # Ra: Addendum circle radius
    Ra = Rpitch + addendum
    # Rr: Root circle radius
    Rr = Rpitch - dedendum
    # Fillet radius
    fRad = 1.5*toothHeight
    # Pitch angle along circule gear
    pitchAngle = 2*pi/z
    baseToPitchAngle = getInvolutePolar(Rb, Rpitch)
    # inicializa pitchToFilletAngle
    pitchToFilletAngle = baseToPitchAngle
    filletAngle = atan(fRad/(fRad+Rr))
    # Radius at top of fillet
    Rf = sqrt(pow((Rr+fRad),2)-pow(fRad,2))
    if(Rb < Rf):
        Rf = Rr + toothHeight
    if(Rf > Rb):
        pitchToFilletAngle -= getInvolutePolar(Rb, Rf)

    # Generate Higuchi involute approximation------
    # Fraction of profile length at end of approx
    fe = 1
    # Fraction of length offset from base to avoid singularity
    fs = 0.01
    if(Rf > Rb):
        #offset start to top of fillet
        fs = (pow(Rf,2)-pow(Rb,2))/(pow(Ra,2)-pow(Rb,2))

    # Approximate in 2 sections, split 25% along the involute
    fm = fs+(fe-fs)/4
    dedBz = involuteBezCoeff(m, z, phi, 3, fs, fm)
    addBz = involuteBezCoeff(m, z, phi, 3, fm, fe)

    # Join the 2 sets of coeffs
    inv = dedBz + addBz[1:]

    # Create the back profile of tooth (mirror image)
    invR = [0 for h in range(len(inv))]
    for i in range(len(inv)):
        #rotate all points to put pitch point at y = 0
        pt = rotate(inv[i], -baseToPitchAngle - (pitchAngle/4))
        inv[i] = pt
        invR[i] = [pt[x], -pt[y]]

    # Calculate section junction points R=back of tooth, Next=front of next tooth
    # top to fillet
    fillet = toCartesian(Rf,-pitchAngle/4-pitchToFilletAngle)
    # flip to make same point on back of tooth
    filletR = [fillet[x], -fillet[y]]
    rootR = toCartesian(Rr, pitchAngle/4+pitchToFilletAngle+filletAngle)
    rootN = toCartesian(Rr, 3*pitchAngle/4-pitchToFilletAngle-filletAngle)
    # top of fillet, front of next tooth
    filletN = rotate(fillet, pitchAngle)

    # ****** create the drawing command data array for the tooth
    data = []
    #---------completar-------------------------------------
    # start at top of fillet
    data = ["M", fillet]
    if(Rf < Rb):
        # line from fillet up to base circle
        data = data + ["L", inv[0]]
    data = data + ["C", inv[1], inv[2], inv[3], inv[4], inv[5], inv[6]]
    # arc across addendum circle, sweep 1 for RHC, 0 for SVG
    data = data + ["A", Ra, Ra, 0, 0, 1, invR[6]]
    # arc across addendum circle, sweep 1 for RHC, 0 for SVG
    data = data + ["C", invR[5], invR[4], invR[3], invR[2], invR[1], invR[0]]
    if(Rf < Rb):
        # line down to top of fillet
        data = data + ["L", filletR]
    # is there a section of root circle between fillets?
    if(rootN[y] > rootR[y]):
        # back fillet, sweep 0 for RHC, 1 for SVG
        data = data + ["A", fRad, fRad, 0, 0, 0, rootR]
        # root circle arc, sweep 1 for RHC, 0 for SVG
        data = data + ["A", Rr, Rr, 0, 0, 1, rootN]

    # sweep 0 for RHC, 1 for SVG
    data = data + ["A", fRad, fRad, 0, 0, 0, filletN]
    return data


def createGearTooth(module, teeth, pressureAngle=20, rotRads=0):
    m = module
    z = teeth
    phi = pressureAngle     # By default 20°
    rot = rotRads           # 0 by default
    # generate the tooth profile
    inData = genGearToothData(m, z, phi)
    outData = []

    # apply arbitrary rotation "rot" to each data poin
    for i in range(len(inData)):
        # skip strings get coords
        if isinstance(inData[i], list):
            # rotate the point
            pt = rotate(inData[i], rot)
            # add the rotated coords to output
            outData.append(pt)
        else:
            # string commands go straight to the output
            outData.append(inData[i])

    # return an array of SVG format draw commands
    return outData


"""
genIntGearToothData
Create an array of drawing commands and their coordinates
to draw a single internal (ring)gear tooth based on a
circle involute using the metric gear standards. Pseudo SVG
path data array is returned. Each coord is an object {x: , y: }
suitable for rotation by later processing if required.
"""
def genIntGearToothData(m, z, phi):
    # ****** gear specifications ******
    # pitch circle to tip circle (ref G.M.Maitra)
    addendum = 0.6*m
    # pitch circle to root radius, sets clearance
    dedendum = 1.25*m
    #-------Calculate radii-------
    # pitch radius
    Rpitch = z*m/2
    # base radius
    Rb = Rpitch*cos(radians(phi))
    # addendum radius
    Ra = Rpitch - addendum
    # root radius
    Rroot = Rpitch + dedendum
    # gear dedendum - pinion addendum
    clearance = 0.25*m
    # radius of top of fillet (end of profile)
    Rf = Rroot - clearance
    # fillet radius, 1 .. 1.5*clearance
    fRad = 1.5*clearance
    # angle between teeth (rads)
    pitchAngle = 2*pi/z
    baseToPitchAngle = getInvolutePolar(Rb, Rpitch)
    # profile starts from base circle
    tipToPitchAngle = baseToPitchAngle
    if(Ra > Rb):
        #start profile from addendum
        tipToPitchAngle -= getInvolutePolar(Rb, Ra)
    pitchToFilletAngle = getInvolutePolar(Rb, Rf) - baseToPitchAngle
    # to make fillet tangential to root
    filletAngle = 1.414*clearance/Rf

    # ****** generate Higuchi involute approximation **********
    # fraction of involute length at end of approx (fillet circle)
    fe = 1
    # fraction of length offset from base to avoid singularity
    fs = 0.01
    if(Ra > Rb):
        # start profile from addendum (tip circle)
        fs = (pow(Ra, 2) - pow(Rb, 2)) / (pow(Rf, 2) - pow(Rb, 2))

    # approximate in 2 sections, split 25% along the profile
    fm = fs+(fe-fs)/4
    addBz = involuteBezCoeff(m, z, phi, 3, fs, fm)
    dedBz = involuteBezCoeff(m, z, phi, 3, fm, fe)
    # join the 2 sets of coeffs (skip duplicate mid point)
    invR = addBz + dedBz[1:]

    # create the front profile of tooth (mirror image)
    inv = [0 for h in range(len(invR))]
    for i in range(len(invR)):
        # rotate involute to put center of tooth at y =
        pt = rotate(invR[i], pitchAngle/4-baseToPitchAngle)
        invR[i] = pt
        # generate the back of tooth profile, flip Y coords
        inv[i] = [pt[x], -pt[y]]

    #****** calculate coords of section junctions**********
    # top of fillet, front of tooth
    fillet = [inv[6][x], inv[6][y]]
    # tip, front of tooth
    tip = toCartesian(Ra, -pitchAngle/4+tipToPitchAngle)
    # addendum, back of tooth
    tipR = [tip[x], -tip[y]]
    rootR = toCartesian(Rroot, pitchAngle/4+pitchToFilletAngle+filletAngle)
    rootNext = toCartesian(Rroot, 3*pitchAngle/4-pitchToFilletAngle-filletAngle)
    # top of fillet, front of next tooth
    filletNext = rotate(fillet, pitchAngle)

    # ****** create the drawing command data array for the tooth *********
    data = []
    # start at top of front profile
    data = ["M", inv[6]]
    data = data + ["C", inv[5], inv[4], inv[3], inv[2], inv[1], inv[0]]
    if(Ra < Rb):
        # line from end of involute to addendum (tip)
        data = data + ["L", tip]
    # arc across tip circle, sweep 1 for RHC, 0 for SVG
    data = data + ["A", Ra, Ra, 0, 0, 1, tipR]
    if (Ra < Rb):
        # line from addendum to start of involute
        data = data ["L", invR[0]]
    data = data + ["C", invR[1], invR[2], invR[3], invR[4], invR[5], invR[6]]

    #there is a section of root circle between fillets
    if (rootR[y] < rootNext[y]):
        # fillet on back of tooth, sweep 1 for RHC, 0 for SVG
        data = data + ["A", fRad, fRad, 0, 0, 1, rootR]
        # root circle arc, sweep 1 for RHC, 0 for SVG
        data = data + ["A", Rroot, Rroot, 0, 0, 1, rootNext]
    #fillet on next, sweep 1 for RHC, 0 for SVG
    data = data + ["A", fRad, fRad, 0, 0, 1, filletNext]

    #return an array of SVG format draw commands
    return data


def createIntGearTooth(module, teeth, pressureAngle=20, rotRads=0):
    m = module
    z = teeth
    phi = pressureAngle
    rot = rotRads
    # generate the tooth profile
    inData = genIntGearToothData(m, z, phi)
    outData = []

    # apply arbitrary rotation "rot" to each data point
    for i in range(len(inData)):
        if isinstance(inData[i], list):
            # rotate point
            pt = rotate(inData[i], rot)
            # add the rotated coords to output
            outData.append(pt)
        else:
            # string commands go straight to the output
            outData.append(inData[i])
    # return an array of SVG format draw commands
    return outData

def rotateTooth(inData, rotRads=0):
    rot = rotRads
    outData = []
    # apply arbitrary rotation "rot" to each data point
    for i in range(len(inData)):
        if isinstance(inData[i], list):
            # rotate point
            pt = rotate(inData[i], rot)
            # add the rotated coords to output
            outData.append(pt)
        else:
            # string commands go straight to the output
            outData.append(inData[i])
    # return an array of SVG format draw commands
    return outData


def createGearOutline(module, teeth, pressureAngle=20, shaftRadius=None):
    m = module
    z = teeth
    phi = pressureAngle
    toothData = genGearToothData(m, z, phi)
    # convert the first tooth into SVG data format
    rotToothData = rotateTooth(toothData)
    # add the unrotated first tooth (including initial "M",x,y)
    gearData = rotToothData
    for i in range(1, z):
        # rotate the tooth to its postiton
        rotToothData = rotateTooth(toothData, 2*pi*i/z)
        # skip the intial "M",x,y command to make path continuos
        gearData = gearData + rotToothData[3:]
    # close the path so it will fill correctly
    gearData.append("Z")
    # -----Shaft definition---------------------
    dedendum = 1.25*m
    # Rpitch : pitch circle radius
    Rpitch = z*m/2
    # Rr: Root circle radius
    Rr = Rpitch - dedendum
    if shaftRadius == None or shaftRadius ==0:
        r = 0
    if shaftRadius <= 0 or shaftRadius >= 0.95*Rr:
        r = 0.2 * Rr
    else:
        r = shaftRadius
    gearData = gearData + ["R", r]
    gearData.append([r, 0, 1.6568541527*r, 90])
    gearData.append([0, r, 1.6568541527*r, 180])
    gearData.append([-r, 0, 1.6568541527*r, -90])
    gearData.append([0, -r, 1.6568541527*r, 0])
    gearData.append("z")

    return gearData


def createIntGearOutline(module, teeth, pressureAngle=20, rimRadius=None):
    m = module
    z = teeth
    phi = pressureAngle
    toothData = genIntGearToothData(m, z, phi)
    # convert the first tooth into SVG dta format
    rotToothData = rotateTooth(toothData)
    # add the unrotated first tooth (including initial "M",x,y)
    gearData = rotToothData
    for i in range(1, z):
        # rotate the tooth to its postiton
        rotToothData = rotateTooth(toothData, 2*pi*i/z)
        # skip the intial "M",x,y command to make path continuos
        gearData = gearData + rotToothData[3:]
    # close the path so it will fill correctly
    gearData.append("Z")
    # -----Rim Radius definition---------------------
    addendum = m
    # Rpitch : pitch circle radius
    Rpitch = z*m/2
    # Ra: Addendum circle radius
    Ra = Rpitch + addendum
    if rimRadius == None or rimRadius ==0:
        r = 0
    if rimRadius <= 0 or rimRadius <= Ra:
        r = 1.1 * Ra
    else:
        r = rimRadius
    # gearData.append(["R", -r,0, "a", r,r, 0,1,0, r*2,0, "a", r,r, 0,1,0, -r*2,0,"z"])
    gearData = gearData + ["R", r]
    gearData.append([r, 0, 1.6568541527*r, 90])
    gearData.append([0, r, 1.6568541527*r, 180])
    gearData.append([-r, 0, 1.6568541527*r, -90])
    gearData.append([0, -r, 1.6568541527*r, 0])
    gearData.append("z")

    return gearData

# todo: convert in comment or delete
#-----------------------Pueba-------------------------------------
# xxa = []
# yya = []
# xxb = []
# yyb = []
#
# # def createGearOutline(module, teeth, pressureAngle=20, shaftRadius=0)
# # da = createGearOutline(10, 40, 20, 60)
# # Dp = z * m
# da = createGearOutline(.15, 40, 20, 2)
# dbb = createIntGearOutline(.15, 20, 20, 1)
#
# for i in range(len(da)):
#     if isinstance(da[i], list):
#         xxa.append(da[i][x])
#         yya.append(da[i][y])
#
# db = rotateTooth(dbb,radians(9))
# for i in range(len(db)):
#     if isinstance(db[i], list):
#         disp = displace(db[i], 0, 1.5)
#         xxb.append(disp[x])
#         yyb.append(disp[y])
#
#
# print(da)
# print(db)
#
# import matplotlib.pyplot as plt
# plt.plot(xxa,yya)
# plt.plot(xxb,yyb)
# plt.show()
#-------------------Prueba--------------------------

