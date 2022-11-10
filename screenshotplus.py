from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pyautogui

def browse():
    # called from save location's change folder button
    filename = filedialog.askdirectory(initialdir="./")
    if (filename != ""):
        explorepathvar.set(filename)

def setuppage():
    # called from page value's quick setup button
    # referenced code:
    # https://stackoverflow.com/questions/49901928/how-to-take-a-screenshot-with-python-using-a-click-and-drag-method-like-snipping
    messagebox.showinfo("Quick Setup", "Drag a box to set page size and position with Left Mouse.\nRight click to cancel.")
    # in case setupclick is called before
    canvas.unbind("<ButtonPress-1>")

    canvas.bind("<ButtonPress-1>", press)
    canvas.bind("<B1-Motion>", move)
    canvas.bind("<ButtonRelease-1>", pressup)
    canvas.bind("<ButtonPress-3>", exitcanvas)

    win.withdraw()
    mast.deiconify()
    
    mast.attributes("-fullscreen", True)
    mast.attributes("-alpha", .3)
    mast.lift()
    mast.attributes("-topmost", True)

def press(event):
    # setuppage() - when first clicking, create selection box
    print(event.x, event.y)
    global pos1x, pos1y
    pos1x = event.x
    pos1y = event.y
    canvas.create_rectangle(0, 0, 1, 1, outline="red", width=5)

def move(event):
    # setuppage() - when dragging mouse, change selection box to new position
    global pos2x, pos2y
    pos2x = event.x
    pos2y = event.y
    canvas.coords(1, pos1x, pos1y, pos2x, pos2y)

def pressup(event):
    # setuppage() - let go of dragon, set values gathered
    print(pos1x, pos1y, pos2x, pos2y)
    # check which corners are the start and endpoints
    if (pos1x < pos2x):
        coordxvar.set(pos1x)
        pagewidthvar.set(pos2x-pos1x)
    else:
        coordxvar.set(pos2x)
        pagewidthvar.set(pos1x-pos2x)

    if (pos1y < pos2y):
        coordyvar.set(pos1y)
        pageheightvar.set(pos2y-pos1y)
    else:
        coordyvar.set(pos2y)
        pageheightvar.set(pos1y-pos2y)
    exitcanvas(event)

def setupclick():
    # called from between screenshots's click quick setup button
    # referenced code:
    # https://stackoverflow.com/questions/49901928/how-to-take-a-screenshot-with-python-using-a-click-and-drag-method-like-snipping
    messagebox.showinfo("Quick Setup", "Left click on desired position.\nRight click to cancel.")
    # in case setuppage is called before
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    
    canvas.bind("<ButtonPress-1>", clickpress)
    canvas.bind("<ButtonPress-3>", exitcanvas)

    win.withdraw()
    mast.deiconify()
    
    mast.attributes("-fullscreen", True)
    mast.attributes("-alpha", .3)
    mast.lift()
    mast.attributes("-topmost", True)

def clickpress(event):
    # setupclick() - on click, save values
    print(event.x, event.y)

    clickxvar.set(event.x)
    clickyvar.set(event.y)
    exitcanvas(event)

def exitcanvas(event):
    # called by either pressup() or clickpress() - hide canvas, return to main window
    mast.withdraw()
    win.deiconify()

def toggleclicks():
    # called by between screenshot's click checkbox - toggle entry/label variables
    if (bool(clickcheckvar.get())):
        clickx["state"] = NORMAL
        clicky["state"] = NORMAL
        clickxlab["state"] = NORMAL
        clickylab["state"] = NORMAL
        clicksetupbtn["state"] = NORMAL
        pausetime["state"] = NORMAL
        pausetimelab["state"] = NORMAL
    else:
        clickx["state"] = DISABLED
        clicky["state"] = DISABLED
        clickxlab["state"] = DISABLED
        clickylab["state"] = DISABLED
        clicksetupbtn["state"] = DISABLED
        if (not (bool(scrollcheckvar.get()))):
            pausetime["state"] = DISABLED
            pausetimelab["state"] = DISABLED
    
