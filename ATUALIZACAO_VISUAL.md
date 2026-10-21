# Atualização visual — 21 de outubro de 2026

## Segunda correção

A imagem original tem 1366×800 píxeis, mas a ilustração termina na linha 650; o restante é uma faixa branca incorporada no PNG. O fundo passa a escalar a área ilustrada de 1366×651 para cobrir o ecrã, mantendo a margem branca abaixo da área visível. O ficheiro de imagem original não foi alterado.

O cartão da história ficou mais compacto, as ações principais ficam numa só linha e os botões de escolha passam a ficar dentro dos cartões. Só o texto de cada opção tem deslocamento interno; o botão permanece visível.

- Área exterior aos cartões transparente, sem o painel branco central.
- Fundo original sem camada branca por cima, fixo ao ecrã e cobrindo a área visível.
- História num cartão com altura limitada e deslocamento interno.
- Três opções em cartões com a mesma altura, com deslocamento interno quando o texto é longo.
- Texto das continuações apresentado literalmente: listas, sublinhados e outros caracteres produzidos pelo modelo não são interpretados como Markdown.
- Botões com rótulos fixos: Escolher opção 1, 2 e 3.
- Tema claro explícito para assegurar contraste com os cartões.

## Aplicar

Guarda o conto antes de reiniciar. Fecha o processo da aplicação com Ctrl+C na janela em que foi iniciado e volta a executar `start_windows.bat`. Não é preciso reinstalar Python ou voltar a descarregar os modelos para aplicar esta alteração.

Se usares uma pasta diferente, copia `project/ui.py` e `.streamlit/config.toml` do ZIP de atualização para os mesmos locais na pasta instalada, substituindo esses ficheiros. A pasta `.venv` e a cache dos modelos não precisam de ser alteradas.

## Limitações e validação

O GPT-2 pré-treinado pode gerar texto em estilo de blogue, referências soltas e continuações incoerentes. Esta atualização corrige apresentação e contenção; não altera nem volta a treinar o modelo.

Os 20 testes de lógica passaram. Foi verificado estruturalmente que as continuações usam texto simples e que os cartões têm alturas limitadas. Foi acrescentado um teste Streamlit com texto longo, Markdown e marcação HTML na segunda ronda.

O teste Streamlit não pôde terminar neste ambiente: a criação do par de sockets interno do Python ficou bloqueada pelas restrições de execução. Também não foi possível iniciar um servidor de pré-visualização separado. Não se declara validação visual do novo layout em execução. A aplicação existente respondeu e gerou três opções reais durante uma verificação separada, ainda com o módulo antigo carregado.
