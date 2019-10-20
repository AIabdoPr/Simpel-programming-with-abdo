from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from random import randrange
import cv2, os

class App(ttk.Frame):

    def __init__(self, parent):
        self.characterlist = []
        self.cn_list = []
        ttk.Frame.__init__(self, parent)
        self.CreateUI()
        self.grid(sticky = (N,S,W,E))
        self.parent = parent
        if not os.path.exists("trainer\\Characters_Names.cn"):
            self.create_cn()
        self.LoadTable()
        f2 = ttk.Frame(parent)
        f2.grid(row = 0, column = 1, sticky = (N,S,W,E))
        bu1 = ttk.Button(f2, text = "تعديل", command = lambda: self.edit())
        bu1.pack()
        # bu2 = ttk.Button(f2, text = "Delete", command = lambda: self.delete())
        # bu2.pack()
        bu3 = ttk.Button(f2, text = "خروج", command = lambda: exit())
        bu3.pack()
        self.parent.after(1, self.chack)

    def CreateUI(self):
        tv = ttk.Treeview(self)
        tv['columns'] = ('name', 'date', 'time', 'path')
        tv.heading("#0", text='الرقم', anchor='w')
        tv.column("#0", anchor="center", width = 50)
        tv.heading('name', text='إسم الوجه')
        tv.column('name', anchor='center', width=150)
        tv.heading('date', text='التاريخ')
        tv.column('date', anchor='center', width=100)
        tv.heading('time', text='الوقت')
        tv.column('time', anchor='center', width=100)
        tv.heading('path', text='مسار الصور')
        tv.column('path', anchor='center', width=200)
        
        tv.bind("<Double-Button-1>", self.show_img)
        tv.bind("<Return>", self.show_img)

        vbary = Scrollbar(self, name = 'vbary', orient=VERTICAL)
        vbary['command'] = tv.yview
        vbary.pack(side = LEFT, fill=Y)
        tv['yscrollcommand'] = vbary.set
        vbarx = Scrollbar(self, name = 'vbarx', orient=HORIZONTAL)
        vbarx['command'] = tv.xview
        vbarx.pack(side = BOTTOM, fill=X)
        tv['xscrollcommand'] = vbarx.set
        tv.pack(side = TOP)
        self.treeview = tv

    def LoadTable(self):
        self.clean_tabel()
        self.characterlist = []
        self.cn_list = open('trainer\\Characters_Names.cn', "r").read().split("\n")
        if(self.cn_list == ['']):
            return
        del(self.cn_list[-1])
        self.num = len(self.cn_list)
        for cn in self.cn_list:
            id, date_time, face_name = cn.split("===")
            if not(date_time == "None"):
                date = "-".join(date_time.split("-")[0:3])
                time = ":".join(date_time.split("-")[3:6])
            else:
                date = time = "None"
            path = r"dataset\User.{}.*.jpg".format(id)
            if not(face_name == "New Face"):
                self.characterlist.append([face_name, date, time, path])
                self.treeview.insert("", "{}".format(id), text=id, values=(face_name, date, time, path))

    def clean_tabel(self):
        x = self.treeview.get_children()
        for item in x:
            self.treeview.delete(item)

    def chack(self):
        if not os.path.exists("trainer\\Characters_Names.cn"):
            self.create_cn()

        a = open('trainer\\Characters_Names.cn', "r").read().split("\n")
        del(a[-1])
        x = self.treeview.get_children()
        i = 0
        for _ in x:
             i = i+1
        if(a != self.cn_list):
            self.clean_tabel()
            # self.cn_load()
            self.LoadTable()
        self.parent.after(1, self.chack)

    def edit(self):
        def save_edit(x):
            self.characterlist[x][0] = ent1.get()
            a = self.cn_list[x].split("===")
            self.cn_list[x] = "===".join([a[0], a[1], self.characterlist[x][0]])
            self.cn_load()
            root.destroy()

        item = self.treeview.selection()[0]
        items = self.treeview.get_children()
        x = items.index(item)

        root = Tk()
        root.title('تعديل: {}'.format(self.characterlist[x][0]))

        ttk.Label(root, text = "الاسم: ").grid(row = 0, column = 0)
        ttk.Label(root, text = "التاريخ: ").grid(row = 1, column = 0)
        ttk.Label(root, text = "الوقت: ").grid(row = 2, column = 0)
        ttk.Label(root, text = "المسار: ").grid(row = 3, column = 0)

        ent1 = ttk.Entry(root, width = 30)
        ent1.grid(row = 0, column = 1)
        ent2 = ttk.Entry(root, width = 30)
        ent2.grid(row = 1, column = 1)
        ent3 = ttk.Entry(root, width = 30)
        ent3.grid(row = 2, column = 1)
        ent4 = ttk.Entry(root, width = 30)
        ent4.grid(row = 3, column = 1)

        ent1.insert(0, self.characterlist[x][0])
        ent2.insert(0, self.characterlist[x][1])
        ent3.insert(0, self.characterlist[x][2])
        ent4.insert(0, self.characterlist[x][3])
        ent2['state'] = ['disabled']
        ent3['state'] = ['disabled']
        ent4['state'] = ['disabled']

        f = ttk.Frame(root)
        f.grid(row = 4, column = 0, columnspan = 2)
        ttk.Button(f, text = "حفظ", command = lambda: save_edit(x)).grid(row = 0, column = 0)
        ttk.Button(f, text = "إلغاء", command = lambda: root.destroy()).grid(row = 0, column = 1)

    # def delete(self):
        # item = self.treeview.selection()[0]
        # items = self.treeview.get_children()
        # x = items.index(item)
        # a = [str(x), "None", "None", "New Face"]
        # self.characterlist[x] = a
        # self.cn_list[x] = "===".join(a)
        # self.cn_load()
        # self.treeview.delete(item)

    def show_img(self, event):
        item = self.treeview.selection()[0]
        items = self.treeview.get_children()
        x = items.index(item)
        path = r"dataset\User.{0}.{1}.jpg".format(x, randrange(1,50))
        img = cv2.imread(path)
        cv2.imshow(self.characterlist[x][0], img)
        cv2.waitKey(0)

    def create_cn(self):
        a = [os.path.join("dataset",f) for f in os.listdir("dataset")]
        cnfile = open('trainer\\Characters_Names.cn', 'w')
        if not(len(a) == 0):
            return
        textlist = []
        for b in a:
            if (b.split(".")[-1] == "jpg"):
                id = b.split(".")[1]
                text = "{0}===None===Face<{0}>\n".format(id)
                textlist.append(text)
        textlist = list(set(textlist))
        textlist.sort()
        cnfile.write("".join(textlist))
        cnfile.close()

    def cn_load(self):
        cnfile = open('trainer\\Characters_Names.cn', 'w')
        text = "\n".join(self.cn_list)
        cnfile.write(str(text)+"\n")
        cnfile.close()
        self.LoadTable()

