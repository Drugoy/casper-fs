import os
import yaml
import random
import string
import argparse
from util import file_op
from termcolor import colored
from util import custom_validator

def random_function_name():
 chars = string.ascii_lowercase + string.digits
 return "f"+''.join(random.choice(chars) for _ in range(10)) 

def code_junk_gen():
 ops = {"x+=1","x-=1","x*=1","x+=2","x+=y","y++","y-=1","y+=1"}
 code = "volatile int x=0,y=0;\n"
 count = 0
 while count<=4:
  ops = random.sample(ops,len(ops))
  for line in ops:
   code += "\t"+str(line)+";\n"
  count += 1
 return code


def banner():
 reset = '\033[0m'
 yellow = '\033[93m'

def banner():
    print("\t____ ____ ____ ___  ____ ____    ____ ____") 
    print("\t|    |__| [__  |__] |___ |__/ __ |___ [__  ") 
    print("\t|___ |  | ___] |    |___ |  \    |    ___] ")
    file = open("util/banner.txt", "r")
    logo = file.read()
    print(colored(logo,'white',attrs=['blink']) )
    file.close()     
    print(colored("\tCasper-fs is a Custom Hidden Linux Kernel Module generator. Each module works in the file system to protect and hide secret files.",'yellow'))
    print(colored("\tVersion 0.3 coded by CoolerVoid - github.com/CoolerVoid/casper-fs",'cyan'))
    print ("\tExample to use:")
    print ("\tpython3 Casper-fs.py --rules rules/my_secret_files.yaml\n")

def arguments():
    parser = argparse.ArgumentParser(description = banner())
    parser.add_argument('-r', '--rules', action = 'store', dest = 'rules_filename', default="rules/fs-rules.yaml", required = True, help = 'file system rules to create a kernel module, look directory rules')
    args = parser.parse_args()
    if os.path.isfile(args.rules_filename):
        return args.rules_filename
    else:
        print ('File rules does not exist!')
        exit(0)
    parser.print_help()
    exit(0)

def Get_config(ConfigFile):
 d={}
 d['hide_list_fs']=""
 d['protect_list_fs']=""
 
 with open(ConfigFile, 'r') as file:
  parsed = yaml.safe_load(file)
 print("Load external config "+ConfigFile)
 print(colored("Scanning with validator","green") )
 custom_validator.is_valid_casper_yaml(parsed)
 print(colored("All right in rules file, next step!","green") )

 for key,value in parsed.items():
  if key == "binary_name":
   d['binary_name']=str(value)
  if key == "module_name":
   d['module_name']=str(value)
  if key == "unhide_module_key":
   d['unhide_module_key']=str(value)
  if key == "hide_module_key":
   d['hide_module_key']=str(value)
  if key == "fake_device_name":
   d['fake_device_name']=str(value)
  if key == "unhide-hide-file-key":
   d['unhide-hide-file-key']=value
  if key == "unprotect-protect-file-key":
   d['unprotect-protect-file-key']=value
  if key == "fs-rules":
   e=value
 
 for v in e:
     for val in v:
         if val == "hidden":
             for n in v['hidden'].values():
                 d['hide_list_fs']=d['hide_list_fs']+'"'+str(n)+"\","
         if val == "protect":
             for n in v['protect'].values():
                 d['protect_list_fs']=d['protect_list_fs']+'"'+str(n)+"\","
  
 d['hide_list_fs']=d['hide_list_fs'][:-1]
 d['protect_list_fs']=d['protect_list_fs'][:-1]
 if len(d['hide_list_fs'])<3 and len(d['protect_list_fs'])<3:
     print(colored("Error!\nYAML file needs a field for a \"hidden\" list or list called \"protect\"!","red"))
     exit(0)
 if len(d['hide_list_fs']) <3:
     d['hide_list_fs']="\"0\""
 if len(d['protect_list_fs']) <3:
     d['protect_list_fs']="\"0\""
 return d


def start_generator(rules_fs):
 v = rules_fs
 # Load content of templates
 template_content_main=file_op.File_to_string("template/main.c")
 template_content_hooked=file_op.File_to_string("template/hooked.c")
 template_content_hooked_h=file_op.File_to_string("template/hooked.h")
 template_content_makefile=file_op.File_to_string("template/Makefile")
 print (colored("Generate Kernel module!","cyan"))
 # main.c
 main_file=template_content_main
 main_file=main_file.replace("CASPER_MODULE_NAME",v['module_name'])
 main_file=main_file.replace("CASPER_FAKE_DEVICE",v['fake_device_name'])
 # random junk code generator
 main_file = main_file.replace("CODE_GEN_FUNC_NAME1", random_function_name())
 main_file = main_file.replace("CODE_GEN_FUNC_NAME2", random_function_name())
 main_file = main_file.replace("CODE_GEN_FUNC_NAME3", random_function_name())
 main_file = main_file.replace("JUNK_CODE_1", code_junk_gen())
 main_file = main_file.replace("JUNK_CODE_2", code_junk_gen())
 main_file = main_file.replace("JUNK_CODE_3", code_junk_gen())
 # hooked.c
 hooked_file=template_content_hooked
 hooked_file=hooked_file.replace("CASPER_HIDE",v['hide_module_key'])
 hooked_file=hooked_file.replace("CASPER_UNHIDE",v['unhide_module_key'])
 hooked_file=hooked_file.replace("UNHIDE_HIDE_FS",v['unhide-hide-file-key'])
 hooked_file=hooked_file.replace("CASPER_PROTECT_UNPROTECT_FS",v['unprotect-protect-file-key'])
 hooked_file=hooked_file.replace("PROTECT_LIST",v['protect_list_fs'])
 hooked_file=hooked_file.replace("HIDE_LIST",v['hide_list_fs'])
 # hooked.h
 hooked_h_file=template_content_hooked_h
 hooked_h_file=hooked_h_file.replace("CASPER_MODULE_NAME",v['module_name'])
 # Makefile
 makefile_file=template_content_makefile
 makefile_file=makefile_file.replace("CASPER_BINARY_NAME",v['binary_name'])
 # save output
 output_makefile="output/Makefile"
 output_hooked="output/hooked.c"
 output_hooked_h="output/hooked.h"
 output_main="output/main.c"
 file_op.WriteFile(output_makefile,makefile_file)
 file_op.WriteFile(output_hooked,hooked_file)
 file_op.WriteFile(output_hooked_h,hooked_h_file)
 file_op.WriteFile(output_main,main_file)
 print (colored("Python Script end, please look the output your custom kernel module at directory output/\n","yellow"))



