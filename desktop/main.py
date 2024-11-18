import tkinter as tk
from tkinter import filedialog
import csv
from tkinter import messagebox
from tkinterweb import HtmlFrame

class TableHeader:
    def __init__(self, headers):
        self.headers = headers
    
    def render(self):
        """ヘッダー部分のHTMLを生成"""
        header_html = "<tr>"
        for header in self.headers:
            header_html += f"<th>{header}</th>"
        header_html += "</tr>"
        return header_html

class TableRow:
    def __init__(self, row_data):
        self.row_data = row_data
    
    def render(self):
        """1行分のデータをHTMLに変換"""
        row_html = "<tr>"
        for cell in self.row_data:
            row_html += f"<td>{cell}</td>"
        row_html += "</tr>"
        return row_html

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        
        # GUI要素
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        # メニューバー
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 「ファイル」メニュー
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open CSV", command=self.load_csv)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # HTML表示用フレーム
        self.html_frame = HtmlFrame(self.frame)
        self.html_frame.pack(fill=tk.BOTH, expand=True)
        
        # CSVデータ
        self.data = []
    
    def load_csv(self):
        # CSVファイルの選択ダイアログを表示
        file_path = filedialog.askopenfilename(
            title="Open CSV File", 
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if not file_path:
            return
        
        # CSVファイルの読み込み
        try:
            with open(file_path, mode='r', encoding='shift_jis') as file:
                reader = csv.reader(file)
                self.data = list(reader)
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file\n{str(e)}")
    
    def display_data(self):
        if not self.data:
            return
        
        # HTMLテーブルの作成
        html_content = "<html><body><table border='1' style='border-collapse: collapse;'>"
        
        # ヘッダーコンポーネント
        header_component = TableHeader(self.data[0])
        html_content += header_component.render()
        
        # 行コンポーネント
        for row in self.data[1:]:
            row_component = TableRow(row)
            html_content += row_component.render()
        
        html_content += "</table></body></html>"
        
        # HTMLを表示
        self.html_frame.load_html(html_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
