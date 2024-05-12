<H1> OTCA - Onde Tem Crime Ambiental (EXPECTATIVA)</H1>

<H2>Sobre o Projeto</H2>

OTCA (Onde Tem Crime Ambiental) é um chatbot projetado para facilitar o acesso à informação sobre legislação ambiental brasileira e permitir a denúncia de crimes ambientais. Este chatbot foi desenvolvido para ser executado em HTML responsivo, garantindo que seja acessível em qualquer dispositivo, seja um celular antigo ou um computador moderno.

<H2>Metodologia</H2>

<H3>O desenvolvimento deste projeto envolveu o uso de várias plataformas e tecnologias:</H3>

<B>Google Colab:</B> Utilizado para desenvolvimento inicial e testes de scripts.

<B>AI Studio e Gemini da Google:</B> Empregado para gerar código, tirar dúvidas, analisar logs e sistematizar os principais artigos da Lei de Crimes Ambientais nº 9.605, de 12 de fevereiro de 1998. Os dados foram então exportados para um arquivo JSON (lei_crimes_ambientais.json).

<B>CodePen:</B> Usado para prototipação rápida do frontend do chatbot.

![visual_codepen](https://github.com/vgbarone/otca-expectativa/assets/156860291/6e000dd3-24e0-4866-95e0-10c51290ed54)

<B>PythonAnywhere:</B> Tentativa de hospedagem da aplicação.

![pythonanywere_erro](https://github.com/vgbarone/otca-expectativa/assets/156860291/2501af26-e960-4d1d-b256-a4803c4fb7f2)

<H2>Tecnologias Utilizadas</H2>

<B>Flask:</B> Framework escolhido para o servidor backend do chatbot.

<B>google-generativeai:</B> API usada para enriquecer e detalhar as respostas do chatbot.

<B>gspread e oauth2client:</B> Ferramentas para integração com Google Sheets, usadas para coletar e gerenciar denúncias.

<B>google-auth e secrets:</B> Usados para a autenticação segura e gerenciamento de configurações sensíveis.

<H2>Estrutura do Código</H2>

O código em Python consulta o arquivo lei_crimes_ambientais.json e usa a API google-generativeai para aprimorar e adicionar informações detalhadas nas respostas. Recebe denúncias, armazena os dados no Google Sheets para alimentar Dashboard com mapa no Google Data Studio.

<H2>Objetivos</H2>

Além de esclarecer dúvidas sobre a Lei de Crimes Ambientais, o chatbot foi projetado para receber denúncias, capturar coordenadas geográficas e, inicialmente para testes, alimentar um Google Sheets. Esse Sheets, por sua vez, deveria alimentar um dashboard com um mapa no Google Data Studio.

<H2>Desafios e Realizações</H2>

Infelizmente, o projeto encontrou obstáculos técnicos, o que impediu a implementação completa conforme o planejado e o prazo. No entanto, o repositório otca-realidade mostra o que foi possível alcançar em 48 horas e serve como uma base para futuras melhorias.
