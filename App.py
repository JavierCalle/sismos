from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import date

app = Flask (__name__)


db = pymysql.connect(host='localhost',user='root',password='',db='Sismos_Ecuador')
cursor = db.cursor()
app.secret_key='mysecretkey'    

@app.route('/')
def home():
    cursor.execute('select * from sismos_historicos_ecuador order by fecha')
    datos = cursor.fetchall()
    #regresion_logistica()
    #redes_neuronales_recurrentes()
    #plt.plot([4,8,13,17,20],[54, 67, 98, 78, 45])
    #plt.show()
    return render_template('index.html',sismos=datos)

@app.route('/agregarsismo', methods=['POST'])
def agregarsismo():
    if request.method=='POST':
        magnitud = request.form['magnitud']
        fecha = request.form['fecha']
        hora = request.form['hora']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        profundidad = request.form['profundidad']
        epicentro = request.form['epicentro']
        sql = 'insert into sismos (magnitud,fecha,hora,latitud,longitud,profundidad,epicentro) values (%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(magnitud,fecha,hora,latitud,longitud,profundidad,epicentro))
        db.commit()
        flash('Sismo agregado satisfactoriamente')
        return redirect(url_for('home'))

@app.route('/obtenersismo/<id>')
def obtenersismo(id):
    cursor.execute('select * from sismos where id_sismo = {}'.format(id))
    dato = cursor.fetchall()
    print(dato[0])
    return render_template('edit_sismo.html',sismo=dato[0])


@app.route('/verprediccion')
def verprediccion():
    return render_template('prediccion.html')

@app.route('/vercontexto')
def vercontexto():
    return render_template('contexto.html')

@app.route('/verredesneuronales')
def verredesneuronales():
    return render_template('redesneuronales.html')

@app.route('/verregresionlogistica')
def verregresionlogistica():
    return render_template('regresionlogistica.html')

@app.route('/verdatosregresion')
def verdatosregresion():
    cursor.execute('select * from regresion')
    dato = cursor.fetchall()
    return render_template('datos_regresion.html',sismos=dato)

@app.route('/verdatosredes')
def verdatosredes():
    cursor.execute('select * from redes_neuronales_LSTM')
    dato = cursor.fetchall()
    return render_template('datos_redes.html',sismos=dato)

@app.route('/obtenersismo/editarsismo/<id>', methods=['POST'])
def editarsismo(id):
    if request.method=='POST':
        magnitud = request.form['magnitud']
        fecha = request.form['fecha']
        hora = request.form['hora']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        profundidad = request.form['profundidad']
        epicentro = request.form['epicentro']
        sql = 'update sismos set magnitud=%s,fecha=%s,hora=%s,latitud=%s,longitud=%s,profundidad=%s,epicentro=%s where id_sismo=%s'
        cursor.execute(sql,(magnitud,fecha,hora,latitud,longitud,profundidad,epicentro,id))
        db.commit()
        flash('Sismo editado satisfactoriamente')
        return redirect(url_for('home'))

@app.route('/eliminarsismo/<string:id>')
def eliminarsismo(id):
    cursor.execute('delete from sismos where id_sismo = {0}'.format(id))
    db.commit()
    flash('Sismo eliminado satisfactoriamente')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run (port=5000, debug=True)
