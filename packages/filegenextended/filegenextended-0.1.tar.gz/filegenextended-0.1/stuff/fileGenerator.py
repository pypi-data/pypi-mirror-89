import os.path
def genFile(fileName):
    # file = open(fileName+'.'+fileExtension, 'w')
    file = open(fileName+'.txt', 'w')
    file.write('Автоматически сгенерированный текст, генератор: ' + os.path.basename(__file__))
    file.close()
pass