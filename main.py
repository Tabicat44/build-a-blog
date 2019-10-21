from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import cgi
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildit@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "Iwishtherewerentants"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    #submitted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.submitted = False

@app.route('/blog')
def index():

    blog_id = str(request.args.get("id"))
    this_blog = Blog.query.get(blog_id)
    
    theblog = Blog.query.all()

    return render_template('blog.html', myblog=theblog, perblog = this_blog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_name = request.form['newtitle']
        blog_content = request.form['newpost']

        if len(blog_name) == 0 or len(blog_content) == 0:
            flash("Woah, there! You can't leave that empty!", "error_message")
        else:
            new_blog = Blog(blog_name, blog_content)
            db.session.add(new_blog)
            db.session.commit()

        
            return redirect('/blog?id=' + str(new_blog.id))
          

    return render_template('newpost.html')

# @app.route('/show-blog', methods=['GET'])
# def show_the_blog():

#     blog_id = request.args.get('id')
#     new_blog = Blog.query.get(blog_id)
#     return render_template('show-blog.html'.format(new_blog), myblog=new_blog)
        
    # tasks = Task.query.filter_by(completed=False).all()
    # completed_tasks = Task.query.filter_by(completed=True).all()
    # return render_template('thepages.html',title="Blogapalooza", 
    #     tasks=tasks, completed_tasks=completed_tasks)


# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()