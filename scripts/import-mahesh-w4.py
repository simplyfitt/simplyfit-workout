import openpyxl,json,datetime,re
wb=openpyxl.load_workbook('data/week4-mahesh.xlsx')
SECS={'WARM-UP':'warmup','MAIN WORKOUT':'main','OPTIONAL':'optional','CARDIO TARGET':'cardio','COOLDOWN':'cooldown'}
def fmt(v):
  if v is None: return ''
  if isinstance(v,datetime.datetime): return f"{v.month}-{v.day}"
  if isinstance(v,float) and v.is_integer(): return str(int(v))
  return str(v).strip()
days=[];gaps=[]
for ws in wb:
  title=fmt(ws['A3'].value) if ws['A3'].value else ws.title
  m=re.search(r'—\s*(.*)',title); focus=m.group(1).strip() if m else ws.title
  dn=re.match(r'(DAY\s*\d+)',title); 
  name=f"Day {len(days)+1} — {focus.title() if focus.isupper() else focus}"
  sec=None;ex=[]
  for r in ws.iter_rows(max_row=80):
    a=fmt(r[0].value)
    if a.upper() in SECS: sec=SECS[a.upper()];continue
    if not sec or a in('Order','Type') : continue
    if sec=='cardio':
      if not a or a.startswith('e.g'): continue
      vals=[fmt(c.value) for c in r[:8]]
      if not any(vals[1:]): continue
      t,dur,zone,s,notes,on,off=vals[:7]
      if a.replace('.','').isdigit(): t,dur,zone,s,notes,on,off=vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7]
      ex.append(dict(name=t,sets=int(float(s)) if s.replace('.','').isdigit() else 1,reps=f"{dur} min" if dur.isdigit() else dur,notes=" · ".join(x for x in [zone and f"Intensity {zone}",on and f"{on} on / {off} off",notes] if x),link="",section='cardio'));continue
    c=r[1]; n=fmt(c.value)
    if not n or n.lower().startswith('e.g') or len(r)<2: continue
    if not re.match(r'^\d+[a-z]?$',a): continue
    link=c.hyperlink.target if c.hyperlink else ''
    if not link: gaps.append(f"{ws.title}: {n}")
    sets=fmt(r[3].value); rest=fmt(r[4].value)
    notes=[x for x in [fmt(r[6].value) if sec=='main' else fmt(r[5].value)] if x]
    if sec=='main' and fmt(r[5].value): notes.insert(0,'Weight: '+fmt(r[5].value))
    if rest: notes.append(f"Rest {rest}{'' if 'sec' in rest else ' sec'}")
    ex.append(dict(name=re.sub(r'\s+',' ',n),sets=int(float(sets)) if sets.replace('.','').isdigit() else 1,reps=fmt(r[2].value),notes=" · ".join(notes),link=link,section=sec))
  days.append(dict(name=name,exercises=ex))
c=dict(id='mahesh',name='Mahesh',token='mahesh-w4',week=dict(title='WEEK 4 — Mahesh',days=days))
db=json.load(open('data/db.json'))
db['clients']=[x for x in db['clients'] if x['token']!='mahesh-w4']+[c]
json.dump(db,open('data/db.json','w'),indent=2)
json.dump(c,open('data/mahesh-week.json','w'),indent=2)
for d in days: print(d['name'],len(d['exercises']),{s:sum(e['section']==s for e in d['exercises']) for s in SECS.values()})
print('total',sum(len(d['exercises']) for d in days),'links',sum(bool(e['link']) for d in days for e in d['exercises']),'gaps',gaps)
print(json.dumps(days[2]['exercises'][-2:],indent=0))
