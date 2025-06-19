import unittest
import tkinter as tk
from main_app import App


class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Toplevel()
        self.app = App(self.root, load_sample=False)

    def tearDown(self):
        self.root.destroy()

    def test_variable_creation(self):
        self.app.var_name.delete(0, tk.END)
        self.app.var_value.delete(0, tk.END)
        self.app.var_name.insert(0, "test_var")
        self.app.var_value.insert(0, "123")
        self.app.add_variable()
        self.assertIn("test_var", self.app.factory.variables)
        self.assertEqual(self.app.factory.variables["test_var"], 123)

    def test_function_creation_and_run(self):
        self.app.factory.variables.clear()
        self.app.factory.functions.clear()
        self.app.func_name.delete(0, tk.END)
        self.app.func_body.delete("1.0", tk.END)
        self.app.func_name.insert(0, "hello")
        self.app.func_body.insert("1.0", 'print("Hello World")')
        self.app.add_function()
        self.assertIn("hello", self.app.factory.functions)
        # 実行して例外が起きないか確認
        self.app.run_function("hello")

    def test_class_creation_and_method(self):
        self.app.factory.variables.clear()
        self.app.factory.functions.clear()
        self.app.class_factory.classes.clear()
        self.app.class_factory.instances.clear()
        self.app.class_name.delete(0, tk.END)
        self.app.prop_name.delete(0, tk.END)
        self.app.prop_value.delete(0, tk.END)
        self.app.method_name.delete(0, tk.END)
        self.app.method_body.delete("1.0", tk.END)
        self.app.class_name.insert(0, "TestClass")
        self.app.prop_name.insert(0, "x")
        self.app.prop_value.insert(0, "10")
        self.app.method_name.insert(0, "show")
        self.app.method_body.insert("1.0", "print(self.x)")
        self.app.add_class()
        cls = self.app.class_factory.classes["TestClass"]
        instance = self.app.class_factory.instances["TestClass"]
        self.assertTrue(hasattr(instance, "x"))
        self.assertEqual(instance.x, 10)
        self.assertTrue(callable(getattr(instance, "show", None)))


if __name__ == "__main__":
    unittest.main()
