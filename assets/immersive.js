(() => {
'use strict';
const canvas=document.getElementById('scalp-space');
if(!canvas)return;
const ctx=canvas.getContext('2d');if(!ctx)return;
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const caption=document.getElementById('scene-caption');
const pause=document.getElementById('scene-pause');
const groups={posterior:['P3','P4','Pz','O1','O2'],frontal:['Fp1','Fp2','F3','F4','F7','F8','Fz']};
// Approximate 10-20 schematic. Coordinates, mesh and connecting arcs are illustrative.
const xy={Fp1:[-.3,.86],Fp2:[.3,.86],F7:[-.8,.46],F3:[-.4,.48],Fz:[0,.5],F4:[.4,.48],F8:[.8,.46],T3:[-.97,0],C3:[-.5,0],Cz:[0,0],C4:[.5,0],T4:[.97,0],T5:[-.8,-.46],P3:[-.4,-.48],Pz:[0,-.5],P4:[.4,-.48],T6:[.8,-.46],O1:[-.3,-.86],O2:[.3,-.86]};
const nodes=Object.entries(xy).map(([name,[x,z]])=>({name,p:[x,Math.sqrt(Math.max(.03,1-x*x-z*z))*1.1,z]}));
let width=600,height=700,angle=-.45,tilt=.44,group='all',paused=reduce.matches,visible=true,last=0,drag=null,frame=0;
const points=[];for(let i=0;i<1100;i++){const y=1-2*(i+.5)/1100,r=Math.sqrt(1-y*y),a=i*2.399963;points.push([Math.cos(a)*r,y*1.13,Math.sin(a)*r]);}
function project([x,y,z]){const ca=Math.cos(angle),sa=Math.sin(angle),ct=Math.cos(tilt),st=Math.sin(tilt);const u=x*ca+z*sa,v=z*ca-x*sa,w=y*ct-v*st,d=y*st+v*ct;const scale=Math.min(width*.36,height*.30)*3.8/(3.8+d);return [width*.52+u*scale,height*.45-w*scale,d,scale];}
function line(vertices,color){ctx.beginPath();vertices.forEach((p,i)=>{const q=project(p);i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]);});ctx.strokeStyle=color;ctx.lineWidth=.65;ctx.stroke();}
function draw(){ctx.clearRect(0,0,width,height);const halo=ctx.createRadialGradient(width*.52,height*.45,0,width*.52,height*.45,Math.min(width,height)*.47);halo.addColorStop(0,'#4cffee0b');halo.addColorStop(1,'#4cffee00');ctx.fillStyle=halo;ctx.fillRect(0,0,width,height);
 // Orbit plane: a visual orientation device, not connectivity data.
 for(const radius of [1.3,1.48]){const path=[];for(let j=0;j<=120;j++){const a=j/120*Math.PI*2;path.push([Math.cos(a)*radius,-.45,Math.sin(a)*radius]);}line(path,'#88ffdc24');}
 for(let k=-3;k<=4;k++){const lat=k/5*Math.PI/2;const path=[];for(let j=0;j<=80;j++){const a=j/80*Math.PI*2;path.push([Math.cos(a)*Math.cos(lat),Math.sin(lat)*1.13,Math.sin(a)*Math.cos(lat)]);}line(path,'#83e8cf18');}
 for(let k=0;k<12;k++){const a=k/12*Math.PI*2,path=[];for(let j=0;j<=60;j++){const t=j/60*Math.PI;path.push([Math.sin(t)*Math.cos(a),Math.cos(t)*1.13,Math.sin(t)*Math.sin(a)]);}line(path,'#83e8cf14');}
 for(const p of points){const q=project(p),alpha=Math.max(.07,.5-q[2]*.24);ctx.fillStyle=`rgba(119,230,208,${alpha})`;ctx.beginPath();ctx.arc(q[0],q[1],q[2]<0?1:.6,0,Math.PI*2);ctx.fill();}
 // Nose gives the schematic an explicit front orientation.
 line([[-.1,.05,1],[0,.14,1.22],[.1,.05,1]],'#b0fff466');
 const selected=nodes.map(n=>({...n,q:project(n.p)})).sort((a,b)=>b.q[2]-a.q[2]);
 for(const n of selected){const active=group==='all'||groups[group].includes(n.name);const color=group==='frontal'?'#c9afff':'#96ffe3';ctx.globalAlpha=active?1:.22;ctx.fillStyle=active?color:'#799ca6';ctx.shadowColor=color;ctx.shadowBlur=active?14:0;ctx.beginPath();ctx.arc(n.q[0],n.q[1],active?4:2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;if(active){ctx.font='10px monospace';ctx.fillText(n.name,n.q[0]+9,n.q[1]-7);ctx.strokeStyle=color+'55';ctx.beginPath();ctx.arc(n.q[0],n.q[1],8,0,Math.PI*2);ctx.stroke();}ctx.globalAlpha=1;}
}
function schedule(){if(!frame)frame=requestAnimationFrame(tick);}
function tick(time){frame=0;if(!visible||document.hidden){last=time;return;}if(!paused&&!drag){angle+=Math.min(time-last,50)*.00009;}last=time;draw();if(!paused)schedule();}
function resize(){const rect=canvas.getBoundingClientRect();width=rect.width;height=rect.height;const dpr=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();schedule();}
function pauseLabel(){pause.textContent=paused?'Resume motion':'Pause motion';pause.setAttribute('aria-pressed',String(paused));}
function choose(value){group=value;document.querySelectorAll('[data-region]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.region===value)));caption.textContent=value==='all'?'19 electrode positions · schematic, not measured brain activity':value==='posterior'?'Posterior region · P3, P4, Pz, O1, O2 · five analysis channels':'Frontal region · Fp1, Fp2, F3, F4, F7, F8, Fz · seven analysis channels';if(value==='posterior')angle=Math.PI-.45;if(value==='frontal')angle=-.45;draw();}
for(const b of document.querySelectorAll('[data-region]'))b.addEventListener('click',()=>choose(b.dataset.region));
pause.addEventListener('click',()=>{paused=!paused;pauseLabel();schedule();});
canvas.addEventListener('pointerdown',e=>{drag={x:e.clientX,a:angle};canvas.setPointerCapture(e.pointerId);});
canvas.addEventListener('pointermove',e=>{if(drag){angle=drag.a+(e.clientX-drag.x)*.008;draw();}});
function release(){drag=null;schedule();}canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);
canvas.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();angle+=e.key==='ArrowLeft'?-.15:.15;draw();}if(e.key===' '){e.preventDefault();paused=!paused;pauseLabel();schedule();}});
const header=document.querySelector('header');
function scroll(){const max=document.documentElement.scrollHeight-innerHeight;document.getElementById('reading-progress').style.width=(max>0?scrollY/max*100:0)+'%';if(!reduce.matches){tilt=.44+Math.min(scrollY/Math.max(header.offsetHeight,1),1)*.38;draw();}}
addEventListener('scroll',scroll,{passive:true});addEventListener('resize',resize);document.addEventListener('visibilitychange',()=>{if(!document.hidden)schedule();});
if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)schedule();}).observe(canvas);
reduce.addEventListener('change',e=>{if(e.matches)paused=true;pauseLabel();schedule();});pauseLabel();resize();scroll();
})();
