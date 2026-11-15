import re,sys,zipfile,shutil,os
src=sys.argv[1]; tmp=src+'.tmp'
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
n=0
def fix(m):
    global n
    body=m.group(1)
    MK=r'<w:(?:ins|del|moveFrom|moveTo)\b[^>]*?(?:/>|>\s*</w:(?:ins|del|moveFrom|moveTo)>)'
    marks=re.findall(MK,body)
    if not marks: return m.group(0)
    rest=re.sub(MK,'',body)
    if body.startswith(''.join(marks)): return m.group(0)
    n+=1
    return '<w:rPr>'+''.join(marks)+rest+'</w:rPr>'
for it in zin.infolist():
    data=zin.read(it.filename)
    if it.filename=='word/document.xml':
        x=data.decode('utf8')
        x=re.sub(r'<w:rPr>((?:(?!</w:rPr>|<w:rPr>).)*?)</w:rPr>',fix,x,flags=re.S)
        data=x.encode('utf8')
    zout.writestr(it,data)
zout.close(); zin.close(); shutil.move(tmp,src); print(src.split('/')[-1],'rPr reordenados:',n)
