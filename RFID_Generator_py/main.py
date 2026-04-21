import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RFIDTagGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID标签生成系统")
        self.root.geometry("950x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')

        # 主框架
        main = ttk.Frame(root, padding="15")
        main.pack(fill=tk.BOTH, expand=True)

        # 第0行：标题 + 版本号
        ttk.Label(main, text="RFID标签生成系统", font=('微软雅黑', 16, 'bold')).grid(row=0, column=0, sticky='w', padx=(0,30))
        ttk.Label(main, text="v1.0.0", font=('微软雅黑', 12)).grid(row=0, column=1, sticky='w')

        # 第1行：设备号 + 编辑框，当前位置
        ttk.Label(main, text="设备号：", font=('微软雅黑', 10)).grid(row=1, column=0, sticky='e', padx=5, pady=8)
        self.device_entry = ttk.Entry(main, width=20)
        self.device_entry.insert(0, "TAG_PRODUCER_001")
        self.device_entry.grid(row=1, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="当前位置：", font=('微软雅黑', 10)).grid(row=1, column=2, sticky='e', padx=(30,5), pady=8)
        self.location_entry = ttk.Entry(main, width=35)
        self.location_entry.insert(0, "经度116.3918173° 纬度39.9797956°")
        self.location_entry.grid(row=1, column=3, sticky='w', padx=5, pady=8)

        # 第2行：通道机 + 下拉框， IP + 编辑框， 端口 + 编辑框， 红色圆形 + 连接按钮
        ttk.Label(main, text="通道机：", font=('微软雅黑', 10)).grid(row=2, column=0, sticky='e', padx=5, pady=8)
        self.channel_combo = ttk.Combobox(main, width=18, values=["生产线通道机001", "生产线通道机002"], state="readonly")
        self.channel_combo.set("生产线通道机001")
        self.channel_combo.grid(row=2, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="IP：", font=('微软雅黑', 10)).grid(row=2, column=2, sticky='e', padx=(30,5), pady=8)
        self.ip_entry = ttk.Entry(main, width=15)
        self.ip_entry.insert(0, "192.168.1.1")
        self.ip_entry.grid(row=2, column=3, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="端口：", font=('微软雅黑', 10)).grid(row=2, column=4, sticky='e', padx=(20,5), pady=8)
        self.port_entry = ttk.Entry(main, width=10)
        self.port_entry.insert(0, "2000")
        self.port_entry.grid(row=2, column=5, sticky='w', padx=5, pady=8)

        # 红色圆形指示灯 (使用Label带●符号)
        self.status_circle = tk.Label(main, text="●", fg="red", font=('微软雅黑', 12))
        self.status_circle.grid(row=2, column=6, padx=(15,5), pady=8)
        self.connect_btn = ttk.Button(main, text="连接", command=self.connect_channel, width=8)
        self.connect_btn.grid(row=2, column=7, sticky='w', padx=5, pady=8)

        # 第3行：工作状态 + 红色圆圈， 异常信息 + 内容
        ttk.Label(main, text="工作状态：", font=('微软雅黑', 10)).grid(row=3, column=0, sticky='e', padx=5, pady=8)
        self.work_status_circle = tk.Label(main, text="●", fg="red", font=('微软雅黑', 12))
        self.work_status_circle.grid(row=3, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="异常信息：", font=('微软雅黑', 10)).grid(row=3, column=2, sticky='e', padx=(30,5), pady=8)
        self.exception_label = ttk.Label(main, text="无异常", font=('微软雅黑', 10), foreground="green")
        self.exception_label.grid(row=3, column=3, sticky='w', padx=5, pady=8)

        # 第4行：生产企业类别代码 + 编辑框， 产品种类和名称 + 下拉框
        ttk.Label(main, text="生产企业类别代码：", font=('微软雅黑', 10)).grid(row=4, column=0, sticky='e', padx=5, pady=8)
        self.manufacture_code = ttk.Entry(main, width=10)
        self.manufacture_code.insert(0, "D6")
        self.manufacture_code.grid(row=4, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="产品种类和名称：", font=('微软雅黑', 10)).grid(row=4, column=2, sticky='e', padx=(30,5), pady=8)
        self.product_combo = ttk.Combobox(main, width=20, values=["高密度震源药柱[箱]", "其他产品"], state="readonly")
        self.product_combo.set("高密度震源药柱[箱]")
        self.product_combo.grid(row=4, column=3, sticky='w', padx=5, pady=8)

        # 第5行：生产许可证编号代码 + 编辑框， 规格型号（数量） + 编辑框
        ttk.Label(main, text="生产许可证编号代码：", font=('微软雅黑', 10)).grid(row=5, column=0, sticky='e', padx=5, pady=8)
        self.license_code = ttk.Entry(main, width=10)
        self.license_code.insert(0, "D6")
        self.license_code.grid(row=5, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="规格型号（数量）：", font=('微软雅黑', 10)).grid(row=5, column=2, sticky='e', padx=(30,5), pady=8)
        self.spec_entry = ttk.Entry(main, width=20)
        self.spec_entry.insert(0, "高密度震源药柱[箱]")
        self.spec_entry.grid(row=5, column=3, sticky='w', padx=5, pady=8)

        # 第6行：包装方式 + 编辑框， 净质量 + 编辑框
        ttk.Label(main, text="包装方式：", font=('微软雅黑', 10)).grid(row=6, column=0, sticky='e', padx=5, pady=8)
        self.pack_entry = ttk.Entry(main, width=10)
        self.pack_entry.insert(0, "D6")
        self.pack_entry.grid(row=6, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="净质量：", font=('微软雅黑', 10)).grid(row=6, column=2, sticky='e', padx=(30,5), pady=8)
        self.net_weight = ttk.Entry(main, width=10)
        self.net_weight.insert(0, "12")
        self.net_weight.grid(row=6, column=3, sticky='w', padx=5, pady=8)

        # 第7行：生产批号 + 编辑框， 生产日期 + 编辑框
        ttk.Label(main, text="生产批号：", font=('微软雅黑', 10)).grid(row=7, column=0, sticky='e', padx=5, pady=8)
        self.batch_entry = ttk.Entry(main, width=15)
        self.batch_entry.insert(0, "D6")
        self.batch_entry.grid(row=7, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(main, text="生产日期：", font=('微软雅黑', 10)).grid(row=7, column=2, sticky='e', padx=(30,5), pady=8)
        self.date_entry = ttk.Entry(main, width=12)
        self.date_entry.insert(0, "20260101")
        self.date_entry.grid(row=7, column=3, sticky='w', padx=5, pady=8)

        # 第8行：生产箱（袋）号 + 编辑框， 手动下发按钮
        ttk.Label(main, text="生产箱（袋）号：", font=('微软雅黑', 10)).grid(row=8, column=0, sticky='e', padx=5, pady=8)
        self.box_entry = ttk.Entry(main, width=15)
        self.box_entry.insert(0, "10")
        self.box_entry.grid(row=8, column=1, sticky='w', padx=5, pady=8)

        self.send_btn = ttk.Button(main, text="手动下发", command=self.manual_send, width=12)
        self.send_btn.grid(row=8, column=3, sticky='w', padx=(30,5), pady=8)

        # 设置列权重，使布局均匀
        for i in range(8):
            main.columnconfigure(i, weight=1)

    def connect_channel(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 将红色圆形变为绿色表示连接成功（可选效果）
        self.status_circle.config(fg="green")
        self.work_status_circle.config(fg="green")
        messagebox.showinfo("连接", f"通道机连接成功！\n点击时间：{current_time}")

    def manual_send(self):
        click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取当前所有输入值
        device = self.device_entry.get()
        location = self.location_entry.get()
        channel = self.channel_combo.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        manufacture = self.manufacture_code.get()
        product = self.product_combo.get()
        license_code = self.license_code.get()
        spec = self.spec_entry.get()
        pack = self.pack_entry.get()
        weight = self.net_weight.get()
        batch = self.batch_entry.get()
        date = self.date_entry.get()
        box = self.box_entry.get()

        info = (f"手动下发时间：{click_time}\n"
                f"设备号：{device}\n"
                f"当前位置：{location}\n"
                f"通道机：{channel}\n"
                f"IP：{ip}  端口：{port}\n"
                f"生产企业类别代码：{manufacture}\n"
                f"产品种类和名称：{product}\n"
                f"生产许可证编号代码：{license_code}\n"
                f"规格型号：{spec}\n"
                f"包装方式：{pack}\n"
                f"净质量：{weight}\n"
                f"生产批号：{batch}\n"
                f"生产日期：{date}\n"
                f"生产箱（袋）号：{box}\n"
                f"指令已发送至通道机。")
        messagebox.showinfo("手动下发", info)
        # 同时打印到控制台
        print(info)
        print("-" * 50)

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDTagGeneratorUI(root)
    root.mainloop()