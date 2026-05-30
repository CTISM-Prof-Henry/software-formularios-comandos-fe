from django.db import migrations, models
import django.db.models.deletion


DESAFIOS = [
    ("D1", "Internacionalizacao"),
    ("D2", "Educacao inovadora e transformadora com excelencia academica"),
    ("D3", "Inclusao Social"),
    ("D4", "Inovacao, geracao de conhecimento e transferencia de tecnologia"),
    ("D5", "Modernizacao e desenvolvimento organizacional"),
    ("D6", "Desenvolvimento local, regional e nacional"),
    ("D7", "Gestao ambiental"),
]

OBJETIVOS = [
    ("PR-D1-02", "D1", "Oportunizar experiencias de internacionalizacao aos alunos."),
    ("PR-D1-03", "D1", "Firmar relacoes de colaboracao internacional para trocas culturais e politicas academicas e de gestao."),
    ("PR-D2-03", "D2", "Possuir curriculos interdisciplinares, flexiveis e atualizados em relacao as demandas da sociedade."),
    ("AI-D2-01", "D2", "Manter um quadro docente capacitado quanto ao uso de praticas pedagogicas."),
    ("AI-D2-02", "D2", "Desenvolver uma cultura de comprometimento organizacional."),
    ("AI-D2-03", "D2", "Oferecer uma infraestrutura de apoio qualificada e de acordo com as necessidades de cada area de conhecimento."),
    ("AI-D2-04", "D2", "Fortalecer a cultura de inovacao, compromisso social e integracao ensino-pesquisa-extensao e entre as areas do conhecimento."),
    ("AS-D2-01", "D2", "Oferecer cursos de excelencia integrados a sociedade."),
    ("AS-D2-02", "D2", "Formar alunos com visao global e humanista, comprometidos com sociedade, meio ambiente e desenvolvimento cientifico e tecnologico."),
    ("AS-D2-03", "D2", "Estimular o sentimento de pertencimento e satisfacao dos alunos para com a UFSM."),
    ("PR-D2-01", "D2", "Fortalecer o aprendizado extra-classe, oportunizando atividades de extensao, insercao social, empreendedorismo, pesquisa e inovacao."),
    ("PR-D2-02", "D2", "Manter metodos de ensino atualizados e de acordo com as expectativas dos alunos."),
    ("PR-D2-04", "D2", "Desenvolver estrategias de permanencia que incentivem o aprendizado e a conclusao do curso em prazo adequado."),
    ("AI-D3-01", "D3", "Preparar o corpo tecnico e docente para lidar com os diferentes aspectos da inclusao social."),
    ("AI-D3-02", "D3", "Disseminar uma cultura etica em relacao a inclusao, diversidade e meio ambiente."),
    ("AS-D3-01", "D3", "Fortalecer as politicas de acesso a universidade em consonancia com acoes afirmativas."),
    ("PR-D3-01", "D3", "Fortalecer as politicas de assistencia estudantil focadas na permanencia, conclusao e bom uso dos recursos."),
    ("AI-D4-01", "D4", "Estimular o desenvolvimento de um quadro docente com pesquisadores de excelencia que sejam referencia."),
    ("AS-D4-01", "D4", "Aumentar a insercao cientifica institucional."),
    ("AI-D4-02", "D4", "Equipar laboratorios de pesquisa conforme necessidades de cada area e uso multiusuario."),
    ("AS-D4-03", "D4", "Desenvolver e inserir na sociedade tecnologias sociais e arte e cultura."),
    ("AI-D4-03", "D4", "Expandir os ambientes de inovacao."),
    ("AS-D4-02", "D4", "Fortalecer a inovacao, o desenvolvimento tecnologico e a transferencia de tecnologias para a sociedade."),
    ("PR-D4-02", "D4", "Implementar projetos interdisciplinares."),
    ("PR-D5-01", "D5", "Otimizar rotinas administrativas e sistemas de informacao, com agilidade, transparencia e qualidade."),
    ("PR-D5-04", "D5", "Desenvolver processos e rotinas de trabalho considerando realidade multicampi e niveis de ensino."),
    ("AI-D5-03", "D5", "Modernizar infraestrutura de TI para suportar necessidades academicas e administrativas."),
    ("AI-D5-04", "D5", "Desenvolver sistema de selecao e progressao docente equilibrando ensino, pesquisa, extensao e particularidades de areas e niveis."),
    ("AI-D5-01", "D5", "Possuir infraestrutura de engenharia e logistica adequada, com acessibilidade e respeito ambiental."),
    ("PR-D5-03", "D5", "Aumentar eficiencia da comunicacao institucional."),
    ("SF-D5-02", "D5", "Incrementar captacao de recursos extra-orcamentarios."),
    ("AI-D5-02", "D5", "Desenvolver competencias gerenciais, tecnicas e de lideranca para manter excelencia."),
    ("AS-D5-01", "D5", "Fortalecer politicas de governanca, transparencia e profissionalizacao da gestao."),
    ("PR-D5-02", "D5", "Adequar a estrutura administrativa com estrategia de alocacao e dimensionamento de pessoal."),
    ("SF-D5-01", "D5", "Aumentar orcamento federal recebido."),
    ("SF-D5-03", "D5", "Desenvolver gestao orcamentaria transparente, eficiente e alinhada a estrategia institucional."),
    ("PR-D6-02", "D6", "Instituir processo de relacionamento e colaboracao com os diversos setores da sociedade."),
    ("AS-D6-03", "D6", "Desenvolver projetos de extensao com foco na intervencao, transformacao e desenvolvimento social."),
    ("PR-D6-01", "D6", "Fomentar projetos de pesquisa aplicados a problemas sociais e universitarios."),
    ("AS-D6-02", "D6", "Oferecer servicos de apoio a comunidade em consonancia com politica de inovacao e extensao universitaria."),
    ("AS-D6-01", "D6", "Desenvolver projetos relacionados a politicas publicas nas areas saude, educacao, inclusao, gestao ambiental etc."),
    ("AS-D7-01", "D7", "Implantar um sistema de gestao ambiental."),
    ("PR-D7-01", "D7", "Manter processos e rotinas que valorizem os aspectos da gestao ambiental."),
]

