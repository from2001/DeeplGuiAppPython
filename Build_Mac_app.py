import os

# 変換したいPythonスクリプトのファイル名
script_name = "DeeplGuiApp"

# py2appを使用してアプリケーションを作成する
os.system("py2applet --make-setup {}".format(script_name))
os.system("python setup.py py2app -A")

# 完了メッセージを表示する
print("Done.")
