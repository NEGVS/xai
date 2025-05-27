# 第一步：检查sharedCSV,MainTable，LimitTable的格式，  未做
# 第二步：根据选择的一个站位的MainTable.csv, LimitsTable.csv,获取到需要哪些tech中的测项，根据SharedCSV中该测项逻辑创建Yaml，
# 最后根据MainTable.csv, LimitsTable.csv,ConditionTable.csv， TestDefinition编译生成多个站位的coverage.lua
# 注：检查完毕后， 根据SharedCSV直接全部转为SharedYaml，其实MainTable和LimitsTable无需修改

# 1.mappingTable的参数，转yaml时转为字符串
# 2.inputs有多个的时候，csv中用逗号分隔，转yaml时转为数组
# 3.input和output的转换， (), [], {}    condition暂时不知
# 4.teardown和main的分开，teardown测项inputs使用find.mainOutput(.......)
# 5.createRecord的input为itemResult的，已经去掉了input，也去掉了limit

import os
import re
import json
import copy
import yaml
import pandas as pd
import getopt
import sys
import shutil
import asyncio

class csv2yaml(object):
    def __init__(self, station, path):
        # 选择的站位
        self.station = station
        # 路径
        self.base_path = path

        # 多个站位所有测项的tech信息，供之后写入yaml文件，使用CoverageFile名称作为key
        self.tech_info_json = {}

        # teardown测项，使用tech名称作为key
        self.teardown_items = {}

        # 需要输入的函数， 默认上一个action
        self.func_useInput = ['avrageALSClearAndIR', 'calALSIVDDAverage', 'regexProcess', 'calcuALSLight', 'calculateRxCL',
            'analysisSIMResponse', 'parseDumpingResult', 'setItemResult', 'sleep', 'createRecord', 
            'judgeLimit', 'catchValueByIndex', 'parseDictReturnValue', 'checkLength', 'combineHexData', 
            'reShuffle', 'callPlugin', 'mappingTable', 'combineAndFormatString', 'statisticsArray', 
            'writeDataToFile', 'CalSikValue', 'getValueFromDictTable', 'checkRingerStatus', 'catchSampleData',
            'floorValue', 'cameraDisplacementData', 'getAllDataFromNVMMatrix', 'flipStringTwoByte', 
            'calculateSNFromNVMMatrix', 'getMaxValuesFromArray', 'customCombineData', 'openWithBaud', 
            'getdictvalue', 'GetDictfromtxtfile', 'getHAL4100LuxErrorFromRACa', 'decodeRACaKey', 
            'parseNCOLEDValue', 'changeScientificToNormal', 'parseNandUID', 'parseNandFCE', 
            'startDataReporting', 'querySFC', 'convertHexToDec', 'hexStringToASCII', 'sfisLink', 
            'checkWhiteList', 'checkSyscfgKey', 'numberSystemTransfer']
    
    def getAllItems(self):
        # 获取teardown测项
        sta_path = os.path.join(self.base_path, 'TestCoverages', self.station, 'Sequences', 'Assets', 'TestSequence')
        main_path = os.path.join(sta_path, 'MainTable.csv')
        main_df = pd.read_csv(main_path, encoding='utf-8', dtype=str).fillna(value='')
        teardown_line_df=main_df[main_df['Technology'].isin(['='])&main_df['Coverage'].isin(['='])&main_df['TestParameters'].isin(['='])]
        line_index = teardown_line_df.index[0]+1
        teardown_df = main_df[line_index:]
        for one in teardown_df.itertuples():
            testName = '_'.join([one.Technology,one.Coverage,one.TestParameters])
            tech_path_key = one.CoverageFile.replace('TestDefinitions/', '').replace('.yaml', '.csv')
            if tech_path_key in self.teardown_items.keys():
                self.teardown_items[tech_path_key].append(testName)
            else:
                self.teardown_items[tech_path_key] = [testName]

    def createYaml(self, params):
        # 根据SharedCSV和TechCSV对应生成SharedYaml和/TestCoverages/QT0/Sequences/Assets/TestSequence/TestDefinition/xxxx.yaml
        # sharedCSV    ==> SharedYaml
        tasks = []
        for key in params.keys():
            csvPath = params[key][0]
            yamlPath = params[key][1]
            station = self.station if key=='stationPath' else ''
            for oneFile in os.listdir(csvPath):
                if oneFile.startswith('.'):
                    continue
                tasks.append(asyncio.ensure_future(self.createOneFile(csvPath, oneFile, yamlPath, station)))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
    async def createOneFile(self, csvPath, oneFile, yamlPath, station):
        print()
        print('------------------createOneFile')
        print(os.path.join(csvPath, oneFile))
        one_tech_json = []
        tech_path = os.path.join(csvPath, oneFile)
        one_tech_df = pd.read_csv(tech_path, encoding='utf-8', dtype=str).fillna(value='')

        start_index = 0
        end_index = len(one_tech_df)
        print('go into loop---0')
        for index, actionRow in one_tech_df[0:].iterrows():
            if (actionRow['Technology']!='' and actionRow['Coverage']!=''):
                print('go into loop---1')
                end_index = index
                one_item_logic = one_tech_df[start_index:end_index]
                # 一个测项的转换，csv to yaml
                if len(one_item_logic)>0:
                    print('一个测项的转换,csv to yaml')
                    techFile = oneFile if station=='' else f"{station}/{oneFile}"
                    one_item_logic_json = self.addTechCSVInfo(one_item_logic, techFile)
                    one_tech_json.append(one_item_logic_json)
                start_index = index 
            if index==len(one_tech_df)-1:
                print('go into loop---2')
                end_index = index + 1
                one_item_logic = one_tech_df[start_index:end_index]
                # 一个测项的转换，csv to yaml
                if len(one_item_logic)>0:
                    print('一个测项的转换,csv to yaml')
                    techFile = oneFile if station=='' else f"{station}/{oneFile}"
                    one_item_logic_json = self.addTechCSVInfo(one_item_logic, techFile)
                    one_tech_json.append(one_item_logic_json)
                start_index = index 
        print('*** before if len')
        if len(one_tech_json) > 0:
            print('&&& after if len')
            # #生成yaml文件
            if not os.path.exists(os.path.abspath(os.path.join(yamlPath))):
                os.makedirs(os.path.abspath(os.path.join(yamlPath)))
            with open(os.path.join(yamlPath, oneFile.replace('.csv', '.yaml')),"w") as f:
                yaml.safe_dump(data=one_tech_json,stream=f, sort_keys=False, allow_unicode=True)
        else:
            print('len(one_tech_json) < 0-------------errors')

    def addTechCSVInfo(self, change_item, tech_name):
        one_item = {
            'technology': change_item.iloc[0].Technology, 
            'coverage': change_item.iloc[0].Coverage,
            'testParameters':change_item.iloc[0].TestParameters
        }
        one_item_inputs = {}     
        one_item_output = {}
        one_item_condition_output = {}
        index = 1
        local_keys = {}     #{'key_name':action2}    lookup
        lastActionName = ''
        item_squence = []

        itemName = '_'.join([change_item.iloc[0].Technology,change_item.iloc[0].Coverage,change_item.iloc[0].TestParameters])
        
        for one in change_item.itertuples():
            actionInputs = []

            # actionName
            actionName = 'action'+str(index)
            index += 1
            oneAction = {'filename':'Common.lua', 'args': [{}]}
            # Policy
            if one.Policy:
                oneAction['policy'] = one.Policy
            # FuncName
            oneAction['args'][0]['FuncName'] = one.TestActions
            
            # Timeout
            if one.Timeout:
                timeout_value = None
                try:
                    timeout_value = int(one.Timeout)
                except Exception as e:
                    timeout_value = float(one.Timeout)
                finally:
                    oneAction['args'][0]['Timeout'] = timeout_value


            # condition
            if one.Condition:
                condition_str = one.Condition
                values = re.findall('([\({].*?[}\)])',one.Condition)
                for v in values:
                    if re.match('([\({].*?[}\)])', condition_str):
                        if re.match(r"\((?P<keyName>.*)\)", v):
                            keyName = re.match(r"\((?P<keyName>.*)\)", v).groupdict()['keyName']
                            actionInputs.append(copy.deepcopy(local_keys[keyName]))
                            condition_str = condition_str.replace(v, f'$({len(actionInputs)})')

                        elif re.match(r"{(?P<conditionKey>.*)}", v):
                            conditionKey = re.match(r"{(?P<conditionKey>.*)}", v).groupdict()['conditionKey']
                            # 判断是否是该测项的condition输出值
                            if conditionKey in one_item_condition_output.keys() and one_item_condition_output[conditionKey]['testname'] == itemName:
                                actionInputs.append(copy.deepcopy(one_item_condition_output[conditionKey]['lookup']))
                            else:
                                actionInputs.append(['inputs', conditionKey])
                                one_item_inputs[conditionKey] = f'conditions["{conditionKey}"]'
                            condition_str = condition_str.replace(v, f'$({len(actionInputs)})')

                oneAction['args'][0]['Condition'] = condition_str
            
            # 先处理输入
            if one.Inputs:
                values = re.findall('([\[\({].*?[}\)\]])',one.Inputs)
                inputs_str = one.Inputs
                for v in values:
                    if re.match(r"\[(?P<keyName>.*)\]", v):
                        keyName = re.match(r"\[(?P<keyName>.*)\]", v).groupdict()['keyName']
                        info_arr = keyName.split(',')
                        if len(info_arr)!=2:
                            print(f"[❌error:]请检查测项{itemName}的输入值{keyName}")
                        # 判断是否是该测项的global输出值
                        if info_arr[0] in one_item_output.keys() and one_item_output[info_arr[0]]['testname'] == itemName:
                            actionInputs.append(copy.deepcopy(one_item_output[info_arr[0]]['lookup']))
                        else:
                            actionInputs.append(['inputs', info_arr[0]])
                            one_item_inputs[info_arr[0]] = [info_arr[1], actionName]
                        inputs_str = inputs_str.replace(v, f'$({len(actionInputs)})')

                    elif re.match(r"\((?P<keyName>.*)\)", v):
                        keyName = re.match(r"\((?P<keyName>.*)\)", v).groupdict()['keyName']
                        actionInputs.append(copy.deepcopy(local_keys[keyName]))
                        inputs_str = inputs_str.replace(v, f'$({len(actionInputs)})')

                    elif re.match(r"{(?P<conditionKey>.*)}", v):
                        conditionKey = re.match(r"{(?P<conditionKey>.*)}", v).groupdict()['conditionKey']
                        # 判断是否是该测项的condition输出值
                        if conditionKey in one_item_condition_output.keys() and one_item_condition_output[conditionKey]['testname'] == itemName:
                            actionInputs.append(copy.deepcopy(one_item_condition_output[conditionKey]['lookup']))
                        else:
                            actionInputs.append(['inputs', conditionKey])
                            one_item_inputs[conditionKey] = f'conditions["{conditionKey}"]'
                        inputs_str = inputs_str.replace(v, f'$({len(actionInputs)})')
                        
                inputs_new = inputs_str.split(',')if ',' in inputs_str else inputs_str
                oneAction['args'][0]['Input'] = inputs_new
            else:
                # 默认输入， 上一个action的输出
                if one.TestActions in self.func_useInput and lastActionName!='':
                    actionInputs.append([lastActionName, 3])
                    oneAction['args'][0]['Input'] = f'$({len(actionInputs)})'

            if one.AdditionalParameters:
                ap_str = one.AdditionalParameters
                if re.findall(r"\$(\(.*?\))", ap_str):
                    for apKey in re.findall(r"\$(\(.*?\))", ap_str):
                        ap_str = ap_str.replace(apKey, f'({len(actionInputs)+1})')
                        actionInputs.append(copy.deepcopy(local_keys[apKey[1:-1]]))

                if re.findall(r"\$(\[.*?\])", ap_str):
                    for apKey in re.findall(r"\$(\[.*?\])", ap_str):
                        info_arr = apKey[1:-1].split(',')
                        if len(info_arr)!=2:
                            print(f"[❌error:]请检查测项{itemName}的AdditionalParameters值{keyName}")
                        ap_str = ap_str.replace(apKey, f'({len(actionInputs)+1})')
                        # 判断是否是该测项的global输出值
                        if info_arr[0] in one_item_output.keys() and one_item_output[info_arr[0]]['testname'] == itemName:
                            actionInputs.append(copy.deepcopy(one_item_output[info_arr[0]]['lookup']))
                        else:
                            actionInputs.append(['inputs', info_arr[0]])
                            one_item_inputs[info_arr[0]] = [info_arr[1], actionName]
                
                if re.findall('\${(.*?)}',ap_str):
                    for apKey in re.findall('\${(.*?)}',ap_str):
                        ap_str = ap_str.replace('{'+apKey+'}', f'({len(actionInputs)+1})')
                        # 判断是否是该测项的condition输出值
                        if apKey in one_item_condition_output.keys() and one_item_condition_output[apKey]['testname'] == itemName:
                            actionInputs.append(copy.deepcopy(one_item_condition_output[apKey]['lookup']))
                        else:
                            actionInputs.append(['inputs', apKey])

                new_ap_data = json.loads(ap_str)
                if 'mappingTable'  in new_ap_data.keys():
                    new_ap_data['mappingTable'] = json.dumps(new_ap_data['mappingTable'])
                oneAction['args'][0]['AdditionalParameters'] = new_ap_data
                if 'paraName' in oneAction['args'][0]['AdditionalParameters'].keys() and len(oneAction['args'][0]['AdditionalParameters'])==1:
                    del oneAction['args'][0]['AdditionalParameters']

                # useInput true, Input需要为数组
                if 'AdditionalParameters' in oneAction['args'][0].keys() and "useInput" in oneAction['args'][0]['AdditionalParameters'].keys() and oneAction['args'][0]['AdditionalParameters']['useInput']:
                    if type(oneAction['args'][0]['Input']) == type(""):
                        oneAction['args'][0]['Input'] = [oneAction['args'][0]['Input']]

            if one.Command:
                command_str = one.Command
                if re.findall(r"\$(\(.*?\))", command_str):
                    for apKey in re.findall(r"\$(\(.*?\))", command_str):
                        command_str = command_str.replace(apKey, f'({len(actionInputs)+1})')
                        actionInputs.append(copy.deepcopy(local_keys[apKey[1:-1]]))
                elif re.findall(r"\$(\[.*?\])", command_str):
                    for apKey in re.findall(r"\$(\[.*?\])", command_str):
                        info_arr = apKey[1:-1].split(',')
                        if len(info_arr)!=2:
                            print(f"[❌error:]请检查测项{itemName}的Command值{apKey}")
                        one_item_inputs[info_arr[0]] = [info_arr[1], actionName]
                        command_str = command_str.replace(apKey, f'({len(actionInputs)+1})')
                        actionInputs.append(['inputs', info_arr[0]])
                elif re.findall('\${(.*?)}',command_str):
                    for apKey in re.findall('\${(.*?)}',command_str):
                        command_str = command_str.replace(apKey, f'({len(actionInputs)+1})')
                        actionInputs.append(['inputs', apKey])
                
                oneAction['args'][0]['Command'] = command_str
            
            # 处理输出
            if one.Outputs:
                values = re.findall('([\[\({].*?[}\)\]])',one.Outputs)
                for i in range(0, len(values)):
                    v = values[i]
                    if re.match(r"\[(?P<keyName>.*)\]", v):
                        keyName = re.match(r"\[(?P<keyName>.*)\]", v).groupdict()['keyName']
                        info_arr = keyName.split(',')
                        if len(info_arr)!=2:
                            print(f"[❌error:]请检查测项{itemName}的输出值{keyName}")
                        one_item_output[info_arr[0]] = {'lookup': [actionName, i+3],'testname': itemName}
                    elif re.match(r"\((?P<keyName>.*)\)", v):
                        keyName = re.match(r"\((?P<keyName>.*)\)", v).groupdict()['keyName']
                        local_keys[keyName] = [actionName, i+3]
                    elif re.match(r"{(?P<conditionKey>.*)}", v):
                        conditionKey = re.match(r"{(?P<conditionKey>.*)}", v).groupdict()['conditionKey']
                        one_item_condition_output[conditionKey] = {'lookup': [actionName, i+3],'testname': itemName}
                    

            # add args for lookup
            for a in actionInputs:
                oneAction['args'].append({'lookup': a})
            
            # SubSubTest
            if one.SubsubTestName:
                oneAction['args'][0]['SubSubTest'] = one.SubsubTestName

            if oneAction['args'][0]=={}:
                del oneAction['args']

            item_squence.append({ actionName: oneAction})
            
            #保存上一个 actionName
            lastActionName = actionName
            
        
        # 测项输入
        one_item['inputs'] = {}
        for k in one_item_inputs.keys():
            if one_item_inputs[k][0] != itemName:
                if type(one_item_inputs[k]) == type([]):
                    arr = one_item_inputs[k][0].split('_')
                    if len(arr)==1 and 'XXXXXX' in arr:
                        print(f'[❌error:]请检查测项{itemName}的输入值{k}')
                    else:
                        testPara = '_'.join([arr[i] for i in range(2,len(arr))])
                        if tech_name in  self.teardown_items.keys() and itemName in self.teardown_items[tech_name]:
                            inputValue = f'find.mainOutput("{arr[0]}","{arr[1]}","{testPara}","{k}")'
                        else:
                            inputValue = f'find.output("{arr[0]}","{arr[1]}","{testPara}","{k}")'
                        one_item['inputs'][k] = inputValue
                else:
                    one_item['inputs'][k] = one_item_inputs[k]

        # 测项输出
        one_item['outputs'] = {}
        for k in one_item_output.keys():
            if 'testname' in one_item_output[k].keys():
                del  one_item_output[k]['testname']
            one_item['outputs'][k] = one_item_output[k]

        # 测项Condition输出
        one_item['conditions'] = {}
        for k in one_item_condition_output.keys():
            if 'testname' in one_item_condition_output[k].keys():
                del  one_item_condition_output[k]['testname']
            one_item['conditions'][k] = one_item_condition_output[k]

        # delete useless
        if one_item['inputs']=={}:
            del one_item['inputs']
        if one_item['outputs']=={}:
            del one_item['outputs']
        if one_item['conditions']=={}:
            del one_item['conditions']
        
        one_item['sequence']= {'actions': item_squence}

        return one_item

