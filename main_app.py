import tkinter as tk
from tkinter import messagebox, scrolledtext
from function_factory import FunctionFactory
from class_factory import ClassFactory


class App:

    def __init__(self, root, load_sample=True):
        self.root = root
        self.root.title("メタプログラミングGUI")
        self.factory = FunctionFactory()
        self.class_factory = ClassFactory()

        # --- 変数定義 ---
        tk.Label(root, text="変数名:").pack()
        self.var_name = tk.Entry(
            root, width=30, fg="black", bg="white", insertbackground="black"
        )
        self.var_name.pack()
        tk.Label(root, text="値:").pack()
        self.var_value = tk.Entry(root, width=30)
        self.var_value.pack()
        self.var_button = tk.Button(root, text="変数を追加", command=self.add_variable)
        self.var_button.pack(pady=5)

        # --- 関数定義 ---
        tk.Label(root, text="関数名:").pack()
        self.func_name = tk.Entry(root, width=30)
        self.func_name.pack()
        tk.Label(root, text="関数の中身 (複数行OK):").pack()
        self.func_body = scrolledtext.ScrolledText(root, height=5, width=40)
        self.func_body.pack()
        self.func_button = tk.Button(root, text="関数を追加", command=self.add_function)
        self.func_button.pack(pady=5)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # --- クラス定義 ---
        tk.Label(root, text="クラス名:").pack()
        self.class_name = tk.Entry(root, width=30)
        self.class_name.pack()
        tk.Label(root, text="継承元クラス名（任意）:").pack()
        self.base_class_name = tk.Entry(root, width=30)
        self.base_class_name.pack()
        tk.Label(root, text="プロパティ名:").pack()
        self.prop_name = tk.Entry(root, width=30)
        self.prop_name.pack()
        tk.Label(root, text="値:").pack()
        self.prop_value = tk.Entry(root, width=30)
        self.prop_value.pack()
        tk.Label(root, text="メソッド名:").pack()
        self.method_name = tk.Entry(root, width=30)
        self.method_name.pack()
        tk.Label(root, text="メソッドの中身 (複数行OK):").pack()
        self.method_body = scrolledtext.ScrolledText(root, height=5, width=40)
        self.method_body.pack()
        self.class_button = tk.Button(root, text="クラスを作成", command=self.add_class)
        self.class_button.pack(pady=5)
        self.class_button_frame = tk.Frame(root)
        self.class_button_frame.pack(pady=10)

        if load_sample:
            self.load_sample_from_file("sample.txt")

    def load_sample_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
            current = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("[var]"):
                    current = "var"
                    continue
                elif line.startswith("[func]"):
                    current = "func"
                    continue
                elif line.startswith("[class]"):
                    current = "class"
                    continue

                if current == "var":
                    if "=" in line:
                        k, v = line.split("=", 1)
                        self.var_name.delete(0, tk.END)
                        self.var_name.insert(0, k.strip())
                        self.var_value.delete(0, tk.END)
                        self.var_value.insert(0, v.strip())
                        self.add_variable()
                elif current == "func":
                    if line.startswith("name:"):
                        self.func_name.delete(0, tk.END)
                        self.func_name.insert(0, line.replace("name:", "").strip())
                    elif line.startswith("body:"):
                        body = line.replace("body:", "").strip().replace("\\n", "\n")
                        self.func_body.delete("1.0", tk.END)
                        self.func_body.insert("1.0", body)
                        self.add_function()
                elif current == "class":
                    if line.startswith("name:"):
                        self.class_name.delete(0, tk.END)
                        self.class_name.insert(0, line.replace("name:", "").strip())
                    elif line.startswith("base:"):
                        self.base_class_name.delete(0, tk.END)
                        self.base_class_name.insert(
                            0, line.replace("base:", "").strip()
                        )
                    elif "=" in line:
                        k, v = line.split("=", 1)
                        self.prop_name.delete(0, tk.END)
                        self.prop_name.insert(0, k.strip())
                        self.prop_value.delete(0, tk.END)
                        self.prop_value.insert(0, v.strip())
                    elif line.startswith("method:"):
                        method_def = line.replace("method:", "").strip().split("|", 1)
                        if len(method_def) == 2:
                            self.method_name.delete(0, tk.END)
                            self.method_name.insert(0, method_def[0].strip())
                            self.method_body.delete("1.0", tk.END)
                            self.method_body.insert(
                                "1.0", method_def[1].replace("\\n", "\n")
                            )
                            self.add_class()
        except Exception as e:
            messagebox.showerror("読み込みエラー", str(e))

    def add_variable(self):
        name = self.var_name.get().strip()
        value = self.var_value.get().strip()
        if not name.isidentifier():
            messagebox.showerror("エラー", "有効な変数名を入力してください")
            return
        if self.factory.create_variable(name, value):
            messagebox.showinfo("成功", f"変数 {name} = {value} を作成しました")
        else:
            messagebox.showerror("失敗", f"{name} を作成できませんでした")

    def add_function(self):
        name = self.func_name.get().strip()
        body = self.func_body.get("1.0", tk.END)
        success, msg = self.factory.create_function(name, body)
        if success:
            # 同名ボタンがあれば削除
            for widget in self.button_frame.winfo_children():
                if widget.cget("text") == f"{name} を実行":
                    widget.destroy()

            btn = tk.Button(
                self.button_frame,
                text=f"{name} を実行",
                command=lambda: self.run_function(name),
            )
            btn.pack(pady=2)
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("エラー", msg)

    def run_function(self, name):
        try:
            self.factory.functions[name]()
        except Exception as e:
            messagebox.showerror("実行エラー", str(e))

    def add_class(self):
        name = self.class_name.get().strip()
        base_name = self.base_class_name.get().strip()
        prop_name = self.prop_name.get().strip()
        prop_value = self.prop_value.get().strip()
        props = ""
        if prop_name and prop_value:
            props = f"{prop_name} = {prop_value}"
        method_name = self.method_name.get().strip()
        method_body = self.method_body.get("1.0", tk.END).strip()
        methods = {}
        if method_name and method_body:
            methods[method_name] = method_body

        success, msg = self.class_factory.create_class(
            name, props, methods, base_name or None
        )
        if success:
            # 同名クラスのメソッドボタンをクリア
            for widget in self.class_button_frame.winfo_children():
                if widget.cget("text").startswith(f"{name}."):
                    widget.destroy()

            instance = self.class_factory.instances[name]
            for attr in dir(instance):
                if callable(getattr(instance, attr)) and not attr.startswith("__"):
                    btn = tk.Button(
                        self.class_button_frame,
                        text=f"{name}.{attr}() を実行",
                        command=lambda n=name, a=attr: self.run_class_method(n, a),
                    )
                    btn.pack(pady=2)
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("エラー", msg)

    def run_class_method(self, class_name, method_name):
        try:
            instance = self.class_factory.instances[class_name]
            getattr(instance, method_name)()
        except Exception as e:
            messagebox.showerror("実行エラー", str(e))
