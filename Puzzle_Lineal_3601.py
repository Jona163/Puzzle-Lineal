from flask import Flask, render_template, request
from Arbol import Nodo

app = Flask(__name__)

def buscar_solucion_BFS(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)
    
    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            nodos_visitados.append(nodo.get_datos())
            dato_nodo = nodo.get_datos()

            # Operador Izquierdo 
            hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izquierdo = Nodo(hijo)
            if hijo_izquierdo.get_datos() not in nodos_visitados and hijo_izquierdo.get_datos() not in [nodo.get_datos() for nodo in nodos_frontera]:
                nodo.set_hijos([hijo_izquierdo])
                nodos_frontera.append(hijo_izquierdo)

            # Operador Central
            hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_central = Nodo(hijo)
            if hijo_central.get_datos() not in nodos_visitados and hijo_central.get_datos() not in [nodo.get_datos() for nodo in nodos_frontera]:
                nodo.set_hijos([hijo_central])
                nodos_frontera.append(hijo_central)

            # Operador Derecho
            hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_derecho = Nodo(hijo)
            if hijo_derecho.get_datos() not in nodos_visitados and hijo_derecho.get_datos() not in [nodo.get_datos() for nodo in nodos_frontera]:
                nodo.set_hijos([hijo_derecho])
                nodos_frontera.append(hijo_derecho)

    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener datos del formulario
        estado_inicial = [int(x) for x in request.form['estado_inicial'].split(',')]
        solucion = [int(x) for x in request.form['solucion'].split(',')]

        # Realizar la búsqueda BFS
        nodo_solucion = buscar_solucion_BFS(estado_inicial, solucion)

        # Reconstruir el camino hacia la solución
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.insert(0, nodo.get_datos())
            nodo = nodo.get_padre()

        return render_template('resultado.html', resultado=resultado)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
