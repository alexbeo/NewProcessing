import os

def convert_pdf_to_txt(file_name):

    txt_file_name = os.popen('p2t.bat' + ' ' + file_name).read()

if __name__ == '__main__':
    convert_pdf_to_txt('20191026_232600_pos_9411.pdf')

    list_of_line = []
    with open('20191026_232600_pos_9411.txt','r') as file:
        line = file.readline()
        while line:
            print(line)
            list_of_line.append(line)
            line = file.readline()

    print(len(list_of_line))
    count = 0
    contractlist = []
    while count < len(list_of_line):
        count += 7
        contractlist.append(list_of_line[26+count:33+count])

    for contract in contractlist[:-8]:
        print(contract)
