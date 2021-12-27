from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import re

open("log.txt", 'w')
error_duplicate_email = 'It seems one of your friends already has this email. Two people can\'t have the same email'
error_invalid_email = 'It seems you have entered invalid email. Please, try again'
error_invalid_name = 'It seems you might have made a mistake. All names in Member Club should: use English alphabet only, be at least 2 letters long each and have no special characters or digits.'


def validate_name(name):
    return re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', name)

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

def write_log(name, email, return_data = "Rendered HTML page"):
    with open('log.txt', 'a') as logs_file:
        log_data = ("Time: {} \nInput in Name: {} \nInput in Email: {} \nWe returned: {} \n\n".format(datetime.now(), name, email, return_data))
        logs_file.write(log_data)
        logs_file.close()


app = Flask(__name__)
df = pd.DataFrame({'Name': [],
                   'Email': [],
                   'Registration date': []})


@app.route('/', methods=['POST', 'GET'])
def index():

    index_name = ''
    index_email = ''
    if request.method == 'POST':
        if validate_name((request.form['Name_ClassName']).strip()):
            index_name = (request.form['Name_ClassName']).strip()
            if validate_email((request.form['Email_ClassName']).strip()):
                index_email = (request.form['Email_ClassName']).strip()
                if not (index_email in df.Email.values):
                    df.loc[len(df.index)] = [index_name,
                                             index_email,
                                             datetime.now().strftime("%Y/%m/%d")]
                else:
                    index_name, index_email = request.form['Name_ClassName'].strip(), request.form['Email_ClassName'].strip()
                    return render_template('index.html',
                               tables=[df.to_html(classes='data')],
                               titles = df.columns.values,
                               error_duplicate_email = error_duplicate_email)
            else:
                index_name, index_email = request.form['Name_ClassName'].strip(), request.form['Email_ClassName'].strip()
                write_log(name=index_name, email=index_email, return_data=error_invalid_email)
                return render_template('index.html',
                               tables=[df.to_html(classes='data')],
                               titles = df.columns.values,
                               error_invalid_email = error_invalid_email)
        else:
            index_name, index_email = request.form['Name_ClassName'].strip(), request.form['Email_ClassName'].strip()
            write_log(name=index_name, email=index_email, return_data=error_invalid_name)
            return render_template('index.html',
                               tables=[df.to_html(classes='data')],
                               titles = df.columns.values,
                               error_invalid_name = error_invalid_name)
        write_log(name=index_name, email=index_email)
        return render_template('index.html',
                               tables=[df.to_html(classes='data')],
                               titles = df.columns.values)
    else:
        write_log(name=index_name, email=index_email)
        return render_template('index.html', tables=[df.to_html(classes='data')], titles = df.columns.values)

if __name__ == "__main__":
    app.run(debug=True)