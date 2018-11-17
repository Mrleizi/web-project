from flask_script import Manager

# 创建app
from utils.app import create_app
from utils.config import Config

app = create_app(Config)

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
