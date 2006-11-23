#!/usr/bin/python
__doc__="""Create_config_gui create the openalea config. Base directory is choosen with a TKinter ui"""


import Tkinter as tk
import tkFileDialog
import tkMessageBox

from create_config import *
import sys
import os

class App(tk.Frame):

    def __init__(self, master):
        """Create GUI"""
        self.init_config()

        tk.Frame.__init__(self, master, padx=40, pady=40)
        self.pack()

        w = tk.Label(self, text="OpenAlea Configuration", font=("Helvetica", 22,"bold"))
        w.pack(side=tk.TOP)

        self.subframe=tk.Frame(self, padx=40, pady=40)
        self.subframe.pack()
        
        w = tk.Label(self.subframe, text="\nChoose the OpenAlea base directory \n",justify=tk.LEFT)
        w.pack()
        
        self.entrytxt = tk.StringVar()
        self.entrytxt.set(self.config.prefix_dir)
        entry = tk.Entry(self.subframe, textvariable=self.entrytxt)
        entry.pack(side=tk.LEFT)

        button = tk.Button(self.subframe, text="Choose Directory", command=self.getPath)
        button.pack(side=tk.LEFT)

        ok = tk.Button(self, text="Next", command=self.onOk)
        ok.pack(side=tk.RIGHT, fill = tk.BOTH,expand = tk.YES )

        cancel = tk.Button(self, text="Cancel", command=self.onCancel)
        cancel.pack(side=tk.LEFT, fill = tk.BOTH, expand = tk.YES)


    def init_config(self):
        """Initialise OpenAlea configuration"""

        #get config object
        self.config=config(None)

    
    def getPath(self):
        dirPath = tkFileDialog.askdirectory(initialdir=self.entrytxt.get(), mustexist=0)
	if(dirPath and dirPath!='' and dirPath!='.'): self.entrytxt.set(dirPath)

    def onOk(self):

        prefix=os.path.normpath(self.entrytxt.get())

        self.config.prefix_dir=prefix

        #create config file
        self.config.create_namespace()
        self.config.write(pj(self.config.namespace,'config.py'))
        tkMessageBox.showinfo("Success", "Configuration file has been created.")

        #ask to install OpenAlea
        if (tkMessageBox.askyesno("Install", "Do you want to install OpenAlea ?")):
                    
            if(run_install()==0):
                tkMessageBox.showinfo("Success", "OpenAlea has been sucessfully installed.")
            else:
                tkMessageBox.showinfo("Error", "Cannot install OpenAlea.")


        sys.exit(0)
    

    def onCancel(self):
        tkMessageBox.showinfo("Exit", "Configuration is not terminated.")
        sys.exit(1)


def run_install():
    """Run python setup.install"""

    commandstr=sys.executable + ' setup.py install'

    #try to import subprocess package
    try:
        import subprocess
        subprocess_enabled=True
    except ImportError:
        subprocess_enabled=False

    if(subprocess_enabled): #subprocess call
        retval=subprocess.call(commandstr, shell=True)

    else: #standard os.system command
        retval=os.system(commandstr)

    return retval
		    
      
    
def main():
     
    root = tk.Tk()
    root.title("OpenAlea Install")

    app = App(root)
    root.mainloop()

   
    

if __name__ == '__main__':
    main()
