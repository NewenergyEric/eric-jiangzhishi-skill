// Native layer layouts. The same story and original art are used in every ratio.
export function makeIntro({story, format, language, art, textBox, sourceHash}) {
  const {width:W,height:H}=format, en=language==='en', ratio=format.id;
  const paper='#FCF8EE',ink='#192F2A',sage='#668274';
  const box=(x,y,w,h,size,extra={})=>({x,y,w,h,size,...extra});
  let shared,scenes;
  if(ratio==='wide'){
    shared={margin:48,header:77,progress:482,icon:[48,20,25,40],brand:box(83,27,470,40,20),repo:box(48,495,650,30,16),language:box(718,497,194,26,13)};
    const head={eyebrow:box(48,100,408,36,18),title:box(48,148,408,154,en?40:44)};
    scenes=[
      {...head,body:box(48,317,408,86,22),cell:[477,156,435,290],note:box(492,103,150,30,18),line:[[492,135],[543,135]],artLabel:box(489,444,423,35,20)},
      {...head,pages:[[488,105,220],[704,159,194]],steps:[0,1,2].map(j=>box(83,311+j*43,366,36,21)),checks:[0,1,2].map(j=>[62,326+j*43]),artLabel:box(489,444,423,35,20)},
      {...head,body:box(48,317,408,86,22),pages:[[496,150,190],[518,124,180],[716,173,182],[730,150,180]],artLabels:[box(503,428,202,32,18),box(721,428,202,32,18)],cta:box(48,426,420,36,22),underline:[48,464,330]}
    ];
  } else if(ratio==='square'){
    shared={margin:36,header:82,progress:674,icon:[36,21,25,40],brand:box(73,28,610,40,22),repo:box(36,691,435,23,12),language:box(469,691,215,23,12)};
    const head={eyebrow:box(36,105,648,36,18),title:box(36,151,648,130,en?44:46)};
    scenes=[
      {...head,body:box(36,307,276,140,24),cell:[321,336,355,237],note:box(335,294,220,34,20),line:[[335,329],[386,329]],artLabel:box(36,608,648,42,22,{align:'center'})},
      {...head,pages:[[36,306,212],[256,333,185]],steps:[0,1,2].map(j=>box(487,328+j*87,196,77,20)),checks:[0,1,2].map(j=>[469,345+j*87]),artLabel:box(36,616,648,38,22,{align:'center'})},
      {eyebrow:box(36,101,648,34,18),title:box(36,142,648,124,en?40:44),body:box(36,270,648,70,22),pages:[[65,351,168],[98,337,158],[411,357,162],[442,334,156]],artLabels:[box(65,586,260,32,18),box(410,586,275,32,18)],cta:box(36,630,648,34,22),underline:[36,666,390]}
    ];
  } else if(ratio==='vertical'){
    shared={margin:54,header:108,progress:1161,icon:[54,39,28,45],brand:box(95,46,570,45,24),repo:box(54,1184,612,32,16),language:box(54,1220,612,30,14)};
    const head={eyebrow:box(54,156,612,42,22),title:box(54,218,612,177,en?58:60)};
    scenes=[
      {...head,body:box(54,421,612,120,30),cell:[54,650,612,408],note:box(70,578,260,42,24),line:[[70,621],[161,621]],artLabel:box(54,1090,612,45,27,{align:'center'})},
      {...head,pages:[[62,644,298],[369,710,264]],steps:[0,1,2].map(j=>box(94,417+j*61,565,46,27)),checks:[0,1,2].map(j=>[68,437+j*61]),artLabel:box(54,1090,612,45,26,{align:'center'})},
      {...head,body:box(54,420,612,119,28),pages:[[58,646,252],[91,614,236],[383,680,249],[415,637,224]],artLabels:[box(54,1034,300,42,24),box(379,1034,289,42,24)],cta:box(54,1107,612,44,27),underline:[54,1152,500]}
    ];
  } else throw new Error('Unknown ratio: '+ratio);

  const measurements=[];
  function type(value,spec,id,weight=450,color=ink) {
    if(!value)return '';
    const {size,align='left',...bounds}=spec;
    const result=textBox(value,bounds,{size,minSize:size,weight,color,field:id,lineHeight:1.36,align});
    const b=result.bounds;
    const x=Math.min(...b.map(x=>x.x)),y=Math.min(...b.map(x=>x.y));
    const right=Math.max(...b.map(x=>x.x+x.w)),bottom=Math.max(...b.map(x=>x.y+x.h));
    measurements.push({id,kind:'text',text:value,bounds,textBounds:{x,y,w:right-x,h:bottom-y},glyphs:b,out:false,overflow:false});
    return result.svg;
  }
  const common=type(story.projectTitle,shared.brand,'brand',650)+type(story.repositoryLabel,shared.repo,'repository',450,sage)
    +(story.sampleLanguage?type(story.sampleLanguage,shared.language,'sampleLanguage',450,sage):'');
  const labels=story.scenes.map((s,i)=>{
    const l=scenes[i],id='scene'+i+'.';
    return {eyebrow:type(s.eyebrow,l.eyebrow,id+'eyebrow',500,sage),title:type(s.title,l.title,id+'title',700),
      body:type(s.body,l.body,id+'body'),artLabel:type(s.artLabel,l.artLabel,id+'artLabel'),note:type(s.artNote,l.note,id+'note',500,sage),
      steps:(s.steps||[]).map((v,j)=>type(v,l.steps[j],id+'step'+j)),
      artLabels:(s.artLabels||[]).map((v,j)=>type(v,l.artLabels[j],id+'artLabel'+j)),cta:type(s.cta,l.cta,id+'cta',650)};
  });
  const clamp=v=>Math.max(0,Math.min(1,v)),ease=v=>1-Math.pow(1-clamp(v),3);
  const moved=(p,angle=0,dx=0,dy=0)=>({rect:[p[0]+dx,p[1]+dy,p[2]],angle});
  function motion(index,local){
    const l=scenes[index];
    if(index===0){
      const a=ease(local/1.25);
      return {cell:[l.cell[0]+(1-a)*(ratio==='vertical'?0:36),l.cell[1]+(1-a)*(ratio==='vertical'?32:ratio==='wide'?-10:12),...l.cell.slice(2)],opacity:a};
    }
    if(index===1){
      const a=ease(local/.85),b=ease((local-.45)/.85);
      return {pages:[
        moved(l.pages[0],-(1-a)*7,(1-a)*(ratio==='vertical'?-12:28),(1-a)*(ratio==='vertical'?28:0)),
        moved(l.pages[1],(1-b)*(ratio==='vertical'?4:8),(1-b)*(ratio==='square'?-12:ratio==='vertical'?12:30),0)
      ]};
    }
    const a=ease(local/.9),b=ease((local-.25)/.9);
    return {pages:[moved(l.pages[0],-(1-a)*8,-(1-a)*15,(1-a)*(ratio==='vertical'?25:0)),moved(l.pages[1],4),
      moved(l.pages[2],(1-b)*(ratio==='vertical'?4:8),(1-b)*25,0),moved(l.pages[3],5)]};
  }
  const image=(uri,[x,y,w,h])=>'<image x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" href="'+uri+'"/>';
  function sheet(uri,[x,y,w],angle=0,dx=0,dy=0){
    x+=dx;y+=dy;const h=w*4/3;
    return '<g transform="rotate('+angle+' '+(x+w/2)+' '+(y+h/2)+')"><rect x="'+(x+4)+'" y="'+(y+6)+'" width="'+w+'" height="'+h+'" fill="'+ink+'" opacity=".07"/><rect x="'+(x-1)+'" y="'+(y-1)+'" width="'+(w+2)+'" height="'+(h+2)+'" fill="'+paper+'" stroke="#B8C7B4"/>'+image(uri,[x,y,w,h])+'</g>';
  }
  function scene(index,local){
    const l=scenes[index],s=labels[index],m=motion(index,local);
    let body=s.eyebrow+s.title+s.body+s.cta;
    if(index===0){
      const b=ease((local-1)/2.5);
      const target=[l.cell[0]+l.cell[2]*(165/435),l.cell[1]+l.cell[3]*(119/290)];
      const points=[...l.line,target],length=points.slice(1).reduce((v,p,i)=>v+Math.hypot(p[0]-points[i][0],p[1]-points[i][1]),0);
      body+='<g opacity="'+m.opacity+'">'+image(art.cell,m.cell)+'</g>';
      body+='<path d="M '+points.map(p=>p.join(' ')).join(' L ')+'" fill="none" stroke="'+sage+'" stroke-width="1.6" stroke-dasharray="'+length+'" stroke-dashoffset="'+((1-b)*length)+'"/><circle cx="'+target[0]+'" cy="'+target[1]+'" r="3" fill="'+sage+'" opacity="'+b+'"/>'+s.note+s.artLabel;
    } else if(index===1){
      body+=sheet(art.cells2,m.pages[1].rect,m.pages[1].angle);
      body+=sheet(art.cells1,m.pages[0].rect,m.pages[0].angle)+s.artLabel;
      const checks=l.checks;
      body+='<path d="M '+checks[0][0]+' '+checks[0][1]+' L '+checks[2][0]+' '+checks[2][1]+'" stroke="#C8DCC6" stroke-width="2" fill="none"/>';
      for(let j=0;j<3;j++){
        const done=ease((local-j*.7)/.5),[x,y]=checks[j];
        body+='<circle cx="'+x+'" cy="'+y+'" r="8" fill="'+(done>.5?'#D9BE64':paper)+'" stroke="'+sage+'"/>'+s.steps[j]+'<path d="M '+(x-3)+' '+y+' l 2 2 l 4 -5" fill="none" stroke="'+ink+'" stroke-width="1.4" opacity="'+done+'"/>';
      }
    } else {
      body+=sheet(art.solar2,m.pages[1].rect,m.pages[1].angle)+sheet(art.solar1,m.pages[0].rect,m.pages[0].angle);
      body+=sheet(art.cells2,m.pages[3].rect,m.pages[3].angle)+sheet(art.cells1,m.pages[2].rect,m.pages[2].angle)+s.artLabels.join('');
      const [x,y,end]=l.underline,d=ease((local-1.3)/.8),len=end-x;
      body+='<path d="M '+x+' '+y+' Q '+((x+end)/2)+' '+(y-4)+' '+end+' '+y+'" fill="none" stroke="#D9BE64" stroke-width="3" stroke-dasharray="'+(len+2)+'" stroke-dashoffset="'+((1-d)*(len+2))+'"/>';
    }
    return body;
  }
  function frame(t,{guide=false}={}){
    let body='<rect width="'+W+'" height="'+H+'" fill="'+paper+'"/>'+common+image(art.icon,shared.icon);
    body+='<path d="M '+shared.margin+' '+shared.header+' H '+(W-shared.margin)+'" stroke="#C8D0BF"/>';
    for(let i=0;i<story.scenes.length;i++){
      const s=story.scenes[i];
      // Separate the outgoing and incoming copy with a short paper-colored dip.
      // Both sentences remain readable on either side of the cut.
      const enter=i===0?1:clamp((t-s.from)/.2),leave=i===2?1:clamp((s.to-t)/.2);
      const opacity=Math.min(enter,leave);
      if(opacity>0&&t>=s.from&&t<=s.to)body+='<g opacity="'+opacity+'">'+scene(i,t-s.from)+'</g>';
    }
    body+='<path d="M '+shared.margin+' '+shared.progress+' H '+(W-shared.margin)+'" stroke="#DCE2D5"/><path d="M '+shared.margin+' '+shared.progress+' H '+(shared.margin+(W-2*shared.margin)*clamp(t/story.duration))+'" stroke="'+sage+'" stroke-width="2"/>';
    if(guide)body+='<rect x="18" y="18" width="'+(W-36)+'" height="'+(H-36)+'" fill="none" stroke="#9E382D" stroke-dasharray="5 5"/>';
    return '<svg xmlns="http://www.w3.org/2000/svg" width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'+body+'</svg>';
  }
  function layer(id,rect,rotation=0){
    let [x,y,w,h]=rect;
    const angle=rotation*Math.PI/180,cx=x+w/2,cy=y+h/2;
    const rw=Math.abs(w*Math.cos(angle))+Math.abs(h*Math.sin(angle)),rh=Math.abs(w*Math.sin(angle))+Math.abs(h*Math.cos(angle));
    return {id,kind:'layer',bounds:{x:cx-rw/2,y:cy-rh/2,w:rw,h:rh},out:false,overflow:false};
  }
  const intersects=(a,b)=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1 && Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>1;
  function measure(time){
    const i=story.scenes.findIndex(s=>time>=s.from&&time<s.to),l=scenes[i],m=motion(i,time-story.scenes[i].from);
    const rows=measurements.filter(m=>!m.id.startsWith('scene')||m.id.startsWith('scene'+i+'.')).map(m=>({...m}));
    const visual=[layer('icon',shared.icon)];
    if(i===0)visual.push(layer('cell',m.cell));
    else m.pages.forEach((p,j)=>visual.push(layer((i===1?['cells1','cells2']:['solar1','solar2','cells1','cells2'])[j],[...p.rect,p.rect[2]*4/3],p.angle)));
    const overlaps=[];
    for(let a=0;a<rows.length;a++)for(let b=a+1;b<rows.length;b++){
      if(rows[a].glyphs.some(x=>rows[b].glyphs.some(y=>intersects(x,y))))overlaps.push([rows[a].id,rows[b].id]);
    }
    for(const r of rows)for(const im of visual)if(r.glyphs.some(b=>intersects(b,im.bounds)))overlaps.push([r.id,im.id]);
    if(i===1)for(const im of visual.filter(v=>v.id!=='icon'))for(const [x,y] of l.checks)
      if(intersects({x:x-9,y:y-9,w:18,h:18},im.bounds))overlaps.push(['step-marker',im.id]);
    return {frame:Math.round(time*story.fps),width:W,height:H,rows:[...rows.map(({glyphs,...r})=>r),...visual],overlaps};
  }
  const samples=[.25,1.5,3.5,4.7,5.05,5.3,6.5,8,9.7,10.05,10.3,11.5,13,15.8].map(measure);
  for(let f=0;f<story.duration*story.fps;f++){
    const sample=measure(f/story.fps);
    if(sample.overlaps.length)throw new Error('Text collision at frame '+f+': '+JSON.stringify(sample.overlaps));
    for(const row of sample.rows){const b=row.bounds;
      if(b.x<0||b.y<0||b.x+b.w>W||b.y+b.h>H)throw new Error('Layer leaves canvas at frame '+f+': '+row.id);
    }
  }
  const audit={mode:'native',embeddedMasterVideo:false,sourceHash,width:W,height:H,samples,allFramesChecked:story.duration*story.fps,errors:[]};
  return {frame,audit,metadata:{width:W,height:H,ratio,language,text:measurements,layout:'independent-text-art-and-motion-layers',engine:story.engine}};
}
