import pgmpy.models as models
import pgmpy.factors.discrete as discrete
import pgmpy.inference as inference

# Definir a estrutura da Rede Bayesiana

model = models.DiscreteBayesianNetwork([('Gripe', 'Febre'), ('Gripe', 'Tosse')])

# Definir as Tabelas de Probabilidade Condicional (CPTs)
# P(Gripe)
cpd_gripe = discrete.TabularCPD(
    variable='Gripe',
    variable_card=2,  # 2 estados: True (1) / False (0)
    values=[[0.05], # P(Gripe=True) = 0.05
            [0.95]] # P(Gripe=False) = 0.95
)

# P(Febre | Gripe)
cpd_febre = discrete.TabularCPD(
    variable='Febre',
    variable_card=2,
    values=[[0.8, 0.1],  # P(Febre=True | Gripe=True), P(Febre=True | Gripe=False)
            [0.2, 0.9]], # P(Febre=False | Gripe=True), P(Febre=False | Gripe=False)
    evidence=['Gripe'],
    evidence_card=[2]
)

# P(Tosse | Gripe)
cpd_tosse = discrete.TabularCPD(
    variable='Tosse',
    variable_card=2,
    values=[[0.7, 0.05],  # P(Tosse=True | Gripe=True), P(Tosse=True | Gripe=False)
            [0.3, 0.95]], # P(Tosse=False | Gripe=True), P(Tosse=False | Gripe=False)
    evidence=['Gripe'],
    evidence_card=[2]
)

# Adiciona as CPTs ao modelo
model.add_cpds(cpd_gripe, cpd_febre, cpd_tosse)


print("Modelo válido:", model.check_model())

#  inferência
infer = inference.VariableElimination(model)

# Cenário: O paciente tem febre e tosse. Qual a probabilidade de ter gripe?
# evidence={variável: estado} onde 0=False, 1=True
query_gripe_com_sintomas = infer.query(
    variables=['Gripe'],
    evidence={'Febre': 1, 'Tosse': 1}
)
print("\nProbabilidade de Gripe dado Febre=True e Tosse=True:")
print(query_gripe_com_sintomas)

# Cenário: O paciente não tem febre nem tosse. Qual a probabilidade de ter gripe?
query_gripe_sem_sintomas = infer.query(
    variables=['Gripe'],
    evidence={'Febre': 0, 'Tosse': 0}
)
print("\nProbabilidade de Gripe dado Febre=False e Tosse=False:")
print(query_gripe_sem_sintomas)