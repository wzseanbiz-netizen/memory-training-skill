# -*- coding: utf-8 -*-
"""从 data.py 生成手机/电脑通用的单文件网页版记忆训练应用。"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

D = {
    "digitCodes": {str(k): v for k, v in data.DIGIT_CODES.items()},
    "wordBank": data.WORD_BANK,
    "poems": data.POEMS,
    "texts": data.SHORT_TEXTS,
    "letterCodes": data.LETTER_CODES,
    "comboCodes": data.COMBO_CODES,
    "wordMethods": data.WORD_METHODS,
    "methodsOverview": data.METHODS_OVERVIEW,
    "leftBrain": data.LEFT_BRAIN,
    "rightBrain": data.RIGHT_BRAIN,
    "memoryCompare": data.MEMORY_COMPARE,
    "twoSteps": data.TWO_STEPS,
    "fiveAbilities": data.FIVE_ABILITIES,
    "chainRules": data.CHAIN_RULES,
    "chainNotes": data.CHAIN_NOTES,
    "associationMethods": data.ASSOCIATION_METHODS,
    "abstractMethods": data.ABSTRACT_METHODS,
    "assocPractice": data.ASSOC_PRACTICE,
    "palaceDef": data.PALACE_DEF,
    "palaceRules": data.PALACE_RULES,
    "palacePreset": data.PALACE_PRESET,
    "poemSteps": data.POEM_STEPS,
    "strategies36": data.STRATEGIES_36,
    "strategyLink": data.STRATEGY_LINK,
    "serialWords": data.SERIAL_WORDS,
    "memoryTestWords": data.MEMORY_TEST_WORDS,
    "pi50": data.PI_50,
    "readPractice": data.READ_PRACTICE,
    "focusNotes": data.FOCUS_NOTES,
    "listenText1": data.LISTEN_TEXT_1,
    "listenText2": data.LISTEN_TEXT_2,
}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #f2f4f8; color: #243044; line-height: 1.6; padding-bottom: 40px;
}
header {
  background: #24406e; color: #fff; padding: 14px 16px; position: sticky; top: 0; z-index: 20;
}
header h1 { font-size: 18px; font-weight: 700; }
header p { font-size: 12px; opacity: .85; }
nav {
  display: flex; gap: 6px; padding: 10px 12px; overflow-x: auto; background: #fff;
  border-bottom: 1px solid #dfe4ee; position: sticky; top: 0; z-index: 19;
}
nav button {
  white-space: nowrap; border: 1px solid #dfe4ee; background: #fff; color: #24406e;
  padding: 8px 14px; border-radius: 8px; font-size: 14px; cursor: pointer;
}
nav button.active { background: #24406e; color: #fff; border-color: #24406e; }
main { padding: 14px 12px; max-width: 900px; margin: 0 auto; }
.card {
  background: #fff; border: 1px solid #e2e8f2; border-radius: 10px; padding: 14px;
  margin-bottom: 14px;
}
h2 { font-size: 17px; color: #24406e; margin-bottom: 8px; }
h3 { font-size: 15px; color: #24406e; margin: 10px 0 6px; }
.muted { color: #6b7688; font-size: 13px; }
.tip { color: #1a6b3c; font-size: 13px; margin-top: 6px; }
.warn { color: #8a4b00; font-size: 13px; margin-top: 6px; }
.err { color: #b00000; font-size: 13px; margin-top: 6px; }
.big { font-size: 22px; font-weight: 700; text-align: center; color: #24406e; margin: 10px 0; }
.q { font-size: 20px; font-weight: 700; text-align: center; color: #24406e; margin: 10px 0; word-break: break-word; }
button.act {
  background: #24406e; color: #fff; border: none; border-radius: 8px; padding: 10px 16px;
  font-size: 14px; cursor: pointer; margin: 4px 4px 4px 0;
}
button.act:active { opacity: .8; }
button.ghost {
  background: #fff; color: #24406e; border: 1px solid #c9d3e6; border-radius: 8px;
  padding: 10px 16px; font-size: 14px; cursor: pointer; margin: 4px 4px 4px 0;
}
button.green { background: #1a6b3c; color: #fff; border: none; border-radius: 8px; padding: 10px 16px; font-size: 14px; cursor: pointer; margin: 4px 4px 4px 0; }
button.red { background: #b00000; color: #fff; border: none; border-radius: 8px; padding: 10px 16px; font-size: 14px; cursor: pointer; margin: 4px 4px 4px 0; }
input, select {
  width: 100%; padding: 10px 12px; border: 1px solid #c9d3e6; border-radius: 8px;
  font-size: 15px; margin: 6px 0; background: #fff;
}
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)); gap: 6px; }
.grid .cell {
  background: #eef2fa; border: 1px solid #d5deef; border-radius: 8px; padding: 8px 4px;
  text-align: center; font-size: 13px;
}
.grid .cell.done { background: #1a6b3c; color: #fff; border-color: #1a6b3c; }
.grid .cell.err { background: #fde3e3; border-color: #b00000; }
.cellbtn {
  background: #eef2fa; border: 1px solid #d5deef; border-radius: 8px; padding: 12px 6px;
  font-size: 14px; cursor: pointer; min-height: 44px;
}
.cellbtn.done { background: #1a6b3c; color: #fff; border-color: #1a6b3c; }
.row { display: flex; flex-wrap: wrap; gap: 6px; }
.list { max-height: 260px; overflow: auto; border: 1px solid #e2e8f2; border-radius: 8px; }
.list div { padding: 8px 10px; border-bottom: 1px solid #eef2fa; font-size: 14px; cursor: pointer; }
.list div:active { background: #eef2fa; }
.poem-lines { white-space: pre-wrap; font-size: 16px; font-weight: 600; }
.para { white-space: pre-wrap; margin: 6px 0; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { border: 1px solid #dfe4ee; padding: 6px 8px; text-align: left; }
th { background: #eef2fa; }
.scroll { max-height: 300px; overflow: auto; }
.home-entry {
  display: block; background: #fff; border: 1px solid #e2e8f2; border-radius: 10px;
  padding: 14px; margin-bottom: 10px; cursor: pointer; text-decoration: none; color: inherit;
}
.home-entry b { color: #24406e; font-size: 16px; }
.home-entry span { display: block; color: #6b7688; font-size: 13px; margin-top: 4px; }
@media (max-width: 480px) {
  header h1 { font-size: 16px; }
  .q { font-size: 18px; }
  .grid { grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); }
}
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-thumb { background: #c9d3e6; border-radius: 3px; }
::-webkit-scrollbar-track { background: transparent; }
.badge {
  display: inline-block; background: #eef2fa; color: #24406e; border-radius: 20px;
  padding: 2px 10px; font-size: 12px; margin-right: 6px;
}
.stat-card { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eef2fa; }
.about p { margin: 8px 0; }
.about ul { margin: 8px 0 8px 20px; }
.about li { margin: 4px 0; }
.home-entry:active, .card button:active { transform: scale(.98); }
"""

HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#24406e">
<meta name="description" content="记数字、记单词、记古诗词、记短文的记忆训练工具，手机电脑通用，无需联网">
<title>记忆法训练助手</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<style>__CSS__</style>
</head>
<body>
<header>
  <h1>记忆法训练助手</h1>
  <p>记数字 · 记单词 · 记古诗词 · 记短文 —— 手机电脑通用 · 离线可用 · 可商用部署</p>
</header>
<nav id="nav"></nav>
<main id="main"></main>
<script>
const D = __DATA__;
"""

print("build_web.py 第一块完成")

JS = r'''
// ---------- 基础工具 ----------
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function loadStats() {
  try { return JSON.parse(localStorage.getItem('mjStats') || '{}'); }
  catch (e) { return {}; }
}
function saveStats(s) { localStorage.setItem('mjStats', JSON.stringify(s)); }
function loadReview() {
  try { return JSON.parse(localStorage.getItem('mjReview') || '[]'); }
  catch (e) { return []; }
}
function saveReview(r) { localStorage.setItem('mjReview', JSON.stringify(r)); }
function record(mod, ok) {
  const s = loadStats();
  s[mod] = s[mod] || { n: 0, ok: 0 };
  s[mod].n += 1;
  if (ok) s[mod].ok += 1;
  saveStats(s);
}

// ---------- 导航 ----------
const PAGES = [
  ['首页', 'home'], ['记数字', 'digit'], ['记单词', 'word'], ['记古诗词', 'poem'],
  ['记短文', 'text'], ['记忆方法', 'method'], ['专注力', 'focus'], ['统计', 'stats'],
  ['关于', 'about']
];
function show(name) {
  $('nav').innerHTML = PAGES.map(p =>
    `<button class="${p[0] === name ? 'active' : ''}" onclick="show('${p[1]}')">${p[0]}</button>`).join('');
  const fns = { home, digit, word, poem, text, method, focus, stats, about };
  $('main').innerHTML = fns[name]();
}

// ---------- 首页 ----------
function home() {
  const total = Object.values(D.wordBank).reduce((a, b) => a + b.length, 0);
  return `
  <div class="card"><h2>四大练习（点击进入）</h2>
    <a class="home-entry" onclick="show('digit')"><b>记数字</b><span>数字编码 1-100、数字串记忆、读数练习、圆周率 50 位</span></a>
    <a class="home-entry" onclick="show('word')"><b>记单词</b><span>小学 / 初中 / 高中共 ${total} 词，看词忆义、看义忆词，每词带记忆提示</span></a>
    <a class="home-entry" onclick="show('poem')"><b>记古诗词</b><span>${D.poems.length} 首经典古诗，画图记忆法 + 逐句背诵自测</span></a>
    <a class="home-entry" onclick="show('text')"><b>记短文</b><span>${D.texts.length} 篇经典短文，关键词提取 + 分段记忆练习</span></a>
  </div>
  <div class="card"><h2>记忆原理（高效记忆两大步骤）</h2>
    <p class="muted">${D.twoSteps.join(' → ')}</p>
    <p class="muted">先把要记的内容转成具体图像，再让图像像锁链一样两两相连、顺序不乱。</p>
    <p class="muted">右脑图像记忆的短时容量远大于声音记忆，记忆效率可提升百倍。</p>
  </div>`;
}

// ---------- 记数字 ----------
const ds = {};
function digit() {
  const codes = Object.entries(D.digitCodes)
    .map(([k, v]) => `<div class="cell">${esc(k === '0' ? '00' : k)}·${esc(v)}</div>`).join('');
  return `
  <div class="card"><h2>一、数字编码表（1-100）</h2>
    <p class="muted">记数字第一步：把数字转成固定图像，再串联记忆。</p>
    <div class="grid">${codes}</div>
  </div>
  <div class="card"><h2>二、数字串记忆练习</h2>
    <select id="dLen" onchange="digitNew()">
      <option value="5">5 位数字</option><option value="8" selected>8 位数字</option>
      <option value="10">10 位数字</option><option value="12">12 位数字</option>
    </select>
    <div class="q" id="dQ">点击“生成数字串”开始</div>
    <div class="row">
      <button class="act" onclick="digitNew()">生成数字串</button>
      <button class="ghost" onclick="digitHint()">显示编码提示</button>
      <button class="ghost" onclick="digitHide()">隐藏，开始回忆</button>
      <button class="green" onclick="digitCheck()">核对答案</button>
    </div>
    <input id="dAns" placeholder="先按编码转图像串联，再输入回忆的数字串">
    <div class="tip" id="dTip"></div>
  </div>
  <div class="card"><h2>三、读数练习</h2>
    <select id="rSel" onchange="readShow()">${D.readPractice.map((s, i) =>
      `<option value="${i}">第 ${i + 1} 组</option>`).join('')}</select>
    <div class="q" id="rShow"></div>
    <div class="row">
      <button class="act" onclick="readShow()">显示数字串</button>
      <button class="ghost" onclick="readHide()">隐藏，开始自测</button>
    </div>
  </div>
  <div class="card"><h2>四、圆周率 50 位</h2>
    <p class="muted">用数字编码把圆周率转成图像，一串一串地记。</p>
    <div class="big" style="font-size:18px;font-weight:700">${esc(D.pi50)}</div>
  </div>`;
}
function digitNew() {
  const len = +$('dLen').value;
  let s = '';
  for (let i = 0; i < len; i++) s += Math.floor(Math.random() * 10);
  ds.cur = s;
  $('dQ').textContent = '数字串：' + s + '\n（把每个数字转成编码图像，像锁链一样串起来）';
  $('dAns').value = '';
  $('dTip').textContent = '';
  $('dTip').className = 'tip';
}
function digitHint() {
  if (!ds.cur) return;
  const enc = [...ds.cur].map(c => c + '→' + D.digitCodes[c]).join('　');
  $('dTip').textContent = '编码提示：' + enc;
  $('dTip').className = 'warn';
}
function digitHide() { if (ds.cur) $('dQ').textContent = '（已隐藏，按串联画面回忆数字串）'; }
function digitCheck() {
  if (!ds.cur) return;
  const ans = ($('dAns').value || '').replace(/\s/g, '');
  const ok = ans === ds.cur;
  record('记数字', ok);
  $('dTip').textContent = (ok ? '回忆正确！' : '再练一次') + '　（正确答案：' + ds.cur + '）';
  $('dTip').className = ok ? 'tip' : 'err';
}
function readShow() { $('rShow').textContent = D.readPractice[$('rSel').value]; }
function readHide() { $('rShow').textContent = '（已隐藏，凭记忆按数字编码读出来）'; }

// ---------- 记单词 ----------
const ws = {};
function word() {
  const levels = Object.keys(D.wordBank);
  return `
  <div class="card"><h2>一、单词记忆练习（看词忆义 / 看义忆词）</h2>
    <div class="row">
      <select id="wLevel" onchange="wordRefresh()">${levels.map((l, i) =>
        `<option value="${i}"${i === 0 ? ' selected' : ''}>${l}</option>`).join('')}</select>
      <select id="wMode" onchange="wordNew()">
        <option value="0">看词忆义（显示单词，回忆释义）</option>
        <option value="1">看义忆词（显示释义，回忆单词）</option>
      </select>
    </div>
    <div class="q" id="wQ">点击“出题”开始</div>
    <div class="row">
      <button class="act" onclick="wordNew()">出题</button>
      <button class="ghost" onclick="wordMeaning()">显示释义</button>
      <button class="ghost" onclick="wordSubmit()">提交单词</button>
      <button class="ghost" onclick="wordTip()">看记忆提示</button>
    </div>
    <input id="wAns" placeholder="看义忆词模式：输入回忆的单词">
    <div class="row">
      <button class="green" onclick="wordGrade(true)">记得</button>
      <button class="red" onclick="wordGrade(false)">再记</button>
    </div>
    <div class="tip" id="wTip"></div>
  </div>
  <div class="card"><h2>二、单词库浏览（点击单词看记忆提示）</h2>
    <div class="list" id="wList"></div>
  </div>`;
}
function wordRefresh() {
  const lv = Object.keys(D.wordBank)[$('wLevel').value];
  const list = D.wordBank[lv];
  $('wList').innerHTML = list.map((w, i) =>
    `<div data-tip="${esc(w[4])}" onclick="wTipShow(this)"><b>${esc(w[0])}</b>　${esc(w[1])}　${esc(w[2])}　${esc(w[3])}</div>`).join('');
}
function wTipShow(el) {
  $('wTip').textContent = '记忆提示：' + el.dataset.tip;
  $('wTip').className = 'tip';
}
function wordNew() {
  const lv = Object.keys(D.wordBank)[$('wLevel').value];
  const list = D.wordBank[lv];
  const review = loadReview().filter(x => x[0] && list.some(w => w[0] === x[0]));
  const pool = review.length ? review : list;
  ws.cur = pool[Math.floor(Math.random() * pool.length)];
  const [w, ph, pos, meaning] = ws.cur;
  if ($('wMode').value === '0') $('wQ').textContent = w + '　' + ph + '　' + pos;
  else $('wQ').textContent = pos + '　' + meaning;
  $('wAns').value = '';
  $('wTip').textContent = '';
  $('wTip').className = 'tip';
}
function wordMeaning() {
  if (!ws.cur) return;
  const [w, ph, pos, meaning, tip] = ws.cur;
  $('wTip').textContent = '释义：' + pos + '　' + meaning + '　【记忆提示：' + tip + '】';
  $('wTip').className = 'tip';
}
function wordTip() {
  if (!ws.cur) return;
  $('wTip').textContent = '记忆提示：' + ws.cur[4];
  $('wTip').className = 'warn';
}
function wordSubmit() {
  if (!ws.cur) return;
  const ans = ($('wAns').value || '').trim().toLowerCase();
  const ok = ans === ws.cur[0].toLowerCase();
  $('wTip').textContent = (ok ? '答对了！' : '再记一次') + '　（正确单词：' + ws.cur[0] + '）';
  $('wTip').className = ok ? 'tip' : 'err';
}
function wordGrade(ok) {
  if (!ws.cur) return;
  record('记单词', ok);
  let r = loadReview();
  if (!ok) {
    if (!r.some(x => x[0] === ws.cur[0])) r.push(ws.cur);
  } else {
    r = r.filter(x => x[0] !== ws.cur[0]);
  }
  saveReview(r);
  $('wTip').textContent = (ok ? '已记为：记得' : '已记为：再记（已加入复习）') + '　（单词：' + ws.cur[0] + '）';
  $('wTip').className = ok ? 'tip' : 'err';
}

// ---------- 记古诗词 ----------
function poem() {
  return `
  <div class="card"><h2>一、画图记忆法</h2>
    <p class="muted">四步：${D.poemSteps.join(' → ')}。读通理解后，把每句诗提取成图像画在脑中，再闭目按图回忆。</p>
  </div>
  <div class="card"><h2>二、古诗库（${D.poems.length} 首，选一首查看与背诵）</h2>
    <select id="pSel" onchange="poemShow()">${D.poems.map((p, i) =>
      `<option value="${i}">${esc(p.title)}（${esc(p.author)}）</option>`).join('')}</select>
    <div class="row" style="margin-top:8px">
      <button class="act" onclick="poemShow()">原文 / 译文 / 图解</button>
      <button class="green" onclick="poemQuiz()">背诵自测</button>
      <button class="ghost" onclick="poemCheck()">显示原文核对</button>
      <button class="green" onclick="poemGrade(true)">记得</button>
      <button class="red" onclick="poemGrade(false)">再记</button>
    </div>
    <div class="poem-lines" id="pBody" style="margin-top:10px"></div>
    <div class="tip" id="pTip"></div>
  </div>`;
}
function poemShow() {
  const p = D.poems[$('pSel').value];
  let html = '《' + p.title + '》　' + p.author + '\n' + p.lines;
  if (p.translation) html += '\n\n【译文】' + p.translation;
  if (p.notes) html += '\n\n【注释】' + p.notes;
  if (p.image_hint) html += '\n\n【图解提示】' + p.image_hint;
  $('pBody').textContent = html;
  $('pTip').textContent = '';
  $('pTip').className = 'tip';
}
function poemQuiz() {
  const p = D.poems[$('pSel').value];
  const hints = p.lines.split('\n').map(l => (l.length > 2 ? l.slice(0, 2) + '……' : l));
  $('pBody').textContent = '《' + p.title + '》自测：先想图，再回忆每句\n\n' + hints.join('\n');
  $('pTip').textContent = '先通读理解，再在脑海中把每句画成图，最后闭目回忆。';
  $('pTip').className = 'warn';
}
function poemCheck() {
  const p = D.poems[$('pSel').value];
  $('pBody').textContent = '《' + p.title + '》原文核对\n\n' + p.lines;
  $('pTip').textContent = '核对后请自评：记得 / 再记。';
  $('pTip').className = 'tip';
}
function poemGrade(ok) {
  const p = D.poems[$('pSel').value];
  record('记古诗', ok);
  $('pTip').textContent = (ok ? '已记为：记得' : '已记为：再记') + '　《' + p.title + '》';
  $('pTip').className = ok ? 'tip' : 'err';
}

// ---------- 记短文 ----------
const ts = { idx: 0 };
function text() {
  return `
  <div class="card"><h2>一、记忆短文（${D.texts.length} 篇）</h2>
    <select id="tSel" onchange="textShowAll()">${D.texts.map((t, i) =>
      `<option value="${i}">${esc(t.title)}（${esc(t.author)}）</option>`).join('')}</select>
    <div class="warn" id="tTipBox" style="margin-top:8px"></div>
    <p class="tip" style="margin-top:6px"><b>关键词：</b><span id="tKeys"></span></p>
  </div>
  <div class="card"><h2>二、正文与分段练习</h2>
    <div class="scroll"><div id="tBody" class="para"></div></div>
    <div class="row" style="margin-top:8px">
      <button class="act" onclick="textShowAll()">显示全文</button>
      <button class="ghost" onclick="textQuiz()">开始自测（只看关键词）</button>
      <button class="ghost" onclick="textPara()">逐段核对</button>
      <button class="green" onclick="textGrade(true)">记得</button>
      <button class="red" onclick="textGrade(false)">再记</button>
    </div>
    <div class="tip" id="tTip2"></div>
  </div>`;
}
function textShowAll() {
  const t = D.texts[$('tSel').value];
  ts.idx = 0;
  $('tTipBox').textContent = '【记忆提示】' + t.tip;
  $('tKeys').textContent = t.keywords.join('　→　');
  $('tBody').textContent = t.paragraphs.map((p, i) => (i + 1) + '、' + p).join('\n\n');
  $('tTip2').textContent = '';
  $('tTip2').className = 'tip';
}
function textQuiz() {
  ts.idx = 0;
  $('tBody').textContent = '（已隐藏正文，先看关键词，在脑中逐段回忆，再点“逐段核对”）';
  $('tTip2').textContent = '先在脑中把关键词串成画面，回忆每段内容。';
  $('tTip2').className = 'warn';
}
function textPara() {
  const t = D.texts[$('tSel').value];
  if (ts.idx >= t.paragraphs.length) {
    $('tTip2').textContent = '已全部核对。点“显示全文”可再次通读。';
    $('tTip2').className = 'tip';
    return;
  }
  $('tBody').textContent = '第 ' + (ts.idx + 1) + ' 段：' + t.paragraphs[ts.idx];
  ts.idx += 1;
  record('记短文');
  $('tTip2').textContent = '已核对第 ' + ts.idx + ' 段，继续回忆下一段。';
  $('tTip2').className = 'tip';
}
function textGrade(ok) {
  const t = D.texts[$('tSel').value];
  record('记短文', ok);
  $('tTip2').textContent = (ok ? '已记为：记得' : '已记为：再记') + '　《' + t.title + '》';
  $('tTip2').className = ok ? 'tip' : 'err';
}

// ---------- 记忆方法 ----------
function tbl3(rows) {
  const heads = ['方法', '示例', '要领'];
  const trs = rows.map(r => '<tr>' + r.map(c => '<td>' + esc(c) + '</td>').join('') + '</tr>').join('');
  return '<table><tr>' + heads.map(h => '<th>' + h + '</th>').join('') + '</tr>' + trs + '</table>';
}
function tbl4(rows, heads) {
  const trs = rows.map(r => '<tr>' + r.map(c => '<td>' + esc(c) + '</td>').join('') + '</tr>').join('');
  return '<table><tr>' + heads.map(h => '<th>' + h + '</th>').join('') + '</tr>' + trs + '</table>';
}
function method() {
  const overview = D.methodsOverview.map(m =>
    `<div class="cell" style="text-align:left;padding:8px"><b>${esc(m[0])}</b><br><span class="muted">${esc(m[1])}</span></div>`).join('');
  const chain = `<p class="muted">定义：将资料转化成图像，像锁链一样一个接一个地连接起来，顺序不乱地记录下来。</p>
    <p class="muted">规则：${D.chainRules.join('；')}</p>
    <h3>注意要点</h3>
    <ul>${D.chainNotes.map(n => '<li class="muted">' + esc(n) + '</li>').join('')}</ul>`;
  const palace = `<p class="muted">${esc(D.palaceDef)}</p>
    <p class="muted">选取规则：${D.palaceRules.join('；')}</p>
    <p class="muted">家里：${D.palacePreset['家里'].join('、')}</p>
    <p class="muted">教室：${D.palacePreset['教室'].join('、')}</p>`;
  const s36 = `<div class="grid">${D.strategies36.map((s, i) =>
    `<div class="cell">${i + 1}·${esc(s)}</div>`).join('')}</div>`;
  return `
  <div class="card"><h2>一、记忆方法总览</h2><div class="grid">${overview}</div></div>
  <div class="card"><h2>二、锁链奇像法（串联联想）</h2>${chain}</div>
  <div class="card"><h2>三、对应联想五法</h2>${tbl3(D.associationMethods)}</div>
  <div class="card"><h2>四、抽象转具象（口诀：提鞋赠刀王）</h2>${tbl4(D.abstractMethods, ['方法', '抽象词', '具象图像', '说明'])}</div>
  <div class="card"><h2>五、记忆宫殿（地点桩）</h2>${palace}</div>
  <div class="card"><h2>六、三十六计</h2>${s36}
    <h3>前 12 计数字编码联想</h3>${tbl4(D.strategyLink, ['数字', '编码', '计名', '联想'])}
  </div>`;
}

// ---------- 专注力 ----------
const sh = { seq: [], expected: 1, start: 0 };
function focus() {
  return `
  <div class="card"><h2>专注力训练说明</h2>
    ${D.focusNotes.map(n => '<p class="muted"><b>' + esc(n[0]) + '：</b>' + esc(n[1]) + '</p>').join('')}
  </div>
  <div class="card"><h2>舒尔特方格（5×5）</h2>
    <div class="grid" id="shGrid" style="grid-template-columns:repeat(5,1fr)"></div>
    <div class="tip" id="shTip"></div>
    <div class="row" style="margin-top:8px">
      <button class="act" onclick="shulteStart()">开始</button>
      <button class="ghost" onclick="shulteReset()">重置</button>
    </div>
  </div>
  <div class="card"><h2>数数拍手（听到指定数字就拍手）</h2>
    <select id="clTarget">
      <option value="0">2、4、7</option><option value="1">3、6、9</option>
      <option value="2">1、4、7</option><option value="3">5、7、9</option>
    </select>
    <div class="big" id="clNum">点击“开始”训练</div>
    <div class="row">
      <button class="green" onclick="clapDo()">拍手</button>
      <button class="act" onclick="clapStart()">开始</button>
      <button class="ghost" onclick="clapReset()">重置</button>
    </div>
    <div class="tip" id="clTip"></div>
  </div>
  <div class="card"><h2>16 词记忆测试（按顺序点击）</h2>
    <div class="grid" id="memGrid" style="grid-template-columns:repeat(4,1fr)"></div>
    <div class="tip" id="memTip"></div>
    <div class="row" style="margin-top:8px">
      <button class="act" onclick="memStart()">开始回忆</button>
      <button class="ghost" onclick="memReset()">重置</button>
    </div>
  </div>
  <div class="card"><h2>听字训练（数一数指定字出现几次）</h2>
    <div class="scroll"><div class="para" id="listenText">${esc(D.listenText1)}</div></div>
    <div class="row" style="margin-top:8px">
      <button class="act" onclick="listenSet(0)">第 1 段（数“红”）</button>
      <button class="act" onclick="listenSet(1)">第 2 段（数“红”）</button>
    </div>
  </div>`;
}
function shulteReset() {
  sh.expected = 1;
  $('shGrid').innerHTML = Array.from({ length: 25 }, () => '<div class="cellbtn"></div>').join('');
  $('shTip').textContent = '';
}
function shulteStart() {
  shulteReset();
  sh.seq = Array.from({ length: 25 }, (_, i) => i + 1);
  for (let i = sh.seq.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [sh.seq[i], sh.seq[j]] = [sh.seq[j], sh.seq[i]];
  }
  $('shGrid').innerHTML = sh.seq.map(n =>
    `<div class="cellbtn" onclick="shulteClick(this)">${n}</div>`).join('');
  sh.start = Date.now();
  $('shTip').textContent = '按 1→25 的顺序依次点击。';
  $('shTip').className = 'tip';
}
function shulteClick(cell) {
  if (sh.expected > 25) return;
  const n = parseInt(cell.textContent, 10);
  if (n === sh.expected) {
    sh.expected += 1;
    cell.className = 'cellbtn done';
    cell.textContent = '✓';
    cell.onclick = null;
    if (sh.expected === 26) {
      const t = ((Date.now() - sh.start) / 1000).toFixed(1);
      record('舒尔特', true);
      $('shTip').textContent = '完成！用时 ' + t + ' 秒（越短越专注）';
      $('shTip').className = 'tip';
    }
  } else {
    $('shTip').textContent = '点错了，从 1 开始按顺序点。';
    $('shTip').className = 'err';
  }
}

const cl = { seq: [], idx: 0, timer: null, right: 0, miss: 0, wrong: 0, curTarget: false, prevTarget: false };
function clapReset() {
  if (cl.timer) { clearInterval(cl.timer); cl.timer = null; }
  cl.idx = 0; cl.right = 0; cl.miss = 0; cl.wrong = 0;
  cl.curTarget = false; cl.prevTarget = false;
  $('clNum').textContent = '点击“开始”训练';
  $('clTip').textContent = '';
}
function clapStart() {
  clapReset();
  cl.seq = Array.from({ length: 30 }, (_, i) => i + 1);
  cl.timer = setInterval(clapNext, 1000);
}
function clapNext() {
  if (cl.idx >= cl.seq.length) {
    clearInterval(cl.timer); cl.timer = null;
    record('拍手训练', cl.right >= 8);
    $('clNum').textContent = '完成！';
    $('clTip').textContent = '正确拍手 ' + cl.right + ' 次，漏拍 ' + cl.miss + ' 次，误拍 ' + cl.wrong + ' 次。';
    $('clTip').className = 'tip';
    return;
  }
  const num = cl.seq[cl.idx];
  const sets = { 0: [2, 4, 7], 1: [3, 6, 9], 2: [1, 4, 7], 3: [5, 7, 9] };
  const tset = new Set(sets[+$('clTarget').value]);
  if (cl.prevTarget) cl.miss += 1;
  $('clNum').textContent = '数字：' + num;
  cl.curTarget = tset.has(num);
  cl.prevTarget = cl.curTarget;
  cl.idx += 1;
}
function clapDo() {
  if (cl.timer === null) { $('clTip').textContent = '先点击“开始”。'; return; }
  if (cl.curTarget) {
    cl.right += 1; cl.prevTarget = false;
    $('clTip').textContent = '拍得对！'; $('clTip').className = 'tip';
  } else {
    cl.wrong += 1;
    $('clTip').textContent = '这个数字不用拍手。'; $('clTip').className = 'err';
  }
}

const mem = { pos: 0, start: 0 };
function memReset() {
  mem.pos = 0;
  $('memGrid').innerHTML = D.memoryTestWords.map(w =>
    '<div class="cellbtn">' + esc(w) + '</div>').join('');
  $('memTip').textContent = '';
}
function memStart() {
  memReset();
  $('memGrid').innerHTML = Array.from({ length: 16 }, () =>
    '<div class="cellbtn" onclick="memClick(this)"></div>').join('');
  mem.start = Date.now();
  $('memTip').textContent = '按记忆顺序点击格子（点对位置会显示词语）。';
  $('memTip').className = 'tip';
}
function memClick(cell) {
  if (mem.pos >= 16) return;
  const idx = [...$('memGrid').children].indexOf(cell);
  if (idx === mem.pos) {
    cell.textContent = D.memoryTestWords[mem.pos];
    cell.className = 'cellbtn done';
    cell.onclick = null;
    mem.pos += 1;
    if (mem.pos === 16) {
      const t = ((Date.now() - mem.start) / 1000).toFixed(1);
      record('记忆测试', true);
      $('memTip').textContent = '全部按顺序点完！用时 ' + t + ' 秒。';
      $('memTip').className = 'tip';
    }
  } else {
    $('memTip').textContent = '顺序不对，回忆原序列再试。';
    $('memTip').className = 'err';
  }
}
function listenSet(i) { $('listenText').textContent = i === 0 ? D.listenText1 : D.listenText2; }

// ---------- 统计 ----------
function stats() {
  const s = loadStats();
  const review = loadReview();
  const reviewCount = review.length;
  if (!Object.keys(s).length) {
    return '<div class="card"><h2>训练记录</h2><p class="muted">还没有训练记录，去四大练习模块练一练吧。</p></div>';
  }
  const order = ['记数字', '记单词', '记古诗', '记短文', '舒尔特', '拍手训练', '记忆测试'];
  const rows = order.filter(k => s[k]).map(k => {
    const rate = s[k].n ? Math.round(s[k].ok * 100 / s[k].n) : 0;
    return '<tr><td>' + k + '</td><td>' + s[k].n + '</td><td>' + s[k].ok + '</td><td>' + rate + '%</td></tr>';
  }).join('');
  const head = '<div class="card"><h2>训练记录（保存在本机浏览器）</h2>';
  const reviewLine = reviewCount ? '<p class="tip">待复习单词：<b>' + reviewCount + '</b> 个（记单词时优先出现）</p>' : '';
  return head + reviewLine +
    '<table><tr><th>模块</th><th>次数</th><th>正确/记得</th><th>正确率</th></tr>' + rows + '</table></div>';
}

// ---------- 关于 ----------
function about() {
  return `
  <div class="card about">
    <h2>关于 记忆法训练助手</h2>
    <p>基于快速记忆法（数字编码、串联联想、记忆宫殿、画图记忆等）的记忆训练工具，
       覆盖<b>记数字、记单词、记古诗词、记短文</b>四大场景，手机、电脑通用，离线可用。</p>
    <h3>核心功能</h3>
    <ul>
      <li>记数字：1-100 数字编码、数字串记忆、读数练习、圆周率 50 位</li>
      <li>记单词：小学 / 初中 / 高中 576 词，看词忆义、看义忆词，未掌握词自动复习</li>
      <li>记古诗词：50 首经典古诗，画图记忆法 + 逐句背诵自测</li>
      <li>记短文：12 篇经典短文，关键词提取 + 分段记忆练习</li>
      <li>记忆方法、专注力训练、训练统计</li>
    </ul>
    <h3>产品与商业</h3>
    <p>本工具可免费使用，也支持<b>私有化部署、内容定制与教育授权</b>，
       详见仓库 README 与 <code>docs/BUSINESS.md</code>。数据与逻辑全部内嵌，无依赖、无广告、可离线运行。</p>
    <p class="muted">训练记录保存在本机浏览器（localStorage），不上传任何数据。</p>
  </div>`;
}

show('home');
'''

APP_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(APP_DIR)
ASSETS_DIR = os.path.join(REPO_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

MANIFEST = {
    "name": "记忆法训练助手",
    "short_name": "记忆训练",
    "description": "记数字、记单词、记古诗词、记短文的记忆训练工具，手机电脑通用，离线可用",
    "start_url": "./index.html",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#f2f4f8",
    "theme_color": "#24406e",
    "lang": "zh-CN",
    "icons": [
        {"src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}
    ],
}

SW_JS = """const CACHE = 'memory-training-v1';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './assets/icon.svg'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
    const copy = res.clone();
    caches.open(CACHE).then(c => c.put(e.request, copy));
    return res;
  })));
});
"""

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#24406e"/>
  <circle cx="256" cy="218" r="98" fill="none" stroke="#ffffff" stroke-width="30"/>
  <circle cx="256" cy="218" r="34" fill="#ffffff"/>
  <path d="M158 336 q98 62 196 0" fill="none" stroke="#7fb3ff" stroke-width="28" stroke-linecap="round"/>
</svg>
"""

html = HTML_HEAD.replace("__CSS__", CSS).replace("__DATA__", json.dumps(D, ensure_ascii=False))
html += JS + "</script>\n<script>\n"
html += "if ('serviceWorker' in navigator) { window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js')); }\n"
html += "</script>\n</body>\n</html>\n"

with open(os.path.join(APP_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
with open(os.path.join(APP_DIR, "manifest.webmanifest"), "w", encoding="utf-8") as f:
    json.dump(MANIFEST, f, ensure_ascii=False, indent=2)
with open(os.path.join(APP_DIR, "sw.js"), "w", encoding="utf-8") as f:
    f.write(SW_JS)
with open(os.path.join(ASSETS_DIR, "icon.svg"), "w", encoding="utf-8") as f:
    f.write(ICON_SVG)

print("已生成 index.html: %.1f KB" % (os.path.getsize(os.path.join(APP_DIR, "index.html")) / 1024))
print("已生成 manifest.webmanifest / sw.js / assets/icon.svg")