def main():
    root = Tk()
    root.title("تتبع الوجوه التلقائي: جدول المعلومات")
    root.maxsize(695, 246)
    root.minsize(695, 246)

    def run():
        os.system('start python "General.py"')
        exit()

    def show(x):
        if(x == 1):
            vid_open = askopenfile(initialdir = "Videos", title = "Open Video", filetypes = (("Videos", "*.mp4;*.wmv;*.avi;*.mpeg;*.mkv;*."), ("All Files", "*.*")))
            link = vid_open.name
            print(link)
            if os.path.exists(str(link)):
                re = str(open("show.s", "r").read().split("\n")[1])
                try:
                    open("show.s", "w").write(link+"\n"+re)
                except:
                    open("show.s", "w").write("0\n"+re)
        elif(x == 2):
            open("show.s", "w").write("0\n")

    def lratio():
        ratio = open("show.s", "r").read().split("\n")
        print(ratio)
        ra_root = Tk()
        r = Scale(ra_root, from_ = 10, to = 100)
        r.pack()

        def writ_e(e):
            open("show.s", "w").write(ratio[0]+"\n"+str(r.get()))

        ra_root.bind('<Motion>', writ_e)
        

    # def geometry():
        # geo_root = Tk()
        # w = Scale(geo_root, from_=10, to=1920)
        # w.pack(side = LEFT)
        # h = Scale(geo_root, from_=10, to=1080)
        # h.pack(side = RIGHT)
        # def pr(x):
            # open("w_h", "w").write("{0}x{1}".format(w.get(), h.get()))
        # geo_root.bind('<Motion>', pr)

    menubar = Menu(root)

    filemenu = Menu(menubar,  tearoff = 1)
    filemenu.add_command(label = "تشغيل الكميرا",  command = lambda:run())
    filemenu.add_command(label = "خروج",  command = lambda: exit())
    menubar.add_cascade(label = "ملف",  menu = filemenu)

    settingmenu = Menu(menubar,  tearoff = 1)
    
    showmenu = Menu(menubar,  tearoff = 0)
    showmenu.add_command(label = "فيديو",  command = lambda: show(1))
    showmenu.add_command(label = "كميرا الجهاز",  command = lambda: show(2))

    settingmenu.add_command(label = "تحديد نسبة الشبه",  command = lambda: lratio())
    # settingmenu.add_command(label = "geometry",  command = lambda: geometry())

    settingmenu.add_cascade(label = "العرض بـ",  menu = showmenu)
    menubar.add_cascade(label = "إعدادات",  menu = settingmenu)
    
    root.config(menu = menubar)

    # h, w = open("w_h", "r").read().split("x")
    w, h = (640, 480)
    w, h = int(w)+20, int((range(0, int(h), 245)[-1]/2)+20)
    root.geometry('695x245+{0}+{1}'.format(w, h))
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()