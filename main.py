#!/usr/bin/env python
import os
import jinja2
import webapp2
from model import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")
    def post(self):
        new_task = self.request.get("input_text")
        new_task = Message(text=new_task)
        new_task.put()
        return self.render_template("new_tasks.html", params={"new_task" : new_task} )
class TaskHandler(BaseHandler):
    def get(self):
        tasks = Message().query(Message.delete != True).fetch()
        return self.render_template("tasks.html", params={"tasks" : tasks} )

class SingleTaskHandler(BaseHandler):
    def get(self, message_id):
        task = Message.get_by_id(int(message_id))
        return self.render_template("task.html", params={
            "task": task})

class EditTaskHandler(BaseHandler):
    def get(self, message_id):
        message= Message.get_by_id(int(message_id))
        return self.render_template("task-edit.html", params={
            "message": message
        })
    def post(self, message_id):
        message_text = self.request.get("message_text")
        message = Message.get_by_id(int(message_id))
        message.text = message_text
        message.put()
        return self.redirect_to("tasks")

class DeleteTaskHandler(BaseHandler):
    def get(self, message_id):
        message= Message.get_by_id(int(message_id))
        return self.render_template("task-delete.html", params={
            "message": message
        })
    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.delete = True
        message.put()
        return self.redirect_to("tasks")

class StatusTaskHandler(BaseHandler):
    def get(self, message_id):
        message= Message.get_by_id(int(message_id))
        return self.render_template("status.html", params={
            "message": message
        })
    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.status = True
        message.put()
        return self.redirect_to("tasks")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/tasks', TaskHandler, name="tasks"),
    webapp2.Route('/task/<message_id:\d+>', SingleTaskHandler),
    webapp2.Route('/task/edit/<message_id:\d+>', EditTaskHandler),
    webapp2.Route('/task/delete/<message_id:\d+>', DeleteTaskHandler),
    webapp2.Route('/task/status/<message_id:\d+>', StatusTaskHandler),

], debug=True)
