#!/usr/bin/env python

# Wirtualny efektor ve_motor odpowiada za pozyskiwanie poleceń z cs oraz sterowanie re_motor (w tym czterema silnikami).

# Rzeczywisty efektor składa się z 4 silników prądu stałego typu:
# 	DC DG02S z przekładnią 48:1,
#	Napięcie zasilania: 3 V,
#	Pobór prądu: 125 mA ( maks. 170 mA),
#	Prędkość obrotowa na wyjściu: 65 ± 10 obr/min,
#	Moment obrotowy na wyjściu: 0,8 kg*cm (0,078 Nm)
# oraz 2 dwukanałowych sterowników silników L298

# Podstawowe bufory:
#	Pamięć wewnętrzna:
#		a) duty_cycle - wypełnienie
#		b) frequency - częstotliwość impulsów PWM
#	Wejście z podsystemu sterowania cs:
#		a) velocity - zadana prędkość z zakresu <0,1>, gdzie 1 to prędkość maksymalna
#		b) pwm = [frequency, duty_cycle] - zadana częstotliwość impulsów PWM oraz wypełnienie
#		c) direction - zadany kierunek ruchu robota - np. 0 - jedź prosto, 1 - jedź do tyłu
#		d) t_move - zadany czas poruszania się robota
#		e) rotate - zadany kierunek obrotu robota - np. 0 - lewo, 1 prawo
#		f) cmd - polecenie, np. MOVE, ROTATE, SET
#	Wyjście z ve_move do re_move (silniki + sterowniki):
#		a) pwm = [freqency, duty_cycle] - częstotliwość oraz wypełenienie
#		b) motor_sginals[motor number] = [signal nr 1 to motor, signal nr 2 to motor] - kierunek obrotu silnika
#		np. sygnały [0,1] - obrót w jedną stronę lub [1,0] - obrót w drugą stronę lub [0,0] - zatrzymanie silnika,
#		gdzie motor number z zakresu <0,3>

# Częstotliwość pracy ve_move: jeszcze nie wiem - zastanowić się później

# FSM dla ve_move:
# Stany:
# a) S_idle - skojarzone z zachowaniem B_idle
# b) S_move - skojarzone z zachowaniem B_move
# c) S_rotate - skojarzone z zachowaniem B_rotate
# d) S_set - skojarzone z zachowaniem B_set
# Warunki początkowe:
# a) f_sigma_1 = if cmd == MOVE dla S_idle -> S_move
# b) f_sigma_2 = if cmd == ROTATE dla S_idle -> S_rotate
# c) f_sigma_3 = if cmf == SET dla S_idle -> S_set
# Diagram stanów:
# a) S_idle -> S_move oraz S_move -> S_idle
# b) S_idle -> S_rotate oraz S_rotate -> S_idle
# c) S_idle -> S_set oraz S_set -> S_idle

# Podstawowe zachowania które powinny być uwzględnione w ve_motor:
# a) B_move - jedź prosto (do przodu/do tyłu) przez zadany czas t_move z prędkością
# b) B_rotate - obróć się np. o 90 stopni (w lewo/prawo)
# c) B_set - zmien frequency oraz duty_cycle dla PWM
# d) B_idle - zachowanie idle - nic nie rób
# Warunki końcowe:
# a) f_tau_move: t>t_time, gdzie t to czas działania zachowania B_move
# b) f_tau_rotate: t>t_time, gdzie t to czas działania zachowania B_rotate
# c) f_tau_set: True

############################################################################
# Definicje klas:
class Pwm:
	duty_cycle=0.0 # <0.0,100.0>
	frequency=50 #[Hz]


############################################################################