let probabilityChart = null;

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const comment = document.getElementById('comment-input').value;
    const model = document.getElementById('model-select').value;
    const errorMsg = document.getElementById('error-message');
    const resultsPanel = document.getElementById('results-panel');
    const btn = document.getElementById('analyze-btn');

    if (!comment.trim()) {
        errorMsg.textContent = "Por favor, escribe un comentario primero.";
        return;
    }

    // Reset UI
    errorMsg.textContent = "";
    btn.textContent = "Analizando...";
    btn.disabled = true;

    try {
        const response = await fetch('/analizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                comentario: comment,
                modelo: model
            })
        });

        const data = await response.json();

        if (data.error) {
            errorMsg.textContent = data.error;
            btn.textContent = "Analizar";
            btn.disabled = false;
            return;
        }

        // Show Results
        resultsPanel.classList.remove('hidden');
        renderResults(data);

    } catch (err) {
        errorMsg.textContent = "Hubo un error de conexión con el servidor.";
    }

    btn.textContent = "Analizar";
    btn.disabled = false;
});

function renderResults(data) {
    const verdictBanner = document.getElementById('verdict-banner');
    const sarcasmTitle = document.getElementById('sarcasm-title');

    // Configurar Banner
    verdictBanner.className = 'verdict-banner'; // reset
    if (data.sarcasmo) {
        verdictBanner.classList.add('verdict-sarcasm');
        sarcasmTitle.textContent = "ES SARCASMO";
    } else {
        verdictBanner.classList.add('verdict-literal');
        sarcasmTitle.textContent = "LENGUAJE LITERAL";
    }

    // Estadísticas
    document.getElementById('stat-model').textContent = data.modelo_usado;
    document.getElementById('stat-tokens').textContent = data.texto_procesado || "[Sin tokens útiles]";

    // Renderizar Gráfica
    renderChart(data.prob_sarcasmo, data.prob_no_sarcasmo);
}

function renderChart(probSarcasm, probNoSarcasm) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');

    if (probabilityChart) {
        probabilityChart.destroy();
    }

    // Si los modelos no devuelven probabilidad real (ej, SVM default), dar 100 y 0
    let s_val = probSarcasm * 100;
    let ns_val = probNoSarcasm * 100;

    probabilityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Prob. Sarcasmo', 'Prob. Literal'],
            datasets: [{
                data: [s_val, ns_val],
                backgroundColor: [
                    '#f43f5e', // Rose for Sarcasm
                    '#10b981'  // Emerald for Literal
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#f8fafc', font: { family: 'Outfit' } }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return ` ${context.label}: ${context.raw.toFixed(1)}%`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}
