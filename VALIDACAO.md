# Estado da validação

Data: 21 de outubro de 2026.

## Atualização após os testes locais do utilizador

O utilizador instalou as dependências e executou a aplicação. As capturas partilhadas mostram geração real de três continuações em português e progressão para outra ronda. A apresentação foi corrigida em seguida, incluindo a área ilustrada do fundo, cartões com texto limitado e botões dentro dos cartões; o utilizador confirmou o resultado visual.

Isto demonstra execução manual local, mas não constitui uma avaliação da qualidade narrativa nem substitui os testes automatizados HTTP/Streamlit. As limitações de execução do ambiente do assistente descritas abaixo mantêm-se. Os 20 testes de lógica foram novamente executados e passaram após as alterações visuais.

## Executado nesta entrega

- Verificação de sintaxe dos 12 ficheiros Python ativos, incluindo testes e instalação.
- Suite `python -m unittest discover -s tests -v`: **26 testes encontrados; 20 passaram; 6 ignorados**.
- Os testes aprovados verificam validação, persistência de escolhas entre atualizações, progressão da história, exportação completa, limites de contexto, configuração predefinida, não carregamento de modelos ao importar, percurso inglês sem tradutores, percurso português com tradução por lote, extração de tokens novos e propagação explícita de falhas.
- O teste do motor utiliza objetos simulados; não foi executada inferência neural.
- Os dois fundos ilustrados e o código de treino/interface originais foram incluídos no pacote como ativos e referência histórica, respetivamente.

## Não executado

- 4 testes HTTP/FastAPI e 2 testes Streamlit: dependências não disponíveis.
- Instalação integral das dependências e compatibilidade das versões resolvidas.
- Downloads de GPT-2 e dos tradutores.
- Inferência real em inglês ou português, qualidade dos contos e consumo de memória/tempo.
- Inspeção visual da interface em execução.
- Construção do contentor Docker.

Foi tentada a instalação das dependências de teste. A consulta não encontrou distribuições no ambiente disponível, e a tentativa de execução com permissões adicionais foi rejeitada automaticamente pela política do ambiente. Não é possível atribuir sucesso aos testes acima sem os executar.

## Próxima validação local

1. Executar `install_windows.bat`.
2. Executar `start_windows.bat` e testar English primeiro.
3. Verificar três alternativas reais, selecionar uma e confirmar que aparece no conto.
4. Guardar o conto e começar um novo.
5. Testar o modo Português.
6. Instalar `requirements-test.txt` e executar todos os testes. Espera-se que nenhum fique ignorado depois de instaladas as dependências.
7. Registar as versões efetivamente instaladas e corrigir qualquer incompatibilidade revelada pelo teste real.

O pacote é uma recuperação de código com validação parcial, não uma declaração de aplicação totalmente testada ou pronta para produção.
