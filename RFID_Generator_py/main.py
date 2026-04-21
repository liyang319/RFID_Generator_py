# main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from SocketClient import SocketClient  # 导入 SocketClient 类


class RFIDTagGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID标签生成系统")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')

        self.socket_client = None  # Socket 客户端实例

        main = ttk.Frame(root, padding="20")
        main.pack(fill=tk.BOTH, expand=True)

        # 主容器：水平居中布局
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=0)
        main.grid_columnconfigure(2, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # 内容框架（包含所有控件和日志）
        content = ttk.Frame(main)
        content.grid(row=0, column=1, sticky='nsew')
        content.grid_columnconfigure(0, weight=1)

        # 上层控件区域（不扩展高度）
        controls = ttk.Frame(content)
        controls.grid(row=0, column=0, sticky='ew')
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
        title_frame.grid(row=0, column=0, columnspan=9, sticky='ew', pady=(0, 15))
        title_frame.columnconfigure(0, weight=1)
        ttk.Label(title_frame, text="RFID标签生成系统", font=('微软雅黑', 16, 'bold')).pack(side='left', expand=True)
        ttk.Label(title_frame, text="v1.0.0", font=('微软雅黑', 12)).pack(side='left', padx=(10, 0))

        # 第1行
        ttk.Label(controls, text="设备号：", font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', padx=(5, 2), pady=8)
        self.device_entry = ttk.Entry(controls, width=25)
        self.device_entry.insert(0, "TAG_PRODUCER_001")
        self.device_entry.grid(row=1, column=1, sticky='w', padx=2, pady=8)

        ttk.Label(controls, text="当前位置：", font=('微软雅黑', 10)).grid(row=1, column=3, sticky='w', padx=(5, 2), pady=8)
        self.location_entry = ttk.Entry(controls, width=35)
        self.location_entry.insert(0, "经度116.3918173° 纬度39.9797956°")
        self.location_entry.grid(row=1, column=4, sticky='w', padx=2, pady=8)

        # 第2行
        ttk.Label(controls, text="通道机：", font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', padx=(5, 2), pady=5)
        self.channel_combo = ttk.Combobox(controls, width=23, values=["生产线通道机001", "生产线通道机002"], state="readonly")
        self.channel_combo.set("生产线通道机001")
        self.channel_combo.grid(row=2, column=1, sticky='w', padx=2, pady=5)

        ttk.Label(controls, text="IP：", font=('微软雅黑', 10)).grid(row=2, column=3, sticky='w', padx=(5, 2), pady=5)
        self.ip_entry = ttk.Entry(controls, width=15)
        self.ip_entry.insert(0, "192.168.1.1")
        self.ip_entry.grid(row=2, column=4, sticky='w', padx=2, pady=5)

        ttk.Label(controls, text="端口：", font=('微软雅黑', 10)).grid(row=2, column=5, sticky='w', padx=(5, 2), pady=5)
        self.port_entry = ttk.Entry(controls, width=10)
        self.port_entry.insert(0, "2000")
        self.port_entry.grid(row=2, column=6, sticky='w', padx=2, pady=5)

        self.status_circle = tk.Label(controls, text="●", fg="red", font=('微软雅黑', 14))
        self.status_circle.grid(row=2, column=7, padx=(5, 2), pady=5)
        self.connect_btn = ttk.Button(controls, text="连接", command=self.connect_channel, width=8)
        self.connect_btn.grid(row=2, column=8, sticky='w', padx=2, pady=5)

        # 第3行
        ttk.Label(controls, text="工作状态：", font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', padx=(5, 2), pady=2)
        self.work_status_circle = tk.Label(controls, text="●", fg="red", font=('微软雅黑', 14))
        self.work_status_circle.grid(row=3, column=1, sticky='w', padx=2, pady=2)

        ttk.Label(controls, text="异常信息：", font=('微软雅黑', 10)).grid(row=3, column=3, sticky='w', padx=(5, 2), pady=2)
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
        ttk.Label(bottom_frame, text="生产企业类别代码：", font=('微软雅黑', 10)).grid(row=0, column=0, sticky='w', padx=(0, 5), pady=8)
        self.manufacture_code = ttk.Entry(bottom_frame, width=25)
        self.manufacture_code.insert(0, "D6")
        self.manufacture_code.grid(row=0, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="产品种类和名称：", font=('微软雅黑', 10)).grid(row=0, column=3, sticky='w', padx=(0, 5), pady=8)
        self.product_combo = ttk.Combobox(bottom_frame, width=33, values=["高密度震源药柱[箱]", "其他产品"], state="readonly")
        self.product_combo.set("高密度震源药柱[箱]")
        self.product_combo.grid(row=0, column=4, sticky='w', padx=5, pady=8)

        # 第6行
        ttk.Label(bottom_frame, text="生产许可证编号代码：", font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', padx=(0, 5), pady=8)
        self.license_code = ttk.Entry(bottom_frame, width=25)
        self.license_code.insert(0, "D6")
        self.license_code.grid(row=1, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="规格型号（数量）：", font=('微软雅黑', 10)).grid(row=1, column=3, sticky='w', padx=(0, 5), pady=8)
        self.spec_entry = ttk.Entry(bottom_frame, width=33)
        self.spec_entry.insert(0, "高密度震源药柱[箱]")
        self.spec_entry.grid(row=1, column=4, sticky='w', padx=5, pady=8)

        # 第7行
        ttk.Label(bottom_frame, text="包装方式：", font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', padx=(0, 5), pady=8)
        self.pack_entry = ttk.Entry(bottom_frame, width=25)
        self.pack_entry.insert(0, "D6")
        self.pack_entry.grid(row=2, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="净质量：", font=('微软雅黑', 10)).grid(row=2, column=3, sticky='w', padx=(0, 5), pady=8)
        self.net_weight = ttk.Entry(bottom_frame, width=33)
        self.net_weight.insert(0, "12")
        self.net_weight.grid(row=2, column=4, sticky='w', padx=5, pady=8)

        # 第8行
        ttk.Label(bottom_frame, text="生产批号：", font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', padx=(0, 5), pady=8)
        self.batch_entry = ttk.Entry(bottom_frame, width=25)
        self.batch_entry.insert(0, "D6")
        self.batch_entry.grid(row=3, column=1, sticky='w', padx=5, pady=8)

        ttk.Label(bottom_frame, text="生产日期：", font=('微软雅黑', 10)).grid(row=3, column=3, sticky='w', padx=(0, 5), pady=8)
        self.date_entry = ttk.Entry(bottom_frame, width=33)
        self.date_entry.insert(0, "20260101")
        self.date_entry.grid(row=3, column=4, sticky='w', padx=5, pady=8)

        # 第9行
        ttk.Label(bottom_frame, text="生产箱（袋）号：", font=('微软雅黑', 10)).grid(row=4, column=0, sticky='w', padx=(0, 5), pady=8)
        self.box_entry = ttk.Entry(bottom_frame, width=25)
        self.box_entry.insert(0, "10")
        self.box_entry.grid(row=4, column=1, sticky='w', padx=5, pady=8)

        self.send_btn = ttk.Button(bottom_frame, text="手动下发", command=self.manual_send, width=15)
        self.send_btn.grid(row=4, column=4, sticky='w', padx=5, pady=8)

        # ========== 系统日志区域 ==========
        log_frame = ttk.LabelFrame(content, text="系统日志", padding="5")
        log_frame.grid(row=1, column=0, sticky='nsew', pady=(10, 0))
        content.grid_rowconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=0)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
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
        """连接按钮回调：使用界面上的IP和端口建立Socket连接"""
        ip = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        if not port_str.isdigit():
            self.log_message(f"端口号无效: {port_str}", tag='error')
            messagebox.showerror("错误", "端口号必须是数字")
            return
        port = int(port_str)

        # 如果已有连接，先断开
        if self.socket_client and self.socket_client.get_connection_status():
            self.socket_client.disconnect()
            self.socket_client = None

        # 创建新的SocketClient实例
        self.socket_client = SocketClient(host=ip, port=port)

        # 设置回调函数（注意回调在子线程中运行，需用after调度到主线程）
        def on_connection(success, msg):
            self.root.after(0, lambda: self._on_connection_result(success, msg))

        def on_error(error_msg):
            self.root.after(0, lambda: self.log_message(f"Socket错误: {error_msg}", tag='error'))

        def on_receive(data):
            # 接收数据回调，可以在日志中显示
            self.root.after(0, lambda: self._on_receive_data(data))

        self.socket_client.set_callbacks(
            receive_callback=on_receive,
            connection_callback=on_connection,
            error_callback=on_error
        )

        # 尝试连接
        self.log_message(f"正在连接 {ip}:{port} ...", tag='info')
        self.socket_client.connect()  # 连接是异步的，结果会通过回调返回

    def _on_connection_result(self, success, msg):
        """处理连接结果（在主线程中执行）"""
        if success:
            self.status_circle.config(fg="green")
            self.work_status_circle.config(fg="green")
            self.log_message(f"连接成功: {msg}", tag='success')
        else:
            self.status_circle.config(fg="red")
            self.work_status_circle.config(fg="red")
            self.log_message(f"连接失败: {msg}", tag='error')
            # 清空客户端对象，避免后续误用
            if self.socket_client:
                self.socket_client.disconnect()
                self.socket_client = None

    def _on_receive_data(self, data):
        """接收到数据时的处理（在主线程中执行）"""
        if isinstance(data, dict):
            self.log_message(f"收到JSON数据: {data}", tag='info')
        elif isinstance(data, bytes):
            # 显示十六进制和字符串形式
            hex_str = data.hex().upper()
            try:
                ascii_str = data.decode('utf-8', errors='replace')
                self.log_message(f"收到二进制数据 ({len(data)}字节): HEX={hex_str}  ASCII={ascii_str}", tag='info')
            except:
                self.log_message(f"收到二进制数据 ({len(data)}字节): HEX={hex_str}", tag='info')
        else:
            self.log_message(f"收到未知类型数据: {data}", tag='info')

    def manual_send(self):
        """手动下发按钮：通过Socket发送数据（如果已连接）"""
        click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 收集界面数据
        data = {
            "device": self.device_entry.get(),
            "location": self.location_entry.get(),
            "channel": self.channel_combo.get(),
            "ip": self.ip_entry.get(),
            "port": self.port_entry.get(),
            "manufacture_code": self.manufacture_code.get(),
            "product": self.product_combo.get(),
            "license_code": self.license_code.get(),
            "spec": self.spec_entry.get(),
            "pack": self.pack_entry.get(),
            "net_weight": self.net_weight.get(),
            "batch": self.batch_entry.get(),
            "date": self.date_entry.get(),
            "box": self.box_entry.get(),
            "timestamp": click_time
        }

        # 如果Socket已连接，则发送数据
        if self.socket_client and self.socket_client.get_connection_status():
            try:
                self.socket_client.send_data(data)
                self.log_message(f"手动下发数据已发送 (批号: {data['batch']}, 箱号: {data['box']})", tag='success')
            except Exception as e:
                self.log_message(f"发送数据失败: {e}", tag='error')
        else:
            self.log_message("未连接到服务器，无法下发数据", tag='warning')
            # 可选：弹出提示
            messagebox.showwarning("未连接", "请先连接服务器再手动下发")

        # 同时保留原有的弹窗信息（便于调试）
        info = (f"手动下发时间：{click_time}\n"
                f"设备号：{data['device']}\n"
                f"当前位置：{data['location']}\n"
                f"通道机：{data['channel']}\n"
                f"IP：{data['ip']}  端口：{data['port']}\n"
                f"生产企业类别代码：{data['manufacture_code']}\n"
                f"产品种类和名称：{data['product']}\n"
                f"生产许可证编号代码：{data['license_code']}\n"
                f"规格型号：{data['spec']}\n"
                f"包装方式：{data['pack']}\n"
                f"净质量：{data['net_weight']}\n"
                f"生产批号：{data['batch']}\n"
                f"生产日期：{data['date']}\n"
                f"生产箱（袋）号：{data['box']}\n"
                f"指令已发送至通道机。")
        messagebox.showinfo("手动下发", info)
        print(info)
        print("-" * 50)

    def __del__(self):
        """析构时确保断开Socket连接"""
        if self.socket_client:
            self.socket_client.disconnect()


if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDTagGeneratorUI(root)
    root.state('zoomed')
    root.mainloop()