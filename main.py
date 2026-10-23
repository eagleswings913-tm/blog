from flask import Flask, render_template, url_for
from post import Post
import requests

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

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
    return render_template("post.html", post=requested_post, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
