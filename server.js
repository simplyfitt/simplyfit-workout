const http=require('http'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const PORT=process.env.PORT||3000,DB=path.join(__dirname,'data/db.json'),PUB=path.join(__dirname,'public');
if(!fs.existsSync(DB))fs.copyFileSync(path.join(__dirname,'data/seed.json'),DB);
const load=()=>JSON.parse(fs.readFileSync(DB)),save=d=>fs.writeFileSync(DB,JSON.stringify(d,null,2));
const send=(r,c,b,t='application/json; charset=utf-8')=>{const ct=t.includes('charset')?t:t+'; charset=utf-8';r.writeHead(c,{'Content-Type':ct});r.end(typeof b=='string'||Buffer.isBuffer(b)?b:JSON.stringify(b))};
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8'};
http.createServer((q,r)=>{const u=new URL(q.url,'http://x'),p=u.pathname;let body='';
q.on('data',c=>body+=c);q.on('end',()=>{try{
if(p==='/api/clients'&&q.method==='GET')return send(r,200,load().clients.map(({id,name,token})=>({id,name,token})));
let m=p.match(/^\/api\/clients\/([\w-]+)$/);
if(m&&q.method==='GET'){const c=load().clients.find(c=>c.id===m[1]);return c?send(r,200,c):send(r,404,{error:'not found'})}
if(m&&q.method==='PUT'){const d=load(),inp=JSON.parse(body);let c=d.clients.find(c=>c.id===m[1]);
 if(!c){c={id:m[1],token:m[1]+'-'+crypto.randomBytes(3).toString('hex')};d.clients.push(c)}
 c.name=inp.name||c.name||m[1];c.week=inp.week||c.week||{title:'New week',days:[]};save(d);return send(r,200,c)}
m=p.match(/^\/api\/logs\/([\w-]+)$/);
if(m&&q.method==='GET'){const c=load().clients.find(c=>c.token===m[1]);return c?send(r,200,{logs:c.logs||{}}):send(r,404,{error:'not found'})}
if(m&&q.method==='PUT'){const d=load(),c=d.clients.find(c=>c.token===m[1]);if(!c)return send(r,404,{error:'not found'});
 const inp=JSON.parse(body||'{}');c.logs=inp.logs||c.logs||{};c.logsUpdatedAt=new Date().toISOString();save(d);return send(r,200,{ok:true})}
m=p.match(/^\/api\/plan\/([\w-]+)$/);
if(m){const c=load().clients.find(c=>c.token===m[1]);return c?send(r,200,{name:c.name,week:c.week}):send(r,404,{error:'not found'})}
let f=p==='/'?'/index.html':p.startsWith('/c/')?'/client.html':p==='/coach'?'/coach.html':p;
f=path.join(PUB,path.normalize(f));if(!f.startsWith(PUB)||!fs.existsSync(f))return send(r,404,'Not found','text/plain');
send(r,200,fs.readFileSync(f),types[path.extname(f)]||'application/octet-stream')}catch(e){send(r,400,{error:e.message})}})
}).listen(PORT,'0.0.0.0',()=>console.log(`SimplyFit on http://localhost:${PORT}  coach: /coach  demo: /c/demo-7f3k`));
