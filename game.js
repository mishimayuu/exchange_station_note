// ============================================================
//  ゲームの進行エンジン（物語は story.js に書いてあります）
// ============================================================
const $ = id => document.getElementById(id);
const SAVE_KEY = 'ekinote_save_v3';
const BLANK = '＿＿＿＿＿＿＿＿＿＿';

let S;                 // ゲームの状態
let ci = 0;            // 今の章
let Q = [];            // 今の章のノード列
let i = 0;             // 今のノード位置
let typing = false, timer = null, fullText = '', targetEl = null, curOpt = {};
let canAdvance = false;
const BG = { 'ホーム': 'platform', '教室': 'classroom', '自宅': 'home', '駅員室': 'office' };
function setBgFile(f) { $('bg').style.backgroundImage = `url(bg/${f}.svg)`; }
function setBg(name) {            // 場所ラベルから背景を選ぶ（古い書き方。bgノード推奨）
  const key = Object.keys(BG).find(k => name.includes(k));
  if (key) setBgFile(BG[key]);
}
let waitTimer = null, sfxTimer = null, audio = null;
function clearWait() { clearTimeout(waitTimer); waitTimer = null; }

// ---------- 効果音（音声ファイルなしで鳴らす簡易版） ----------
function ac() {
  try { audio = audio || new (window.AudioContext || window.webkitAudioContext)(); if (audio.state === 'suspended') audio.resume(); } catch (e) { audio = null; }
  return audio;
}
function playSound(kind, count) {
  const a = ac(); if (!a) return;
  const t0 = a.currentTime + .05;
  if (kind === 'steps') {                       // ざっ、ざっ
    for (let k = 0; k < (count || 6); k++) {
      const len = a.sampleRate * .12, buf = a.createBuffer(1, len, a.sampleRate), d = buf.getChannelData(0);
      for (let j = 0; j < len; j++) d[j] = (Math.random() * 2 - 1) * Math.pow(1 - j / len, 2.5);
      const src = a.createBufferSource(); src.buffer = buf;
      const f = a.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 900; f.Q.value = .7;
      const g = a.createGain(); g.gain.value = .35;
      src.connect(f); f.connect(g); g.connect(a.destination); src.start(t0 + k * .52);
    }
  } else if (kind === 'chime') {                // ピーンポーンパーン
    [[784, 0], [659, .5], [523, 1.0]].forEach(([hz, dt]) => {
      const o = a.createOscillator(), g = a.createGain(); o.type = 'sine'; o.frequency.value = hz;
      g.gain.setValueAtTime(.0001, t0 + dt); g.gain.exponentialRampToValueAtTime(.3, t0 + dt + .02);
      g.gain.exponentialRampToValueAtTime(.0001, t0 + dt + .6);
      o.connect(g); g.connect(a.destination); o.start(t0 + dt); o.stop(t0 + dt + .65);
    });
  }
}

// S.a    ... 返事の選択の記録。S.a['質問ID'] = 選んだ選択肢の v
// S.said ... 選んだ返事の文章そのもの。S.said['質問ID'] = 'ノートに書いた文'
// S.f    ... 自由に使えるフラグ置き場（{k:'do'} や e で書き込む）
const newState = () => ({ ch: 0, trust: 0, a: {}, said: {}, f: {}, done: {}, miss: 0 });
const T = x => (typeof x === 'function' ? x(S) : x);
const ok = o => !o.if || o.if(S);

// ---------- セーブ ----------
function save() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(S)); } catch (e) {} }
function loadSave() { try { return JSON.parse(localStorage.getItem(SAVE_KEY)); } catch (e) { return null; } }

// ---------- 開始 ----------
function start(state) {
  S = Object.assign(newState(), state || {});
  $('titleScreen').hidden = true;
  $('ending').hidden = true;
  $('topbar').hidden = false;
  startChapter(S.ch);
}

function startChapter(n) {
  ci = n; S.ch = n; save();
  const c = CHAPTERS[n];
  $('chTitle').textContent = c.title;
  $('stage').className = c.bg;
  $('fade').classList.remove('on'); $('bg').className = ''; $('sfx').textContent = '';
  if (c.img) setBgFile(c.img);
  Q = [{ k: 'title', x: c.title }, ...c.nodes];
  i = 0;
  render();
}

