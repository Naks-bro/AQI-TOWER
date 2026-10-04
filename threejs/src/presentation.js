// Current R03M CAD presentation; illustrative motion, not solved airflow.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const canvas = document.querySelector('#model');
const renderer = new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setClearColor(0xeaf0f1);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(36,1,.01,30);
camera.position.set(1.25,1.04,1.48);
const controls = new OrbitControls(camera,canvas);
controls.target.set(0,.32,0);controls.enableDamping=true;
controls.minDistance=.65;controls.maxDistance=4;
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
document.querySelector('#reset').onclick=()=>{camera.position.set(1.25,1.04,1.48);controls.target.set(0,.32,0);cut=false;airOn=false;explode=0;document.querySelector('#explode').value=0;update();};
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
update();tick();
window.AQI_VIEWER_READY={objects:meshes.length,source:'R03M actual CAD tessellation',simulation:false};
