het paln is een ai die je code / github repo uitleest en aan de hand daarvan suggesties geeft hoe het beter had gekund





1. ollama en Django intergratie is goed mogelijk:

 	https://aidevhub.medium.com/ai-models-in-web-apps-using-django-with-ollama-63879e27baf5

 	https://markaicode.com/optimize-ollama-code-review-ai-qa/





2\. het idee is om een ollama server te draaien los van Django en daar dan request naar te sturn vanuit Django of vanuit een API



plan van aanpak:

1. een model uitkiezen dat lokaal te draaien is of op mijn server thuis

2\. Django intergratie maken zodat ik met de ai kan chatten en kan debuggen

3\. kijken of ik contact kan opnemen met david van de HAN (gelukt wacht nu op reactie)



gekozen ai agents:

1. codellama:7b-code    # Best for syntax and logic review
2. deepseek-coder:6.7b  # Excellent for bug detection
3. magicoder:7b         # Strong at security analysis

gebruik nu qwen2.5-coder:7b als annotatie ai

Minimum: 16GB RAM, 4-core CPU

Recommended: 32GB RAM, 8-core CPU, NVMe SSD

Optimal: 64GB RAM, 16-core CPU, dedicated GPU



Ik raad aan om te kijken naar Langgraph of Langchain, dan hoef je niet handmatige calls te maken.

Ze hebben gratis video cursussen op hun website, als je daar doorheen bent kan je alles ermee bouwen wat je wilt

Langgraph werkt het beste voor je usecase, dan maak je eigenlijk een flowchart waarin je je AI plaatst

docker compose is erg inefficient door de wsl virtualisatie laag

het best is om een systeem te maken dat op linux en widows kan draaien, zodat ik altijd native de ai kan draaien zonder bottlenecks


Student repo → Preprocessing node
             → Language detection & dependency graph
             → Syntax agent (linting) [per file + context]
             → Security agent (cross-file)
             → Testing agent (tests coverage, edge cases)
             → Project analysis agent (structure, naming, modularity)
             → Hoofd AI synthesizer (combineer alle agent reports)
             → Per-level pedagogical feedback
             → Final structured report