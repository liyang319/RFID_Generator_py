import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class RFIDTagGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID标签生成系统")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')

        main = ttk.Frame(root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)

        # 主容器布局：内容区域可扩展，日志区域固定高度
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=0)
        main.grid_columnconfigure(0, weight=1)

        # 内容框架（水平居中）
        content = ttk.Frame(main)
        content.grid(row=0, column=0, sticky='nsew')
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=0)
        content.columnconfigure(2, weight=1)

        controls = ttk.Frame(content)
        controls.grid(row=0, column=1, sticky='nsew')

        # controls 内部列配置（与原布局相同）
        for i in range(9):
            controls.columnconfigure(i, weight=0)
        controls.columnconfigure(8, weight=1)
        controls.columnconfigure(0, minsize=120)
        controls.columnconfigure(1, minsize=200)
        controls.columnconfigure(2, minsize=20)
        controls.columnconfigure(3, minsize=100)
        controls.columnconfigure(4, minsize=200)
        controls.columnconfigure(5, minsize=60)
        controls.columnconfigure(6, minsize=80)

        # 标题
        title_frame = ttk.Frame(controls)
        title_frame.grid(row=0, column=0, columnspan=9, sticky='ew', pady=(0,15))
        title_frame.columnconfigure(0, weight=1)
        ttk.Label(title_frame, text="RFID标签生成系统", font=('微软雅黑', 16, 'bold')).pack(side='left', expand=True)
        ttk.Label(title_frame, text="v1.0.0", font=('微软雅黑', 12)).pack(side='left', padx=(10,0))

        # 第1行
        ttk.Label(controls, text="设备号：", font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', padx=(5,2), pady=8)
        self.device_entry = ttk.Entry(controls, width=25)
        self.device_entry.insert(0, "TAG_PRODUCER_001")
        self.device_entry.grid(row=1, column=1, sticky='w', padx=2, pady=8)

        ttk.Label(controls, text="当前位置：", font=('微软雅黑', 10)).grid(row=1, column=3, sticky='w', padx=(5,2), pady=8)
        self.location_entry = ttk.Entry(controls, width=35)
        self.location_entry.insert(0, "经度116.3918173° 纬度39.9797956°")
        self.location_entry.grid(row=1, column=4, sticky='w', padx=2, pady=8)

        # 第2行
        ttk.Label(controls, text="通道机：", font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', padx=(5,2), pady=5)
        self.channel_combo = ttk.Combobox(controls, width=23, values=["生产线通道机001", "生产线通道机002"], state="readonly")
        self.channel_combo.set("生产线通道机001")
        self.channel_combo.grid(row=2, column=1, sticky='w', padx=2, pady=5)

        ttk.Label(controls, text="IP：", font=('微软雅黑', 10)).grid(row=2, column=3, sticky='w', padx=(5,2), pady=5)
        self.ip_entry = ttk.Entry(controls, width=15)
        self.ip_entry.insert(0, "192.168.1.1")
        self.ip_entry.grid(row=2, column=4, sticky='w', padx=2, pady=5)

        ttk.Label(controls, text="端口：", font=('微软雅黑', 10)).grid(row=2, column=5, sticky='w', padx=(5,2), pady=5)
        self.port_entry = ttk.Entry(controls, width=10)
        self.port_entry.insert(0, "2000")
        self.port_entry.grid(row=2, column=6, sticky='w', padx=2, pady=5)

        self.status_circle = tk.Label(controls, text="●", fg="red", font=('微软雅黑', 14))
        self.status_circle.grid(row=2, column=7, padx=(5,2), pady=5)
        self.connect_btn = ttk.Button(controls, text="连接", command=self.connect_channel, width=8)
        self.connect_btn.grid(row=2, column=8, sticky='w', padx=2, pady=5)

        # 第3行
        ttk.Label(controls, text="工作状态：", font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', padx=(5,2), pady=2)
        self.work_status_circle = tk.Label(controls, text="●", fg="red", font=('微软雅黑', 14))
        self.work_status_circle.grid(row=3, column=1, sticky='w', padx=2, pady=2)

        ttk.Label(controls, text="异常信息：", font=('微软雅黑', 10)).grid(row=3, column=3, sticky='w', padx=(5,2), pady=2)
        self.exception_label = ttk.Label(controls, text="无异常", font=('微软雅黑', 10), foreground="green")
        self.exception_label.grid(row=3, column=4, sticky='w', padx=2, pady=2)

        # 分割线
        ttk.Separator(controls, orient='horizontal').grid(row=4, column=0, columnspan=9, sticky='ew', pady=10)

        # 第5-9行（均匀分布）
        bottom_frame = ttk.Frame(controls)
        bottom_frame.grid(row=5, column=0, columnspan=9, sticky='ew', pady=5)
        bottom_frame.columnconfigure(0, weight=0)
        bottom_frame.columnconfigure(1, weight=0)
        bottom_frame.columnconfigure(2, weight=1)
        bottom_frame.columnconfigure(3, weight=0)
        bottom_frame.columnconfigure(4, weight=0)
        bottom_frame.columnconfigure(5, weight=0)

        # 第5行
        ttk.Label(bottom_frame, text="生产企业类别代码：", font=('微软雅黑', 10)).grid(row=0, column=0, sticky='w', padx=(0,5), pady=8)
        self.manufacture_code = ttk.Entry(bottom_frame, width=25)
        self.manufacture_code.insert(0, "D6")
        self.manufacture_code.grid(row=0, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="产品种类和名称：", font=('微软雅黑', 10)).grid(row=0, column=3, sticky='w', padx=(0,5), pady=8)
        self.product_combo = ttk.Combobox(bottom_frame, width=33, values=["高密度震源药柱[箱]", "其他产品"], state="readonly")
        self.product_combo.set("高密度震源药柱[箱]")
        self.product_combo.grid(row=0, column=4, sticky='w', padx=5, pady=8)

        # 第6行
        ttk.Label(bottom_frame, text="生产许可证编号代码：", font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', padx=(0,5), pady=8)
        self.license_code = ttk.Entry(bottom_frame, width=25)
        self.license_code.insert(0, "D6")
        self.license_code.grid(row=1, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="规格型号（数量）：", font=('微软雅黑', 10)).grid(row=1, column=3, sticky='w', padx=(0,5), pady=8)
        self.spec_entry = ttk.Entry(bottom_frame, width=33)
        self.spec_entry.insert(0, "高密度震源药柱[箱]")
        self.spec_entry.grid(row=1, column=4, sticky='w', padx=5, pady=8)

        # 第7行
        ttk.Label(bottom_frame, text="包装方式：", font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', padx=(0,5), pady=8)
        self.pack_entry = ttk.Entry(bottom_frame, width=25)
        self.pack_entry.insert(0, "D6")
        self.pack_entry.grid(row=2, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="净质量：", font=('微软雅黑', 10)).grid(row=2, column=3, sticky='w', padx=(0,5), pady=8)
        self.net_weight = ttk.Entry(bottom_frame, width=33)
        self.net_weight.insert(0, "12")
        self.net_weight.grid(row=2, column=4, sticky='w', padx=5, pady=8)

        # 第8行
        ttk.Label(bottom_frame, text="生产批号：", font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', padx=(0,5), pady=8)
        self.batch_entry = ttk.Entry(bottom_frame, width=25)
        self.batch_entry.insert(0, "D6")
        self.batch_entry.grid(row=3, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="生产日期：", font=('微软雅黑', 10)).grid(row=3, column=3, sticky='w', padx=(0,5), pady=8)
        self.date_entry = ttk.Entry(bottom_frame, width=33)
        self.date_entry.insert(0, "20260101")
        self.date_entry.grid(row=3, column=4, sticky='w', padx=5, pady=8)

        # 第9行
        ttk.Label(bottom_frame, text="生产箱（袋）号：", font=('微软雅黑', 10)).grid(row=4, column=0, sticky='w', padx=(0,5), pady=8)
        self.box_entry = ttk.Entry(bottom_frame, width=25)
        self.box_entry.insert(0, "10")
        self.box_entry.grid(row=4, column=1, sticky='w', padx=5, pady=8)

        self.send_btn = ttk.Button(bottom_frame, text="手动下发", command=self.manual_send, width=15)
        self.send_btn.grid(row=4, column=4, sticky='w', padx=5, pady=8)

        # ========== 系统日志区域 ==========
        log_frame = ttk.LabelFrame(main, text="系统日志", padding="5")
        log_frame.grid(row=1, column=0, sticky='ew', pady=(10,0))
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky='nsew')
        self.log_text.tag_config('info', foreground='black')
        self.log_text.tag_config('success', foreground='green')
        self.log_text.tag_config('error', foreground='red')
        self.log_text.tag_config('warning', foreground='orange')

        self.log_message("系统启动", tag='info')

    def log_message(self, msg, tag='info'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

    def connect_channel(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_circle.config(fg="green")
        self.work_status_circle.config(fg="green")
        self.log_message(f"连接通道机成功 (IP: {self.ip_entry.get()}, 端口: {self.port_entry.get()})", tag='success')
        messagebox.showinfo("连接", f"通道机连接成功！\n点击时间：{current_time}")

    def manual_send(self):
        click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        self.log_message(f"手动下发 - 批号: {batch}, 箱号: {box}, 日期: {date}", tag='info')
        self.log_message(f"  设备号: {device}, 通道机: {channel}, IP: {ip}:{port}", tag='info')
        self.log_message(f"  产品: {product}, 规格: {spec}, 净质量: {weight}kg", tag='info')

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
        print(info)
        print("-" * 50)

if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDTagGeneratorUI(root)
    root.state('zoomed')
    root.mainloop()