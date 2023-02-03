from tkinter import messagebox

import psutil
import wmi
import platform
import time
import pynvml
import ctypes
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

w = wmi.WMI()
pynvml.nvmlInit()

root = Tk()

root.title('Hardware Info')

# 调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 调用api获得当前的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置缩放因子
root.tk.call('tk', 'scaling', ScaleFactor / 75)

# 设置窗口的大小
root.geometry("680x680")
# 获取电脑屏幕的分辨率
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# 获取窗口的大小
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
# 计算窗口居中时的坐标
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - window_height // 1.2
# 设置窗口坐标
root.geometry("+%d+%d" % (x, y))

# root.resizable(0, 0)
root.resizable(False, False)
font1 = tkFont.Font(family='Times', size=12)  # 创建字体
root.option_add('*Font', font1)
frame = Frame(root).pack()


# root.geometry('300x30')


def users():
    # 使用者信息
    for BIOSs in w.Win32_ComputerSystem():
        cput.insert('1.0', '电脑名称：' + str(BIOSs.Caption) + '\n' + '\n')
        cput.insert('1.0', '使用者：' + str(BIOSs.UserName) + '\n')
        cput.insert('1.0', '---------------------------------使用者信息---------------------------------' + '\n')


def bioss():
    # bios信息
    bios = w.Win32_BIOS()[0]
    cput.insert('1.0', '完整版本信息：' + str(bios.BIOSVersion) + '\n' + '\n')
    cput.insert('1.0', '内部识别号：' + str(bios.BuildNumber) + '\n')
    cput.insert('1.0', '代码集：' + str(bios.CodeSet) + '\n')
    cput.insert('1.0', '当前语言：' + str(bios.CurrentLanguage) + '\n')
    cput.insert('1.0', '简要描述信息：' + str(bios.Description) + '\n')
    cput.insert('1.0', '识别码：' + str(bios.IdentificationCode) + '\n')
    cput.insert('1.0', '制造商：' + str(bios.Manufacturer) + '\n')
    cput.insert('1.0', '名称：' + str(bios.Name) + '\n')
    cput.insert('1.0', '是否主BIOS：' + str(bios.PrimaryBIOS) + '\n')
    cput.insert('1.0', '安装日期：' + str(bios.InstallDate) + '\n')
    cput.insert('1.0', '发布日期：' + str(str(bios.ReleaseDate)[0:8]) + '\n')
    cput.insert('1.0', '序列号：' + str(bios.SerialNumber) + '\n')
    cput.insert('1.0', 'BIOS版本：' + str(bios.Version) + '\n')
    cput.insert('1.0', '---------------------------------BIOS信息---------------------------------' + '\n')


def boards():
    # 主板信息
    c = wmi.WMI()
    sys = c.Win32_OperatingSystem()[0]
    cput.insert('1.0', '操作系统：' + str(sys.Caption) + '\n' + '\n')
    cput.insert('1.0', '操作系统位数：' + str(platform.architecture()) + '\n')
    cput.insert('1.0', '电脑硬件架构：' + str(platform.machine()) + '\n')
    cput.insert('1.0', '电脑的网络名称：' + str(platform.node()) + '\n')
    cput.insert('1.0', '操作系统版本号：' + str(platform.version) + '\n')
    obj = w.Win32_ComputerSystem()[0]
    cput.insert('1.0', '主板型号：' + str(obj.model) + '\n')
    cput.insert('1.0', '主板制造商：' + str(obj.Manufacturer) + '\n')
    cput.insert('1.0', '主板数量：' + str(len(w.Win32_Processor())) + '\n')
    for board_id in w.Win32_BaseBoard():
        cput.insert('1.0', '主板序列号：' + str(board_id.SerialNumber) + '\n')
    cput.insert('1.0', '---------------------------------主板信息---------------------------------' + '\n')


def mems():
    # 内存信息
    i = 0
    total_m = 0
    for memModule in w.Win32_PhysicalMemory():
        totalMemSize = int(memModule.Capacity)
        cput.insert('1.0', '内存厂商：' + str(memModule.Manufacturer) + '\n' + '\n')
        cput.insert('1.0', '内存型号：' + str(memModule.PartNumber) + '\n')
        cput.insert('1.0', '内存大小：' + str(int(totalMemSize / 1024 ** 3)) + 'G' + '\n')
        total_m += int(totalMemSize / 1024 ** 3)
        cput.insert('1.0', f'--内存条--' + '\n')
    cput.insert('1.0', '总内存大小：' + str(total_m) + 'G' + '\n\n')
    cput.insert('1.0', '---------------------------------内存信息---------------------------------' + '\n')


