from flask import Flask, render_template, url_for, request
from post import Post
import requests
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

blog_url = "https://api.npoint.io/447fc531556504b2223e"
posts = requests.get(blog_url).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"], post["author"], post["date"], post["image"])
    post_objects.append(post_obj)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", all_posts=post_objects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # name = request.form["name"]
        # email = request.form["email"]
        # phone = request.form["phone"]
        # message = request.form["message"]
        # return f"name = {name}, email = {email}, phone = {phone}, message = {message}"
        send_email()
        return render_template('contact.html', sent_successfully=True)
    else:
        return render_template('contact.html', sent_successfully=False)

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
            image_path = 'assets/img/' + requested_post.image
            print(image_path)
            image_url = url_for('static', filename=image_path)
            print(image_url)
            return render_template("post.html", post=requested_post, image_url=image_url, error_message="")
    return render_template("post.html", post="", image_url="", error_message=f"Post with index : {index} NOT FOUND")

def send_email():
    app_password = os.getenv("APP_PASSWORD")
    receiver_email = os.getenv("EMAIL_TO")
    if not receiver_email or not app_password:
        raise ValueError("Missing environment variables for email or password.")
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    email_message = f"name = {name}, email = {email}, phone = {phone}, message = {message}"
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = receiver_email
    message["Subject"] = "New Contact"
    message.attach(MIMEText(email_message))
    message_string = message.as_string()
    # send email
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user= receiver_email, password= app_password)

        connection.sendmail(
            from_addr=email,
            to_addrs=receiver_email,
            msg=message_string
        )

def send_email2():
    app_password = os.getenv("APP_PASSWORD")
    receiver_email = os.getenv("EMAIL_TO")
    if not receiver_email or not app_password:
        raise ValueError("Missing environment variables for email or password.")
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    email_message = f"name = {name}, email = {email}, phone = {phone}, message = {message}"
    email = EmailMessage()
    email['from'] = request.form["name"]
    email['to'] = receiver_email
    email['subject'] = "New Contact"
    email.set_content(email_message)

    with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as smtp:
        smtp.login(user=receiver_email, password=app_password)
        smtp.send_message(email)
        print('Email sent!')

if __name__ == "__main__":
    app.run(debug=True)
