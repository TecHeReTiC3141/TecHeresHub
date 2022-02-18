from markupsafe import escape
from jinja2 import Template, FileSystemLoader, Environment

data = [{'Name': 'Tec', 'Age': 16, 'Job': 'ML'},
        {'Name': 'Ovad', 'Age': 17, 'Job': 'Physics'},
        {'Name': 'jedoron', 'Age': 14, 'Job': 'friend'}]


file_loader = FileSystemLoader('../templates')
env = Environment(loader=file_loader)
templ = env.get_template('reqister_form.html')


print(templ.render(title='Register, please'))
