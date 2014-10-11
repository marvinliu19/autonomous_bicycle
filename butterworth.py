import Adafruit_BBIO.ADC as ADC
import math
import time 

ADC.setup()

r1 = 0.01
r2 = 0.02
r3 = 0.03
r4 = 0.04
r5 = 0.05

c1 = 1/math.tan(math.pi*r1)
c2 = 1/math.tan(math.pi*r2)
c3 = 1/math.tan(math.pi*r3)
c4 = 1/math.tan(math.pi*r4)
c5 = 1/math.tan(math.pi*r5)

q = math.sqrt(2)

b01 = 1/(1+(q*c1)+(c1*c1))
b02 = 1/(1+(q*c2)+(c2*c2))
b03 = 1/(1+(q*c3)+(c3*c3))
b04 = 1/(1+(q*c4)+(c4*c4))
b05 = 1/(1+(q*c5)+(c5*c5))

b11 = 2*b01
b12 = 2*b02
b13 = 2*b03
b14 = 2*b04
b15 = 2*b05

b21 = b01
b22 = b02
b23 = b03
b24 = b04
b25 = b05

a11 = 2*(c1*c1-1)*b01
a12 = 2*(c2*c2-1)*b02
a13 = 2*(c3*c3-1)*b03
a14 = 2*(c4*c4-1)*b04
a15 = 2*(c5*c5-1)*b05

a21 = -(1-(q*c1)+c1*c1)*b01
a22 = -(1-(q*c2)+c2*c2)*b02
a23 = -(1-(q*c3)+c3*c3)*b03
a24 = -(1-(q*c4)+c4*c4)*b04
a25 = -(1-(q*c5)+c5*c5)*b05

z01 = 0
z02 = 0
z03 = 0
z04 = 0
z05 = 0

z11 = z01
z12 = z02
z13 = z03
z14 = z04
z15 = z05

z21 = z11
z22 = z12
z23 = z13
z24 = z14
z25 = z15

y01 = z01
y02 = z02
y03 = z03
y04 = z04
y05 = z05

y11 = y01
y12 = y02
y13 = y03
y14 = y04
y15 = y05

y21 = y11
y22 = y12
y23 = y13
y24 = y14
y25 = y15

z = ADC.read("P9_40")*360

tcurr=time.time()
tinit=time.time()
dif = tcurr-tinit
while dif < 5:
	if z21 == 0:
		y01 = z
	else:
		y01 = b01*z01 + b11*z11 + b21*z21 + a11*y11 + a21*y21

	if z22 == 0:
		y02 = z
	else:
		y02 = b02*z02 + b12*z12 + b22*z22 + a12*y12 + a22*y22

	if z23 == 0:
		y03 = z
	else:
		y03 = b03*z03 + b13*z13 + b23*z23 + a13*y13 + a23*y23

	if z24 == 0:
		y04 = z
	else:
		y04 = b04*z04 + b14*z14 + b24*z24 + a14*y14 + a24*y24

	if z25 == 0:
		y05 = z
	else:
		y05 = b05*z05 + b15*z15 + b25*z25 + a15*y15 + a25*y25


	print ('%.4f  %.2f  %.2f  %.2f  %.2f  %.2f  %.2f' % (dif, z, y01, y02, 
y03, y04, y05))

	z = ADC.read("P9_40")*360
	

	## Update
	z21 = z11
	z22 = z12
	z23 = z13
	z24 = z14
	z25 = z15

	z11 = z01
	z12 = z02
	z13 = z03
	z14 = z04
	z15 = z05

	z01 = z
	z02 = z
	z03 = z
	z04 = z
	z05 = z

	y21 = y11
	y22 = y12
	y23 = y13
	y24 = y14
	y25 = y15

	y11 = y01
	y12 = y02
	y13 = y03
	y14 = y04
	y15 = y05

	time.sleep(.01)
	tcurr=time.time()
	dif = tcurr-tinit
