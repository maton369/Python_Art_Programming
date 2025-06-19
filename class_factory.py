class ClassFactory:
    def __init__(self):
        self.classes = {}
        self.instances = {}

    def create_class(self, name, props, methods, base_class_name=None):
        if not name.isidentifier():
            return False, "クラス名が無効です"

        class_dict = {}

        # プロパティ定義
        try:
            for line in props.strip().splitlines():
                var_code = line.strip()
                if "=" in var_code:
                    key, val = var_code.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    try:
                        evaluated = eval(val, globals())
                    except Exception:
                        evaluated = val  # クォートがなくても文字列として扱う
                    class_dict[key] = evaluated
        except Exception as e:
            return False, f"プロパティ定義エラー: {e}"

        # メソッド定義（辞書形式で受け取り、キーがメソッド名、値が処理内容）
        try:
            for method_name, body in methods.items():
                if not method_name.isidentifier():
                    return False, f"無効なメソッド名: {method_name}"
                method_body = "\n".join(
                    "    " + line for line in body.strip().splitlines()
                )
                method_code = f"def {method_name}(self):\n{method_body}"
                exec(method_code, globals(), class_dict)
        except Exception as e:
            return False, f"メソッド定義エラー: {e}"

        # クラス作成
        try:
            new_class = type(name, (object,), class_dict)
            self.classes[name] = new_class
            self.instances[name] = new_class()
            return True, f"クラス {name} を作成しました"
        except Exception as e:
            return False, f"クラス作成エラー: {e}"
