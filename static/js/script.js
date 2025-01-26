document.getElementById('download-btn').addEventListener('click', function() {
    // Pegando as informações do clima diretamente da página HTML
    const cidade = document.querySelector('h1').textContent.replace('Clima em ', '');
    const temperatura = document.querySelector('p:nth-child(2)').textContent.replace('Temperatura: ', '');
    const sensacaoTermica = document.querySelector('p:nth-child(3)').textContent.replace('Sensação Térmica: ', '');
    const umidade = document.querySelector('p:nth-child(4)').textContent.replace('Umidade: ', '');
    const condicao = document.querySelector('p:nth-child(5)').textContent.replace('Condição: ', '');

    const climaInfo = `
        Cidade: ${cidade}
        Temperatura: ${temperatura}
        Sensação Térmica: ${sensacaoTermica}
        Umidade: ${umidade}
        Condição: ${condicao}
    `;

    // Criar o arquivo de texto
    const blob = new Blob([climaInfo], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'informacoes_clima.txt';  // Mudança para .txt
    a.click();
    URL.revokeObjectURL(url);
});