def usage():
    print("-h/--help: help document")
    print("-s/--station: 当前工程/TestCoverage中的一个站位名，例如QT0")

if __name__=='__main__':
    # 单个使用Main.csv Limit.csv Condition.csv SharedCSV 生成SharedYaml以及coverage.lua
    # 获取ATS_SCHOONER_TEST中的站位信息及SharedCSV
    
    station = 'QT0'
    schooner_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_stations = [i if not i.startswith('.') else '' for i in os.listdir(os.path.join(schooner_path,'TestCoverages'))]
    
    try:
        options, args = getopt.getopt(sys.argv[1:], "hs:", ["Help", "station="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()
    if len(options)==0:
        usage()
        exit()
    else:
        for k, path in options:
            if k in ("-s", "--station"):
                station = path
                if path not in all_stations:
                    print(f'{path} not in TestCoverage.')
                    exit()
            else:
                usage()
                exit()

    csv2yaml = csv2yaml(station, schooner_path)
    print("========== start create yaml files ========")
    # 获取teardown测项
    csv2yaml.getAllItems()

    # SharedYaml生成, StationYaml生成
    station_path = os.path.join(csv2yaml.base_path, 'TestCoverages', csv2yaml.station, 'Sequences')
    params = {
        'sharedPath':[os.path.join(csv2yaml.base_path, 'SharedCSV'), os.path.join(csv2yaml.base_path, 'SharedYaml')],
        'stationPath':[os.path.join(station_path, 'TechCSV'), os.path.join(station_path, 'Assets', 'TestSequence', 'TestDefinitions', csv2yaml.station)],
    
    }
    csv2yaml.createYaml(params)

    # create coverage.lua
    # testDefinitions有包含sharedYaml和stationYaml, 先将sharedYaml移到TestDefinitions下，生成后又移回去   
    fileList = os.listdir(os.path.join(csv2yaml.base_path, 'SharedYaml'))
    for file in fileList:
        src = os.path.join(csv2yaml.base_path, 'SharedYaml', file)
        new = os.path.join(station_path, 'Assets', 'TestSequence', 'TestDefinitions')
        shutil.copy(src, new)
    print()
    print("==========")
    print("==========")
    print("==========")
    print("==========")
    print(f"========== start create {station} coverage.lua ========")
    sta_sequence_path = os.path.join(station_path, 'Assets', 'TestSequence')
    sta_path_main = os.path.join(sta_sequence_path, "MainTable.csv")
    sta_path_limit = os.path.join(sta_sequence_path, "LimitsTable.csv")
    sta_path_condition = os.path.join(sta_sequence_path, "ConditionTable.csv")
    tech_path = sta_sequence_path
    output_path = os.path.join(station_path, 'Modules', "coverage")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    os.system(f"sh {schooner_path}/Framework/Modules/Schooner/Compiler/SchoonerCompiler \
    -m {sta_path_main} \
    -l {sta_path_limit} \
    -c {sta_path_condition} \
    -t {tech_path} \
    -o {output_path}/coverage.lua")

    for file in fileList:
        new = os.path.join(station_path, 'Assets', 'TestSequence', 'TestDefinitions', file)
        os.remove(new)

        
