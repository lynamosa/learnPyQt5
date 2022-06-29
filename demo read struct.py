# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 21:16:22 2022

@author: lynat
"""

import struct
cfg = []
typeStruct = {'int32':'I','float':'f', 'double':'d', 'long':'l', 'int':'i', 'int64':'q'}
uSpace = (b'\x00\x00').decode('utf-16')
game = "JD"
path = "data/elements.data"

log = open('log.txt', 'w', encoding='utf8')

def cfg2py(txt):
    strStruct = ''
    num=[1]
    typ=[typeStruct[txt[0]]]
    for n in txt[1:]:
        if n.startswith('wstring'):
            typ.append(n[8:] + 's')
            num.append(1)
        elif n in typeStruct:
            if typeStruct[n]==typ[-1]:
                num[-1]+=1
            else:
                typ.append(typeStruct[n])
                num.append(1)
        else:
            print(n, 'Unknow type struct')
            
    for n in range(len(typ)):
        if num[n]>1:
            strStruct+= str(num[n])+typ[n]
        else:
            strStruct+= typ[n]
            
    return strStruct
    
def cfgLoad():
    global cfg
    x = open(r'G:\users\Downloads\source El\sELedit\configs\JD_reborn_17class_v168.cfg', 'r', encoding='utf8', errors='ignore').read().split('\n')
    
    for j in range(3,len(x), 5):
        tbl_Name = x[j]
        tbl_Step = int(x[j+1])-4
        tbl_Item = x[j+2].split(';')
        tbl_Type = x[j+3].split(';')
        tbl_PySt = cfg2py(tbl_Type)
        cfg.append([tbl_Name, tbl_Step,tbl_Item, tbl_Type, tbl_PySt])
        #print(tbl_PySt)

def data2list(data, size, itemStruct):
    print(size[0], struct.calcsize(itemStruct),itemStruct)
    ls = []
    for i in range(size[1]):
        sData = data[i*size[0]:(i+1)*size[0]]
        ls.append(struct.unpack(itemStruct, sData))
    return ls

cfgLoad()
el_tbl = []
with open('elements.data', 'rb') as f:
    hdr = f.read(4)
# =============================================================================
#     el_data = []
#     for n in range(len(cfg)):
#         cf=cfg[n]
#         tbl_pass = f.read(cf[1])
#         
#         tbl_size = struct.unpack('<II', f.read(8))
#         el_data.append(data2list(f.read(tbl_size[0]*tbl_size[1]), tbl_size, cf[4]))
# =============================================================================
        

    ###### Fix struct for new file ###########
    for n in range(5):
        cf=cfg[n]
        tbl = []
        tbl_pass = f.read(cf[1])
        tbl_size = struct.unpack('<II', f.read(8))
        print(f.tell(),tbl_size,cf[1],cf[0])
        for item in range(tbl_size[1]):
            tbl.append(struct.unpack(cf[4], f.read(tbl_size[0])))
        el_tbl.append(tbl)
        
        # f.seek(tbl_size[0]*tbl_size[1],1)
        #print(tbl_size[0], tbl_size[1], cf[1], cf[0])
        # pos = f.tell()
        # log.write(f'{tbl_size[0]}\t{struct.calcsize(cf[4])}\t{tbl_size[1]}\t{cf[1]}\t{f.tell()}\t{cf[0]}\n')
        # if tbl_size[0]>struct.calcsize(cf[4]):
        #     num = int((tbl_size[0]-struct.calcsize(cf[4]))/4)
        #     cfg[n][2]+=['unk' for z in range(num)]
        #     cfg[n][3]+=['int32' for z in range(num)]
        #     cfg[n][4]=cfg2py(cfg[n][3])
        #     log.write(f'-->{num}\n')
        # elif tbl_size[0]<struct.calcsize(cf[4]):
        #     log.write(f'Edit table: {n} - outsize\n')
    
# =============================================================================
#     # - - - - - SAVE - - - - - #
#     with open(r'G:\users\Downloads\source El\sELedit\configs\JD_reborn_17class_v168.cfg', 'w', encoding='utf8') as sv:
#         sv.write(f'{len(cfg)}\n{len(cfg)}\n')
#         for cf in cfg:
#             sv.write(f'\n{cf[0]}\n')
#             sv.write(f'{cf[1]+4}\n')
#             sv.write('{}\n'.format(';'.join(cf[2])))
#             sv.write('{}\n'.format(';'.join(cf[3])))
# =============================================================================

print('finish')
log.close()

