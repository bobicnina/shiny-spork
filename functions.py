import os.path

''' shinySpork

    file in Dimacs format  -->  file in which we write the solution
                                (if output file is not defined,
                                 it is named "_solution.txt")       '''

def shinySpork(fileInput, fileOutput):
    cnf, nbvar, nbclauses = readFile(fileInput)
    status, _, values = dpll(cnf, nbvar, dict())

    if fileOutput is False:                         
        fileOutput = fileInput.replace('.txt', '_solution.txt')
        writeFile(values, fileOutput)               #write solution to file

    elif not os.path.isfile(fileOutput):            
        writeFile(values, fileOutput)               #output filename is given

    else:                                           
        res = []
        for key, value in values.items():
            if value:
                res.append(key)                     
            else:
                res.append(-key)                    

        file = open(fileOutput)
        lines = file.readlines()
        solution = lines[0].split()
        goodSol = True

        for i in range(0, len(res)):                #check solution
            r = res[abs(int(solution[i]))-1]
            if r != int(solution[i]):
                goodSol = False
                return False, dict()                #we didn't find a satisfying
                break                               #valuation

        if goodSol is True:
            return True, dict()                     #cnfFormula is satisfiable
                                                    #and we have a solution


''' readFile

    file in DIMACS format  -->  cnfFormula in CNF, nb of all variables in CNF,
                                nb of clauses in cnfFormula  '''

def readFile(inputFile):
    file = open(inputFile)
    lines = file.readlines()
    nbvar = 0
    nbclauses = 0
    cnf = []
    
    for line in lines:
        if line[0] == 'c':
            continue
        elif line[0] == 'p':
            nb = [int(s) for s in line.split() if s.isdigit()]
            nbvar = nb[0]
            nbclauses = nb[1]
            continue
        else:
            cnfFormula = {}
            for n in line.split():
                n = int(n)
                if n < 0:
                    cnfFormula[abs(n)] = False
                elif n > 0:
                    cnfFormula[n] = True
            cnf.append(cnfFormula)
          
    return cnf, nbvar, nbclauses


''' writeFile

    solution as list of variables  -->  file in which we write the solution  '''

def writeFile(solution, file):
    openF = open(file, 'w')
    for key, value in solution.items():
        if value:
            openF.write(str(key) + ' ')
        else:
            openF.write(str(-key) + ' ')
    openF.close()

''' findAllVars

    cnfFormula in CNF  -->  list of all variables which appear in cnfFormula '''

def findAllVars(phi):
    vars = set()
    for c in phi:                   
        for l in c:           #go through formula phi
            vars.add(l)       #add a variable to a list of variables
    return vars

''' findUnitAndPureClauses

    finding all variables and spliting them in two subsets:

subset called unit clauses where are variables from clauses with length = 1
subset called pure clauses where are variables from clauses with length > 1

    in both subsets are only variables which always appear in same form
    (e.g. True or False)

    cnfFormula in CNF, nb of all variables in CNF  -->
                unit clauses, pure clauses, nb of repeats for all variables '''

def findUnitAndPureClauses(phi, nbvar):
    unitClauses = dict()
    pureClauses = dict()
    nbOfRepeats = dict()
    
    ''' check cnfFormula and change value in dictionary
    possible dictionary's values: True  = appear as p
                                  False = appear as -p
                                  None  = appear as p and -p '''
    for l in phi:
        if len(l) == 1:                         #unit clause
            for var in l:               
                value = l[var]
                if var in unitClauses and value != unitClauses[var]: 
                    return False, False, False #if l and -l in it, clause can't be true
                elif not (var in unitClauses):
                    unitClauses[var] = value
    
    for l in phi:
        for var in l:                   #general case
            value = l[var]
            if var in unitClauses:  
                continue;               #var is already in unitClauses, skip
            
            if var in nbOfRepeats:
                nbOfRepeats[var] += 1
            else:
                nbOfRepeats[var] = 1
            
            if var in pureClauses:

                if pureClauses[var] is not value:
                    pureClauses[var] = None #var is already in pureClauses
                                            #but in other form, so we delete it
            else:
                pureClauses[var] = value    #var is not in pureClauses yet 
    
    pureClausesOld = dict(pureClauses)
    for var in pureClausesOld:
        value = pureClauses[var]
        if value is None:
            del pureClauses[var]
        else:
            del nbOfRepeats[var]    #if p=None then remove from pureClauses and fix nbOfRepeats
    
    return unitClauses, pureClauses, nbOfRepeats


