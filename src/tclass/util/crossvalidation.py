#encoding: utf8
"""
N-fold crossvalidation implementation.

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from time import clock
from xml.dom.minidom import Document

from tclass.util.metrics import Measures

def cross_validation(corpus, classifier, real_class, iterations, \
                     quotient, result_file, name = "Validation"):
    """
    @param iterations: int. Number of iterations
    @param quotient: float. Size of the training partition relative to the
                            whole corpus size.
    @param name: (optional) string. Basename of the log files.
    """
    
    print str(quotient * 100) + '% of the corpus used for training.'
    
    f = open("validation.log","wt")
    fi = open (result_file, "at")
    
    start = clock()
    F1 = [0,0,100]
    Recall = [0,0,100]
    Precision = [0,0,100]
    for i in range(iterations):
        print "\n\nIteration " + str(i+1)
        f.write(str(i)+" ")
        (train, test) = corpus.partition(quotient)
#        print train, test
        classifier.train(train, real_class)
        (result, ids) = classifier.classify(test)
        classifier.clear()
        measures = Measures(test, real_class, result)
        recall = measures.recall()*100
        precision = measures.precision()*100
        f_1 = measures.f_1()*100
        print 'recall: '+str(recall)+'%'
        f.write(str(recall)+" ")
        print 'precision: '+str(precision)+'%'
        f.write(str(precision)+" ")
        print 'f1: '+str(f_1)+'%'
        f.write(str(f_1)+"\n")
        F1[0] += f_1
        Recall[0] += recall
        Precision[0] += precision
        if recall > Recall[1]:
            Recall[1] = recall
        if recall < Recall[2]:
            Recall[2] = recall
        if precision > Precision[1]:
            Precision[1] = precision
        if precision < Precision[2]:
            Precision[2] = precision
        if f_1 > F1[1]:
            F1[1] = f_1
        if f_1 < F1[2]:
            F1[2] = f_1
        f1 = open (name + str(i), "wt")
        for line in result:
            f1.write(str(line)+"\n")
        f1.close()
        
    end = clock()
    print "\n-----------------------\nAverage time used for each task: " + \
          str((end-start)/iterations) + " seconds"
    print "Average f1 = " + str(F1[0]/iterations) + "%"
    print "Average precision = " + str(Precision[0]/iterations) + "%"
    print "Average recall = " + str(Recall[0]/iterations) + "%"
    
    print "Best f1 = " + str(F1[1]) + "%"
    print "Best precision = " + str(Precision[1]) + "%"
    print "Best recall = " + str(Recall[1]) + "%"
    
    print "Worst f1 = " + str(F1[2]) + "%"
    print "Worst precision = " + str(Precision[2]) + "%"
    print "Worst recall = " + str(Recall[2]) + "%"
    
    f.close()
    fi.write("%f    %f    %f    %f    %f    %f    %f    %f    %f    %f    %f\n"\
            % (quotient, Recall[0]/iterations, Recall[0]/iterations, \
               F1[0]/iterations, Recall[1], Precision[1], F1[1], Recall[2],\
               Precision[2], F1[2], (end-start)/iterations))
    fi.close()
        
    
    
def cross_validation_xml(corpus, classifier, real_class, iterations, \
                     quotient, result_file, name = "Validation"):
    """
    @param iterations: int. Number of iterations
    @param quotient: float. Size of the training partition relative to the
                            whole corpus size.
    @param name: (optional) string. Basename of the log files.
    """
    
    print str(quotient * 100) + '% of the corpus used for training.'
    
    # abre o arquivo de resultado de classificacao
    used = open ("Log/"+name+".xml" , "wt")
    dom = Document()
    teste = dom.createElement('Teste')
    dom.appendChild(teste)
    
    start = clock()
    F1 = 0
    Recall = 0
    Precision = 0
    maxF1 = 0
    maxRec = 0
    maxPre = 0
    
    _file = open ("Log/"+result_file, "wt")
    _file.write("Treino ;Iteracao ;Precision ;Recall ;F1;\n")
    for i in range(iterations):
        print "\n\nIteration " + str(i+1)
        _file.write(str(quotient * 100)+"%;"+ str(i)+";")
        (train, tes) = corpus.partition(quotient)
#        print train, test
        classifier.train(train, real_class)
        (result, ids) = classifier.classify(tes)
        classifier.clear()
        measures = Measures(tes, real_class, result)        
        
        # Calcula as variaveis
        pre = measures.recall()*100
        if(pre > maxPre):
            maxPre = pre 
        rec = measures.precision()*100
        if(rec > maxRec):
            maxRex = rec
        f1 = measures.f_1()*100
        if(f1 > maxF1):
            maxF1 = f1
            
        # Escreve na tela os resultados
        print 'recall: '+str(pre)+'%'
        _file.write(str(pre)+";")
        print 'precision: '+str(rec)+'%'
        _file.write(str(rec)+";")
        print 'f1: '+str(f1)+'%'
        _file.write(str(f1)+";\n")
        F1 += f1
                
        # obtem os dados do corpus que sera usado no teste
        test = tes.get_documents()
        nomes = tes.get_classes()
#       numero = ts.getnum()
        
        # gerando o xml de saida
        y = w= z= 0
        iteracao = dom.createElement('Iteracao')
        teste.appendChild(iteracao)
        iteracao.setAttribute("num",str(i))
        iteracao.setAttribute("precision",str(pre))
        iteracao.setAttribute("recall",str(rec))
        iteracao.setAttribute("f1",str(f1))
        while y < len(test):
            nomes2 = nomes["list"][y].split("\\")
            tipoCritica = dom.createElement(nomes2[len(nomes2)-2])
            iteracao.appendChild(tipoCritica)
            while z < len(test[y]):
                critica = dom.createElement('Critica')
                tipoCritica.appendChild(critica)
#               critica.setAttribute("id",str(numero[y][z]))
                critica.setAttribute("result",repr(result[z+w]))
                bag = dom.createElement('BagOfWords')
                critica.appendChild(bag)
                words = ""
                for numword in test[y][z]:
                    words = words +tes.lex_word(numword).encode("UTF-8")+" "
                cddata = dom.createCDATASection(words)
                bag.appendChild(cddata)
                z += 1
            w=z
            z=0
            y += 1
        
    end = clock()
    time = str((end-start)/iterations)
    resultado = dom.createElement('Resultado')
    teste.appendChild(resultado)
    resultado.setAttribute("maxprecision",str(maxPre))
    resultado.setAttribute("maxrecall",str(maxRec))
    resultado.setAttribute("maxf1",str(maxF1))
    resultado.setAttribute("tempo",str(time))
    dom.writexml(used,""," ",'\n',"utf-8")
    print "\n-----------------------\nAverage time used for each task: "+time+" seconds"
    print "Average f1 = "+str(F1/iterations)+"%"
    print "tempo total = "+str(end-start)
    used.close()
    _file.close()





