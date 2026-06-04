import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PRODUTOS = {
    "financas": {
        "name": "Método Finanças Pro",
        "promise": "sair do vermelho em 90 dias",
        "niche": "finanças pessoais",
    },
    "marketing": {
        "name": "Fórmula de Lançamento Digital",
        "promise": "fazer a primeira venda online em 30 dias",
        "niche": "marketing digital",
    },
    "saude": {
        "name": "Desafio 30 dias crescimento capilar",
        "promise": "fazer a primeira venda online em 30 dias",
        "niche": "campanha saude",
    }
}

ANGULOS = {
    "financas": [
        ("A virada de quem trabalha por conta própria",
         "Autônomos raramente se identificam com conteúdos de 'CLT'. Falar direto pra quem não tem salário fixo cria conexão imediata e diferencia dos concorrentes com linguagem genérica."),
        
        ("Como parar de ganhar bem e continuar sem dinheiro",
         "O paradoxo de ganhar acima da média mas não sobrar nada é a dor real de muita gente. Um título assim para o scroll e gera alta taxa de salvamento."),
    ],
    "marketing": [
        ("Como vender todo dia sem parecer desesperado",
         "A maior dor de quem vende online é sentir que está incomodando o seguidor. Resolver esse conflito emocional antes da técnica cria identificação imediata."),
        ("A estratégia de quem fatura com menos de 5k seguidores",
         "Quebra o mito de que só quem tem muitos seguidores vende. Perfeito para criadores em crescimento que sentem que ainda não chegou a hora de monetizar."),
    ],
    "saude": [
        ("O segredo para recuperar o volume e a autoestima em 4 semanas",
         "Foca na dor emocional da queda de cabelo e na perda de autoconfiança, conectando o desafio a uma transformação pessoal rápida e tangível."),
        
        ("A rotina simples de 5 minutos que ativa o crescimento capilar",
         "Ataca a objeção da falta de tempo ou preguiça. Funciona muito bem para pessoas ocupadas que querem resultados, mas não conseguem seguir protocolos complexos.")
    ]
}

ROTEIROS = {
    "instagram": [
        "{creator} — olha isso. Você sabia que a maioria dos {publico} comete esse erro toda semana sem perceber?\n\n[PAUSA — aproxima a câmera]\n\nEu também cometi. Até conhecer o {produto}.\n\nA promessa é simples: {promessa}. Parece exagerado, mas funcionou pra mim.\n\nLink na bio. R${preco} — corre porque não vai durar.\n\n#youshop #afiliado",
        "Pergunta rápida pro meu público de {publico}: você ainda não conseguiu {promessa}?\n\n[CORTE]\n\nFoi exatamente isso que me fez testar o {produto}. E funcionou.\n\nR${preco} — link na bio 👇\n\n#youshop #recomendo",
    ],
    "tiktok": [
        "POV: você é {publico} e ainda não resolveu {promessa} 😬\n\n[texto na tela: 'Até eu descobrir isso aqui']\n\nO {produto} mudou o jogo pra mim. R${preco} no link da bio.\n\n#youshop #fyp #dica",
        "Conta pra mim nos comentários: você já tentou {promessa} antes? ⬇️\n\nSe sim, você precisa conhecer o {produto} — {creator} recomenda.\n\nR${preco} · link na bio\n\n#youshop #tiktokbrasil",
    ],
    "youtube": [
        "Neste vídeo, vou te mostrar como finalmente {promessa}! Se você é {publico}, sabe o quanto isso pode ser frustrante, mas o {produto} facilita todo o processo.\n\n👉 Garanta o seu por apenas R${preco} no link abaixo:\n[INSERIR LINK]\n\n🔔 Não esqueça de se inscrever no canal e deixar seu like se esse conteúdo te ajudou!\n\n#youshop #review #dicas",
        "O segredo para {promessa} revelado! 😱\n\nTestei o {produto} e aqui está a verdade. Se você é {publico} e quer resultados reais, essa é a melhor opção atual por R${preco}.\n\n🛒 O link oficial está no primeiro comentário fixado!\n👤 Apresentado por: {creator}\n\n#youshop #youtubeshorts #viral"
    ]
}

