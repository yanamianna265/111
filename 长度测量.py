import tkinter as tk
from tkinter import ttk, messagebox
import random

class BeautifulApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        # 配置主窗口
        self.root.title("🎯 随机长度生成器 - 美化版")
        self.root.geometry("600x400")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(True, True)
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # 配置不同元素的样式
        style.configure('Title.TLabel', 
                       font=('Arial', 20, 'bold'),
                       background='#2C3E50',
                       foreground='#E74C3C')
        
        style.configure('Normal.TLabel',
                       font=('Arial', 12),
                       background='#2C3E50',
                       foreground='#ECF0F1')
        
        style.configure('Custom.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10),
                       background='#E74C3C',
                       foreground='white')
        
        style.configure('Success.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10),
                       background='#27AE60',
                       foreground='white')
    
    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, 
                               text="🎯 随机长度生成器", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, 
                 text="请输入您的姓名：", 
                 style='Normal.TLabel').pack(anchor='w')
        
        self.name_entry = ttk.Entry(input_frame, 
                                   font=('Arial', 12),
                                   width=30)
        self.name_entry.pack(fill=tk.X, pady=5)
        self.name_entry.bind('<Return>', lambda e: self.generate_length())
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, 
                  text="🚀 生成随机长度", 
                  style='Success.TButton',
                  command=self.generate_length).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, 
                  text="🎪 弹窗显示结果", 
                  style='Custom.TButton',
                  command=self.show_popup_result).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, 
                  text="❌ 退出", 
                  style='Custom.TButton',
                  command=self.root.quit).pack(side=tk.LEFT, padx=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, 
                                     text=" 📊 生成结果 ",
                                     style='Normal.TLabel')
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, 
                                  font=('Consolas', 11),
                                  bg='#1C2833',
                                  fg='#F39C12',
                                  wrap=tk.WORD,
                                  height=8,
                                  relief=tk.FLAT,
                                  borderwidth=2)
        
        scrollbar = ttk.Scrollbar(result_frame, 
                                 orient=tk.VERTICAL, 
                                 command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # 初始提示
        self.show_initial_message()
    
    def show_initial_message(self):
        initial_text = "✨ 欢迎使用随机长度生成器！\n\n"
        initial_text += "📝 请在上方输入您的姓名\n"
        initial_text += "🚀 点击按钮生成0-30厘米的随机长度\n"
        initial_text += "🎪 使用弹窗功能在独立窗口查看结果\n"
        initial_text += "🎯 相同姓名会得到相同结果\n\n"
        initial_text += "等待您的输入..."
        self.result_text.insert(tk.END, initial_text)
        self.result_text.config(state=tk.DISABLED)
    
    def generate_length(self, name=None):
        """生成随机长度并在主界面显示"""
        if name is None:
            name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showerror("输入错误", "⚠️ 请输入有效的姓名！")
            return None
        
        # 生成随机长度
        random.seed(name)
        length = random.randint(0, 30)
        
        # 在主界面显示结果
        self.display_result_in_main(name, length)
        
        return length
    
    def display_result_in_main(self, name, length):
        """在主界面文本框中显示结果"""
        # 清空并更新结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 根据长度设置颜色和评价
        comment, color = self.get_comment_and_color(length)
        
        # 格式化输出
        result = f"🎯 生成结果详情\n"
        result += f"{'='*30}\n\n"
        result += f"👤 姓名：{name}\n"
        result += f"📏 长度：{length} 厘米\n"
        result += f"💬 评价：{comment}\n\n"
        result += f"🎲 唯一标识：{hash(name) % 10000:04d}\n"
        result += f"⭐ 等级：{'★★★★★' if length > 25 else '★★★★' if length > 20 else '★★★' if length > 10 else '★★' if length > 5 else '★'}"
        
        self.result_text.insert(tk.END, result)
        self.result_text.tag_configure("color", foreground=color)
        self.result_text.tag_add("color", "3.0", "3.end")
        self.result_text.config(state=tk.DISABLED)
    
    def get_comment_and_color(self, length):
        """根据长度获取评价和颜色"""
        if length <= 5:
            return "🔻 非常短小精悍！", "#E74C3C"
        elif length <= 10:
            return "📏 有点短哦～", "#E67E22"
        elif length <= 20:
            return "✅ 中等长度，刚刚好！", "#F1C40F"
        elif length <= 25:
            return "📐 长度不错哟！", "#2ECC71"
        else:
            return "🚀 超级长度，太棒了！", "#9B59B6"
    
    def show_popup_result(self):
        """在弹窗中显示结果"""
        name = self.name_entry.get().strip()
        
        if not name:
            messagebox.showerror("输入错误", "⚠️ 请输入有效的姓名！")
            return
        
        # 生成长度
        length = self.generate_length(name)
        if length is None:
            return
        
        # 创建弹窗
        self.create_result_popup(name, length)
    
    def create_result_popup(self, name, length):
        """创建结果弹窗"""
        # 创建新窗口
        popup = tk.Toplevel(self.root)
        popup.title("🎯 随机长度生成结果")
        popup.geometry("500x400")
        popup.configure(bg='#34495E')
        popup.resizable(False, False)
        popup.transient(self.root)  # 设置为主窗口的子窗口
        popup.grab_set()  # 模态窗口
        
        # 居中显示
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (500 // 2)
        y = (popup.winfo_screenheight() // 2) - (400 // 2)
        popup.geometry(f"+{x}+{y}")
        
        # 获取评价和颜色
        comment, color = self.get_comment_and_color(length)
        
        # 弹窗内容
        main_frame = tk.Frame(popup, bg='#34495E', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, 
                              text="🎯 长度生成结果", 
                              font=('Arial', 20, 'bold'),
                              bg='#34495E',
                              fg='#E74C3C')
        title_label.pack(pady=(0, 20))
        
        # 用户信息框
        info_frame = tk.LabelFrame(main_frame, 
                                  text=" 👤 用户信息 ",
                                  font=('Arial', 12, 'bold'),
                                  bg='#2C3E50',
                                  fg='#ECF0F1',
                                  relief=tk.GROOVE,
                                  bd=2)
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, 
                text=f"姓名：{name}",
                font=('Arial', 12),
                bg='#2C3E50',
                fg='#ECF0F1').pack(pady=10)
        
        # 结果框
        result_frame = tk.LabelFrame(main_frame, 
                                    text=" 📏 生成结果 ",
                                    font=('Arial', 12, 'bold'),
                                    bg='#2C3E50',
                                    fg='#ECF0F1',
                                    relief=tk.GROOVE,
                                    bd=2)
        result_frame.pack(fill=tk.X, pady=10)
        
        # 长度显示（大字体突出显示）
        length_label = tk.Label(result_frame, 
                               text=f"{length} 厘米",
                               font=('Arial', 24, 'bold'),
                               bg='#2C3E50',
                               fg=color)
        length_label.pack(pady=15)
        
        # 评价
        comment_label = tk.Label(result_frame, 
                                text=comment,
                                font=('Arial', 14),
                                bg='#2C3E50',
                                fg='#ECF0F1')
        comment_label.pack(pady=5)
        
        # 进度条显示
        progress_frame = tk.Frame(result_frame, bg='#2C3E50')
        progress_frame.pack(fill=tk.X, pady=10, padx=20)
        
        # 进度条标签
        tk.Label(progress_frame, 
                text="长度进度：",
                font=('Arial', 10),
                bg='#2C3E50',
                fg='#BDC3C7').pack(anchor='w')
        
        # 自定义进度条
        progress_bg = tk.Frame(progress_frame, bg='#7F8C8D', height=20)
        progress_bg.pack(fill=tk.X, pady=5)
        
        progress_width = (length / 30) * 440  # 计算进度条宽度
        progress_fg = tk.Frame(progress_bg, bg=color, height=20, width=progress_width)
        progress_fg.place(relx=0, rely=0, relheight=1.0)
        
        # 进度百分比
        percent_label = tk.Label(progress_frame, 
                                text=f"{length}/30 厘米 ({length/30*100:.1f}%)",
                                font=('Arial', 10),
                                bg='#2C3E50',
                                fg='#ECF0F1')
        percent_label.pack(anchor='e')
        
        # 详细信息
        detail_frame = tk.LabelFrame(main_frame, 
                                   text=" 📊 详细信息 ",
                                   font=('Arial', 12, 'bold'),
                                   bg='#2C3E50',
                                   fg='#ECF0F1',
                                   relief=tk.GROOVE,
                                   bd=2)
        detail_frame.pack(fill=tk.X, pady=10)
        
        details = f"""唯一标识：{hash(name) % 10000:04d}
等级评价：{'★★★★★' if length > 25 else '★★★★' if length > 20 else '★★★' if length > 10 else '★★' if length > 5 else '★'}
随机种子：{name}"""
        
        detail_text = tk.Text(detail_frame, 
                             height=4,
                             font=('Consolas', 10),
                             bg='#1C2833',
                             fg='#F39C12',
                             relief=tk.FLAT,
                             wrap=tk.WORD)
        detail_text.insert(tk.END, details)
        detail_text.config(state=tk.DISABLED)
        detail_text.pack(fill=tk.X, padx=10, pady=10)
        
        # 按钮区域
        button_frame = tk.Frame(main_frame, bg='#34495E')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, 
                 text="🔄 再次生成", 
                 font=('Arial', 11, 'bold'),
                 bg='#3498DB',
                 fg='white',
                 relief=tk.RAISED,
                 bd=2,
                 command=lambda: self.regenerate_in_popup(popup, name)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, 
                 text="✅ 关闭", 
                 font=('Arial', 11, 'bold'),
                 bg='#27AE60',
                 fg='white',
                 relief=tk.RAISED,
                 bd=2,
                 command=popup.destroy).pack(side=tk.LEFT, padx=10)
    
    def regenerate_in_popup(self, popup, name):
        """在弹窗中重新生成"""
        popup.destroy()  # 关闭当前弹窗
        self.show_popup_result()  # 重新打开弹窗

def main():
    root = tk.Tk()
    app = BeautifulApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()