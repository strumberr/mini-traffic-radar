#Author - strumber
#Contact Email - stormurbiz@gmail.com


import machine
import time
from machine import Pin, SoftI2C
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

# oled
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c2 = SoftI2C(scl=Pin(17), sda=Pin(16))
oled_width = 128
oled_height = 64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

second_oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c2)

first_ir = Pin(6, Pin.IN, Pin.PULL_DOWN)
second_ir = Pin(5, Pin.IN, Pin.PULL_DOWN)

avg_speed_list = []

number_loops = []

with open('SB4.pbm', 'rb') as f:
    f.readline() # The first 3 lines of PBM files are info not related to the image
    f.readline() # the 3 readlines remove these lines
    f.readline() # You can check this by opening the PBM file with a notepad
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data, 32, 32, framebuf.MONO_HLSB)
oled.blit(fbuf, 5, 5, 0)
oled.rect(0, 5, 110, 38, 1)
oled.text(f"Designed", 40, 10)
oled.text(f"By", 40, 20)
oled.text(f"Storm", 40, 30)
oled.show()

with open('workahead.pbm', 'rb') as f:
    f.readline() # The first 3 lines of PBM files are info not related to the image
    f.readline() # the 3 readlines remove these lines
    f.readline() # You can check this by opening the PBM file with a notepad
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data, 60, 60, framebuf.MONO_HLSB)
second_oled.blit(fbuf, 35, 5, 0)
second_oled.show()