// ---------- 表示 ----------
function setView(v) {            // 'day'=文字枠 / 'note'=ノート / 'both'=両方 / 'none'=絵だけ
  $('dayBox').hidden = !(v === 'day' || v === 'both');
  $('notebook').hidden = !(v === 'note' || v === 'both');
  if (v === 'none') $('hint').textContent = '';
}
function clearChoices() { $('choices').innerHTML = ''; }
function addChoice(label, fn) {
  const b = document.createElement('button');
  b.textContent = label;
  b.onclick = e => { e.stopPropagation(); fn(); };
  $('choices').appendChild(b);
}

// 文字を1文字ずつ表示。opt.from: 途中から打ち始める位置 / opt.done: 打ち終わったあとの処理
function say(el, text, opt = {}) {
  clearTimeout(timer);
  fullText = text; targetEl = el; typing = true; canAdvance = false;
  curOpt = { advance: opt.advance !== false, done: opt.done };
  $('hint').textContent = '';
  let k = opt.from || 0;
  el.textContent = text.slice(0, k);
  if (text.length <= k) { finishTyping(); return; }
  // 1文字ごとの待ち時間。句読点・「‥」・改行では少し間を置く（opt.sp: 基本の速さ ms、opt.pm: 間の倍率）
  const sp = opt.sp || 34, pm = opt.pm == null ? 1 : opt.pm;
  const gap = c => '‥…'.includes(c) ? 150 * pm : '。！？'.includes(c) ? 260 * pm
    : c === '\n' ? 220 * pm : '、，'.includes(c) ? 110 * pm : 0;
  const tick = () => {
    k++; el.textContent = fullText.slice(0, k);
    if (k >= fullText.length) { finishTyping(); return; }
    timer = setTimeout(tick, sp + gap(fullText[k - 1]));
  };
  timer = setTimeout(tick, sp);
}
function finishTyping() {
  clearTimeout(timer);
  if (!typing) return;
  targetEl.textContent = fullText; typing = false;
  if (curOpt.done) curOpt.done();
  else if (curOpt.advance) { canAdvance = true; $('hint').textContent = 'クリック / Enter で次へ ▼'; }
}
function go() { i++; render(); }

// ---------- 返事を書く ----------
// parts = 文字列（先に書かれる文）と {id, o:[選択肢]}（空欄）を並べたもの。
// 文字列が先にあれば「途中まで書いてから選ぶ」、選択肢が先頭なら「いきなり選ぶ」になる。
function runReply(n) {
  const parts = (n.parts || [n.pre || '', { id: n.id, o: n.o }, n.post || '']).filter(p => p !== '');
  setView('note');
  $('paper').className = 'paper me';
  $('by').textContent = '私の返事';
  const finish = acc => {
    $('noteText').textContent = acc;
    $('by').textContent = '私の返事';
    canAdvance = true; $('hint').textContent = 'クリック / Enter で次へ ▼';
  };
  const step = (pi, acc) => {
    if (pi >= parts.length) { finish(acc); return; }
    const p = parts[pi];
    if (typeof p === 'string' || typeof p === 'function') {
      const full = acc + T(p);
      say($('noteText'), full, { sp: 30, pm: .8, from: acc.length, done: () => step(pi + 1, full) });
      return;
    }
    const opts = p.o.filter(ok);
    $('noteText').textContent = acc + BLANK;
    $('by').textContent = '私の返事（空欄を選ぼう）';
    $('hint').textContent = '';
    opts.forEach(o => {
      const label = T(o.l);
      addChoice(label, () => {
        clearChoices();
        if (p.id) { S.a[p.id] = o.v !== undefined ? o.v : label; S.said[p.id] = label; }
        if (o.e) o.e(S);
        step(pi + 1, acc + label);
      });
    });
  };
  step(0, '');
}

