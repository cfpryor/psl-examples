import os
import re
import sys
import shutil
import subprocess
import tempfile

CLI_RUN='run.sh'
DATA_PATH='../data'
RESULTS='Results'

DATA_DIR=os.path.join(DATA_PATH, 'entity-resolution')
FETCH_PATH=os.path.join(DATA_PATH, 'fetchData.sh')

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = tempfile.mkstemp()
    with os.fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.find(pattern) != -1:
                    new_file.write(subst)
                else:
                    new_file.write(line)
    #Remove original file
    os.remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)
    os.system("chmod +x " + file_path)

def resetData(patternReplace, patternRemove = 'readonly RAW_DATA_NAME=\'entity-resolution-'):
    fullpattern = patternRemove+patternReplace+'\'\n'
    replace(FETCH_PATH, patternRemove, fullpattern)
    if os.path.isdir(DATA_DIR):
        shutil.rmtree(DATA_DIR)

    for item in os.listdir(DATA_PATH):
        if item.endswith(".tar.gz"):
            os.remove(os.path.join(DATA_PATH, item))

def weightLearning(weightlearning):
    if(weightlearning):
        replace(CLI_RUN, '# runWeightLearning', '   runWeightLearning\n')
    else:
        replace(CLI_RUN, '  runWeightLearning', '   # runWeightLearning\n')

def run(runtype):
    subprocess.call(['../data/fetchData.sh'])
    os.system("mkdir ../data/entity-resolution")
    os.system("mv entity-resolution/* ../data/entity-resolution")
    os.system("mv *.tar.gz ../data")
    os.system("rm -R entity-resolution/")
    os.system("python3 makeAuthorBlocks.py ../data/entity-resolution/learn/authorName_obs.txt > ../data/entity-resolution/learn/authorBlock_obs.txt")
    os.system("python3 makeAuthorBlocks.py ../data/entity-resolution/eval/authorName_obs.txt > ../data/entity-resolution/eval/authorBlock_obs.txt")

    if (runtype == 1):
        os.system("cp pslModels/entity-resolution-all-blocking.psl entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-all-blocking.psl entity-resolution-learned.psl")
    if (runtype == 2):
        os.system("cp pslModels/entity-resolution-blocking.psl entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-blocking.psl entity-resolution-learned.psl")
    if (runtype == 3):
        os.system("cp pslModels/entity-resolution-no-blocking.psl  entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-no-blocking.psl  entity-resolution-learned.psl")
    if (runtype == 4):
        os.system("cp pslModels/entity-resolution-all-blocking-transitivity.psl entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-all-blocking-transitivity.psl entity-resolution-learned.psl")
    if (runtype == 5):
        os.system("cp pslModels/entity-resolution-blocking-transitivity.psl entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-blocking-transitivity.psl entity-resolution-learned.psl")
    if (runtype == 6):
        os.system("cp pslModels/entity-resolution-no-blocking-transitivity.psl entity-resolution.psl")
        os.system("cp pslModels/entity-resolution-no-blocking-transitivity.psl entity-resolution-learned.psl")

    os.system("./run.sh >out.txt 2>err.txt")

def cleanup(outdir, outpath):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    os.system("mv out.txt "+outpath)
    os.system("mv err.txt "+outpath)
    os.system("mv inferred-predicates "+outpath)
    os.system("mv entity-resolution-learned.psl "+outpath)

if __name__ == '__main__':
    work = [
            ['small', False, 6, 'Results/Small/', 'NoBlockingTransitivityNoWeight'],
            ['small', True, 6, 'Results/Small/', 'NoBlockingTransitivityWeight'],
            ]
    '''work = [
            ['small', True, 4, 'Results/Small/', 'AllBlockingTransitivityWeight'],
            ['small', False, 4, 'Results/Small/', 'AllBlockingTransitivityNoWeight'],
            ['medium', True, 4, 'Results/Medium/', 'AllBlockingTransitivityWeight'],
            ['medium', False, 4, 'Results/Medium/', 'AllBlockingTransitivityNoWeight'],
            ['large', True, 4, 'Results/Large/', 'AllBlockingTransitivityWeight'],
            ['large', False, 4, 'Results/Large/', 'AllBlockingTransitivityNoWeight'],
            ['small', True, 6, 'Results/Small/', 'NoBlockingTransitivityWeight'],
            ['small', False, 6, 'Results/Small/', 'NoBlockingTransitivityNoWeight'],
            
            ['small', True, 1, 'Results/Small/', 'AllBlockingWeight'],
            ['small', False, 1, 'Results/Small/', 'AllBlockingNoWeight'],
            ['medium', True, 1, 'Results/Medium/', 'AllBlockingWeight'],
            ['medium', False, 1, 'Results/Medium/', 'AllBlockingNoWeight'],
            ['large', True, 1, 'Results/Large/', 'AllBlockingWeight'],
            ['large', False, 1, 'Results/Large/', 'AllBlockingNoWeight'],
            
            ['small', True, 2, 'Results/Small/', 'BlockingWeight'],
            ['small', False, 2, 'Results/Small/', 'BlockingNoWeight'],
            ['medium', True, 2, 'Results/Medium/', 'BlockingWeight'],
            ['medium', False, 2, 'Results/Medium/', 'BlockingNoWeight'],
            ['large', True, 2, 'Results/Large/', 'BlockingWeight'],
            ['large', False, 2, 'Results/Large/', 'BlockingNoWeight'],
            
            ['small', True, 5, 'Results/Small/', 'BlockingTransitivityWeight'],
            ['small', False, 5, 'Results/Small/', 'BlockingTransitivityNoWeight'],
            ['medium', True, 5, 'Results/Medium/', 'BlockingTransitivityWeight'],
            ['medium', False, 5, 'Results/Medium/', 'BlockingTransitivityNoWeight'],
            ['large', True, 5, 'Results/Large/', 'BlockingTransitivityWeight'],
            ['large', False, 5, 'Results/Large/', 'BlockingTransitivityNoWeight'],
            
            ['small', True, 3, 'Results/Small/', 'NoBlockingWeight'],
            ['small', False, 3, 'Results/Small/', 'NoBlockingNoWeight'],
            ['medium', True, 3, 'Results/Medium/', 'NoBlockingWeight'],
            ['medium', False, 3, 'Results/Medium/', 'NoBlockingNoWeight'],
            ]'''

    for item in work: 
        resetData(item[0])
        weightLearning(item[1])
        run(item[2])
        cleanup(item[3], os.path.join(item[3], item[4]))



