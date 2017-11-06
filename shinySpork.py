import sys
from functions import *

if len(sys.argv) == 3 and os.path.isfile(sys.argv[2]):
    print('Checking solution for', sys.argv[1],'.')
    status, _ = shinySpork(sys.argv[1], sys.argv[2])
    if status is True:
        print('\t Good solution!')
    else:
        print('\t Wrong solution!')
else:
    print("Generating solution for ", sys.argv[1], '.')
    if len(sys.argv) == 2:
        shinySpork(sys.argv[1], False)
    else:
        shinySpork(sys.argv[1], sys.argv[2])
