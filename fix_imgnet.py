


infile = 'imagenet_class_index.json'

f = open(infile,'r')
fstring = f.read()
f.close()
print(fstring[:100])


fstring = fstring.replace('{','')
fstring = fstring.replace('}','')

fstring = fstring.replace('], ','\n')
fstring = fstring.replace(', ','\t')
fstring = fstring.replace(': [','\t')
fstring = fstring.replace('"','')

f = open('fixed_'+infile,'w+')
fstring = f.write(fstring)
f.close()

#print(fstring[:100])
