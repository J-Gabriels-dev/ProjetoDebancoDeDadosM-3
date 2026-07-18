# Template LaTeX — Relatório Técnico de Software (RTS)

## Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — IFPI

---

## Objetivo

Este projeto LaTeX fornece um template institucional completo para a elaboração do **Relatório Técnico de Software (RTS)**, exigido como Trabalho de Conclusão de Curso (TCC) no Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas do Instituto Federal de Educação, Ciência e Tecnologia do Piauí (IFPI).

O template está em conformidade com:
- **ABNT NBR 14724:2024** — Apresentação de trabalhos acadêmicos;
- **ABNT NBR 10520:2023** — Citações em documentos;
- **ABNT NBR 6023:2018** — Referências bibliográficas;
- **Resolução Normativa nº 180/2023** — Regulamento do TCC do IFPI;
- **Diretrizes do PPC** — Estrutura específica do RTS;
- **Manual de Trabalhos Acadêmicos do IFPI (2024)**.

---

## Estrutura do Projeto

```
main.tex              → Arquivo principal (importa todos os demais)
configuracoes.tex     → Pacotes, configurações de estilo e aparência
preambulo.tex         → Dados do trabalho (título, autor, orientador, etc.)
referencias.bib       → Arquivo de referências bibliográficas (BibTeX)
README.md             → Este arquivo
LICENSE               → Licença do projeto

capitulos/
    agradecimentos.tex   → Página de agradecimentos
    epigrafe.tex         → Epígrafe (opcional)
    resumo.tex           → Resumo em português
    abstract.tex         → Abstract (resumo em inglês)
    siglas.tex           → Lista de siglas e abreviaturas
    introducao.tex       → Seção 1 - Introdução
    tecnologias.tex      → Seção 2 - Tecnologias Envolvidas
    modelagem.tex        → Seção 3 - Modelagem do Projeto
    software.tex         → Seção 4 - Software
    consideracoes.tex    → Seção 5 - Considerações Finais

figuras/                 → Pasta para armazenar todas as imagens
```

---

## Como Abrir no Overleaf

1. Faça o download do arquivo `.zip` deste projeto.
2. Acesse [https://www.overleaf.com](https://www.overleaf.com) e faça login.
3. Clique em **Novo Projeto** → **Carregar Projeto**.
4. Selecione o arquivo `.zip`.
5. O Overleaf abrirá automaticamente o projeto pronto para edição.

---

## Como Compilar

### No Overleaf
- O Overleaf detecta automaticamente o compilador. Certifique-se de que o compilador está configurado como **pdfLaTeX** e o processador de bibliografia como **Biber**.
- Para verificar: Menu → Configurações → Compilador: **pdfLaTeX** | Bibliografia: **Biber**.

### Localmente
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

---

## Como Adicionar Capítulos

1. Crie um novo arquivo `.tex` na pasta `capitulos/` (ex: `capitulos/novo_capitulo.tex`).
2. Inicie o arquivo com `\chapter{Nome do Capítulo}`.
3. No arquivo `main.tex`, adicione `\input{capitulos/novo_capitulo}` na posição desejada.

---

## Como Inserir Figuras

1. Coloque a imagem na pasta `figuras/` (formatos aceitos: `.png`, `.jpg`, `.pdf`).
2. No texto, utilize:

```latex
\begin{figure}[htb]
\centering
\caption{Descrição da figura}
\label{fig:nome_referencia}
\includegraphics[width=0.8\textwidth]{figuras/nome_arquivo.png}
\source{Elaborada pelo autor (2024).}
\end{figure}
```

---

## Como Adicionar Referências

1. Abra o arquivo `referencias.bib`.
2. Adicione a entrada no formato BibTeX. Exemplo:

```bibtex
@book{sobrenome_ano,
  title     = {Título do Livro},
  author    = {Nome Sobrenome},
  year      = {2023},
  publisher = {Editora},
  address   = {Cidade}
}
```

3. No texto, cite com `\cite{sobrenome_ano}` ou `\textcite{sobrenome_ano}`.

---

## Como Criar Novas Seções

```latex
\section{Nome da Seção}       % Nível 2 (ex: 1.1)
\subsection{Nome}             % Nível 3 (ex: 1.1.1)
\subsubsection{Nome}          % Nível 4 (ex: 1.1.1.1)
```

---

## Solução para Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `Undefined control sequence` | Pacote não carregado ou comando digitado errado | Verifique a ortografia do comando e se o pacote está em `configuracoes.tex` |
| `File not found` | Imagem ou arquivo `.tex` com nome errado | Verifique o nome exato do arquivo (maiúsculas/minúsculas importam) |
| `Citation undefined` | Referência não encontrada no `.bib` | Verifique se a chave no `\cite{}` corresponde exatamente à entrada no `referencias.bib` |
| `Missing $ inserted` | Caractere especial (`_`, `%`, `&`) sem escape | Use `\_`, `\%`, `\&` no texto |
| Bibliografia não aparece | Biber não foi executado | No Overleaf, vá em Menu → Bibliografia → Biber. Localmente, execute `biber main` |

---

## Licença

Este template é distribuído sob a licença **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Consulte o arquivo `LICENSE` para mais detalhes.

---

## Créditos

Template elaborado para o Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas do IFPI — Campus Angical.
