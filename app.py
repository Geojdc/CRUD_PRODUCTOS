from flask import Flask,render_template,url_for,request,redirect
import sqlite3

app= Flask (__name__)
#Creacion de bd y tabla
def inicializar_bd():
    conn=sqlite3.connect("almacen.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto(
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
        )
        """
    )
    # cursor.execute(
    #     """
    #     INSERT INTO producto (descripcion,cantidad,precio)VALUES('Escoba',2,10)
    #     """
    # )
    # cursor.execute(
    #     """
    #     DELETE FROM producto where id=4
    #     """
    # )
    conn.commit()
    conn.close()
inicializar_bd()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos")
def productos():
    conn=sqlite3.connect("almacen.db")
    #permite manejar los registros como diccionarios
    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()
    cursor.execute("select * from producto")
    #para recuperar los registros guardar dentro de la variable productos
    productos=cursor.fetchall()
    #para mostrar
    return render_template("productos/index.html",productos=productos)

@app.route("/productos/nuevo")
def nuevo():
    return render_template('/productos/nuevo.html')
# funcion para guardar los datos del formulario
@app.route("/productos/nuevo/guardar",methods=['POST'])
def guardar():
    descripcion=request.form['descripcion']
    cantidad=request.form['cantidad']
    precio=request.form['precio']

    conn=sqlite3.connect("almacen.db")
    cursor=conn.cursor()

    cursor.execute("INSERT INTO producto (descripcion,cantidad,precio)VALUES(?,?,?)",(descripcion,cantidad,precio))
    conn.commit()
    conn.close()
    return redirect('/productos')

# editar
@app.route("/productos/editar/<int:id>")
def editar(id):
    conn=sqlite3.connect("almacen.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("select * from producto where id=?",(id,))
    # para obtener el registro  se usa fetchone  para un solo registro y lo guardamos en la variable 
    # producto
    producto= cursor.fetchone()
    conn.close()
    # luego aqui enviar a ese formulario de editar.html para recuperar los datos
    return render_template("/productos/editar.html",producto=producto)
#  aqui crear otra funcion para guardar los datos de editar
@app.route("/productos/actualizar",methods=['POST'])
def actualizar():
    id=request.form['id']
    descripcion=request.form['descripcion']
    cantidad=request.form['cantidad']
    precio=request.form['precio']
    conn=sqlite3.connect("almacen.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE producto set descripcion=?,cantidad=?,precio=? where id=?",(descripcion,cantidad,precio,id))
    conn.commit()
    conn.close()
    return redirect ("/productos")

# eliminar
@app.route("/productos/eliminar/<int:id>")
def eliminar(id):
    conn=sqlite3.connect("almacen.db")
    cursor=conn.cursor()
    cursor.execute("delete from producto where id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

        
        
        
    















if __name__=="__main__":
    app.run(debug=True)
