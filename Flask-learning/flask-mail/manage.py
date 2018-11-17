from flask import Flask
from flask_mail import Mail, Message

from flask_script import Manager

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 465  # 设置邮箱端口为465，默认为25，由于阿里云禁止了25端口，所以需要修改
app.config["MAIL_USE_SSL"] = True  # 163邮箱需要开启SSL
app.config['MAIL_USE_TLS'] = False

app.config["MAIL_USERNAME"] = "1982540042@qq.com"
app.config["MAIL_PASSWORD"] = "kzxuedxlbsvaceaf"  # 这里为开启IMAP/SMTP所获取的授权码

# mail = Mail(app)
mail = Mail()
mail.init_app(app)


@app.route("/send_mail/")
def send_mail():
    """
    发送邮件， sender为发送者邮箱， recipients为接受者邮箱
    """
    message = Message(subject="测试邮件标题", sender=app.config["MAIL_USERNAME"], recipients=["1290368872@qq.com"])
    message.body = "测试邮件的内容1  你好啊!! what are you doing now"
    message.html = "<h1 style='color:red;'>Hello Friend, How Are You ?</h1>"

    # mail.send(message)

    # 或者调用下面的方法
    send_email(message)

    return "邮件1发送成功!"


def send_email(msg):
    with app.app_context():
        mail.send(msg)


manage = Manager(app=app)

if __name__ == "__main__":
    manage.run()
