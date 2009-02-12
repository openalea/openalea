import os


filename = './deploygui/openalea_deploygui_alea_install_gui_ref.rst'
text = open(filename).read()


foutput = open(filename, 'w')

#search for everything before 'Inheritance diagram'
# and write it
text = text.split('- Inheritance diagram:')



foutput.write(text[0])

#Then, all the remaining part except the diagram inheritance part
for line in text[1].split('\n'):
    if ':parts: 2' in line or 'inheritance-diagram' in line:
        continue
    else:
        foutput.write(line +'\n')
foutput.close()