def togglescrolls():
    # called by between screenshot's scroll checkbox - toggle entry/label variables
    if (bool(scrollcheckvar.get())):
        scrollx["state"] = NORMAL
        scrolly["state"] = NORMAL
        scrollxlab["state"] = NORMAL
        scrollylab["state"] = NORMAL
        scrolltextinfo["state"] = NORMAL
        pausetime["state"] = NORMAL
        pausetimelab["state"] = NORMAL
    else:
        scrollx["state"] = DISABLED
        scrolly["state"] = DISABLED
        scrollxlab["state"] = DISABLED
        scrollylab["state"] = DISABLED
        scrolltextinfo["state"] = DISABLED
        if (not (bool(clickcheckvar.get()))):
            pausetime["state"] = DISABLED
            pausetimelab["state"] = DISABLED

def screenshot():
    # called by start button - check for bad inputs and take screenshots
    try:
        pagex = int(coordx.get())
        pagey = int(coordy.get())
        pageh = int(pageheight.get())
        pagew = int(pagewidth.get())
        clickposx = int(clickx.get())
        clickposy = int(clicky.get())
        scrollnumx = int(scrollx.get())
        scrollnumy = int(scrolly.get())
        pyautogui.PAUSE = float(pausetime.get())
        path = explorepathvar.get()
        if (path == "Current Directory"):
            path = "."
        totalpages = int(numpages.get())

        # hide window
        win.withdraw()

        for curpage in range(totalpages):
            filename = "%s.png" % (curpage+1)
            img = pyautogui.screenshot(filename, region=(pagex, pagey, pagew, pageh))
            img.save(path + "/" + filename)
            if (bool(clickcheckvar.get())):
                pyautogui.click(clickposx, clickposy)
            if (bool(scrollcheckvar.get())):
                pyautogui.scroll(scrollnumy)
                pyautogui.hscroll(scrollnumx)
        # show window again
        win.deiconify()

    except ValueError:
        win.deiconify()
        messagebox.showerror("Input Error", "All entries (except for the pause time) must be whole numbers.\nAll entries (except for X and Y values) must also be positive.")
    except Exception as e:
        print(e)
        win.deiconify()
        if (pagew <= 0 or pageh <= 0):
            messagebox.showerror("Input Error", "Page Width and Page Height must be positive whole numbers.")
        else:
            messagebox.showerror("Error", "An Error Occured:\n"+str(e))

def  screenshotenter(event):
    # only called by pressing hotkey to run rather than clicking
    screenshot()

# create main window object and widgets
win = Tk()
win.title("Screenshot Plus v1")

# global variables used by quick setup
pos1x = None
pos1y = None
pos2x = None
pos2y = None

# PAGE VALUES
fr = LabelFrame(win, text="Page Values")
fr.grid(row=0, column=0, columnspan=2, rowspan=5, padx=40, sticky=NS)
# PAGE VALUES - VALUES
Label(fr, text="Left Corner X ").grid(row=0, column=0)
coordxvar = StringVar(fr, value="0")
coordx = Entry(fr, textvariable=coordxvar, width=5, justify=RIGHT)
coordx.grid(row=0, column=1)
Label(fr, text="Left Corner Y ").grid(row=1, column=0)
coordyvar = StringVar(fr, value="0")
coordy = Entry(fr, textvariable=coordyvar, width=5, justify=RIGHT)
coordy.grid(row=1, column=1)
Label(fr, text="Page Width").grid(row=2, column=0)
pagewidthvar = StringVar(fr, value="100")
pagewidth = Entry(fr, textvariable=pagewidthvar, width=5, justify=RIGHT)
pagewidth.grid(row=2, column=1)
Label(fr, text="Page Height").grid(row=3, column=0)
pageheightvar = StringVar(fr, value="100")
pageheight = Entry(fr, textvariable=pageheightvar, width=5, justify=RIGHT)
pageheight.grid(row=3, column=1)
setupbtn = Button(fr, text="Quick Setup", command=setuppage)
setupbtn.grid(row=4, column=0, columnspan=2, sticky=EW, pady=(10,0))

