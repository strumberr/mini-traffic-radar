#link network https://projects.raspberrypi.org/en/projects/get-started-pico-w/2

import machine
import time
from machine import Pin, SoftI2C, ADC, PWM
import ssd1306
from time import sleep
import random
import framebuf




photo_pin = machine.ADC(26)
photo_pin2 = machine.ADC(27)

led = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(7, machine.Pin.OUT)
flash = machine.Pin(8, machine.Pin.OUT)

button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)




second_ir = Pin(6, Pin.IN, Pin.PULL_DOWN)
second_ir_left = Pin(11, Pin.IN, Pin.PULL_DOWN)
second_ir_right = Pin(10, Pin.IN, Pin.PULL_DOWN)

first_ir = Pin(5, Pin.IN, Pin.PULL_DOWN)
first_ir_left = Pin(9, Pin.IN, Pin.PULL_DOWN)
first_ir_right = Pin(19, Pin.IN, Pin.PULL_DOWN)

avg_speed_list = []

number_loops = []

while True:
    led.value(1)
    led2.value(0)
    
   

    

    while True:
        
       
        n_loops = len(number_loops)

        
        first_ir_val = first_ir.value()
        first_ir_left_val = first_ir_left.value()
        first_ir_right_val = first_ir_right.value()
        
        print(first_ir_val)
        time.sleep(.005)
        
        if first_ir_val == 0 or first_ir_left_val == 0 or first_ir_right_val == 0:
            
          

                
            led.value(0)
            led2.value(1)
            start = time.ticks_ms()
            
            print(f"Time at: {start}")
            print("time started")
            print(f"Final Value: {first_ir_val}")
            break
        

    while True:
    

            
        second_ir_val = second_ir.value()
        second_ir_val_left = second_ir_left.value()
        second_ir_val_right = second_ir_right.value()
        
        print(second_ir_val)
        time.sleep(.005)
        if second_ir_val == 0 or second_ir_val_left == 0 or second_ir_val_right == 0:
            led.value(1)
            led2.value(0)
            end = time.ticks_ms()
            print(f"Time end: {end}")
            time_total = end - start
            time_total_sec = time_total / 1000
            
            speed_cms = 75.5/time_total_sec
            speed_kmh = speed_cms/27.778            
            if speed_kmh >= 3:
                
                print(f"Time: {float(time_total_sec)}")
                print(f"Final Value: {second_ir_val}")
                print(f"Speed: {speed_cms} cm/s")
                print(f"Speed: {speed_kmh} km/h")
                
              
                decimal_points_cms = '%.2f' % speed_cms
                decimal_points_kmh = '%.2f' % speed_kmh
                
                avg_speed_list.append(decimal_points_kmh)
                print(avg_speed_list)
                el_list = len(avg_speed_list)
                sum_all_el_list = sum(float(i) for i in avg_speed_list)
                print(sum_all_el_list)
                average_speed_kmh = sum_all_el_list/el_list
                
                number_loops.append(decimal_points_kmh)

                
                print(decimal_points_cms)
                
                str_time = str(time_total_sec)
              
              
                
                
            
            else:
                
                
                    
                    
                
                print(f"Time: {float(time_total_sec)}")
                print(f"Final Value: {second_ir_val}")
                print(f"Speed: {speed_cms} cm/s")
                print(f"Speed: {speed_kmh} km/h")
              
                decimal_points_cms = '%.2f' % speed_cms
                decimal_points_kmh = '%.2f' % speed_kmh
                
                avg_speed_list.append(decimal_points_kmh)
                print(avg_speed_list)
                el_list = len(avg_speed_list)
                sum_all_el_list = sum(float(i) for i in avg_speed_list)
                print(sum_all_el_list)
                average_speed_kmh = sum_all_el_list/el_list
                
                number_loops.append(decimal_points_kmh)

                
                str_time = str(time_total_sec)
                
                time.sleep(random.uniform(0.1, 0.7))
                

                
            break
        
    led.value(0)
