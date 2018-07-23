import os
import re
INFERENCE_COMPLETE = 'Inference complete.'
EVALUATION_RESULTS = 'Evaluation results for'

def loadData(file_path, findList=[INFERENCE_COMPLETE,EVALUATION_RESULTS]):
    returnList = []
    with open(file_path) as file:
        for line in file:
            for find in findList:
                if find in line:
                    cleanline = re.sub(r'[^0-9a-zA-Z.]', ' ', line)
                    cleanline = re.sub(r'\s+', ' ', cleanline).strip()
                    returnList.append(cleanline.split(' '))
    return returnList

def writeData(size, weight, transitivity, blocking, results, file='results.csv'):
    if not os.path.isfile(file):
        with open(file, "w") as f:
            key = "Size,Weight Learning,Transitivity,Blocking,Inference Time(ms),Total Time(ms),Author - Accuracy,Author - F1,Author - Positive Class Precision,Author - Positive Class Recall,Author - Negative Class Precision,Author - Negative Class Recall,Paper - Accuracy,Paper - F1,Paper - Positive Class Precision,Paper - Positive Class Recall,Paper - Negative Class Precision,Paper - Negative Class Recall\n"
            f.write(key)
        f.close()
    with open(file, "a") as f:
        key = size+","+weight+","+transitivity+","+blocking+","+results[0][0]+","+results[1][0]+","+results[1][9]+","+results[1][11]+","+results[1][15]+","+results[1][19]+","+results[1][23]+","+results[1][27]+","+results[2][9]+","+results[2][11]+","+results[2][15]+","+results[2][19]+","+results[2][23]+","+results[2][27]+"\n"
        f.write(key)

if __name__ == '__main__':
    writeData('small', 'True', 'False', 'All', loadData('Results/Small/AllBlockingWeight/out.txt'))
    writeData('small', 'False', 'False', 'All', loadData('Results/Small/AllBlockingNoWeight/out.txt'))
    writeData('medium', 'True', 'False', 'All', loadData('Results/Medium/AllBlockingWeight/out.txt'))
    writeData('medium', 'False', 'False', 'All', loadData('Results/Medium/AllBlockingNoWeight/out.txt'))
    writeData('large', 'True', 'False', 'All', loadData('Results/Large/AllBlockingWeight/out.txt'))
    writeData('large', 'False', 'False', 'All', loadData('Results/Large/AllBlockingNoWeight/out.txt'))
    
    writeData('small', 'True', 'True', 'All', loadData('Results/Small/AllBlockingTransitivityWeight/out.txt'))
    writeData('small', 'False', 'True', 'All', loadData('Results/Small/AllBlockingTransitivityNoWeight/out.txt'))
    writeData('medium', 'True', 'True', 'All', loadData('Results/Medium/AllBlockingTransitivityWeight/out.txt'))
    writeData('medium', 'False', 'True', 'All', loadData('Results/Medium/AllBlockingTransitivityNoWeight/out.txt'))
    writeData('large', 'True', 'True', 'All', loadData('Results/Large/AllBlockingTransitivityWeight/out.txt'))
    writeData('large', 'False', 'True', 'All', loadData('Results/Large/AllBlockingTransitivityNoWeight/out.txt'))
    
    writeData('small', 'True', 'False', 'Transitivity', loadData('Results/Small/BlockingWeight/out.txt'))
    writeData('small', 'False', 'False', 'Transitivity', loadData('Results/Small/BlockingNoWeight/out.txt'))
    writeData('medium', 'True', 'False', 'Transitivity', loadData('Results/Medium/BlockingWeight/out.txt'))
    writeData('medium', 'False', 'False', 'Transitivity', loadData('Results/Medium/BlockingNoWeight/out.txt'))
    writeData('large', 'True', 'False', 'Transitivity', loadData('Results/Large/BlockingWeight/out.txt'))
    writeData('large', 'False', 'False', 'Transitivity', loadData('Results/Large/BlockingNoWeight/out.txt'))
    
    writeData('small', 'True', 'True', 'Transitivity', loadData('Results/Small/BlockingTransitivityWeight/out.txt'))
    writeData('small', 'False', 'True', 'Transitivity', loadData('Results/Small/BlockingTransitivityNoWeight/out.txt'))
    writeData('medium', 'True', 'True', 'Transitivity', loadData('Results/Medium/BlockingTransitivityWeight/out.txt'))
    writeData('medium', 'False', 'True', 'Transitivity', loadData('Results/Medium/BlockingTransitivityNoWeight/out.txt'))
    writeData('large', 'True', 'True', 'Transitivity', loadData('Results/Large/BlockingTransitivityWeight/out.txt'))
    writeData('large', 'False', 'True', 'Transitivity', loadData('Results/Large/BlockingTransitivityNoWeight/out.txt'))

    writeData('small', 'True', 'False', 'None', loadData('Results/Small/NoBlockingWeight/out.txt'))
    writeData('small', 'False', 'False', 'None', loadData('Results/Small/NoBlockingNoWeight/out.txt'))
    writeData('medium', 'True', 'False', 'None', loadData('Results/Medium/NoBlockingWeight/out.txt'))
    writeData('medium', 'False', 'False', 'None', loadData('Results/Medium/NoBlockingNoWeight/out.txt'))