def disks():
    # 物理磁盘信息
    disk = w.Win32_DIskDrive()[0]
    cput.insert('1.0', '硬盘说明：' + str(disk.Manufacturer) + '\n' + '\n')
    for disk in w.Win32_DiskDrive(InterfaceType="IDE"):
        cput.insert('1.0', '硬盘名称：' + str(disk.Caption) + '\n')
    cput.insert('1.0', '硬盘序列号：' + str(disk.SerialNumber) + '\n')
    cput.insert('1.0', '硬盘容量：' + str(int(int(disk.Size) / (1024 * 1024 * 1024))) + 'G' + '\n')
    cput.insert('1.0', '---------------------------------硬盘信息---------------------------------' + '\n')


def hands():
    # 显卡信息
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 这里的0是GPU id
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    cput.insert('1.0', '驱动版本号：' + str(pynvml.nvmlSystemGetDriverVersion()) + '\n' + '\n')
    cput.insert('1.0', '显卡总显存：' + str(int(meminfo.total / (1024 ** 2))) + 'M' + '\n')
    cput.insert('1.0', '显卡已使用显存：' + str(int(meminfo.used / (1024 ** 2))) + 'M' + '\n')
    cput.insert('1.0', '显卡剩余显存：' + str(int(meminfo.free / (1024 ** 2))) + 'M' + '\n')
    cput.insert('1.0', '显卡数量：' + str(pynvml.nvmlDeviceGetCount()) + '\n')
    for xk in w.Win32_VideoController():
        cput.insert('1.0', '显卡名称：' + str(xk.name) + '\n')
    cput.insert('1.0', '---------------------------------显卡信息---------------------------------' + '\n')


def cpus():
    # cpu信息
    ope = w.Win32_OperatingSystem()[0]
    cput.insert('1.0', 'CPU生产号：' + ope.SerialNumber + '\n' + '\n')
    for cpu in w.Win32_Processor():
        cput.insert('1.0', 'CPU序列号：' + cpu.ProcessorId.strip() + '\n')
    for cpu in w.Win32_Processor():
        cput.insert('1.0', 'CPU线程数：' + str(psutil.cpu_count()) + '\n')
        cput.insert('1.0', 'CPU核心数：' + str(cpu.NumberOfcores) + '\n')
        cput.insert('1.0', 'CPU型号：' + str(cpu.Name) + '\n')
    cput.insert('1.0', '---------------------------------CPU信息---------------------------------' + '\n')


def init():
    cput.insert('1.0', '正在查询本机硬件信息......' + '\n')


def macs():
    # MAC地址
    for mac in w.Win32_NetworkAdapter():
        cput.insert('1.0', 'MAC地址：' + str(mac.MACAddress) + '\n')
    cput.insert('1.0', '---------------------------------MAC地址---------------------------------' + '\n')


def cal():
    cals.insert(0, '总字符数：' + str(len(cput.get('1.0', 'end'))))


def delete():
    cals.delete(0, 'end')
    cput.delete('1.0', 'end')


def copy_text():
    root.clipboard_clear()
    root.clipboard_append(cput.get("1.0", "end"))
    messagebox.showinfo("提示", "复制成功！")


def query():
    cput.insert(END, "正在查询本机硬件信息......\n")
    root.update()
    macs()
    users()
    bioss()
    boards()
    mems()
    disks()
    hands()
    cpus()
    # 关闭正在查询的消息
    cput.delete("end - 18 chars", "end")
    root.update()
    messagebox.showinfo("提示", "查询成功！")


cput = StringVar()
# cals = StringVar()
cput = Text(root)
cput.place(x=10, y=50, height=560, width=655)
button = Button(root, text='获取硬件信息', padding=0,
                command=query)
button.place(x=10, y=630, height=28, width=120)
button = Button(root, text='复制当前内容', padding=0,
                command=copy_text)
button.place(x=276, y=630, height=28, width=120)
button = Button(root, text='清除当前内容', padding=0, command=delete)
button.place(x=543, y=630, height=28, width=120)
cals = Entry(frame)
# cals.place(x=10, y=10, height=20, width=130)
time = Label(frame, text=time.strftime("运行时间: %Y-%m-%d %H:%M:%S", time.localtime()))
time.place(x=395, y=10, height=28, width=350)
time = Label(frame, text="Python env: 3.9")
time.place(x=10, y=10, height=28, width=200)
root.mainloop()
