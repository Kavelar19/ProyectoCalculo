from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__, static_url_path='/static')

# Rutas para tus páginas
@app.route('/')
def home():
 return render_template('index.html')

@app.route('/pages/tecnicas')
def tecnicas():
    return render_template('pages/tecnicas.html')

@app.route("/definida")
def definida():
    return render_template("pages/definida.html")

@app.route("/indefinida")
def indefinida():
    return render_template("pages/indefinida.html")

@app.route("/partes")
def partes():
    return render_template("pages/partes.html")

@app.route("/sustitucion")
def sustitucion():
    return render_template("pages/sustitucion.html")
@app.route("/Volumen")
def volumen():
    return render_template("pages/volumen.html")
@app.route("/impropias")
def impropias():
    return render_template("pages/impropias.html")
    


# --------------------------
# API para calcular integrales
# --------------------------

@app.route("/api/integral_definida", methods=["POST"])
def integral_definida():
    data = request.json
    expr_str = data.get("funcion", "")
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))

    x = sp.symbols('x')
    try:
        expr = sp.sympify(expr_str)
        # Calcular la antiderivada
        F = sp.integrate(expr, x)
        # Evaluar en límites
        Fb = F.subs(x, b)
        Fa = F.subs(x, a)
        integral = Fb - Fa
        from sympy import latex, Eq, simplify
        # Crear expresiones LaTeX para cada paso
        antiderivada_latex = latex(Eq(sp.Function('F')(x), F + sp.Symbol('C')))
        Fb_simpl = simplify(Fb)
        Fa_simpl = simplify(Fa)
        eval_b_latex = latex(Eq(sp.Function('F')(b), Fb_simpl))
        eval_a_latex = latex(Eq(sp.Function('F')(a), Fa_simpl))
        resta_latex = latex(Eq(sp.Symbol('I'), Fb_simpl - Fa_simpl))
        decimal_latex = f"\\approx {float(integral):.8f}"

        # Redondear el resultado decimal para mejor presentación
        decimal_rounded = f"\\approx {round(float(integral), 4)}"

        # Convertir el resultado a float redondeado para mostrar en texto plano
        resultado_redondeado = round(float(integral), 4)

        pasos = (
            f"\\{{1️⃣ Identificar los límites y la función}}\\\\\n"
            f"Primero, identificamos los límites de integración y la función a integrar. Aquí, el límite inferior es \\(a={a}\\), el límite superior es \\(b={b}\\), y la función es \\(f(x) = {latex(expr)}\\).\\\\[10pt]\n"
            f"\\{{2️⃣ Calcular la antiderivada}} \\(F(x)\\)\\\\\n"
            f"Calculamos la antiderivada \\(F(x)\\), que es la función cuya derivada es \\(f(x)\\). En este caso:\\\\\n"
            f"\\[\n"
            f"F(x) = \\int {latex(expr)}\\,dx = {latex(F)} + C\n"
            f"\\]\n\n"
            f"\\{{3️⃣ Evaluar}} \\(F(b) - F(a)\\)\\\\\n"
            f"Evaluamos la antiderivada en los límites superior e inferior y restamos los resultados, según el teorema fundamental del cálculo:\\\\\n"
            f"\\[\n"
            f"\\int_{{{b}}}^{{{a}}} {latex(expr)}\\,dx = F({b}) - F({a}) = {eval_b_latex.rsplit('=',1)[1].strip()} - {eval_a_latex.rsplit('=',1)[1].strip()}\n"
            f"\\]\n\n"
            f"\\{{4️⃣ Simplificar el resultado}}\\\\\n"
            f"Realizamos la resta y simplificamos para obtener el valor numérico final:\\\\\n"
            f"\\[\n"
            f"{resta_latex.rsplit('=',1)[1].strip()} = {decimal_rounded}\n"
            f"\\]\n\n"
            f"\\{{5️⃣ (Opcional) Interpretar como área}}\\\\\n"
            f"Este resultado representa el área bajo la curva \\(f(x)\\) entre \\(x=a\\) y \\(x=b\\).\n"
        )
        return jsonify({
            "resultado": str(integral),
            "pasos": pasos
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/integral_indefinida", methods=["POST"])
def integral_indefinida():
    data = request.json
    expr_str = data.get("funcion", "")

    x = sp.symbols('x')
    try:
        expr = sp.sympify(expr_str)
        integral = sp.integrate(expr, x)
        pasos = f"∫ {expr_str} dx = {integral} + C"
        return jsonify({
            "resultado": str(integral),
            "pasos": pasos
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)