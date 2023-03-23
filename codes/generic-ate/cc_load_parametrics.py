from misc_codes.equipment_settings import *
from misc_codes.general_settings import *
########################################## USER INPUT ##########################################
# INPUT
vin_list = [90, 115, 230, 265]
soak_time_per_line = GENERAL_CONSTANTS.SOAK_TIME_PER_LINE_COMPARISON_CHECK
# OUTPUT
vout = 20
iout = 1.5
config = [(20,1.5), (15,2), (9,3), (5,3), (5,1)]
percent_list = [100,75,50,25,10,5,0]
# percent_list = range(100, -1, -1) # 100% to 0% loading
cc_list = [(iout*percent/100 if percent != 0 else 0) for percent in percent_list]

# PROJECT DETAILS
project = "DER-991"
excel_name = input(">> Excel Name: ")
test = f"Load Regulation - CC Load"

waveforms_folder = GENERAL_FUNCTIONS().CREATE_PATH(project, test)
########################################## USER INPUT ##########################################

def main():
    df = GENERAL_FUNCTIONS().CREATE_DF_WITH_HEADER(GENERAL_CONSTANTS.HEADER_LIST_CC_LOAD)
    
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(1)

    no_load_state = False

    for vin in vin_list:
        
        EQUIPMENT_FUNCTIONS().AC_TURN_ON(vin)
        soak(soak_time_per_line)

        for cc in cc_list:

            no_load_state = EQUIPMENT_FUNCTIONS().SWITCH_STATE(vout, cc, no_load_state)

            if cc != 0: EQUIPMENT_FUNCTIONS().ELOAD_CC_ON(EQUIPMENT_ADDRESS.ELOAD_CHANNEL, cc)
            else: EQUIPMENT_FUNCTIONS().ELOAD_OFF(EQUIPMENT_ADDRESS.ELOAD_CHANNEL)
            
            
            
            output_list = EQUIPMENT_FUNCTIONS().COLLECT_DATA_SINGLE_OUTPUT_CC_LOAD(vin, vout, cc)
            export_to_excel(df, waveforms_folder, output_list, excel_name=excel_name, sheet_name=excel_name, anchor="B2")

    GENERAL_FUNCTIONS().PRINT_FINAL_DATA_DF(df)
    EQUIPMENT_FUNCTIONS().DISCHARGE_OUTPUT(4)

if __name__ == "__main__":
    estimated_time =  len(vin_list)*len(cc_list)*soak_time_per_line
    GENERAL_FUNCTIONS().ESTIMATED_TEST_TIME(estimated_time)
    
    headers(test)
    main()
    footers(waveform_counter)
