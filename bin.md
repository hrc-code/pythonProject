### 安装虚拟环境  最后一个为虚拟环境的名字
python -m venv .venv
### 激活虚拟环境
.venv\Scripts\activate
### 退出虚拟环境
deactivate
### 导入依赖
pip install -r requirements.txt
### 导出依赖
pip freeze > requirements.txt
