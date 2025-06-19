class ClassFactory:
    def __init__(self):
        self.classes = {}
        self.instances = {}

    def create_class(self, name, props, methods):
        if not name.isidentifier():
            return False, "クラス名が無効です"

        class_dict = {}

        # プロパティの定義をclass_dictへ
        try:
            for line in props.strip().splitlines():
                exec(line, globals(), class_dict)
        except Exception as e:
            return False, f"プロパティ定義エラー: {e}"

        # メソッド定義をclass_dictへ
        try:
            exec(methods, globals(), class_dict)
        except Exception as e:
            return False, f"メソッド定義エラー: {e}"

        try:
            new_class = type(name, (object,), class_dict)
            self.classes[name] = new_class
            self.instances[name] = new_class()
            return True, f"クラス {name} を作成しました"
        except Exception as e:
            return False, f"クラス作成エラー: {e}"
