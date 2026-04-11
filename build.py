#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
山海志异 - 内容构建脚本
用法: 双击运行 build.py，或在命令行 python build.py

修改 content/ 目录下的 .yaml 文件后，运行此脚本，
自动生成最新的 index.html 网页。
"""

import os
import re
import yaml

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'template.html')
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.html')

# ==================== 加载 YAML 数据 ====================
def load_yaml(filename):
    path = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(path):
        print(f"  [WARN] 文件不存在: {filename}")
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

meta = load_yaml('meta.yaml')
characters = load_yaml('characters.yaml')
world = load_yaml('world.yaml')
storyboard = load_yaml('storyboard.yaml')
contact = load_yaml('contact.yaml')

# ==================== 辅助函数 ====================

def tag_list(tags):
    """将标签列表转成 HTML span"""
    if not tags:
        return ''
    html = ''
    for t in tags:
        html += f'<span class="tag">{t}</span>\n      '
    return html.strip()

def ability_br(ability_text):
    """把换行转成 <br>"""
    return ability_text.strip().replace('\n', '<br>\n            ')

def char_type_to_badge(char_type):
    """角色类型 → CSS class"""
    return {
        'protagonist': 'badge-protagonist',
        'supporting': 'badge-supporting',
        'antagonist': 'badge-antagonist',
    }.get(char_type, 'badge-supporting')

def dot_color_to_class(color):
    return {'gold': 'dot-gold', 'blue': 'dot-blue', 'red': 'dot-red'}.get(color, 'dot-gold')

# ==================== 生成各区块 HTML ====================

def build_cover():
    tags_html = tag_list(meta.get('tags', []))
    return f'''
    <div class="cover-tags">
      {tags_html}
    </div>
'''

def build_characters():
    html = ''
    for char in characters.get('characters', []):
        badge_class = char_type_to_badge(char.get('type', 'supporting'))
        badge_text = char.get('badge', '')
        img_src = char.get('img', '')
        ability_html = ability_br(char.get('ability', ''))
        desc = char.get('desc', '').strip().replace('\n', ' ')

        # 图片处理
        if img_src and os.path.exists(os.path.join(BASE_DIR, img_src)):
            img_html = f'<img src="{img_src}" alt="{char.get("name", "")}" style="width:100%;aspect-ratio:1/1;object-fit:cover;">'
        else:
            img_html = ''

        html += f'''
      <div class="char-card">
        <div class="char-img-wrap">
          {img_html}
          <div class="char-badge {badge_class}">{badge_text}</div>
        </div>
        <div class="char-info">
          <div class="char-name">{char.get('name', '')}</div>
          <div class="char-name-en">{char.get('name_en', '')}</div>
          <div class="char-desc">{desc}</div>
          <div class="char-ability">
            {ability_html}
          </div>
        </div>
      </div>
'''
    return html

def build_world():
    html = ''
    for entry in world.get('world_entries', []):
        img_src = entry.get('img', '')
        if img_src and os.path.exists(os.path.join(BASE_DIR, img_src)):
            img_html = f'<img src="{img_src}" alt="{entry.get("title", "")}">'
        else:
            img_html = f'<div style="width:100%;aspect-ratio:16/9;background:linear-gradient(135deg,#1a0a2e,#16213e,#0f3460);"></div>'

        text = entry.get('text', '').strip().replace('\n', ' ')
        html += f'''
        <div class="world-card">
          <div class="world-card-img">{img_html}</div>
          <div class="world-card-body">
            <div class="world-card-title">{entry.get('title', '')}</div>
            <div class="world-card-text">{text}</div>
          </div>
        </div>
        <br>
'''
    return html

def build_powers():
    html = ''
    for p in world.get('powers', []):
        dot_class = dot_color_to_class(p.get('dot_color', 'gold'))
        html += f'''
            <li class="power-item">
              <div class="power-dot {dot_class}"></div>
              <div>
                <div class="power-name">{p.get('name', '')}</div>
                <div class="power-desc">{p.get('desc', '')}</div>
              </div>
            </li>
'''
    return html

def build_storyboard():
    frames_html = ''
    for frame in storyboard.get('frames', []):
        num = frame.get('num', '')
        img_src = frame.get('img', '')
        desc = frame.get('desc', '').strip().replace('\n', ' ')
        dialogue = frame.get('dialogue', '').strip().replace('\n', ' ')

        if img_src and os.path.exists(os.path.join(BASE_DIR, img_src)):
            frame_img = f'<img src="{img_src}" alt="帧{num}" style="width:100%;height:100%;object-fit:cover;">'
        else:
            frame_img = '<div class="icon">🎬</div><strong>帧' + str(num) + ' · 待配图</strong>'

        frames_html += f'''
        <div class="frame-card">
          <div class="frame-img">
            {frame_img}
          </div>
          <div class="frame-body">
            <div class="frame-num">帧 {num:02d}</div>
            <div class="frame-desc">{desc}</div>
            <div class="frame-dialogue">{dialogue}</div>
          </div>
        </div>
'''
    return frames_html

def build_contact():
    items = []
    if contact.get('email'):
        items.append(f'<a href="mailto:{contact["email"]}">📧 {contact["email"]}</a>')
    if contact.get('weibo'):
        items.append(f'<a href="{contact["weibo"]}" target="_blank">🌐 微博</a>')
    if contact.get('bilibili'):
        items.append(f'<a href="{contact["bilibili"]}" target="_blank">📺 哔哩哔哩</a>')
    if contact.get('twitter'):
        items.append(f'<a href="{contact["twitter"]}" target="_blank">𝕏 Twitter</a>')
    if contact.get('wechat'):
        items.append(f'<span>💬 微信号：{contact["wechat"]}</span>')

    links_html = '\n            '.join(items)
    intro = contact.get('intro', '')
    collab = contact.get('collaboration', '')
    return links_html, intro, collab

# ==================== 主模板替换 ====================

def main():
    print("正在读取模板...")
    if not os.path.exists(TEMPLATE_FILE):
        print(f"错误：模板文件不存在: {TEMPLATE_FILE}")
        print("请确保 template.html 存在于项目根目录。")
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Cover
    template = template.replace('{{ meta.title }}', meta.get('title', '山海志异'))
    template = template.replace('{{ meta.subtitle }}', meta.get('subtitle', ''))
    template = template.replace('{{ meta.author }}', meta.get('author', ''))
    template = template.replace('{{ meta.tags }}', build_cover())

    # Characters
    template = template.replace('{{ characters.cards }}', build_characters())

    # World
    template = template.replace('{{ world.cards }}', build_world())
    template = template.replace('{{ world.powers }}', build_powers())

    # Storyboard
    ep_title = storyboard.get('episode_title', '')
    ep_desc = storyboard.get('episode_desc', '')
    template = template.replace('{{ storyboard.episode_title }}', ep_title)
    template = template.replace('{{ storyboard.episode_desc }}', ep_desc)
    template = template.replace('{{ storyboard.frames }}', build_storyboard())

    # Contact
    links_html, intro, collab = build_contact()
    template = template.replace('{{ contact.links }}', links_html)
    template = template.replace('{{ contact.intro }}', intro)
    template = template.replace('{{ contact.collaboration }}', collab)

    # 清理未替换的 {{ }} 占位符（将它们变成醒目提示）
    template = re.sub(r'\{\{ ([^}]+) \}\}', r'<span style="color:#ff6b6b;border:1px dashed #ff6b6b;padding:0 4px;">[内容缺失: \1]</span>', template)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"✅ index.html 已生成！共 {len(template)} 字节")
    print(f"   打开 {OUTPUT_FILE} 查看，或部署到 GitHub Pages")

if __name__ == '__main__':
    main()