while True:
    led.value(1)
    led2.value(0)
    
    if not button.value():
        oled.fill(0)
        oled.rect(8, 12, 110, 43, 1)
        oled.text(f"EMERGENCY", 27, 23)
        oled.text(f"STOP", 47, 37)
        oled.show()
        led.value(0)
        led2.value(1)
        break

    while True:
        
        if not button.value():
            oled.fill(0)
            oled.rect(8, 12, 110, 43, 1)
            oled.text(f"EMERGENCY", 27, 23)
            oled.text(f"STOP", 47, 37)
            oled.show()
            led.value(0)
            led2.value(1)
            break

        n_loops = len(number_loops)
        oled.text(f"GO!! Cars: {n_loops}#", 0, 50)
        oled.show()
        first_ir_val = first_ir.value()
        print(first_ir_val)
        time.sleep(.02)
        
        if first_ir_val == 0:
            
            if not button.value():
                oled.fill(0)
                oled.rect(8, 12, 110, 43, 1)
                oled.text(f"EMERGENCY", 27, 23)
                oled.text(f"STOP", 47, 37)
                oled.show()
                led.value(0)
                led2.value(1)
                break

            led.value(0)
            led2.value(1)
            start = time.ticks_ms()
            
            print(f"Time at: {start}")
            print("time started")
            print(f"Final Value: {first_ir_val}")
            break
        
    while True:
        
        if not button.value():
            oled.fill(0)
            oled.rect(8, 12, 110, 43, 1)
            oled.text(f"EMERGENCY", 27, 23)
            oled.text(f"STOP", 47, 37)
            oled.show()
            led.value(0)
            led2.value(1)
            break

        second_ir_val = second_ir.value()
        print(second_ir_val)
        time.sleep(.02)
        if second_ir_val == 0:
            led.value(1)
            led2.value(0)
            end = time.ticks_ms()
            print(f"Time end: {end}")
            time_total = end - start
            time_total_sec = time_total / 1000
            
            speed_cms = 15/time_total_sec
            speed_kmh = speed_cms/27.778
            
            if speed_kmh >= 3:
                
                print(f"Time: {float(time_total_sec)}")
                print(f"Final Value: {second_ir_val}")
                print(f"Speed: {speed_cms} cm/s")
                print(f"Speed: {speed_kmh} km/h")
                
                oled.fill(0)
                oled.show()
                
                decimal_points_cms = '%.2f' % speed_cms
                decimal_points_kmh = '%.2f' % speed_kmh
                
                avg_speed_list.append(decimal_points_kmh)
                print(avg_speed_list)
                el_list = len(avg_speed_list)
                sum_all_el_list = sum(float(i) for i in avg_speed_list)
                print(sum_all_el_list)
                average_speed_kmh = sum_all_el_list/el_list
                
                number_loops.append(decimal_points_kmh)

                oled.text(f"Time: {float(time_total_sec)} sec.", 0, 0)
                oled.text(f"Cm: {decimal_points_cms} cm/s", 0, 10)
                oled.text(f"Km: {decimal_points_kmh} km/h", 0, 20)
                oled.text(f"Avg. {'%.2f' % average_speed_kmh} km/h", 0, 30)
                oled.show()
                
                second_oled.fill(0)
                second_oled.text(f"Too Fast!", 27, 23)
                second_oled.text(f"Slow Down", 25, 37)
                second_oled.show()
                time.sleep(0.5)
                second_oled.fill(0)
                second_oled.show()
                time.sleep(0.5)
                
                second_oled.fill(0)
                second_oled.text(f"Too Fast!", 27, 23)
                second_oled.text(f"Slow Down", 25, 37)
                second_oled.show()
                time.sleep(0.5)
                second_oled.fill(0)
                second_oled.show()
                time.sleep(0.5)
                
                second_oled.fill(0)
                second_oled.text(f"Too Fast!", 27, 23)
                second_oled.text(f"Slow Down", 25, 37)
                second_oled.show()
                time.sleep(0.5)
                second_oled.fill(0)
                second_oled.show()
                time.sleep(0.5)
                
                second_oled.fill(0)
                second_oled.text(f"Too Fast!", 27, 23)
                second_oled.text(f"Slow Down", 25, 37)
                second_oled.show()
                time.sleep(0.5)
                second_oled.fill(0)
                second_oled.show()
                time.sleep(0.5)
                
                with open('workahead.pbm', 'rb') as f:
                    f.readline() # The first 3 lines of PBM files are info not related to the image
                    f.readline() # the 3 readlines remove these lines
                    f.readline() # You can check this by opening the PBM file with a notepad
                    data = bytearray(f.read())
                fbuf = framebuf.FrameBuffer(data, 60, 60, framebuf.MONO_HLSB)
                second_oled.blit(fbuf, 35, 5, 0)
                second_oled.show()
            
            else:
                
                print(f"Time: {float(time_total_sec)}")
                print(f"Final Value: {second_ir_val}")
                print(f"Speed: {speed_cms} cm/s")
                print(f"Speed: {speed_kmh} km/h")
                
                oled.fill(0)
                oled.show()
                
                decimal_points_cms = '%.2f' % speed_cms
                decimal_points_kmh = '%.2f' % speed_kmh
                
                avg_speed_list.append(decimal_points_kmh)
                print(avg_speed_list)
                el_list = len(avg_speed_list)
                sum_all_el_list = sum(float(i) for i in avg_speed_list)
                print(sum_all_el_list)
                average_speed_kmh = sum_all_el_list/el_list
                
                number_loops.append(decimal_points_kmh)

                oled.text(f"Time: {float(time_total_sec)} sec.", 0, 0)
                oled.text(f"Cm: {decimal_points_cms} cm/s", 0, 10)
                oled.text(f"Km: {decimal_points_kmh} km/h", 0, 20)
                oled.text(f"Avg. {'%.2f' % average_speed_kmh} km/h", 0, 30)
                oled.show()
                
                
                oled.rect(0, 45, 120, 15, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                if not button.value():
                    oled.fill(0)
                    oled.rect(8, 12, 110, 43, 1)
                    oled.text(f"EMERGENCY", 27, 23)
                    oled.text(f"STOP", 47, 37)
                    oled.show()
                    led.value(0)
                    led2.value(1)
                    break

                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 14, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 28, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 42, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                if not button.value():
                    oled.fill(0)
                    oled.rect(8, 12, 110, 43, 1)
                    oled.text(f"EMERGENCY", 27, 23)
                    oled.text(f"STOP", 47, 37)
                    oled.show()
                    led.value(0)
                    led2.value(1)
                    break

                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 56, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 70, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 84, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                if not button.value():
                    oled.fill(0)
                    oled.rect(8, 12, 110, 43, 1)
                    oled.text(f"EMERGENCY", 27, 23)
                    oled.text(f"STOP", 47, 37)
                    oled.show()
                    led.value(0)
                    led2.value(1)
                    break

                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 98, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.rect(0, 45, 120, 15, 1)
                oled.fill_rect(2, 47, 116, 11, 1)
                oled.show()
                time.sleep(random.uniform(0.1, 0.7))
                
                oled.fill_rect(0, 40, 130, 43, 0)
                
                if not button.value():
                    oled.fill(0)
                    oled.rect(8, 12, 110, 43, 1)
                    oled.text(f"EMERGENCY", 27, 23)
                    oled.text(f"STOP", 47, 37)
                    oled.show()
                    led.value(0)
                    led2.value(1)
                    break
            break
        
    led.value(0)