MACROPROCESSOS = [
    "Assistencia Estudantil",
    "Compras, Suprimentos e Patrimonio",
    "Comunicacao Institucional",
    "Controle Ambiental",
    "Controle Bibliografico e Editorial",
    "Documentos",
    "Ensino",
    "Extensao",
    "Inclusao Social",
    "Infraestrutura de Pesquisa e Inovacao",
    "Infraestrutura dos Campi",
    "Inovacao e Empreendedorismo",
    "Orcamento e Financas",
    "Pesquisa",
    "Pesquisa Institucional",
    "Pessoas",
    "Planejamento Academico",
    "Planejamento Pedagogico",
    "Projetos Academicos",
    "Registro e Controle Academico",
    "Relacoes Institucionais",
    "Tecnologia da Informacao",
]


def carregar_dados(apps, schema_editor):
    Desafio = apps.get_model("riscos", "Desafio")
    Objetivo = apps.get_model("riscos", "Objetivo")
    Macroprocesso = apps.get_model("riscos", "Macroprocesso")
    Risco = apps.get_model("riscos", "Risco")

    desafios = {}
    for codigo, nome in DESAFIOS:
        desafio, _ = Desafio.objects.update_or_create(
            codigo=codigo,
            defaults={"nome": nome},
        )
        desafios[codigo] = desafio

    objetivos = {}
    for codigo, desafio_codigo, descricao in OBJETIVOS:
        objetivo, _ = Objetivo.objects.update_or_create(
            codigo=codigo,
            defaults={"desafio": desafios[desafio_codigo], "descricao": descricao},
        )
        objetivos[codigo] = objetivo

    macroprocessos = []
    for nome in MACROPROCESSOS:
        macroprocesso, _ = Macroprocesso.objects.get_or_create(nome=nome)
        macroprocessos.append(macroprocesso)

    desafio_padrao = desafios["D5"]
    objetivo_padrao = objetivos["PR-D5-01"]
    macroprocesso_padrao = macroprocessos[0]
    Risco.objects.filter(desafio__isnull=True).update(desafio=desafio_padrao)
    Risco.objects.filter(objetivo__isnull=True).update(objetivo=objetivo_padrao)
    Risco.objects.filter(macroprocesso__isnull=True).update(
        macroprocesso=macroprocesso_padrao
    )


class Migration(migrations.Migration):
    dependencies = [
        ("riscos", "0002_risco_unidade"),
    ]

    operations = [
        migrations.CreateModel(
            name="Desafio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=10, unique=True)),
                ("nome", models.CharField(max_length=180)),
            ],
            options={
                "verbose_name": "Desafio",
                "verbose_name_plural": "Desafios",
                "ordering": ["codigo"],
            },
        ),
        migrations.CreateModel(
            name="Macroprocesso",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, unique=True)),
            ],
            options={
                "verbose_name": "Macroprocesso",
                "verbose_name_plural": "Macroprocessos",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Objetivo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=20, unique=True)),
                ("descricao", models.TextField()),
                ("desafio", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="objetivos", to="riscos.desafio")),
            ],
            options={
                "verbose_name": "Objetivo",
                "verbose_name_plural": "Objetivos",
                "ordering": ["codigo"],
            },
        ),
        migrations.AddField(
            model_name="risco",
            name="desafio",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.desafio"),
        ),
        migrations.AddField(
            model_name="risco",
            name="macroprocesso",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.macroprocesso"),
        ),
        migrations.AddField(
            model_name="risco",
            name="objetivo",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.objetivo"),
        ),
        migrations.RunPython(carregar_dados, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="risco",
            name="desafio",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.desafio"),
        ),
        migrations.AlterField(
            model_name="risco",
            name="macroprocesso",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.macroprocesso"),
        ),
        migrations.AlterField(
            model_name="risco",
            name="objetivo",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="riscos", to="riscos.objetivo"),
        ),
    ]
