// Buscador de temas
const searchInput = document.getElementById("search");
if (searchInput) {
  searchInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      const query = this.value.toLowerCase();
      if (query.includes("impropia")) {
        window.location.href = "pages/impropias.html";
      } else if (query.includes("tecnicas")) {
        window.location.href = "pages/tecnicas.html";
      }else if (query.includes("home")) {
        window.location.href = "index.html";
      }else if (query.includes("partes")) {
        window.location.href = "pages/partes.html";
      } else if (query.includes("sustituc")) {
        window.location.href = "pages/sustitucion.html";  // ojo: revisa que coincida el nombre real
      } else if (query.includes("fracciones")) {
        window.location.href = "pages/parciales.html";    // ojo: revisa que coincida el nombre real
      } else if (query.includes("área") || query.includes("area")) {
        window.location.href = "pages/area.html";
      } else if (query.includes("volumen")) {
        window.location.href = "pages/volumen.html";
      } else {
        window.location.href = "#temas"; // por defecto lo manda al índice
      }
    }
  });
}

// Calculadora simple de ejemplo (derivadas / integrales estáticas)
async function calcular() {
  let expr = document.getElementById("expression").value;
  let op = document.getElementById("operation").value;
  let resultado = document.getElementById("resultado");
  let pasos = document.getElementById("pasos");

  if (op === "derivada") {
    resultado.innerHTML = `Derivada de ${expr}: 2x + 3 (ejemplo estático)`;
    pasos.innerHTML = "Paso 1: Diferenciar x² → 2x<br>Paso 2: Diferenciar 3x → 3<br>Paso 3: Sumar → 2x + 3";
  } else {
    resultado.innerHTML = `Integral de ${expr}: (x³/3) + (3x²/2) + C (ejemplo estático)`;
    pasos.innerHTML = "Paso 1: Integrar x² → x³/3<br>Paso 2: Integrar 3x → (3x²/2)<br>Paso 3: Sumar + C";
  }
}

// Calculadora de integrales definidas (con Flask)
document.addEventListener("DOMContentLoaded", function () {
  const btnDef = document.getElementById("btnCalcularDef");

  if (btnDef) {
    btnDef.addEventListener("click", async () => {
      const funcion = document.getElementById("funcionDef").value;
      const a = document.getElementById("limiteA").value;
      const b = document.getElementById("limiteB").value;

      // Hacer la petición al servidor Flask
      const response = await fetch("/api/integral_definida", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ funcion: funcion, a: a, b: b })
      });

      const data = await response.json();

      // Mostrar resultados en la página
      if (data.resultado) {
        document.getElementById("respuestaDef").innerText = data.resultado;

        // Mostrar pasos con formato matemático usando MathJax
        const pasosDef = document.getElementById("math-content");
        pasosDef.innerHTML = data.pasos;

        // Renderizar con MathJax para que se vea bien la notación matemática
        if (window.MathJax) {
          MathJax.typesetPromise([pasosDef]).catch(function (err) {
            console.error('MathJax typeset failed: ' + err.message);
          });
        }
      } else {
        document.getElementById("respuestaDef").innerText = "Error: " + data.error;
        document.getElementById("pasosDef").innerText = "";
      }
    });
  }
});

// Calculadora de integrales indefinidas (agregado para indefinida.html)
async function calcularIntegralIndef() {
  const funcion = document.getElementById("funcionIndef").value;

  try {
    const response = await fetch("/api/integral_indefinida", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ funcion: funcion })
    });

    const data = await response.json();

    if (data.resultado) {
      document.getElementById("respuestaIndef").innerText = data.resultado;
      document.getElementById("pasosIndef").innerText = data.pasos;
    } else {
      document.getElementById("respuestaIndef").innerText = "Error: " + data.error;
      document.getElementById("pasosIndef").innerText = "";
    }
  } catch (error) {
    document.getElementById("respuestaIndef").innerText = "Error en la petición: " + error;
    document.getElementById("pasosIndef").innerText = "";
  }
}
