"""IMPORT DEPENDENCIES"""
from time import time, sleep
import sys
import os
import math
from powi.equipment import ACSource, PowerMeter, ElectronicLoad, Oscilloscope, LEDControl
from powi.equipment import headers, create_folder, footers, waveform_counter, soak, convert_argv_to_int_list, tts, prompt
from filemanager import path_maker, remove_file
import winsound as ws
from playsound import playsound
waveform_counter = 0

from datetime import datetime
now = datetime.now()
date = now.strftime('%Y_%m_%d')	

##################################################################################

"""COMMS"""
ac_source_address = 5
source_power_meter_address = 1 
load_power_meter_address = 2
eload_address = 8
scope_address = "10.125.10.184"

"""USER INPUT"""
vin_list = [120,230]

test = input("Enter test name: ")


"""DO NOT EDIT BELOW THIS LINE"""
##################################################################################

"""EQUIPMENT INITIALIZE"""
ac = ACSource(ac_source_address)
pms = PowerMeter(source_power_meter_address)
pml = PowerMeter(load_power_meter_address)
eload = ElectronicLoad(eload_address)
scope = Oscilloscope(scope_address)


def scope_settings():
    """CHANNEL SETTINGS"""
    scope.channel_settings(state='ON', channel=1, scale=100, position=-1, label="Input Voltage", color='YELLOW', rel_x_position=20, bandwidth=20, coupling='AC', offset=0)
    scope.channel_settings(state='ON', channel=2, scale=2, position=3, label="ZCD_IN", color='ORANGE', rel_x_position=40, bandwidth=20, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=3, scale=1, position=-1, label="RelayON Pulse", color='LIGHT_BLUE', rel_x_position=60, bandwidth=20, coupling='DCLimit', offset=0)
    scope.channel_settings(state='ON', channel=4, scale=2, position=-4, label="Q1 Regulator", color='PINK', rel_x_position=80, bandwidth=20, coupling='DCLimit', offset=0)
    
    """MEASURE SETTINGS"""
    scope.measure(1, "MAX,RMS,FREQ")
    scope.measure(2, "MAX,MIN")
    scope.measure(3, "MAX,MIN")
    scope.measure(4, "MAX,MIN")

    """HORIZONTAL SETTINGS"""
    scope.time_position(10)
    scope.record_length(50E6)
    scope.time_scale(1)

    """ZOOM SETTINGS"""
    scope.remove_zoom()
    # scope.add_zoom(rel_pos=21.727, rel_scale=1)
    
    """TRIGGER SETTINGS"""
    trigger_channel =2
    trigger_level = 1
    trigger_edge = 'POS'
    scope.edge_trigger(trigger_channel, trigger_level, trigger_edge)


    scope.stop()
    sleep(2)

def operation():
    global waveform_counter
    
    scope_settings()
    
    for vin in vin_list:

        scope.run_single()
        sleep(3)

        ac.voltage = vin
        ac.turn_on()

        sleep(3)
        print("Turn switch on")
        sleep(3)

        sleep(4)
        ac.turn_off()

        # scope.add_zoom(rel_pos=42.972, rel_scale=1)
        # input("Adjust startup cursor")
        # scope.add_zoom(rel_pos=21.727, rel_scale=1)
        input("Capture waveform?")

        filename = f'{test}, {vin}Vac, {ac.frequency}Hz.png'
        waveforms_folder = f'C:/Users/ccayno/Desktop/DER-867 LNK-TNZ ONOFF Switch/Test Data/{date}/{vin}Vac_{ac.frequency}Hz'
        path = path_maker(f'{waveforms_folder}')
        scope.get_screenshot(filename, path)
        print(filename)
        waveform_counter += 1
        
        
        capturing_condition = input("Press ENTER to continue capture waveform. Press anything else to stop capturing waveforms. ")
        i = 1
        while capturing_condition == '':
            filename = f'{test}, {vin}Vac, {ac.frequency}Hz, ({i}).png'
            waveforms_folder = f'C:/Users/ccayno/Desktop/DER-867 LNK-TNZ ONOFF Switch/Test Data/{date}/{vin}Vac_{ac.frequency}Hz'
            path = path_maker(f'{waveforms_folder}')
            scope.get_screenshot(filename, path)
            print(filename)
            waveform_counter += 1
            i += 1
            capturing_condition = input("Press ENTER to continue capture waveform. Press anything else to stop capturing waveforms. ")





def main():
    global waveform_counter
    operation()
        
if __name__ == "__main__":
    headers(test)
    main()
    footers(waveform_counter)