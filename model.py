import math;
from gurobipy import *

# 
d={}
d={ ("Doce","Doce"):  0,  ("Doce","Bom"):math.inf,  ("Doce","Sky"):6000, ("Doce","Moon"):5000, ("Doce","Mars"):5500,
    ("Bom","Doce"):math.inf,  ("Bom","Bom"):0,  ("Bom","Sky"): 6000, ("Bom","Moon"): 5800, ("Bom","Mars"):4800,
    ("Sky","Doce"):    6000, ("Sky","Bom"): 5000, ("Sky","Sky"): 0, ("Sky","Moon"): 500 , ("Sky","Mars"): 2000,
    ("Moon","Doce"):5000, ("Moon","Bom"):500,  ("Moon","Sky"): 500, ("Moon","Moon"): 0, ("Moon","Mars"): 1000,
    ("Mars","Doce"):5500, ("Mars","Bom"):4800, ("Mars","Sky"): 2000, ("Mars","Moon"): 1000, ("Mars","Mars"): 0}

t={}
# Doce – Sky – Doce
t[1, 1] = d["Doce","Sky"]/25 * 2
t[1, 2] = d["Doce","Sky"]/20 * 2

# Doce – Mars – Doce
t[2, 1] = d["Doce","Mars"]/25 * 2
t[2, 2] = d["Doce","Mars"]/20 * 2

# Doce – Sky – Mars - Doce
t[3, 1] = d["Doce","Sky"]/25 + d["Sky","Mars"]/30 + d["Mars","Doce"]/25
t[3, 2] = d["Doce","Sky"]/20 + d["Sky","Mars"]/24 + d["Mars","Doce"]/20

# Doce – Mars – Sky – Doce
t[4, 1] = d["Doce","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Doce"]/25
t[4, 2] = d["Doce","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Doce"]/20

# Bom – Sky – Bom
t[5, 1] = d["Bom","Sky"]/25 * 2
t[5, 2] = d["Bom","Sky"]/20 * 2

# Bom – Mars – Bom
t[6, 1] = d["Bom","Mars"]/25 * 2
t[6, 2] = d["Bom","Mars"]/20 * 2

# Bom – Sky - Mars – Bom
t[7, 1] = d["Bom","Sky"]/25 + d["Sky","Mars"]/30 + d["Mars","Bom"]/25
t[7, 2] = d["Bom","Sky"]/20 + d["Sky","Mars"]/24 + d["Mars","Bom"]/20

# Bom – Mars - Sky - Bom
t[8, 1] = d["Bom","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Bom"]/25
t[8, 2] = d["Bom","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Bom"]/20

# Doce – Moon – Doce
t[9, 1] = d["Doce","Moon"]/25 * 2

# Doce – Sky - Moon – Doce
t[10, 1] = d["Doce","Sky"]/25 + d["Sky","Moon"]/30 + d["Moon","Doce"]/25

# Doce – Moon - Mars - Doce
t[11, 1] = d["Doce","Moon"]/25 + d["Moon","Mars"]/30 + d["Mars","Doce"]/25

# Doce – Moon - Sky - Doce
t[12, 1] = d["Doce","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Doce"]/25

# Doce – Mars – Moon – Doce
t[13, 1] = d["Doce","Mars"]/25 + d["Mars","Moon"]/30 + d["Moon","Doce"]/25

# Bom – Moon – Bom
t[14, 1] = d["Bom","Moon"]/25 * 2

# Bom – Sky - Moon – Bom
t[15, 1] = d["Bom","Sky"]/25 + d["Sky","Moon"]/30 + d["Moon","Bom"]/25

# Bom - Moon – Mars - Bom
t[16, 1] = d["Bom","Moon"]/25 + d["Moon","Mars"]/30 + d["Mars","Bom"]/25

# Bom - Moon – Sky - Bom
t[17, 1] = d["Bom","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Bom"]/25

# Bom – Mars - Moon - Bom
t[18, 1] = d["Bom","Mars"]/25 + d["Mars","Moon"]/30 + d["Moon","Bom"]/25


# Number of ships
S1 = [i for i in range(1, 19)]
S2 = [i for i in range(1, 9)]

model = Model("IOPE")

# Number of vehicles of type 1
x={}
a={}
for i in S1:
    x[i,1]=model.addVar(vtype="I", name="x(%s,%s)" % (i,1))
    for i in S1:
        a[i,1]=model.addVar(vtype="I", name="a(%s,%s)" % (i,1))
model.update()  # vars were added
    
# Number of vehicles of type 2
x={}
for i in S2:
    x[i,2]=model.addVar(vtype="I", name="x(%s,%s)" % (i,2))
    for i in S1:
        a[i,2]=model.addVar(vtype="I", name="a(%s,%s)" % (i,2))
model.update()  # vars were added
    
# # Number of trips done with vehicles type 1
# y={}
# for i in S1:
#     y[i,1]=model.addVar(vtype="I", name="y(%s,%s)" % (i,1))
# model.update()  # vars were added
    
# # Number of trips done with vehicles 2
# x={}
# for i in S2:
#     y[i,2]=model.addVar(vtype="I", name="y(%s,%s)" % (i,2))
# model.update()  # vars were added

for i in S1:
    model.addConstr(quicksum( t[j,1] * a[j,1] for j in S1) <= 345 * 24, "c1(%s,%s)" % (i,1))

for i in S2:
    model.addConstr(quicksum( t[j,2] * a[j,2] for j in S2) <= 345 * 24, "c2(%s,%s)" % (i,2))

# TODO: Change to costs
model.setObjective(quicksum(x[i,2] for i in S2) + quicksum(x[i,1] for i in S1), GRB.MINIMIZE)

model.update() 
    
model.optimize()