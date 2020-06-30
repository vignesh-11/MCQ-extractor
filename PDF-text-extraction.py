import fitz
import re
import json
pdf_document = 'general_science.pdf'
text_file = open('content.txt', 'w', encoding='utf-8')
doc = fitz.open(pdf_document)
for i in range(10,140):
        page1 = doc.loadPage(i)
        page1text = page1.getText('text')
        text_file.write(page1text)
doc.close()
text_file.close()
output = open('output.json', 'w', encoding='utf-8')

questions = []

with open(file='content.txt', mode='r', encoding='utf8') as f:
    lines = f.readlines()

    is_label = False  # means matched: 17.|(a)|(b)|(c)|(d)
    statement = ''
    option_a = ''
    option_b = ''
    option_c = ''
    option_d = ''
    is_statement = False
    is_option_a = False
    is_option_b = False
    is_option_c = False
    is_option_d = False
    question_no = 1
    for line in lines:
        if re.match(r'^\d+\.$', line):
            is_statement = is_label = True
            is_option_a = is_option_b = is_option_c = is_option_d = False
        elif re.match(r'^\(a\)$', line):
            is_option_a = is_label = True
            is_statement = is_option_b = is_option_c = is_option_d = False
        elif re.match(r'^\(b\)$', line):
            is_option_b = is_label = True
            is_statement = is_option_a = is_option_c = is_option_d = False
        elif re.match(r'^\(c\)$', line):
            is_option_c = is_label = True
            is_statement = is_option_a = is_option_b = is_option_d = False
        elif re.match(r'^\(d\)$', line):
            is_option_d = is_label = True
            is_statement = is_option_a = is_option_b = is_option_c = False
        else:
            is_label = False

        if is_label:
            continue

        if is_statement:
            statement += line
        elif is_option_a:
            option_a = line.rstrip()
        elif is_option_b:
            option_b = line.rstrip()
        elif is_option_c:
            option_c = line.rstrip()
        elif is_option_d:
            option_d = line.rstrip()

            if statement:
                statement = re.sub(r"\n|\u2018|\u2019|\u00ba|\u00b0|\u2013|\u00ae|\u2014", " ", statement)
                option_a = re.sub(r'\u2013|\u00ba|\u00b0|\u2019|\u00bd|\u2014|\u00d7',"", option_a)
                option_b = re.sub(r'\u2013|\u00ba|\u00b0|\u2019|\u00bd|\u2014|\u00d7',"", option_b)
                option_c = re.sub(r'\u2013|\u00ba|\u00b0|\u2019|\u00bd|\u2014|\u00d7',"", option_c)
                option_d = re.sub(r'\u2013|\u00ba|\u00b0|\u2019|\u00bd|\u2014|\u00d7',"", option_d)

                option_a = re.sub(r'\u00be\u00be\u00ae',"---->", option_a)
                option_b = re.sub(r'\u00be\u00be\u00ae',"---->", option_b)
                option_c = re.sub(r'\u00be\u00be\u00ae',"---->", option_c)
                option_d = re.sub(r'\u00be\u00be\u00ae',"---->", option_d)
                questions.append({
                    'question (' + str(question_no) + ')': statement.rstrip(),
                    'options': ['(a)' + option_a, '(b)' +  option_b,'(c)' +  option_c, '(d)' + option_d]
                })
                statement = option_a = option_b = option_c = option_d = ''
                question_no = question_no + 1
output.write(json.dumps(questions, indent=4))
f.close()
output.close()
