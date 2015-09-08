

import os
import sys

dstfile = ''
dotfile = ''

def get_lines(path):
    
    f = open(path)
    lines = f.readlines()
    f.close()
    return lines

def set_lines(path,lines):
    
    f = open(path,'w')
    f.writelines(lines)
    f.close()
    
def egypt(argv):

 
    expandfiles = argv[1:]
    for elm in expandfiles:
        if not elm.strip().endswith('expand'):
            print 'srcfile name error: '+elm
    if not expandfiles:
        return []

    egypt_cmd = 'egypt '+' '.join(expandfiles)
    lines = os.popen(egypt_cmd).read()

    return lines.split('\n')

def get_primary_funcs(lines):

    leads = []
    staffs = [] 
    for line in lines:
        if line.find('->') == -1:
            continue

        elms = line.strip().split()
        lead = eval(elms[2])
        staff = eval(elms[0])
        if lead not in leads:
            leads.append(lead)
        if staff not in staffs:
            staffs.append(staff)

    # print 'leads  ----------'+str(leads)    
    in_use = []
    for lead in leads:
        if lead in staffs:
            in_use.append(lead) 
    # print 'in_use  ---------'+str(in_use)

    for lead in in_use:
        leads.remove(lead)

    # print 'leads  -----------'+str(leads)
    # print 'staffs  -----------'+str(staffs)
    return leads
 
def get_lead_lines(funcname,base_lines):
   
    lines = base_lines[:]
    
    funclist = []
    funclist.append(funcname)
    
    funclines = ['digraph callgraph {\n']
    while len(funclist) > 0:
    
        uselines = []
        newleads = []
        
        for line in lines:
            if line.find('->') == '-1':
                continue
            elms = line.strip().split()
            if len(elms) != 4:
                continue
            
            staff = eval(elms[0])
            lead = eval(elms[2])
            # print 'staff '+staff+'-- lead '+lead
            if lead in funclist:
                newleads.append(staff)

                funclines.append(line+'\n')
                uselines.append(line)
            
        for useline in uselines:
            lines.remove(useline)
        # print str(newleads) 
        funclist = newleads
    
    funclines.append('}\n')
    return funclines

def get2_lead_lines(funcname,base_lines):

    lines = base_lines[:]

    funclist = []
    funclist.append(funcname)

    funclines = ['digraph callgraph {\n']
    while len(funclist) > 0:

        uselines = []
        newleads = []

        for line in lines:
            if line.find('->') == '-1':
                continue
            elms = line.strip().split()
            if len(elms) != 4:
                continue

            staff = eval(elms[0])
            lead = eval(elms[2])
            # print 'staff '+staff+'-- lead '+lead
            if lead in funclist:
                newleads.append(staff)

                funclines.append(line+'\n')
                uselines.append(line)

        for useline in uselines:
            lines.remove(useline)
            base_lines.remove(useline)
        # print str(newleads) 
        funclist = newleads

    funclines.append('}\n')
    return funclines

def create_png(funcdot,funcpng):
    cmd = ' cat '+funcdot+'|'+'dot -Gsize=200,200 -Grankdir=LR -Tpng -o ' +funcpng
    os.system(cmd)

def main(argv):

    leaddir = 'dotpng'
    dotdir = 'dotpng/dot'
    pngdir = 'dotpng/png'
    if not os.path.exists(leaddir):
        os.system('mkdir -p '+dotdir)
        os.system('mkdir -p '+pngdir)

    lines = egypt(sys.argv)
    leads = get_primary_funcs(lines)
    print leads
#    return 
#    funcname = 'flashcache_map'
    for funcname in leads:
        lead_lines = get2_lead_lines(funcname,lines)

        funcdot = dotdir+'/'+funcname+'.dot'
        funcpng = pngdir+'/'+funcname+'.png' 
        set_lines(funcdot,lead_lines)
        create_png(funcdot,funcpng)

if __name__ == '__main__':

    main(sys.argv)


