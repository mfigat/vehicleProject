#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # BCM lub BOARD numerowanie
GPIO.setup(4,GPIO.OUT) # 1 silnik sterowanie 1
GPIO.setup(17,GPIO.OUT) # 1 silnik sterowanie 2
GPIO.setup(27,GPIO.OUT) # 2 1
GPIO.setup(22,GPIO.OUT) # 2 2
GPIO.setup(20,GPIO.OUT) # 3 1
GPIO.setup(21,GPIO.OUT) # 3 2
GPIO.setup(12,GPIO.OUT) # 4 1
GPIO.setup(16,GPIO.OUT) # 4 2
GPIO.setup(5,GPIO.OUT) # tylne PWM 1 silnik
GPIO.setup(6,GPIO.OUT) # tylne PWM 2 silnik
GPIO.setup(24,GPIO.OUT) # przednie 1 silnik
GPIO.setup(25,GPIO.OUT) # przednie 2 silnik

p1 = GPIO.PWM(5,50) # utworz obiekt p1 dla PWM sterujacego silnikiem 1 ( port GPIO5) z czestotliwoscia 50 Hz
p2 = GPIO.PWM(6,50) # silnik 2 (port GPIO6) czestotliwosc 50 Hz
p3 = GPIO.PWM(24,50) # silnik 3 (port GPIO24) czestotliowsc 50 Hz
p4 = GPIO.PWM(25,50) # silnik 4 (port GPIO25) czestotliwosc 50 Hz

# p.start(x) - zadaj wyjscie PWM na obiekcie p z DutyCycle (wypelnienie) - x, gdzie x od 0.0 do 100.0%
# p.stop() - zatrzymaj wyjscie dla PWM
# p.ChangeDutyCycle(x) - zmien duty cycle (%)
# p.ChangeFrequency(x) - zmien czestotliwosc (Hz)

## Test obiektu p1
#p1.start(50.0)
#GPIO.output(4,1)
#GPIO.output(17,0)
#time.sleep(4)
##p1.ChangeFrequency(20.0)
#p1.ChangeDutyCycle(10.0)
#time.sleep(4)
#p1.stop()

# ustawienie czestotliwosci dla PWM
frequency=50.0
# rozpoczecie przesylu sygnalu PWM
p1.start(frequency)
p2.start(frequency)
p3.start(frequency)
p4.start(frequency)

# stale lub zmienne do petli while
# dotycza kierunku obrotu kol
i=0 # j - razy robot bedzie jechal do przodu do tylu 
j=2
#dotycza zmiany PWM
k=0
l=10

increment = 100.0/(l*2)


# petla while
while i<j:
	# 4 kola do przodu
	GPIO.output(27,0)
	GPIO.output(4,0)
	GPIO.output(20,0)
	GPIO.output(12,0)
	GPIO.output(17,1)
	GPIO.output(22,1)
	GPIO.output(21,1)
	GPIO.output(16,1)

	# zerowanie k
	k=0
	# wewnetrzna petla while 
	while k<l:
		dc=50+k*increment
		p1.ChangeDutyCycle(dc)
		p2.ChangeDutyCycle(dc)
		p3.ChangeDutyCycle(dc)
		p4.ChangeDutyCycle(dc)
		time.sleep(0.2)
		k=k+1
	
	# 4 kola do tylu
	GPIO.output(22,0)
	GPIO.output(17,0)
	GPIO.output(21,0)
	GPIO.output(16,0)
	GPIO.output(4,1)
	GPIO.output(27,1)
	GPIO.output(20,1)
	GPIO.output(12,1)
	
	# zerowanie k
	k=0
	
	# wewnetrzna petla while
	while k<l:
		dc=50+k*increment
		p1.ChangeDutyCycle(dc)
		p2.ChangeDutyCycle(dc)
		p3.ChangeDutyCycle(dc)
		p4.ChangeDutyCycle(dc)
		time.sleep(0.2)
		k=k+1

	# Zatrzymanie kol
	GPIO.output(27,0)
	GPIO.output(4,0)
	GPIO.output(20,0)
	GPIO.output(12,0)
	i=i+1
# koniec petli while

# wylaczenie przesylu PWM
p1.stop()
p2.stop()
p3.stop()
p4.stop()

GPIO.cleanup() # czyszczenie
