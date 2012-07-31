#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import urllib.request
import re
from bs4 import BeautifulSoup
from tkinter import messagebox


root = Tk()#Toplevel(mroot)
root.minsize ( width=600, height=250 )
root.title("JNTUH Results")
firstframe = ttk.Frame(root)
firstframe.grid(pady=10)

# head
heading = ttk.Label(firstframe, text='JNTUH Results')
heading.grid()

# connect button def
def checkinternet(*args):
    try:
            urllib.request.urlopen('http://jntuh.ac.in/results/')
           
            geturls()
            getmyurls()
            secondframe.grid(column=0, row=0, sticky=N,pady=10)
            thirdframe.grid(column=1,row=0, sticky=N, pady=10)
            firstframe.destroy()

    except:
            checkmessege.set('Unable to connect to server \n check your internet connection or\n JNTU server is not responding')
   
   

checkmessege = StringVar()
#gui button and label

ttk.Button(firstframe, text="connect", command=checkinternet).grid(pady=10,padx=70)
ttk.Label(firstframe, textvariable=checkmessege).grid(pady=10,padx=10)
# end of firstframe



def geturls():
    res = open('tmpfr', 'w')
    page = urllib.request.urlopen('http://jntuh.ac.in/results/')
    parser = BeautifulSoup(page)

    reslist = parser.find_all('a')
   
    for e in reslist:
            print(e, file=res)

def getmyurls():               
    file2 = open('tmpfr', 'r')
    file3 = open('tmpr', 'w')
    for line in file2:
            if re.search('B.Tech.+R0[79]', line):
                    print(line, file=file3)
try:                   
    geturls()
    getmyurls()
except:
    pass


file4 = open('tmpr')
d = dict()
rtext =  ()
rlink =  ()
for line in file4:
    extract = BeautifulSoup(line)
    for link in extract.find_all('a'):
            rtext = rtext + (link.get_text(),)
            rlink = rlink + (link.get('href'),)
           




def getresultspage(purl):
        resultspage = urllib.request.urlopen(purl)
        rparser = BeautifulSoup(resultspage)
        itag = rparser.find('input',id='ecode', type='hidden')
        value = itag['value']
        return value
 
# second frame gui=================================================
#===================================================================
#=================================================================
lnames = StringVar(value=rtext)
 
def listbinding(*args):
        global clink
        idxs = reslinkbox.curselection()
        idx = int(idxs[0])
        # current link selected in the listbox by the user
        clink = rlink[idx]
 
secondframe = ttk.Frame(root)
#secondframe.grid(column=0, row=2, sticky=N,pady=10)
 
 
reslinkbox = Listbox(secondframe, listvariable=lnames, width=22)
reslinkbox.grid(column=0,row=0, sticky=N, padx=10, columnspan=2)
#binding
reslinkbox.bind('<<ListboxSelect>>', listbinding)
       
#
def abt():
        messagebox.showinfo(message= 'JNTUH results \nCSE: Aurora Technological Institute')
about = ttk.Button(secondframe, text='about', command=abt)
about.grid(column=0,row=1,pady=30)
 
 
 
def showresults(ht,ecode):
       
        respage = urllib.request.urlopen('http://jntuh.ac.in/results/htno/'+ht+'/'+ecode)
        resparser = BeautifulSoup(respage)
        try:
                infolisthtml = resparser.find_all('table')[0].find_all('td')
                markslisthtml = resparser.find_all('table')[1].find_all('td')
                markslist = list()
                for e in markslisthtml:
                        markslist.append(e.get_text())
               
                infolist = list()
                for e in infolisthtml:
                        infolist.append(e.get_text())
 
                return (infolist, markslist)
        except:
                print('invalid hall tikcet no')
                return ('invalid', 'hallticket')
 
 
#gui hall ticket page ==============================================================================================
def gethtno():
        infochildren = infoframe.children
        for e in infochildren:
                infochildren[e].grid_remove()
        markschildren = marksframe.children
        for e in markschildren:
                markschildren[e].grid_remove()
 
 
 
        recode = getresultspage(clink)
 
        value = htno.get() #stringvar method
       
 
        gminfolist =  showresults(value, recode)
        ginfolist = gminfolist[0]
        gmarkslist = gminfolist[1]
       
 
       
        irow = 0
        icolumn = 0
        for e in ginfolist:
                ttk.Label(infoframe, text=e).grid(column=icolumn, row=irow, sticky=W,padx=5, pady=1)
                icolumn+=1
                if icolumn==2:
                        icolumn=0
                        irow+=1
        mcolumn = 0
        mrow = 0
        for e in gmarkslist:
                ttk.Label(marksframe, text=e).grid(column=mcolumn, row=mrow, sticky=W, padx=5, pady=1)
                mcolumn+=1
                if mcolumn == 6:
                        mcolumn = 0
                        mrow+=1
       
        ht_entry.delete(0,'end')
 
 
 
 
 
 
 
       
thirdframe = ttk.Frame(root)
#thirdframe.grid(column=1,row=2,columnspan=3, sticky=N, pady=10)
 
 
htno = StringVar()
#input frame for entering hallticket and submit button
inputframe = ttk.Frame(thirdframe)
inputframe.grid(column=0,row=0)
 
 
infoframe = ttk.Frame(thirdframe)
marksframe = ttk.Frame(thirdframe)
 
infoframe.grid(column=0,row=1, pady=20, padx=5)
marksframe.grid(column=0,row=2)
 
infoframe['borderwidth'] = 1
infoframe['relief'] = 'groove'
 
marksframe['borderwidth'] = 1
marksframe['relief'] = 'sunken'
 
 
 
 
 
 
#inputframe
ht_entry = ttk.Entry(inputframe, width=10, textvariable=htno)
ht_entry.grid(column=0, row=0, sticky=W,padx=15)
submit = ttk.Button(inputframe, text='submit', command=gethtno)
submit.grid(column=2, row=0, sticky=W)
 
       
 
 
 
 
 
 
 
 
 
root.mainloop()