function render() {
  if (i >= Q.length) { ci + 1 < CHAPTERS.length ? startChapter(ci + 1) : showEnding(); return; }
  const n = Q[i];
  clearChoices(); canAdvance = false; clearWait();

  switch (n.k) {
    case 'title':
      setView('day'); $('who').textContent = ''; $('loc').textContent = '';
      say($('dayText'), n.x);
      break;
    case 'loc':
      $('loc').textContent = n.x; setBg(n.x); go(); break;
    case 'bg':                       // 背景を変える。fx:'shake' で画面を揺らす
      setBgFile(n.x); $('bg').className = n.fx || ''; $('sfx').textContent = ''; go(); break;
    case 'sfx':                      // 効果音。t=画面に出す擬音の文字 / snd='steps'|'chime' / count=足音の回数
      clearTimeout(sfxTimer);
      $('sfx').textContent = n.t || '';
      if (n.snd) playSound(n.snd, n.count);
      if (n.t) sfxTimer = setTimeout(() => { $('sfx').textContent = ''; }, n.ms || 3500);
      go(); break;
    case 'wait':                     // t ミリ秒、絵だけ見せる（クリックで飛ばせる）
      setView('none'); waitTimer = setTimeout(go, n.t || 2000); break;
    case 'fade':                     // ゆっくり暗転
      setView('none'); $('fade').style.transitionDuration = (n.t || 3000) + 'ms';
      $('fade').classList.add('on'); waitTimer = setTimeout(go, (n.t || 3000) + 600); break;
    case 'do':                       // 状態を書き換えるだけ（画面には出ない）
      n.e(S); go(); break;
    case 'if': {                     // 過去の返事などで場面を分ける
      const list = (n.c(S) ? n.t : n.f) || [];
      Q.splice(i + 1, 0, ...list);
      go(); break;
    }
    case 'n':
    case 's':
      if (n.cover) {                 // ノートの表紙を見せながら話す
        setView('both'); $('paper').className = 'paper cover'; $('by').textContent = ''; $('noteText').textContent = n.cover;
      } else setView('day');
      $('who').textContent = n.k === 's' ? n.w : '';
      say($('dayText'), T(n.x), n.k === 'n' ? { sp: 48, pm: 1.2 } : { sp: 38 });
      break;
    case 'p':
    case 'me':
      setView('note');
      $('paper').className = 'paper ' + (n.k === 'p' ? 'partner' : 'me');
      $('by').textContent = n.by || (n.k === 'p' ? '相手からのノート' : '私の返事');
      say($('noteText'), T(n.x), { sp: 30, pm: .8 });
      break;
    case 'r':
      runReply(n); break;
    case 'menu': {
      const rest = n.o.filter(o => !S.done[o.id] && ok(o));
      if (!rest.length) { go(); break; }
      setView('day'); $('who').textContent = '';
      $('dayText').textContent = T(n.x);
      $('hint').textContent = '';
      rest.forEach(o => addChoice(T(o.l), () => {
        S.done[o.id] = 1;
        Q.splice(i + 1, 0, ...o.n, n);   // 会話のあと、同じ選択肢に戻る
        i++; render();
      }));
      break;
    }
    case 'guess':
      setView('day'); $('who').textContent = '';
      $('dayText').textContent = T(n.x);
      $('hint').textContent = '';
      n.o.forEach(o => addChoice(T(o.l), () => {
        if (o.ok) { go(); return; }
        S.miss++;
        Q.splice(i + 1, 0,
          { k: 'n', x: o.hint },
          { k: 'n', x: '……何かが違う。これまでのノートを思い出してみよう。' },
          { ...n, o: n.o.filter(x => x !== o) });
        i++; render();
      }));
      break;
    case 'ending':
      showEnding(n); break;
  }
}

function advance() {
  if (typing) { finishTyping(); return; }
  if (waitTimer) { clearWait(); go(); return; }
  if (canAdvance) { canAdvance = false; go(); }
}

// ---------- エンディング ----------
function showEnding(n = {}) {
  try { localStorage.removeItem(SAVE_KEY); } catch (e) {}
  $('endTitle').textContent = n.title || 'おわり';
  $('endName').textContent = n.x || '';
  $('endStats').innerHTML = n.stats ? T(n.stats) : '';
  $('ending').hidden = false;
}

// ---------- イベント ----------
$('stage').addEventListener('click', advance);
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') { if (!$('titleScreen').hidden) return; e.preventDefault(); advance(); }
});
$('newBtn').onclick = () => start(newState());
$('contBtn').onclick = () => start(loadSave());
$('retryBtn').onclick = () => start(newState());

(function init() {
  const sv = loadSave();
  if (sv && typeof sv.ch === 'number') $('contBtn').hidden = false;
})();
