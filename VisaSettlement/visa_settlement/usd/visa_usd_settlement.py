import os, re,sys
from pathlib import Path

visa_file_path = Path('F:\\Office_work\\settlement\\APRIL\\2020.04.06\\EVE\\d200407_r2_t061128_prod\\EP747.txt')

str_120 = 'REPORT ID:  VSS-120                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  '
pattern_120 = re.compile('s?REPORT ID:  VSS-120                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  ')

str_130 = 'REPORT ID:  VSS-130                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  '
pattern_130 = re.compile('s?REPORT ID:  VSS-130                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  ')

str_140 = 'REPORT ID:  VSS-140                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  '
pattern_140 = re.compile('s?REPORT ID:  VSS-140                                         VISANET SETTLEMENT SERVICE                        PAGE:              1  ')


with open(visa_file_path,'r') as read_file, open('visa_120.txt','w') as out_120_file:
    writing = False
  
    
    for line in read_file:
        if  pattern_120.match(line):
            
            # if line.startswith(' REPORTING FOR:      9000432017 JBBL SUMMARY               INTERNATIONAL SETTLEMENT SERVICE                    PROC DATE:   01MAY20  '):
            writing = True
            
        if writing:
            out_120_file.write(line)
        
        if line.startswith('                                                   ***  END OF VSS-120 REPORT  ***                                                   '):
            writing= False

       
        
with open(visa_file_path,'r') as read_file, open('visa_130.txt','w') as out_130_file:

    for line in read_file:
        if  pattern_130.match(line):            
            
            # if line.startswith(' REPORTING FOR:      9000432017 JBBL SUMMARY               INTERNATIONAL SETTLEMENT SERVICE                    PROC DATE:   01MAY20  '):
             writing = True
            
              
            
        if writing:
           
            out_130_file.write(line)
        
        if line.startswith('                                                    *** END OF VSS-130 REPORT ***                                                    '):
            writing= False          

with open(visa_file_path,'r') as read_file, open('visa_140.txt','w') as out_140_file:          
    for line in read_file:
        if  pattern_140.match(line):
            # print(writing)
            # if line.startswith(' REPORTING FOR:      9000432017 JBBL SUMMARY               INTERNATIONAL SETTLEMENT SERVICE                    PROC DATE:   01MAY20  '):
            writing = True
            
        if writing:
            out_140_file.write(line)
        
        if line.startswith('                                                    *** END OF VSS-140 REPORT ***                                                    '):
            writing= False
        
        


with open('visa_120.txt','r') as extract_file, open('extract_120.txt','w') as extract:
    start_writing = False
    for line in extract_file:
        if line.startswith(' REPORTING FOR:      9000432006 408840 NW2                 INTERNATIONAL SETTLEMENT SERVICE                    PROC DATE:   01MAY20  '):
            start_writing = True
        
        if start_writing:
            extract.write(line)
        
        if line.startswith('                                                   ***  END OF VSS-120 REPORT  ***                                                   '):
            start_writing =False



with open('visa_120.txt','r') as extract_file, open('extract_120.txt','w') as extract:
    start_writing = False
    for line in extract_file:
        if line.startswith(' REPORTING FOR:      9000432006 408840 NW2                 INTERNATIONAL SETTLEMENT SERVICE                    PROC DATE:   01MAY20  '):
            start_writing = True
        
        if start_writing:
            extract.write(line)
        
        if line.startswith('                                                   ***  END OF VSS-120 REPORT  ***                                                   '):
            start_writing =False



with open('visa_130.txt','r') as extract_file, open('extract_130.txt','w') as extract_f:
    start_writing = False
    count = 0
    for line in extract_file:
        if line.startswith('                                                    *** END OF VSS-130 REPORT ***                                                    '):
           count = count + 1
        
        if count == 5:
            # if line.startswith('                                                    *** END OF VSS-130 REPORT ***                                                    '):
                # start_writing = True

            # if start_writing:
                extract_f.write(line)
        
            # if line.startswith('                                                    *** END OF VSS-130 REPORT ***                                                    '):
                # start_writing = False



with open('visa_140.txt','r') as extract_file, open('extract_140.txt','w') as extract_f:
    start_writing = False
    for line in extract_file:
        if line.startswith(' REPORTING FOR:      9000432002 DEB 408833 INT            INTERNATIONAL SETTLEMENT SERVICE                     PROC DATE:   01MAY20  '):
            start_writing = True
        
        if start_writing: 
            extract_f.write(line)
        
        if line.startswith('                                                    *** END OF VSS-140 REPORT ***                                                    '):
            start_writing = False







# atm_cash_list = []
# with open('extract_120.txt','r') as file_120:
#     write = False
#     for line in file_120:
#         if line.startswith('   TOTAL ATM CASH                                                2            21,000.00CR               173.96                       '):
#             write = True
            
#         if write:
#             atm_cash_list.append(line.split(' '))
        
#         if line.startswith('   TOTAL ATM CASH                                                2            21,000.00CR               173.96                       '):
#             write = False
        

# atm_cash_filter_list = []

# for values in atm_cash_list:
#     for value in values:
#         if value != '':
#             atm_cash_filter_list.append(value)
        

# print(atm_cash_filter_list)
# date = atm_cash_filter_list[2]
# count = atm_cash_filter_list[3]
# atm_cash_str= atm_cash_filter_list[4]
# interchange_amount = atm_cash_filter_list[5]

