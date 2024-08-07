from pypdf import PdfReader
import textwrap
global content
global gifts
global content2
def readForm():
    reader = PdfReader('Spiritual Gifts Assessment Frat.pdf')
    pdf_content = ""
    for i, pdf_page in enumerate(reader.pages):
        pdf_content = pdf_content + pdf_page.extract_text()
    global content
    global content2
    content = pdf_content
    content2 = pdf_content
    GrabGifts()

def GrabGifts():
    global content
    global gifts
    start_phrase ="Body of Christ and the local church."
    end_phrase = "SPIRITUAL GIFTS WORKSHEET"
    gifts = content[content.index(end_phrase):]
    content = content[content.index(start_phrase)+len(start_phrase):content.index(end_phrase)]

def splitMarks():
    global content
    lst = []

    lst = content.split("Mark")
    for i, para in enumerate(lst):
        lst[i] = para.strip()
    return lst[1:]

def littleSplit():
    lst = splitMarks()
    for i, val in enumerate(lst):
        lst[i] = val[val.index("LITTLE NONE")+12:] #12 is size of little none plus extra space
    return lst

def intoStringToList():
    global content
    global content2
    lst = littleSplit()
    cont = "\n ".join(lst)
    bill = ""
    bill = cont.split("\n \n")
    for i,val in enumerate(bill):
        bill[i] = val[val.index(".")+1:]
    return bill

def removeSpace():
    global content
    lst = intoStringToList()
    for i, val in enumerate(lst):
        lst[i] = val.replace("\n", "")
    content = lst

def makeFile(): #DO NOT RERUN - MINOR ERRORS MANUALLY FIXED IN TXT FILE
    global content
    removeSpace()
    content = "\n".join(content)
    with open("Questions2.txt", "w") as output:
        output.write(content)
### RUN BELOW IF MODIFICATIONS ARE NEEDED, AVOID MODIFYING ABOVE

def get_questions():
    question_file = open("Questions2.txt", "r") 
    questions = question_file.read() 
    questions_into_list = questions.split("\n")
    question_file.close() 
    return questions_into_list

def CheckUnfiltered():
    global content2
    removeSpace()
    return content2 

readForm()