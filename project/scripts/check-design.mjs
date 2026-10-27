#!/usr/bin/env node
/**
 * 设计约束检查：组件与页面样式只能引用 tokens.css 中的变量（规则见 docs/design/visual.md）。
 * 报错项：写死的字号/行高/间距、字面颜色、transition: all、非零字面圆角、
 *        ease-in 缓动、scale(0) 入场、超过 300ms 的字面时长、带模糊/扩散的字面投影。
 * 确有必要的例外，在同一行加注释 design-ok 并写明原因。
 *
 * 扫描 src/ 下的 .css 与 .astro / .vue / .svelte 的 <style> 块；任何名为 tokens.css 的文件跳过。
 * 用法：node scripts/check-design.mjs（建议接进 package.json 的 check 脚本）
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (/\.(astro|vue|svelte|css)$/.test(e.name)) out.push(p);
  }
  return out;
}

/** 返回 [起始行号, 样式文本] 列表；组件文件只取 <style> 块 */
function styleBlocks(file, text) {
  if (file.endsWith('.css')) return [[1, text]];
  const blocks = [];
  const re = /<style[^>]*>([\s\S]*?)<\/style>/g;
  let m;
  while ((m = re.exec(text))) {
    const line = text.slice(0, m.index).split('\n').length;
    blocks.push([line, m[1]]);
  }
  return blocks;
}

/** 字面投影：拆成逗号分隔的各层，var(--shadow-*) 与 none 之外，模糊或扩散半径不为 0 即报错（1–2px 细线式投影允许） */
function literalShadow(value) {
  return value
    .split(/,(?![^(]*\))/)
    .map((s) => s.trim())
    .some((layer) => {
      if (!layer || layer === 'none' || /^var\(--shadow-[a-z0-9-]+\)$/.test(layer)) return false;
      const lengths = layer.replace(/inset/g, '').match(/-?\d*\.?\d+(px|rem|em)|\b0\b/g) ?? [];
      return lengths.slice(2).some((v) => parseFloat(v) !== 0);
    });
}

const RULES = [
  {
    name: '字号或行高写死',
    test: (l) => /\b(font-size|line-height)\s*:[^;]*\b\d+(\.\d+)?px/.test(l) || /\bfont\s*:[^;]*\b\d+(\.\d+)?px/.test(l),
  },
  {
    name: '间距写死（请用 --sp-*）',
    test: (l) => {
      const m = /\b(padding|margin|gap|column-gap|row-gap)(-[a-z-]+)?\s*:([^;]+)/.exec(l);
      if (!m) return false;
      const px = m[3].match(/\b\d+(\.\d+)?px\b/g) ?? [];
      return px.some((v) => !['0px', '1px', '2px'].includes(v));
    },
  },
  {
    name: '字面颜色（请用颜色变量）',
    test: (l) => !/mask(-image)?\s*:/.test(l) && /(#[0-9a-fA-F]{3,8}\b|\b(rgb|rgba|hsl|hsla|oklch)\()/.test(l),
  },
  { name: 'transition: all', test: (l) => /transition(-property)?\s*:[^;]*\ball\b/.test(l) },
  {
    name: '非零圆角（请用 --radius-*）',
    test: (l) => {
      const m = /border-radius\s*:\s*([^;]+)/.exec(l);
      return !!m && !/^(0(px)?|var\(.+\)|(0(px)?|var\([^)]+\))(\s+(0(px)?|var\([^)]+\)))*)\s*(!important)?$/.test(m[1].trim());
    },
  },
  {
    name: 'ease-in 缓动（进入与退出用 --ease-out，屏内移动用 --ease-in-out）',
    test: (l) => /\b(transition|animation)(-timing-function)?\s*:[^;]*\bease-in\b(?!-out)/.test(l),
  },
  {
    name: 'scale(0) 入场（起点不小于 0.9）',
    test: (l) => /\bscale(3d)?\(\s*0(\.0+)?\s*[,)]/.test(l) || /\bscale\s*:\s*0(\.0+)?\s*(;|$)/.test(l),
  },
  {
    name: '动效时长超过 300ms（请用 --dur-*）',
    test: (l) => {
      const m = /\b(transition|animation)(-duration)?\s*:([^;]+)/.exec(l);
      if (!m) return false;
      const ms = m[3].match(/\b\d+(\.\d+)?(ms|s)\b/g) ?? [];
      return ms.some((v) => (v.endsWith('ms') ? parseFloat(v) : parseFloat(v) * 1000) > 300);
    },
  },
  {
    name: '字面投影（请用 --shadow-*；细线式 1–2px 投影除外）',
    test: (l) => {
      const m = /\bbox-shadow\s*:\s*([^;]+)/.exec(l);
      return !!m && literalShadow(m[1]);
    },
  },
];

const problems = [];
const srcDir = path.join(root, 'src');
if (!fs.existsSync(srcDir)) {
  console.log('没有 src/，跳过设计约束检查');
  process.exit(0);
}
for (const file of walk(srcDir)) {
  const rel = path.relative(root, file).split(path.sep).join('/');
  if (path.basename(rel) === 'tokens.css') continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const [start, css] of styleBlocks(file, text)) {
    css.split('\n').forEach((line, i) => {
      if (line.includes('design-ok') || /^\s*(\/\*|\*)/.test(line)) return;
      for (const r of RULES) if (r.test(line)) problems.push(`${rel}:${start + i}  ${r.name}  ${line.trim()}`);
    });
  }
}

if (problems.length) {
  console.error(`设计约束检查未通过（${problems.length} 处）：\n` + problems.join('\n'));
  process.exit(1);
}
console.log('设计约束检查通过');