# number_str = ''
# for digit in atm_cash_str:
#     if digit.isdigit() or digit == '.' :
#             number_str = number_str + digit

# actual_amount = float(number_str) - (int(count) * 500)
# print(actual_amount)

atm_count_130 = ''
atm_commision_130 = ''
atm_after_reversal_commision_130 = ''
def function_extract_130():
    atm_cash130_list = []
    with open('extract_130.txt','r') as file_130:
        write = False
        count = 0

        for line in file_130:
        
            if line.startswith('    ATM CASH                                                                                                                         '):
                write = True
                
                
            if write:
                atm_cash130_list.append(line.split(' '))
            
            if line.startswith('                                                                                                                                     '):
                count = count +1

            if count == 4:
                write= False   
                break
        
    total_list_count = len(atm_cash130_list)
    list_index_to_be_extracted = total_list_count - 3
    print(len(atm_cash130_list))
    extracted_at130_list = atm_cash130_list[list_index_to_be_extracted]
    extracted_atm130_list_values = []


    for value in extracted_at130_list:
        if value != '':
            extracted_atm130_list_values.append(value)
            
    print(extracted_atm130_list_values)

    if len(extracted_atm130_list_values) == 7:
        atm_count_130 = int(extracted_atm130_list_values[3])
        atm_commision_130 = float(extracted_atm130_list_values[5])
        print(atm_count_130,atm_commision_130)
    else:
        atm_count_130 = extracted_atm130_list_values[3]
        reversal_amount = extracted_atm130_list_values[5]
        atm_after_reversal_commision_130 = float(extracted_atm130_list_values[6]) - reversal_amount


function_extract_130()


decline_count_130 = ''
decline_commision_130 = ''
def function_decline_extract_130():
    decline_cash130_list = []
    with open('extract_130.txt','r') as file_130:
        file_read = file_130.readlines()
        write = False
        count_blank = 0
        line_count = 0
        total_blank_count = 10
        for line in file_read:
            if line.startswith('                                                                                                                                     '):
                count_blank = count_blank +1
        print(count)

        count_difference = total_blank_count - count_blank
        actual_count = total_blank_count - count_difference
        print(actual_count)
        for line in file_read:
          
            if line.startswith('    ATM DECLINE                                                                                                                      '):
                write = True
                print('true')                
                
            if write:
                decline_cash130_list.append(line.split(' '))
            
            if line.startswith('                                                                                                                                     '):
                line_count = line_count +1
                print(line_count)
            
            if actual_count == 10:
                if line_count == 8:                
                    write = False 
                    break  
            elif actual_count  == 8:
                if line_count == 6:
                    write = False
                    break
            elif actual_count == 6:
                if line_count == 4:
                    write = False
                    break

           



    # print(decline_cash130_list)
    total_list_count = len(decline_cash130_list)
    print(total_list_count)
    list_index_to_be_extracted = total_list_count - 3
    print(len(decline_cash130_list))
    extracted_decline130_list = decline_cash130_list[list_index_to_be_extracted]
    extracted_atm130_list_values = []

    for value in extracted_decline130_list:
        if value != '':
            extracted_atm130_list_values.append(value)
            
    print(extracted_atm130_list_values)

    if len(extracted_atm130_list_values) == 7:
        decline_count_130 = int(extracted_atm130_list_values[3])
        decline_commision_130 = float(extracted_atm130_list_values[5])
        print(decline_count_130,decline_commision_130)
    else:
        atm_count_130 = extracted_atm130_list_values[3]
        reversal_amount = extracted_atm130_list_values[5]
        atm_after_reversal_commision_130 = float(extracted_atm130_list_values[6]) - reversal_amount

function_decline_extract_130()

inquiry_count_130 = ''
inquiry_commision_130 = ''
def function_inquiry_extract_130():
    inquiry_cash130_list = []
    with open('extract_130.txt','r') as file_130:
        write = False
        count = 0
        total_blank_count = 10
        for line in file_130:
            if line.startswith('                                                                                                                                     '):
                count = count +1
                # print(count)

        count_difference = total_blank_count - count
        actual_count = total_blank_count - count_difference

        # for line in file_130:
        
        #     if line.startswith('    ATM BALANCE INQUIRY                                                                                                              '):
        #         write = True
                  
        #     if write:
        #         inquiry_cash130_list.append(line.split(' '))
            
           
        #     if count == 6:
        #         write= False   
        #         break

   
    # total_list_count = len(inquiry_cash130_list)
    # list_index_to_be_extracted = total_list_count - 3
    # print(len(inquiry_cash130_list))
    # extracted_inquiry130_list = inquiry_cash130_list[list_index_to_be_extracted]
    # extracted_inquiry130_list_values = []

    # for value in extracted_inquiry130_list:
    #     if value != '':
    #         extracted_inquiry130_list_values.append(value)
            
    # print(extracted_inquiry130_list_values)

    # if len(extracted_inquiry130_list_values) == 7:
    #     inquiry_count_130 = int(extracted_inquiry130_list_values[3])
    #     inquiry_commision_130 = float(extracted_inquiry130_list_values[5])
    #     print(inquiry_count_130,inquiry_commision_130)
    # else:
    #     inquiry_count_130 = extracted_inquiry130_list_values[3]
    #     reversal_amount = extracted_inquiry130_list_values[5]
    #     inquiry_after_reversal_commision_130 = float(extracted_inquiry130_list_values[6]) - reversal_amount

function_inquiry_extract_130()