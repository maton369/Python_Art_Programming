class FunctionFactory:
    def __init__(self):
        self.functions = {}
        self.variables = {}

    def create_variable(self, name, value):
        try:
            # 型推論付きの変数評価
            try:
                evaluated = eval(value, globals())
            except Exception:
                # eval できないものは文字列として扱う
                evaluated = value

            globals()[name] = evaluated
            self.variables[name] = evaluated
            return True
        except Exception as e:
            print(f"変数エラー: {e}")
            return False

    def create_function(self, name, body):
        if not name.isidentifier():
            return False, "関数名が無効です"

        code = f"def {name}():\n"
        for line in body.strip().splitlines():
            code += "    " + line + "\n"  # インデント

        try:
            exec(code, globals())
            self.functions[name] = eval(name)
            return True, "関数を作成しました"
        except Exception as e:
            return False, str(e)