''' simplify
 if p is True than remove all clauses where p appears
 if p is False than remove all variables from clauses where p appears
    
    cnfFormula in CNF, unit clauses, pure clauses, variables with set values,
    nb of repeats for all variables

        -->    

            updated cnfFormula in CNF, updated variables with set values,
            updated nb of repeats for all variables '''

def simplify(phi, unitClauses, pureClauses, values, nbOfRepeats):
    
    phiNew = list(phi)
    
    for l in unitClauses:                       #first check all unit clauses
        value = unitClauses[l]
        values[l] = value
        currentElement = dict()
        currentElement[l] = value
        if l not in pureClauses:
            if value is True:
                phiNew, nbOfRepeats = \
            removeCnfForm(phiNew, currentElement, nbOfRepeats)
                currentElement[l] = False
                phiNew = removeVar(phiNew, currentElement)
            else:
                phiNew, nbOfRepeats = \
                removeCnfForm(phiNew, currentElement, nbOfRepeats)
                currentElement[l] = True
                phiNew = removeVar(phiNew, currentElement)
        elif pureClauses[l] is True or pureClauses[l] is False:
            phiNew, nbOfRepeats = removeCnfForm(phiNew, currentElement, nbOfRepeats)
    
    for l in pureClauses:                           #then check all pure
        value = pureClauses[l]                      #clauses      
        currentElement = dict()
        currentElement[l] = value
        values[l] = value
        
        phiNew, nbOfRepeats = removeCnfForm(phiNew, currentElement, nbOfRepeats)
    
    return phiNew, values, nbOfRepeats


''' removeCnfForm

 cnfFormula in CNF, variable p with value (True or False),
 nb of repeats for all variables
         -->
             updated cnfFormula in CNF, updated nb of repeats for all variables '''

def removeCnfForm(phi, var, nbOfRepeats):
    newFormula = []
    for l in phi:
        for x in var:
            if x not in l or (x in l and var[x] is not l[x]):
                newFormula.append(l)
            else:
                for literal in nbOfRepeats:
                    if literal in l:
                        nbOfRepeats[literal] -= 1
    return newFormula, nbOfRepeats


''' removeVar
    cnfFormula in CNF, variable p with value (True or False)
        --> updated cnfFormula in CNF '''

def removeVar(phi, var):
    formulaNew = []
    for l in phi:
        lNew = dict(l)
        for x in var:
            if x in l and var[x] is l[x]:
                del lNew[x]
        formulaNew.append(lNew)
    return formulaNew


''' dpll
    cnfFormula in CNF, nb of all variables in CNF, variables with set values
        -->    
            boolean status if DPLL algorithm was successful or not,
            updated or old cnfFormula in CNF,
            updated or old variables with set values '''

def dpll(fiInput, nbvar, values):

    fiInput2 = list(fiInput)
    phiNew = list(fiInput2)
    vals = dict(values)
    
    while True:
        unitClauses, pureClauses, nbOfRepeats = findUnitAndPureClauses(fiInput2,
                                                                       nbvar)
        if unitClauses is False:
            return False, fiInput, vals
        
        if len(unitClauses) == 0 and len(pureClauses) == 0:
            break;
        
        phiNew, values, nbOfRepeats = simplify(fiInput2, unitClauses, pureClauses,
                                               values, nbOfRepeats)
        
        fiInput2 = list(phiNew)             #simplify as much as possible


    if len(phiNew) == 0:                    #phiNew is empty
        return True, [], values             #we solve it

    elif dict() in phiNew:                  #empty dictionary is member of cnfFormula
        return False, fiInput, dict();      #we can't solve it

    else:                                   #set any other var to True or
                                            #False and try again
        otherClauses = sorted(nbOfRepeats, key = nbOfRepeats.get, reverse=True)
        for otherClause in otherClauses:
            currentElement = dict()
            currentElement[otherClause] = True
            fiNew2 = list(phiNew)
            fiNew2.append(currentElement)
            status, oldFormula, values = dpll(fiNew2, nbvar, values)
            if status is False:
                fiNew2 = list(oldFormula)
                fiNew2[len(fiNew2)-1][otherClause] = False  #change currentElement
                                                            #value from True to False
                return dpll(fiNew2, nbvar, values)
            else:
                return True, oldFormula, values              #values.pop(otherClause, True)

















            
