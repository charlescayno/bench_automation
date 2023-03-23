from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
test = "Battery Discharge"
########################################## USER INPUT ##########################################

def discharge_battery(vout,iout):
    while(vout > 18):
        vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
        EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(7, iout)
        print(f"Vbat = {vout:.2f} V, Iout = {iout} A")
        sleep(1)
    # EQUIPMENT_FUNCTIONS().ELOAD_OFF(7)

def main_battery_discharge():
    EQUIPMENT_FUNCTIONS().AC_TURN_OFF()

    vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
    while (vout > 18.2):
        
        for i in range(10, 2, -1):
            while (vout > 18.2):
                EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(7, i)
                print(f"Vbat = {vout:.2f} V, Iout = {i} A")
                soak(2)
                vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()
            EQUIPMENT_FUNCTIONS().ELOAD_OFF(7)
            soak(10)
            vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()

        soak(30)
        vout = EQUIPMENT_FUNCTIONS().OUTPUT_VOLTAGE_POWER_METER()


if __name__ == "__main__":
 
    headers(test)
    main_battery_discharge()
    print("Discharge complete")

    footers(waveform_counter)