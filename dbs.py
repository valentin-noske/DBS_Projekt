import re
from flask import Flask, render_template, request
from flask_wtf import FlaskForm,Form
import os
import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from werkzeug.utils import redirect
from wtforms.fields.core import SelectField


def plot(country, indicator):
    if indicator in economic_output:
        indicator_table = "Economic_Output"
    elif indicator in energy:
        indicator_table = "Energy"
    else:
        indicator_table = "Population"

    mycursor.execute("Select Distinct CO2_Emission, P.Year, " + indicator + " From (Country C Join " + indicator_table +
                     " X ON C.Country_Code = X.Country_Code) Left Join Pollution P ON C.Country_Code = P.Country_Code And P.Year = X.Year Where C.Name = '" + country + "' And P.Year BETWEEN 1950 And 2015")

    myresult = mycursor.fetchall()

    mycursor.execute(
        "Select CO2_Emission From Pollution ORDER By CO2_Emission Desc LIMIT 1")

    mycursor.execute(
        "Select " + indicator + " From " + indicator_table + " ORDER By " + indicator + " Desc LIMIT 1")

    co2_x = []
    co2_y = []
    indicator_x = []
    indicator_y = []

    for x in myresult:
        if x[0] != None:
            co2_x.append(x[0])
            co2_y.append(x[1])
        if x[2] != None:
            indicator_x.append(x[2])
            indicator_y.append(x[1])

    fig, ax1 = plt.subplots()
    ax1.set_title(country)
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Co2_Emission', color='green')
    ax1.plot(co2_y, co2_x, color='green')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.set_ylabel(indicator, color='blue')
    ax2.plot(indicator_y, indicator_x, color='blue')
    ax2.tick_params(axis='y', labelcolor='black')

    fig.tight_layout()
    plt.savefig("static/test.png")

mydb = mysql.connector.connect(
    host="localhost",
    user="valentin",
    password="Mastermind",
    database="DBS_Project"
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.debug = True

mycursor = mydb.cursor(buffered=True)

population = ['Population_total', 'Population_growth']
economic_output = ['GDP', 'Live_Animals', 'Manufacturing_Employment']
energy = ['Energy_Consumption', 'Atomic_Energy', 'Coal_Energy', 'Renewable_Energy']
indicators = []
for x in (population+economic_output+energy):
    indicators.append(x)
mycursor.execute("Select Name From Country")
result = mycursor.fetchall()
countries = []
for x in result:
    countries.append(x[0])

class Form(FlaskForm):
    indicator = SelectField('indicator', choices=indicators)
    country = SelectField('country', choices=countries)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        country = str(request.form.get('country'))
        indicator = str(request.form.get('indicator'))
        plot(country, indicator)
        return redirect('/')
    else:
        form = Form()
        return render_template('test.html', form=form)




if __name__ == "__main__":
    
    app.run(port=int(os.getenv('PORT', 5000)))


