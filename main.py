from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_promedio(nota1, nota2, nota3):
    return round((nota1 + nota2 + nota3) / 3, 1)


def obtener_estado(promedio, asistencia):
    if promedio >= 40 and asistencia >= 75:
        return "APROBADO"
    return "REPROBADO"


def nombre_mas_largo(nombres):
    mayor = nombres[0]
    for nombre in nombres:
        if len(nombre) > len(mayor):
            mayor = nombre
    return mayor, len(mayor)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    valores = {}
    promedio = None
    estado = None
    error = None

    if request.method == "POST":
        valores = request.form
        try:
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            nota3 = float(request.form["nota3"])
            asistencia = float(request.form["asistencia"])
        except ValueError:
            error = "Todos los campos deben ser numeros."
        else:
            notas_validas = all(10 <= n <= 70 for n in (nota1, nota2, nota3))
            if not notas_validas:
                error = "Las notas deben estar entre 10 y 70."
            elif not 0 <= asistencia <= 100:
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio = calcular_promedio(nota1, nota2, nota3)
                estado = obtener_estado(promedio, asistencia)

    return render_template("ejercicio1.html", valores=valores,
                           promedio=promedio, estado=estado, error=error)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    valores = {}
    nombre = None
    cantidad = None
    error = None

    if request.method == "POST":
        valores = request.form
        nombres = [request.form["nombre1"].strip(),
                   request.form["nombre2"].strip(),
                   request.form["nombre3"].strip()]
        if "" in nombres:
            error = "Debes ingresar los 3 nombres."
        elif len(set(n.lower() for n in nombres)) < 3:
            error = "Los 3 nombres deben ser diferentes."
        else:
            nombre, cantidad = nombre_mas_largo(nombres)

    return render_template("ejercicio2.html", valores=valores,
                           nombre=nombre, cantidad=cantidad, error=error)


if __name__ == "__main__":
    app.run(debug=True)