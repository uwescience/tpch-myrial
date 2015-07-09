
subbed = None
with open('q2.myl') as f:
  qs = f.read()
  subbed = qs.format(REGION="EUROPE", TYPE="BRASS", SIZE=15)

with open('q2.a.myl', 'w') as f:
  f.write(subbed)