LEGENDAS = [
    "Você já parou pra pensar por que algumas pessoas conseguem {promessa} e outras ficam travadas no mesmo lugar? 🤔\n\nSpoiler: não é sorte. É método.\n\nO {produto} existe exatamente pra isso — e por R${preco} é impossível não tentar.\n\n🔗 Link na bio\n\n#youshop #{nichotag} #produtodigital",
    "Eu precisava falar disso antes que alguém me pergunte de novo ⬇️\n\nSim, o {produto} realmente entrega: {promessa}.\n\nTestei. Funcionou. R${preco} — link na bio 👆\n\n#{nichotag} #recomendo #youshop",
    "Sabe aquele empurrãozinho que faltava pra você finalmente {promessa}? É isso. 🚀\n\nSem enrolação, direto ao ponto.\n\nDescubra como o {produto} pode acelerar seus resultados. Tudo isso por apenas R${preco}.\n\n🔗 Corre no link da bio pra acessar!\n\n#{nichotag} #youshop #transformacao"
]

EMAILS = [
    "Oi,\n\nAqui é {creator}. Normalmente não mando e-mail sobre produto nenhum — mas esse eu precisava te contar.\n\nO {produto} promete {promessa}. Parece direto ao ponto porque é. Testei, funcionou, e o preço de R${preco} torna impossível não indicar para os {publico} que me acompanham.\n\nAcessa aqui e vê você mesmo: [LINK YOUSHOP]\n\nAbração,\n{creator}",
    "Olá,\n\nPassei os últimos dias com o {produto} na mão — um material focado em {promessa} para {publico}.\n\nFuncionou como prometido. E por R${preco}, o custo-benefício é difícil de bater.\n\nSe você está levando isso a sério, vale muito a pena: [LINK YOUSHOP]\n\nAté mais,\n{creator}",
    "Tudo bem?\n\nEu sei o quanto pode ser frustrante tentar {promessa} e sentir que não está saindo do lugar.\n\nFoi exatamente por isso que o {produto} me chamou tanta atenção. Ele vai direto ao problema, sem enrolação, feito sob medida para {publico} que precisam de resultados práticos e rápidos.\n\nE o melhor de tudo: o investimento é de apenas R${preco}.\n\nSe você quer resolver isso de uma vez por todas, clica no link abaixo para conferir:\n[LINK YOUSHOP]\n\nAbraços,\n{creator}"
]


def gerar_kit_venda(product_key, creator_name, creator_audience, product_price, creator_network, creator_tone):


    produto = PRODUTOS[product_key]
    angulo, justificativa = random.choice(ANGULOS[product_key])
    nichotag = produto["niche"].replace(" ", "").replace("ç", "c").replace("ã", "a")


    if creator_network == "tiktok":
        rede_key = "tiktok"
    elif creator_network == "youtube":
        rede_key = "youtube"
    else:
        rede_key = "instagram"

    roteiro = random.choice(ROTEIROS[rede_key]).format(
        creator=creator_name,
        publico=creator_audience,
        produto=produto["name"],
        promessa=produto["promise"],
        preco=product_price,
    )

    legenda = random.choice(LEGENDAS).format(
        produto=produto["name"],
        promessa=produto["promise"],
        preco=product_price,
        nichotag=nichotag,
    )

    email = random.choice(EMAILS).format(
        creator=creator_name,
        produto=produto["name"],
        promessa=produto["promise"],
        preco=product_price,
        publico=creator_audience,
    )

    return {
        "angulo_unico": angulo,
        "justificativa": justificativa,
        "roteiro_video": roteiro,
        "legenda": legenda,
        "email": email,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    try:
        resultado = gerar_kit_venda(
            product_key=data["product_key"],
            creator_name=data["creator_name"],
            creator_audience=data["creator_audience"],
            product_price=data["product_price"],
            creator_network=data["creator_network"],
            creator_tone=data["creator_tone"],
        )
        return jsonify({"success": True, "data": resultado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
