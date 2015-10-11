import urllib as u
import requests
import cookielib

import Tkinter

class Attendance(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.query = ""
        self.initialize()
        

    def initialize(self):
        self.grid()
        self.entryVariable = Tkinter.StringVar()
        self.entryVariable2 = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry2 = Tkinter.Entry(self,textvariable=self.entryVariable2)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry2.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entry2.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter rollno here(.eg. 1 ).")
        self.entryVariable2.set(u"Enter the course here...")
        button = Tkinter.Button(self,text=u"Show Attendance!",command=self.OnButtonClick)
        button.grid(column=1,row=0)
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello please give a rollno")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        self.entry2.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        self.downloadstuff("opening result for roll no: "+self.entryVariable.get()+" in dept: "+self.entryVariable2.get()+" (You pressed ENTER)")
        
        
    def OnPressEnter(self,event):
        self.labelVariable.set( "opening result for roll no: "+self.entryVariable.get()+" in dept: "+self.entryVariable2.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.downloadstuff(self.entryVariable.get(),self.entryVariable2.get())


    def getname(self,urls):
        from BeautifulSoup import BeautifulSoup as Soup
        from BeautifulSoup import SoupStrainer
        import re
        import urllib2
        try:
            soup=Soup(urls, parseOnlyThese=SoupStrainer("td"))
            y = re.findall(r'<b.*?>(.*?)</b>',str(soup))
            return y[1]
        except:
            print("nothing to download")

        
    def download(self,html,filename):
        html = html.text
        html = html.encode('utf-8')
        html = str(html)
        f = open(filename,'w')
        f.write(html)
        f.close()

    def getpage(self,theurl,args,s):
        username = ''
        password = ''
        acc_pwd = dict([(k, v) for k,v in zip (args[::2], args[1::2])])
        r = s.get(theurl,stream=True)
        r = s.post(theurl, data=acc_pwd)
        if 'drpcourse' and 'txtrollno' in acc_pwd:
            username = acc_pwd['drpcourse']
            password = acc_pwd['txtrollno']
            data = r.text
            name=self.getname(data)
            try:
                if 'User Name' not in name:
                    print name
                    print str(".//"+username+"-"+name+".html")
                    self.download(r,".//"+str(username)+"-"+str(name)+".html")
                    import webbrowser
                    theurl = str(username)+"-"+str(name)+".html"
                    
                    webbrowser.open(theurl)
            except:
                print("nothing to print")

    def downloadstuff(self,r,dep):
        dept = str(dep)
        rollno = self.getrollnos(int(r),int(r)+1)
        s = requests.Session()
        self.getpage('http://xaviers.edu.in/demouser/Checklogin.php',['myusername', dept, 'mypassword', rollno, 'Submit', 'Login'],s)
        self.getpage('http://xaviers.edu.in/demouser/StudentAttendance.php',['drpcourse', dept, 'txtrollno', rollno, 'Submit', 'Show Attendance'],s)
        s.close()

    
    def getrollnos(self,start,end):
        rollnos = []
        for i in range(start,end):
            if len(str(i))>1:
                i = "0"+str(i)
                rollnos.append(i)
            elif len(str(i)) == 1:
                i = "00"+str(i)
                rollnos.append(i)
        return rollnos

    def openpage(self,url):
        f = open(url,'r')
        for i in f.readlines():
            return i
#################################################


if __name__ == "__main__":
    app = Attendance(None)
    app.title('YOUR ATTENDANCE')
   
    app.mainloop()
    



