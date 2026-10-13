// Bilingual composition using the maintained Motion Story renderer. See media/intro/README.md.
import {readFile, writeFile, mkdir, copyFile, access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const argv = process.argv.slice(2);
function option(name, fallback) {
  const i = argv.indexOf('--' + name);
  if (i < 0) return fallback;
  if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('Missing value for --' + name);
  return argv[i + 1];
}
const preview = argv.includes('--preview');
const language = option('lang', 'zh');
if (!['zh','en'].includes(language)) throw new Error('--lang must be zh or en.');
const suffix = language === 'en' ? '.en' : '';
const engineRoot = path.resolve(option('motion-story', path.join(root, '.build/tools/eric-intro-motion-skill')));
const storyName = `story${suffix}.json`;
const story = JSON.parse(await readFile(path.join(root, 'media/intro', storyName), 'utf8'));
const engineCommit = execFileSync('git', ['rev-parse', 'HEAD'], {cwd: engineRoot, encoding: 'utf8', windowsHide: true}).trim();
if (engineCommit !== story.engine.commit) throw new Error('Use the Motion Story commit recorded in story.json.');
execFileSync('git', ['diff', '--exit-code', 'HEAD', '--', story.engine.path], {cwd: engineRoot, windowsHide: true});
const engine = path.join(engineRoot, story.engine.path, 'scripts');
const {renderStory, png, run, inspectVideo} = await import(pathToFileURL(path.join(engine, 'render.mjs')).href);
const {textBox} = await import(pathToFileURL(path.join(engine, 'text.mjs')).href);
const out = path.join(root, 'media/intro');
const scratch = path.join(root, '.build/intro-render', language);
const assets = path.join(root, '.build/intro-assets');
await mkdir(scratch, {recursive: true});
await mkdir(assets, {recursive: true});
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const sourceHashes = {};
sourceHashes['scripts/build_intro.mjs'] = hash(await readFile(fileURLToPath(import.meta.url)));
const runtimeHashes = {};
for (const file of execFileSync('git', ['ls-files', `${story.engine.path}/scripts`, `${story.engine.path}/package.json`, `${story.engine.path}/package-lock.json`, `${story.engine.path}/assets/fonts`], {cwd: engineRoot, encoding:'utf8', windowsHide:true}).trim().split('\n')) {
  runtimeHashes[file] = hash(await readFile(path.join(engineRoot, file)));
}

// Downsample only for the small video; full-resolution artwork stays in examples.
async function raster(relative, width) {
  const original = path.join(root, relative), digest = hash(await readFile(original));
  sourceHashes[relative] = digest;
  const cached = path.join(assets, `${digest}-${width}.png`);
  if (!await access(cached).then(() => true, () => false)) {
    await run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', original, '-vf', `scale=${width}:-1:flags=lanczos`, '-frames:v', '1', '-update', '1', '-map_metadata', '-1', cached]);
  }
  return 'data:image/png;base64,' + (await readFile(cached)).toString('base64');
}
const art = {
  cell: await raster('examples/cells/art/animal-cell.png', 720),
  icon: await raster('examples/cells/art/icon-microscope.png', 96),
  cells1: await raster('examples/cells/output/page-01.png', 450),
  cells2: await raster('examples/cells/output/page-02.png', 450),
  solar1: await raster('examples/solar-system/output/page-01.png', 450),
  solar2: await raster('examples/solar-system/output/page-02.png', 450)
};
const paper = '#FCF8EE', ink = '#192F2A', sage = '#668274';
const text = [];
function typeset(value, x, y, w, h, size, field, weight = 450, color = ink) {
  const result = textBox(value, {x,y,w,h}, {size, minSize: size, weight, color, field, lineHeight: 1.42});
  text.push({...result, svg: undefined});
  return result.svg;
}
const common = typeset(story.projectTitle, 83, 27, 470, 40, 20, 'project', 650)
  + typeset(story.repositoryLabel, 48, 495, 650, 30, 16, 'repository', 450, sage)
  + (story.sampleLanguage ? typeset(story.sampleLanguage, 718, 497, 194, 26, 13, 'sampleLanguage', 450, sage) : '');
const labels = story.scenes.map((s, i) => ({
  eyebrow: typeset(s.eyebrow, 48, 100, 408, 36, 18, `scene${i}.eyebrow`, 500, sage),
  title: typeset(s.title, 48, 148, 408, 154, language === 'en' ? 40 : 44, `scene${i}.title`, 700),
  body: s.body ? typeset(s.body, 48, 317, 408, 86, 22, `scene${i}.body`) : '',
  steps: (s.steps || []).map((line, j) => typeset(line, 83, 311 + j*43, 366, 36, 21, `scene${i}.step${j}`)),
  artLabel: s.artLabel ? typeset(s.artLabel, 489, 444, 423, 35, 20, `scene${i}.artlabel`) : '',
  artNote: s.artNote ? typeset(s.artNote, 492, 103, 150, 30, 18, `scene${i}.artnote`, 500, sage) : '',
  artLabels: (s.artLabels || []).map((line,j) => typeset(line, 503 + j*218, 428, 202, 32, 18, `scene${i}.artlabel${j}`)),
  cta: s.cta ? typeset(s.cta, 48, 426, 420, 36, 22, `scene${i}.cta`, 650) : ''
}));
const clamp = v => Math.max(0, Math.min(1, v));
const ease = v => 1 - Math.pow(1-clamp(v), 3);
const bitmap = (uri,x,y,w,h) => `<image x="${x}" y="${y}" width="${w}" height="${h}" href="${uri}"/>`;
function sheet(uri, x, y, w, rotation = 0) {
  const h = w*4/3;
  return `<g transform="rotate(${rotation} ${x+w/2} ${y+h/2})"><rect x="${x+4}" y="${y+6}" width="${w}" height="${h}" fill="#192F2A" opacity=".07"/><rect x="${x-1}" y="${y-1}" width="${w+2}" height="${h+2}" fill="#FCF8EE" stroke="#B8C7B4"/>${bitmap(uri,x,y,w,h)}</g>`;
}
function scene(index, local) {
  const s = labels[index];
  let body = s.eyebrow + s.title + s.body + s.cta;
  if (index === 0) {
    const reveal = ease(local/1.25), line = ease((local-1)/2.5);
    body += `<g transform="translate(${(1-reveal)*36} ${(1-reveal)*12})" opacity="${reveal}">${bitmap(art.cell,477,156,435,290)}</g>`;
    // This line leads to the nucleus in the supplied illustration.
    body += `<path d="M 492 135 L 543 135 L 642 275" fill="none" stroke="${sage}" stroke-width="1.4" stroke-dasharray="223" stroke-dashoffset="${(1-line)*223}"/>`;
    body += `<circle cx="642" cy="275" r="3" fill="${sage}" opacity="${line}"/>` + s.artLabel + s.artNote;
  } else if (index === 1) {
    const a = ease(local/.85), b = ease((local-.45)/.85);
    body += sheet(art.cells2, 704 + (1-b)*30, 159, 194, (1-b)*8);
    body += sheet(art.cells1, 488 + (1-a)*28, 105, 220, -(1-a)*7);
    body += s.artLabel;
    body += `<path d="M 62 333 V 416" fill="none" stroke="#C8DCC6" stroke-width="2"/>`;
    for (let j=0;j<3;j++) {
      const done = ease((local-j*.7)/.5);
      body += `<circle cx="62" cy="${326+j*43}" r="8" fill="${done>.5?'#D9BE64':'#FCF8EE'}" stroke="${sage}"/>` + s.steps[j];
      body += `<path d="M 59 ${326+j*43} l 2 2 l 4 -5" fill="none" stroke="${ink}" stroke-width="1.4" opacity="${done}"/>`;
    }
  } else {
    const a = ease(local/.9), b = ease((local-.25)/.9);
    body += sheet(art.solar2, 518, 124, 180, 4);
    body += sheet(art.solar1, 496-(1-a)*15, 150, 190, -(1-a)*8);
    body += sheet(art.cells2, 730, 150, 180, 5);
    body += sheet(art.cells1, 716+(1-b)*25, 173, 182, (1-b)*8);
    body += s.artLabels.join('');
    const underline = ease((local-1.3)/.8);
    body += `<path d="M 48 464 Q 207 460 330 464" fill="none" stroke="#D9BE64" stroke-width="3" stroke-dasharray="283" stroke-dashoffset="${(1-underline)*283}"/>`;
  }
  return body;
}
function frame(t, {guide=false}={}) {
  let body = `<rect width="960" height="540" fill="${paper}"/>` + common + bitmap(art.icon,48,20,25,40);
  body += `<line x1="48" y1="77" x2="912" y2="77" stroke="#C8D0BF"/>`;
  for (let i=0;i<story.scenes.length;i++) {
    const s = story.scenes[i];
    // Crossfades preserve each scene's own layers and measured layout.
    const opacity = i===0 ? clamp((s.to+.25-t)/.5) : Math.min(clamp((t-s.from+.25)/.5), i===2 ? 1 : clamp((s.to+.25-t)/.5));
    if (opacity>0) body += `<g opacity="${opacity}">${scene(i,Math.max(0,t-s.from))}</g>`;
  }
  body += `<line x1="48" y1="482" x2="912" y2="482" stroke="#DCE2D5"/><line x1="48" y1="482" x2="${48+864*clamp(t/story.duration)}" y2="482" stroke="${sage}" stroke-width="2"/>`;
  if (guide) body += '<rect x="36" y="18" width="888" height="507" fill="none" stroke="#9E382D" stroke-dasharray="5 5"/>';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">${body}</svg>`;
}
const composition = {story, frame, metadata:{width:960,height:540,text,safe:{left:.0375,right:.0375,top:.033,bottom:.0278},layout:'custom-original-art-and-page-layers',engine:story.engine}};
for (const [name,at] of [['scene-01',3.5],['scene-02',8],['scene-03',13],['transition-01',5],['transition-02',10]]) {
  await writeFile(path.join(scratch,name+'.png'),png(frame(at),960));
}
await writeFile(path.join(scratch,'safe.png'),png(frame(13,{guide:true}),960));
await writeFile(path.join(scratch,'layout.json'),JSON.stringify(composition.metadata,null,2)+'\n');
if (preview) {
  console.log(`Preview frames and measured text are in .build/intro-render/${language}.`);
} else {
  const report = await renderStory(story, {composition,width:960,height:540,out:scratch,fps:story.fps,formats:['mp4','png'],force:true,onProgress:console.log});
  await copyFile(path.join(scratch,'intro.mp4'),path.join(out,`intro${suffix}.mp4`));
  // A smaller GIF uses the same frame clock, without changing the composition.
  await run('ffmpeg', ['-hide_banner','-loglevel','error','-y','-i',path.join(out,`intro${suffix}.mp4`),'-filter_complex',`fps=${story.gifFps},scale=${story.gifWidth}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:reserve_transparent=0[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle`,'-loop','0','-an','-map_metadata','-1',path.join(out,`intro${suffix}.gif`)]);
  report.outputs.gif = await inspectVideo(path.join(out,`intro${suffix}.gif`), {width:story.gifWidth,height:story.height*story.gifWidth/story.width,duration:story.duration,fps:story.gifFps,gif:true});
  if (report.outputs.mp4.bytes>story.budgets.mp4Bytes || report.outputs.gif.bytes>story.budgets.gifBytes) throw new Error('Media exceeds the size budget in story.json.');
  await writeFile(path.join(out,`poster${suffix}.png`),png(frame(13),960));
  const version = (await readFile(path.join(root,'VERSION'),'utf8')).trim();
  const manifest = {version,language:story.language,engine:story.engine,runtimeHashes,storySha256:hash(await readFile(path.join(out,storyName))),sourceHashes,outputs:report.outputs,sampledFrames:report.sampledFrames,sampledUniqueFrames:report.sampledUniqueFrames,posterSha256:hash(await readFile(path.join(out,`poster${suffix}.png`))),budgets:story.budgets,platformPreviewVerified:false};
  await writeFile(path.join(out,`report${suffix}.json`),JSON.stringify(manifest,null,2)+'\n');
  console.log(JSON.stringify({mp4Bytes:report.outputs.mp4.bytes,gifBytes:report.outputs.gif.bytes,seconds:story.duration}));
}
