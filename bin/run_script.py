# -*- coding: UTF-8 -*-
import argparse
import subprocess
import os
import sys
import time
import glob
import multiprocessing
import textwrap


#path = os.getcwd()

def get_args():
    # create argument parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        =========================================================================
        Description: run script including cycle and multiprocess.
        Version: 2022-05-30
        @Author: lyj
        """),
        epilog=textwrap.dedent("""
        Example: python run_script.py -i run.sh -t 20
        =========================================================================
        """))
    # add arguments
    parser.add_argument('-i', '--script', required=True,
                        help='to run script')
    parser.add_argument('-t', '--threads', default='20', 
                        help='Choice the number of threads')

    # convert the arguments to a dictionary
    args = parser.parse_args()
    return args

def run_script(sh_script, threads):
    sh_path = os.path.dirname(sh_script)
    sh_name = os.path.basename(sh_script)
    unfinish_sh = {}
    myfile = open(sh_script)
    numb = len(myfile.readlines())
    if os.path.exists('{0}/run_{1}/'.format(sh_path, sh_name)) and len(glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name))) == numb:
        if len(glob.glob('{0}/run_{1}/*.Check'.format(sh_path, sh_name))) == len(glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name))):
            print('Check last time run {} shell have completed.'.format(sh_script))
        else:
            for sh in glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name)):
                if os.path.exists('{}.Check'.format(sh)):
                    pass
                else:
                    k = 0
                    for efil in glob.glob('{}.*e*'.format(sh)):
                        #if os.path.getsize(efil) != 0:
                        k += 1  
                        #else:
                            #pass
                    if k == 3:
                        sys.exit()
                    else:
                        unfinish_sh[sh] = k
            multi_process(unfinish_sh, threads)
            run_script(sh_script, threads)
    else:
        subprocess.call('mkdir -p {0}/run_{1}/'.format(sh_path, sh_name), shell=True)
        subprocess.call('cd {3}/run_{4}/ && csplit {0} /\\n/ -n {1} -s {{*}} -f {2} -b \'%0{1}d.sh\''.format(sh_script, len(str(numb)), sh_name.replace("sh", ""), sh_path, sh_name), shell=True)
        subprocess.call('rm {0}/run_{1}/*.*00.sh {0}/run_{1}/*.0.sh'.format(sh_path, sh_name), shell=True)
        for sh in glob.glob('{0}/run_{1}/*.sh'.format(sh_path, sh_name)):
            subprocess.call('sed -i "$ s|$| \&\& echo This-Work-is-Completed! \&\& touch {0}.Check|" {0}'.format(sh), shell=True)
            unfinish_sh[sh] = 0
        #print(unfinish_sh.items())
        multi_process(unfinish_sh, threads)
        run_script(sh_script, threads)

def multi_process(script_dict, threads):
    # printing main program process id 
    print("ID of main process: {}".format(os.getpid())) 
    
    tmp = {}
    for i in range(threads):
        while len(script_dict) != 0:
            tmp[list(script_dict.keys())[0]] = script_dict[list(script_dict.keys())[0]]
            del script_dict[list(script_dict.keys())[0]]
    # creating processes
    proc = []
    if len(list(tmp.keys())) < threads:
        for t in range(len(list(tmp.keys()))):
            proc.append(multiprocessing.Process(target=run_cycle, args=(list(tmp.keys())[t], tmp[list(tmp.keys())[t]])))
    else:
        for t in range(threads):
            proc.append(multiprocessing.Process(target=run_cycle, args=(list(tmp.keys())[t], tmp[list(tmp.keys())[t]])))

    # starting processes
    k = 1
    for p in proc:
        p.start() 
        print("ID of the {0} process: {1}".format(k, p.pid))
        time.sleep(10)
        k += 1
    # wait until processes are finished
    for p in proc:
        p.join() 

def run_cycle(key, val):
    if val == 1:
        print('throw job {0} in the 2 cycle\n'.format(key))
        #print("That will continue the uncomplete jobs.\n")
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            val += 1
            run_cycle(key, val)
    elif val == 2:
        print('throw job {0} in the 3 cycle\n'.format(key))
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            print('Program stopped because the rerun cycle number has reached 3, the {} jobs unfinished.'.format(key))
            os._exit(0)
            sys.exit() 
    elif val == 3:
        print('Program stopped because the rerun cycle number has reached 3, the {} jobs unfinished.'.format(key))
        os._exit(0)
        sys.exit() 
    else:
        print('throw job {0} in the 1 cycle\n'.format(key))
        subprocess.run('bash {0} >>{0}.{1}o{2} 2>>{0}.{1}e{2}'.format(key, val+1, int(time.time())), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        time.sleep(5)
        if os.path.exists('{}.Check'.format(key)):
            pass
        else:
            val += 1
            run_cycle(key, val)


if __name__ == "__main__":
    args = get_args()
    print('Number of CPUs in the system: {}'.format(os.cpu_count()))
    run_script(args.script, int(args.threads))
