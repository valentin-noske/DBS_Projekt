from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True


#Connection-Object= mysql.connector.connect(host = <host-name> , user = <username> , passwd = <password> )  

@app.route('/', methods=['GET'])
def dropdown():
    indicators = ['Erneuerbare-Energie', 'BIP']
    countries = ['Germany', 'France']
    return render_template('test.html', indicators=indicators, countries=countries)




if __name__ == "__main__":
    app.run()
