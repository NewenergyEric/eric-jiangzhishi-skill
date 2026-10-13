// Native bilingual films with resumable frames and compact encodes.
import {readFile,writeFile,mkdir,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {makeIntro} from './intro-composition.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),argv=process.argv.slice(2);
function option(name,fallback){
  const i=argv.indexOf('--'+name);
  if(i<0)return fallback;
  if(!argv[i+1]||argv[i+1].startsWith('--'))throw new Error('Missing --'+name);
  return argv[i+1];
}
const language=option('lang','zh'),ratio=option('ratio','wide');
if(!['zh','en'].includes(language))throw new Error('--lang must be zh or en');
const preview=argv.includes('--preview'),suffix=language==='en'?'.en':'';
const media=path.join(root,'media/intro'),storyName='story'+suffix+'.json';
const story=JSON.parse(await readFile(path.join(media,storyName),'utf8'));
const profiles=JSON.parse(await readFile(path.join(media,'formats.json'),'utf8'));
const format=profiles.formats.find(f=>f.id===ratio);
if(!format)throw new Error('--ratio must be wide, square or vertical');
const engineRoot=path.resolve(option('motion-story',path.join(root,'.build/tools/eric-intro-motion-skill')));
const git=(...args)=>execFileSync('git',args,{cwd:engineRoot,encoding:'utf8',windowsHide:true}).trim();
if(git('rev-parse','HEAD')!==story.engine.commit)throw new Error('Use the pinned engine revision in the storyboard');
git('diff','--exit-code','HEAD','--',story.engine.path,'skills/social-motion/scripts/native-audit.mjs');
const engine=path.join(engineRoot,story.engine.path,'scripts');
const {png,run,inspectVideo}=await import(pathToFileURL(path.join(engine,'render.mjs')).href);
const {textBox}=await import(pathToFileURL(path.join(engine,'text.mjs')).href);
const {assertNativeAudit}=await import(pathToFileURL(path.join(engineRoot,'skills/social-motion/scripts/native-audit.mjs')).href);
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const out=ratio==='wide'?media:path.join(media,ratio);
const scratch=path.join(root,'.build/intro-render',ratio,language),assetCache=path.join(root,'.build/intro-assets');
await mkdir(out,{recursive:true});await mkdir(scratch,{recursive:true});await mkdir(assetCache,{recursive:true});
const sourceHashes={},runtimeHashes={},rasterHashes={};
for(const name of ['scripts/build_intro.mjs','scripts/intro-composition.mjs','media/intro/formats.json'])
  sourceHashes[name]=hash(await readFile(path.join(root,name)));
for(const name of git('ls-files',story.engine.path+'/scripts',story.engine.path+'/package.json',story.engine.path+'/package-lock.json',story.engine.path+'/assets/fonts','skills/social-motion/scripts/native-audit.mjs').split('\n'))
  runtimeHashes[name]=hash(await readFile(path.join(engineRoot,name)));
async function raster(relative,width){
  const original=path.join(root,relative),digest=hash(await readFile(original));
  sourceHashes[relative]=digest;
  const cached=path.join(assetCache,digest+'-'+width+'.png');
  if(!await access(cached).then(()=>true,()=>false))
    await run('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',original,'-vf','scale='+width+':-1:flags=lanczos','-frames:v','1','-update','1','-map_metadata','-1',cached]);
  const pixels=await readFile(cached);
  rasterHashes[relative]=hash(pixels);
  return 'data:image/png;base64,'+pixels.toString('base64');
}
const art={
  cell:await raster('examples/cells/art/animal-cell.png',720),
  icon:await raster('examples/cells/art/icon-microscope.png',96),
  cells1:await raster('examples/cells/output/page-01.png',450),
  cells2:await raster('examples/cells/output/page-02.png',450),
  solar1:await raster('examples/solar-system/output/page-01.png',450),
  solar2:await raster('examples/solar-system/output/page-02.png',450)
};
const storySha256=hash(await readFile(path.join(media,storyName)));
const sourceHash=hash(JSON.stringify({storySha256,sourceHashes,runtimeHashes,rasterHashes}));
const composition=makeIntro({story,format,language,art,textBox,sourceHash});
assertNativeAudit(composition.audit);
const points=[['scene-01',3.5],['scene-02',8],['scene-03',13],['before-cut-01',4.75],['after-cut-01',5.25],['before-cut-02',9.75],['after-cut-02',10.25]];
for(const [name,at] of points)await writeFile(path.join(scratch,name+'.png'),png(composition.frame(at),format.width));
await writeFile(path.join(scratch,'safe.png'),png(composition.frame(13,{guide:true}),format.width));
await writeFile(path.join(scratch,'layout.json'),JSON.stringify(composition.metadata,null,2)+'\n');
await writeFile(path.join(scratch,'audit.json'),JSON.stringify(composition.audit,null,2)+'\n');
if(preview){
  console.log(JSON.stringify({preview:true,language,ratio,width:format.width,height:format.height,measuredScenes:3}));
} else {
  const visualKey=hash(JSON.stringify({sourceHash,width:format.width,height:format.height,fps:story.fps}));
  const cache=path.join(root,'.build/intro-frame-cache',visualKey),indexFile=path.join(cache,'index.json');
  await mkdir(cache,{recursive:true});
  let index=await readFile(indexFile,'utf8').then(JSON.parse,()=>({key:visualKey,frames:{}}));
  if(index.key!==visualKey)throw new Error('Unexpected frame cache key');
  const count=Math.round(story.duration*story.fps);
  let reused=0,rendered=0;
  for(let i=0;i<count;i++){
    const name=String(i).padStart(6,'0')+'.png',f=path.join(cache,name);
    const old=index.frames[name];
    const bytes=old?await readFile(f).catch(()=>null):null;
    if(bytes&&hash(bytes)===old)reused++;
    else{
      const frame=png(composition.frame(i/story.fps),format.width);
      await writeFile(f,frame);index.frames[name]=hash(frame);rendered++;
    }
    if(i%48===0){
      await writeFile(indexFile,JSON.stringify(index)+'\n');
      console.log(ratio+'/'+language+' frames '+i+'/'+count);
    }
  }
  await writeFile(indexFile,JSON.stringify(index)+'\n');
  const movie=path.join(out,'intro'+suffix+'.mp4'),gif=path.join(out,'intro'+suffix+'.gif');
  const encodeKey=hash(JSON.stringify({visualKey,encoding:profiles.encoding,ffmpeg:await run('ffmpeg',['-version'])}));
  const encodeReceipt=path.join(scratch,'encode.json');
  const receipt=await readFile(encodeReceipt,'utf8').then(JSON.parse,()=>null);
  const previous=await readFile(movie).catch(()=>null);
  const encodeHit=receipt?.key===encodeKey&&previous&&hash(previous)===receipt.sha256;
  if(!encodeHit){
    await run('ffmpeg',['-hide_banner','-loglevel','error','-y','-framerate',String(story.fps),'-i',path.join(cache,'%06d.png'),
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v:0','-map','1:a:0',
      '-frames:v',String(count),'-t',String(story.duration),'-c:v','libx264','-preset',profiles.encoding.preset,
      '-crf',String(profiles.encoding.crf),'-pix_fmt','yuv420p','-vf','setsar=1','-c:a','aac','-b:a',profiles.encoding.audioBitrate,
      '-shortest','-movflags','+faststart','-map_metadata','-1','-threads','4',movie]);
    await writeFile(encodeReceipt,JSON.stringify({key:encodeKey,sha256:hash(await readFile(movie))})+'\n');
  }
  await run('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',movie,'-filter_complex',
    'fps='+format.gifFps+',scale='+format.gifWidth+':-1:flags=lanczos,split[a][b];[a]palettegen=max_colors='+format.gifColors+':reserve_transparent=0[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle',
    '-loop','0','-an','-map_metadata','-1',gif]);
  const poster=path.join(out,'poster'+suffix+'.png'),cover=path.join(out,'cover'+suffix+'.png');
  await writeFile(poster,png(composition.frame(13),format.width));
  await run('ffmpeg',['-hide_banner','-loglevel','error','-y','-i',poster,'-filter_complex',
    'scale='+format.coverWidth+':-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:reserve_transparent=0[p];[b][p]paletteuse=dither=bayer:bayer_scale=5',
    '-frames:v','1','-update','1','-map_metadata','-1',cover]);
  // Keep only PNG image data and palette chunks; omit encoder metadata.
  const coverRaw=await readFile(cover),chunks=[coverRaw.subarray(0,8)];
  for(let offset=8;offset<coverRaw.length;){
    const size=coverRaw.readUInt32BE(offset),type=coverRaw.toString('ascii',offset+4,offset+8);
    if(['IHDR','PLTE','tRNS','IDAT','IEND'].includes(type))chunks.push(coverRaw.subarray(offset,offset+12+size));
    offset+=12+size;
  }
  await writeFile(cover,Buffer.concat(chunks));
  const outputs={
    mp4:await inspectVideo(movie,{width:format.width,height:format.height,duration:story.duration,fps:story.fps}),
    gif:await inspectVideo(gif,{width:format.gifWidth,height:Math.round(format.height*format.gifWidth/format.width),duration:story.duration,fps:format.gifFps,gif:true})
  };
  for(const ext of ['mp4','gif']){
    if(outputs[ext].bytes>format.budgets[ext+'Bytes'])throw new Error('Size budget exceeded: '+ratio+' '+ext);
    await run('ffmpeg',['-v','error','-xerror','-i',ext==='mp4'?movie:gif,'-f','null','-']);
  }
  const coverBytes=await readFile(cover);
  if(coverBytes.length>format.budgets.coverBytes)throw new Error('Cover exceeds size budget');
  const sampledFrames=[0,.13,.28,.47,.63,.81].map(t=>hash(png(composition.frame(t*story.duration),480)));
  if(new Set(sampledFrames).size!==sampledFrames.length)throw new Error('Missing motion in samples');
  await writeFile(path.join(out,'audit'+suffix+'.json'),JSON.stringify(composition.audit,null,2)+'\n');
  const manifest={version:(await readFile(path.join(root,'VERSION'),'utf8')).trim(),language:story.language,ratio:format.ratio,
    engine:story.engine,runtimeHashes,rasterHashes,storyFile:'media/intro/'+storyName,storySha256,sourceHashes,sourceHash,format,encoding:profiles.encoding,
    outputs,sampledFrames:sampledFrames.length,sampledUniqueFrames:new Set(sampledFrames).size,
    posterSha256:hash(await readFile(poster)),cover:{bytes:coverBytes.length,sha256:hash(coverBytes)},
    auditSha256:hash(await readFile(path.join(out,'audit'+suffix+'.json'))),budgets:format.budgets,
    cache:{visualKey,reusedFrames:reused,renderedFrames:rendered,encodeHit:Boolean(encodeHit)},fullDecodeVerified:true,platformPreviewVerified:false};
  await writeFile(path.join(out,'report'+suffix+'.json'),JSON.stringify(manifest,null,2)+'\n');
  console.log(JSON.stringify({language,ratio,mp4Bytes:outputs.mp4.bytes,gifBytes:outputs.gif.bytes,coverBytes:coverBytes.length,reusedFrames:reused,renderedFrames:rendered}));
}