# BETWEEN FRAMES
fr2 = LabelFrame(win, text="Between Screenshots")
fr2.grid(row=0, column=2, columnspan=4, rowspan=5, padx=(0,40))
# BEWTEEN FRAMES - CLICK
clickcheckvar = IntVar(fr2, value=1)
clickcheck = Checkbutton(fr2, text="Click", variable=clickcheckvar, command=toggleclicks)
clickcheck.grid(row=0, column=0, columnspan=2)
clickxlab = Label(fr2, text="Click X")
clickxlab.grid(row=1, column=0)
clickxvar = StringVar(fr2, value="50")
clickx = Entry(fr2, textvariable=clickxvar, width=5, justify=RIGHT)
clickx.grid(row=1, column=1)
clickylab = Label(fr2, text="Click Y")
clickylab.grid(row=2, column=0)
clickyvar=StringVar(fr2, value="50")
clicky = Entry(fr2, textvariable=clickyvar, width=5, justify=RIGHT)
clicky.grid(row=2, column=1)
clicksetupbtn = Button(fr2, text="Quick Setup", command=setupclick)
clicksetupbtn.grid(row=3, column=0, columnspan=2, stick=EW)
# BETWEEN FRAMES - SCROLL
scrollcheckvar = IntVar()
scrollcheck = Checkbutton(fr2, text="Scroll", variable=scrollcheckvar, command=togglescrolls)
scrollcheck.grid(row=0, column=2, columnspan=2)
scrollxlab = Label(fr2, text="Scroll X ", state=DISABLED)
scrollxlab.grid(row=1, column=2)
scrollx = Entry(fr2, textvariable=StringVar(fr2, value="0"), width=5, justify=RIGHT, state=DISABLED)
scrollx.grid(row=1, column=3)
scrollylab = Label(fr2, text="Scroll Y ", state=DISABLED)
scrollylab.grid(row=2, column=2)
scrolly = Entry(fr2, textvariable=StringVar(fr2, value="0"), width=5, justify=RIGHT, state=DISABLED)
scrolly.grid(row=2, column=3)
scrolltextinfo = Label(fr2, text="(Scroll X not available\non Windows.)", font=("Arial", 7), state=DISABLED)
scrolltextinfo.grid(row=3, column=2, columnspan=2)
# BETWEEN FRAMES - PAUSE
pausetimelab = Label(fr2, text="Pause Time (s)  ")
pausetimelab.grid(row=4, column=0, columnspan=3)
pausetime = Entry(fr2, textvariable=StringVar(fr2, value="0.1"), width=5, justify=RIGHT)
pausetime.grid(row=4, column=2, columnspan=2)

# SAVE LOCATION
fr3 = LabelFrame(win, text="Save Location")
fr3.grid(row=5, column=0, columnspan=6, padx=40, pady=40, sticky=EW)
# SAVE LOCATION - DIRECTORY
explorebtn = Button(fr3, text="Change Folder", command = browse).grid(row=0, column=0, columnspan=2, sticky=N)
explorepathvar = StringVar()
explorepathvar.set("Current Directory")
Label(fr3, textvariable=explorepathvar, wraplength=400).grid(row=0, column=2, columnspan=4, stick=W, padx=20)

# UNCATEGORIZED - NUMBER OF SCREENSHOTS
Label(win, text="Number of Pages").grid(row=6, column=0, columnspan=2, pady=(0,40))
numpages = Entry(win, textvariable=StringVar(win, value="1"), width=5, justify=RIGHT)
numpages.grid(row=6, column=2, pady=(0,40), sticky=W)
# UNCATEGORIZED - START SCREENSHOTS
startbtn = Button(win, text="Start [ENTER]", command=screenshot)
startbtn.grid(row=6, column=3, columnspan=3, padx=(0,40), pady=(0,40), sticky=EW)
win.bind("<Return>", screenshotenter)

mast = Toplevel(win)
canvasframe = Frame(mast)
canvasframe.pack(fill=BOTH, expand=YES)
canvas = Canvas(canvasframe, cursor="cross", background="gray")
canvas.pack(fill=BOTH, expand=YES)
mast.withdraw()

win.mainloop()

