// Current R03M CAD presentation; illustrative motion, not solved airflow.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import {roomScenario} from './room_scenario.mjs';
const canvas = document.querySelector('#model');
const renderer = new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setClearColor(0xeaf0f1);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(36,1,.01,200);
camera.position.set(2.6,1.9,3.2);
const controls = new OrbitControls(camera,canvas);
controls.target.set(.45,.80,0);controls.enableDamping=true;
controls.minDistance=.65;controls.maxDistance=100;
scene.add(new THREE.HemisphereLight(0xffffff,0x708891,2.8));
for(const [x,y,z,p] of [[2,4,3,3],[-3,2,-2,1.5]]){
 const l=new THREE.DirectionalLight(0xffffff,p);l.position.set(x,y,z);scene.add(l);
}
const palette={panel:0x276975,support:0x53636a,filter:0xf2ad55,fan:0x183843,guard:0x41a99c,seal:0x715c44,hardware:0x91a0a7,reservation:0xac70a5};
const materials=Object.fromEntries(Object.entries(palette).map(([k,c])=>[k,new THREE.MeshStandardMaterial({color:c,roughness:.55,metalness:k==='hardware'?.4:.1,side:THREE.DoubleSide})]));
const assembly=new THREE.Group();scene.add(assembly);
const meshes=[];
for(const p of window.AQI_PARTS){
 const g=new THREE.BufferGeometry();
 g.setAttribute('position',new THREE.Float32BufferAttribute(p.vertices.flatMap(v=>[(v[0]-265)/1000,v[2]/1000,-(v[1]-170)/1000]),3));
 g.setIndex(p.triangles.flat());g.computeVertexNormals();
 const m=new THREE.Mesh(g,materials[p.kind]);m.name=p.name;
 m.userData={...p,vertices:undefined,triangles:undefined};assembly.add(m);meshes.push(m);
}
const floor=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xeaf0f1,roughness:1}));
floor.rotation.x=-Math.PI/2;floor.position.y=-.004;scene.add(floor);
// Simple original mannequin, exactly 1.70 m tall; not a demographic measurement.
const human=new THREE.Group();human.position.x=1.05;scene.add(human);
const humanMat=new THREE.MeshStandardMaterial({color:0xbe8972,roughness:.85});
function limb(a,b,r=.055){const from=new THREE.Vector3(...a),to=new THREE.Vector3(...b),d=to.clone().sub(from);const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,d.length(),12),humanMat);m.position.copy(from.add(to).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());human.add(m);}
for(const sign of [-1,1]){limb([sign*.08,.08,0],[sign*.09,.86,0],.07);limb([sign*.2,1.40,0],[sign*.25,.85,0],.045);const shoe=new THREE.Mesh(new THREE.BoxGeometry(.13,.08,.24),humanMat);shoe.position.set(sign*.08,.04,.035);human.add(shoe);}
const torso=new THREE.Mesh(new THREE.CapsuleGeometry(.17,.38,8,12),humanMat);torso.scale.z=.65;torso.position.y=1.12;human.add(torso);
limb([0,1.44,0],[0,1.54,0],.05);
const head=new THREE.Mesh(new THREE.SphereGeometry(.10,20,16),humanMat);head.position.y=1.60;human.add(head);
function label(text,pos,width){const c=document.createElement('canvas');c.width=640;c.height=100;const ctx=c.getContext('2d');ctx.fillStyle='#ffffffee';ctx.fillRect(0,0,640,100);ctx.fillStyle='#174b58';ctx.font='bold 32px system-ui';ctx.textAlign='center';ctx.fillText(text,320,61);const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),depthTest:false}));sprite.position.set(...pos);sprite.scale.set(width,width/6.4,1);return sprite;}
human.add(label('1.70 m scale reference',[0,1.86,0],.9));
const prototypeLabel=label('Prototype envelope: 0.631 m high',[0,.84,0],1.0);scene.add(prototypeLabel);
const room=new THREE.Group();scene.add(room);room.visible=false;
const roomMat=new THREE.LineBasicMaterial({color:0x779a9c,transparent:true,opacity:.55});
const grid=new THREE.GridHelper(1,10,0x82aaa8,0xc5d9d7);grid.position.y=.002;room.add(grid);
let roomEdges=null,roomLabel=null;
let humanOn=true,roomOn=false;
function fitContext(){
 const area=Number(document.querySelector('#room-area').value),h=Number(document.querySelector('#room-height').value);
 const radius=roomOn?Math.hypot(Math.sqrt(area)/Math.SQRT2,h/2):humanOn?1.35:.65;
 const aspect=Math.max(.35,canvas.clientWidth/Math.max(1,canvas.clientHeight));
 const distance=radius/(Math.sin(THREE.MathUtils.degToRad(camera.fov/2))*Math.min(1,aspect))*1.12;
 controls.target.set(roomOn?0:humanOn?.45:0,roomOn?h/2:humanOn?.85:.32,0);
 camera.position.copy(controls.target).add(new THREE.Vector3(1,.65,1.3).normalize().multiplyScalar(distance));
}
function updateRoom(){
 const area=Number(document.querySelector('#room-area').value),height=Number(document.querySelector('#room-height').value),cadr=Number(document.querySelector('#assumed-cadr').value),reduction=Number(document.querySelector('#target-reduction').value),minutes=Number(document.querySelector('#elapsed-minutes').value);
 const result=roomScenario(area,height,cadr,reduction,minutes),side=Math.sqrt(area);
 document.querySelector('#area-value').textContent=`${area} m² (${(area*10.7639104167).toFixed(0)} ft²)`;
 document.querySelector('#height-value').textContent=`${height.toFixed(1)} m`;
 document.querySelector('#cadr-value').textContent=`${cadr} m³/h — assumed`;
 document.querySelector('#elapsed-value').textContent=`${minutes} min`;
 document.querySelector('#target-time').textContent=result.targetMinutes===null?'No modeled cleaning':`${result.targetMinutes.toFixed(1)} min`;
 document.querySelector('#room-summary').textContent=`Ideal time for ${(reduction*100).toFixed(0)}% fewer particles. Room: ${area} m² × ${height.toFixed(1)} m = ${result.volume.toFixed(1)} m³. Equivalent clean-air changes: ${result.rate.toFixed(2)}/hour (not outdoor ventilation).`;
 document.querySelector('#remaining-summary').textContent=`At ${minutes} min: ${(result.remaining*100).toFixed(1)}% of starting particles remain in this ideal scenario. Not an AQI or health/safety reading.`;
 document.querySelector('#required-rate').textContent=`To reach this ${Math.round(reduction*100)}% goal in 30 min, this model requires ${result.requiredCadr30.toFixed(1)} m³/h effective clean air. D01 has not demonstrated that rate.`;
 document.querySelector('#flow-bound').textContent=`If installed airflow were 300 m³/h and particle capture were perfect, the ideal ${Math.round(reduction*100)}% time could not be below ${(result.requiredCadr30/300*30).toFixed(1)} min. Neither airflow nor capture is verified.${cadr>300?' Your assumed CADR exceeds that screening flow: it cannot describe that operating point.':''}`;
 const points=Array.from({length:81},(_,i)=>`${35+i/80*253},${105-Math.exp(-result.rate*(i/80*4))*93}`);
 document.querySelector('#decay-path').setAttribute('d','M'+points.join(' L'));
 document.querySelector('#time-dot').setAttribute('cx',35+minutes/240*253);
 document.querySelector('#time-dot').setAttribute('cy',105-result.remaining*93);
 if(roomEdges){room.remove(roomEdges);roomEdges.geometry.dispose();room.remove(roomLabel);roomLabel.material.map.dispose();roomLabel.material.dispose();}
 const box=new THREE.BoxGeometry(side,height,side);roomEdges=new THREE.LineSegments(new THREE.EdgesGeometry(box),roomMat);box.dispose();roomEdges.position.y=height/2;room.add(roomEdges);grid.scale.set(side,1,side);
 roomLabel=label(`${side.toFixed(2)} × ${side.toFixed(2)} × ${height.toFixed(1)} m room`,[0,height+.15,-side/2],Math.min(side,3));room.add(roomLabel);
}
for(const id of ['room-area','room-height','assumed-cadr','target-reduction','elapsed-minutes'])document.querySelector('#'+id).addEventListener('input',()=>{updateRoom();if(roomOn&&['room-area','room-height'].includes(id))fitContext();});
document.querySelector('#human').onclick=()=>{humanOn=!humanOn;human.visible=humanOn;document.querySelector('#human').classList.toggle('active',humanOn);fitContext();};
document.querySelector('#room').onclick=()=>{roomOn=!roomOn;room.visible=roomOn;document.querySelector('#room').classList.toggle('active',roomOn);fitContext();};
updateRoom();
const paths=[];
for(const sign of [-1,1]) for(let j=0;j<4;j++){
 const x=-.17+j*.11;
 paths.push(new THREE.CatmullRomCurve3([new THREE.Vector3(x,.26,sign*.5),new THREE.Vector3(x,.26,sign*.20),new THREE.Vector3(x,.38,0),new THREE.Vector3(x,.76,0)]));
}
const air=new THREE.Group();scene.add(air);
const beads=[];
for(const path of paths)for(let j=0;j<8;j++){
 const bead=new THREE.Mesh(new THREE.SphereGeometry(.004,8,6),new THREE.MeshBasicMaterial({color:0x18a6ac}));
 air.add(bead);beads.push({bead,path,phase:j/8});
}
let mode='simple',cut=false,explode=0,playing=true,airOn=false;
function update(){
 for(const m of meshes){
  const e=m.userData.explode;
  m.position.set(e[0]/1000*explode,e[2]/1000*explode,-e[1]/1000*explode);
  m.visible=!(cut&&['panel','guard'].includes(m.userData.kind));
 }
 air.visible=airOn&&explode===0;
 document.querySelector('#simple-copy').hidden=mode!=='simple';
 document.querySelector('#technical-copy').hidden=mode!=='technical';
 document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
 document.querySelector('#cut').classList.toggle('active',cut);
 document.querySelector('#air').classList.toggle('active',airOn);
}
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;update();});
document.querySelector('#explode').oninput=e=>{explode=Number(e.target.value);update();};
document.querySelector('#cut').onclick=e=>{cut=!cut;e.target.classList.toggle('active',cut);update();};
document.querySelector('#air').onclick=e=>{airOn=!airOn;e.target.classList.toggle('active',airOn);if(airOn){cut=true;explode=0;document.querySelector('#explode').value=0;}update();};
document.querySelector('#motion').onclick=e=>{playing=!playing;e.target.textContent=playing?'Pause motion':'Play motion';};
document.querySelector('#reset').onclick=()=>{cut=false;airOn=false;explode=0;document.querySelector('#explode').value=0;fitContext();update();};
const ray=new THREE.Raycaster();
canvas.addEventListener('click',e=>{
 const r=canvas.getBoundingClientRect();ray.setFromCamera(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,-((e.clientY-r.top)/r.height)*2+1),camera);
 const hit=ray.intersectObjects(meshes.filter(m=>m.visible))[0];
 if(hit){document.querySelector('#selection').textContent=hit.object.name+' · '+hit.object.userData.kind+' · '+(hit.object.userData.note||'CAD fit envelope; review only');}
});
const clock=new THREE.Clock();let t=0;
function tick(){requestAnimationFrame(tick);if(playing)t+=clock.getDelta();else clock.getDelta();
 const r=canvas.getBoundingClientRect();if(renderer.domElement.width!==Math.round(r.width*renderer.getPixelRatio())||renderer.domElement.height!==Math.round(r.height*renderer.getPixelRatio())){renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}
 beads.forEach(({bead,path,phase})=>bead.position.copy(path.getPoint((t*.17+phase)%1)));
 controls.update();renderer.render(scene,camera);
}
fitContext();update();tick();
window.AQI_VIEWER_READY={objects:meshes.length,source:'R03M actual CAD tessellation',simulation:false};
