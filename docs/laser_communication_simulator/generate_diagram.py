#!/usr/bin/env python3
"""Generate an editable Visio XML drawing and an SVG preview.

The output intentionally uses only vector primitives and text so that labels,
boxes, connectors, and line-art remain editable after opening the VDX in Visio.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent
W, H = 1920, 1080
BLUE = "#2F6F98"
DARK = "#172B3A"
MUTED = "#4C6473"
PALE = "#EDF6FB"
PALE2 = "#F6FAFC"
ORANGE = "#E58A32"
GREEN = "#2C8B72"


def svg_text(x, y, text, size=28, weight=400, anchor="start", fill=DARK):
    return (f'<text x="{x}" y="{y}" font-family="Microsoft YaHei,Noto Sans CJK SC,'
            f'PingFang SC,Arial,sans-serif" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}">{escape(text)}</text>')


def multiline(x, y, lines, size=25, gap=44, bullet=True):
    out = []
    for i, line in enumerate(lines):
        prefix = "▸  " if bullet else ""
        out.append(svg_text(x, y + i * gap, prefix + line, size, 500))
    return "\n".join(out)


def build_svg():
    s = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{BLUE}"/></marker>
  <marker id="arrowOrange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{ORANGE}"/></marker>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-opacity=".13"/></filter>
  <linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="#F5B35B" stop-opacity=".25"/><stop offset="1" stop-color="#E36B3D" stop-opacity=".5"/></linearGradient>
</defs>
<rect width="1920" height="1080" fill="#FFFFFF"/>
{svg_text(960, 62, '激光通信模拟器——激光链路验证闭环', 40, 700, 'middle')}
{svg_text(960, 98, '姿态与环境复现 · 星间远场等效 · 通信质量评估', 21, 400, 'middle', MUTED)}
''']
    panels = [(30,130,500,830),(550,130,820,830),(1390,130,500,830)]
    for x,y,w,h in panels:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{PALE2}" stroke="{BLUE}" stroke-width="2.5" filter="url(#shadow)"/>')
    headers = [(50,150,460,"1. 姿轨与环境模拟组件"),(570,150,780,"2. 激光远场模拟组件（核心光学系统）"),(1410,150,460,"3. 激光通信性能测试组件")]
    for x,y,w,t in headers:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="72" rx="8" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>')
        s.append(svg_text(x+w/2,y+47,t,27 if w<500 else 28,700,"middle"))
    s.append(multiline(70,270,["六自由度运动模拟","微振动谱 / 轨道相对运动复现","冷黑真空热环境模拟"],25,46))
    s.append(multiline(590,270,["离轴抛物面镜平行光管","程控光强衰减 / 波前畸变加载","指向抖动模拟","短距离 → 等效数万公里远场光斑"],24,44))
    s.append(multiline(1430,270,["误码率全自动测试","跟瞄精度测试","通信速率测试"],25,46))

    # Left: six-degree-of-freedom platform and vacuum chamber.
    s += [f'<g stroke="{DARK}" stroke-width="3" fill="none">',
          '<ellipse cx="280" cy="790" rx="165" ry="28" fill="#DDEAF1"/>',
          '<rect x="125" y="730" width="310" height="60" rx="10" fill="#F7FAFC"/>',
          '<line x1="160" y1="730" x2="220" y2="585"/><line x1="400" y1="730" x2="340" y2="585"/>',
          '<line x1="215" y1="730" x2="260" y2="580"/><line x1="345" y1="730" x2="300" y2="580"/>',
          '<ellipse cx="280" cy="575" rx="92" ry="18" fill="#DDEAF1"/>',
          '<rect x="205" y="485" width="150" height="90" rx="18" fill="#FFFFFF"/>',
          '<ellipse cx="280" cy="485" rx="75" ry="16" fill="#EDF6FB"/>',
          '<path d="M225 485V430 Q280 390 335 430V485" fill="#E8F3F8"/>',
          '<ellipse cx="280" cy="430" rx="55" ry="13"/>',
          '<path d="M150 700 Q95 610 155 505 Q200 445 235 405" stroke="#4F86A6" stroke-width="15"/>',
          '<circle cx="150" cy="700" r="20" fill="#fff"/><circle cx="155" cy="505" r="20" fill="#fff"/>',
          '<circle cx="235" cy="405" r="18" fill="#fff"/><path d="M235 405l55 28" stroke-width="12"/>',
          '</g>',
          svg_text(280,855,"卫星终端六自由度模拟台",24,600,"middle"),
          svg_text(380,465,"真空舱",22,600), svg_text(83,625,"微振动",20,600,fill=BLUE),
          svg_text(442,740,"轨道运动",20,600,"end",BLUE)]

    # Center: optical chain and diverging beam.
    s += [f'<g stroke="{DARK}" stroke-width="3" fill="none">',
          '<rect x="590" y="695" width="120" height="92" rx="18" fill="#E8F3F8"/>',
          '<circle cx="710" cy="741" r="34" fill="#fff"/>',
          '<circle cx="710" cy="741" r="15" fill="#F6A34F"/>',
          f'<path d="M725 728 L1225 590 L1225 890 L725 754 Z" fill="url(#beam)" stroke="none"/>',
          '<ellipse cx="895" cy="741" rx="34" ry="115" fill="#EAF4F9" stroke-width="7"/>',
          '<ellipse cx="895" cy="741" rx="12" ry="82"/>',
          '<ellipse cx="1110" cy="741" rx="34" ry="145" fill="#EAF4F9" stroke-width="7"/>',
          '<ellipse cx="1110" cy="741" rx="12" ry="105"/>',
          '<line x1="725" y1="741" x2="1250" y2="741" stroke="#D66B32" stroke-dasharray="12 8"/>',
          '<rect x="965" y="712" width="74" height="58" rx="8" fill="#FFF3E5"/>',
          '<path d="M975 755l15-28 15 28 15-28" stroke="#E58A32"/>',
          '<rect x="1180" y="700" width="75" height="82" rx="8" fill="#F0ECFA"/>',
          '<path d="M1194 738q12-22 24 0t24 0" stroke="#715BA3"/>',
          '<ellipse cx="1295" cy="741" rx="32" ry="170" fill="#FFF4E7" stroke="#E58A32" stroke-width="4" stroke-dasharray="8 7"/>',
          '</g>',
          svg_text(650,825,"激光终端",22,600,"middle"),
          svg_text(895,570,"离轴抛物面镜",22,600,"middle"),
          svg_text(1002,805,"程控衰减器",20,600,"middle"),
          svg_text(1217,812,"波前畸变加载器",20,600,"middle"),
          svg_text(1290,550,"等效远场光斑",23,700,"middle",ORANGE),
          svg_text(1290,580,"（星间数万公里链路效果）",18,400,"middle",MUTED)]
    # Jitter arrow around chain.
    s.append(f'<path d="M760 655 Q820 610 865 650" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrow)"/>')
    s.append(svg_text(810,620,"指向抖动",19,600,"middle",BLUE))

    # Right: test cabinet.
    s += [f'<g stroke="{DARK}" stroke-width="3" fill="none">',
          '<rect x="1500" y="430" width="280" height="395" rx="8" fill="#E9F1F5"/>',
          '<rect x="1520" y="460" width="240" height="315" fill="#FFFFFF"/>',
          '<rect x="1540" y="485" width="200" height="90" rx="5" fill="#DDEAF1"/>',
          '<rect x="1560" y="505" width="95" height="45" fill="#BFD8E5"/>',
          '<circle cx="1685" cy="528" r="9"/><circle cx="1715" cy="528" r="9"/>',
          '<rect x="1540" y="600" width="200" height="140" rx="7" fill="#F8FBFC"/>',
          '</g>',
          svg_text(1640,637,"自动测试结果",22,700,"middle",BLUE),
          svg_text(1570,676,"误码率",20,500), svg_text(1715,676,"1×10⁻⁹",20,700,"end",GREEN),
          svg_text(1570,707,"跟瞄精度",20,500), svg_text(1715,707,"0.1 μrad",20,700,"end",GREEN),
          svg_text(1570,738,"通信速率",20,500), svg_text(1715,738,"10 Gbps",20,700,"end",GREEN),
          svg_text(1640,860,"通信性能测试机柜",24,600,"middle")]

    # Closed-loop arrows and footer.
    s.append(f'<path d="M465 910 H585" fill="none" stroke="{BLUE}" stroke-width="7" marker-end="url(#arrow)"/>')
    s.append(f'<path d="M1360 910 H1480" fill="none" stroke="{BLUE}" stroke-width="7" marker-end="url(#arrow)"/>')
    s.append(f'<path d="M1730 900 V990 H190 Q100 990 100 900" fill="none" stroke="{BLUE}" stroke-width="7" marker-end="url(#arrow)"/>')
    s.append(svg_text(960,930,"终端状态 → 远场传输 → 性能评估",29,700,"middle",BLUE))
    s.append(svg_text(960,1025,"三大组件协同联动，完整构建激光链路地面验证闭环",30,700,"middle"))
    s.append('</svg>')
    return "\n".join(s)


def vdx_shape(sid, x, y, w, h, text="", fill="255,255,255", line="47,111,152", radius=False, font=0.18, bold=False):
    # Visio coordinates use inches with origin at bottom-left.
    txt = escape(text)
    return f'''<Shape ID="{sid}" NameU="Shape.{sid}" Type="Shape">
<XForm><PinX>{x}</PinX><PinY>{y}</PinY><Width>{w}</Width><Height>{h}</Height><LocPinX>{w/2}</LocPinX><LocPinY>{h/2}</LocPinY><Angle>0</Angle></XForm>
<Line><LineWeight>0.012</LineWeight><LineColor>{line}</LineColor><LinePattern>1</LinePattern></Line>
<Fill><FillForegnd>{fill}</FillForegnd><FillPattern>1</FillPattern></Fill>
<Geom IX="0"><MoveTo IX="1"><X>0</X><Y>0</Y></MoveTo><LineTo IX="2"><X>{w}</X><Y>0</Y></LineTo><LineTo IX="3"><X>{w}</X><Y>{h}</Y></LineTo><LineTo IX="4"><X>0</X><Y>{h}</Y></LineTo><LineTo IX="5"><X>0</X><Y>0</Y></LineTo></Geom>
<Char IX="0"><Font>0</Font><Color>23,43,58</Color><Size>{font}</Size><Style>{1 if bold else 0}</Style></Char>
<Para IX="0"><HorzAlign>1</HorzAlign><Bullet>0</Bullet></Para><Text>{txt}</Text></Shape>'''


def vdx_line(sid, x1, y1, x2, y2, color="47,111,152", weight=.025, arrow=True):
    w, h = abs(x2-x1) or .001, abs(y2-y1) or .001
    return f'''<Shape ID="{sid}" NameU="Connector.{sid}" Type="Shape">
<XForm><PinX>{(x1+x2)/2}</PinX><PinY>{(y1+y2)/2}</PinY><Width>{w}</Width><Height>{h}</Height><LocPinX>{w/2}</LocPinX><LocPinY>{h/2}</LocPinY></XForm>
<XForm1D><BeginX>{x1}</BeginX><BeginY>{y1}</BeginY><EndX>{x2}</EndX><EndY>{y2}</EndY></XForm1D>
<Line><LineWeight>{weight}</LineWeight><LineColor>{color}</LineColor><LinePattern>1</LinePattern><EndArrow>{4 if arrow else 0}</EndArrow><EndArrowSize>2</EndArrowSize></Line>
<Geom IX="0"><MoveTo IX="1"><X>0</X><Y>0</Y></MoveTo><LineTo IX="2"><X>{w}</X><Y>{h}</Y></LineTo></Geom></Shape>'''


def build_vdx():
    shapes=[]; sid=1
    def box(*args, **kwargs):
        nonlocal sid; shapes.append(vdx_shape(sid,*args,**kwargs)); sid+=1
    def line(*args, **kwargs):
        nonlocal sid; shapes.append(vdx_line(sid,*args,**kwargs)); sid+=1
    # Page: 16 x 9 inches. Keep every semantic unit separate/editable.
    box(8,8.65,15.6,.45,"激光通信模拟器——激光链路验证闭环",fill="255,255,255",line="255,255,255",font=.30,bold=True)
    panels=[(2.35,4.85,4.3,6.9),(8,4.85,6.7,6.9),(13.65,4.85,4.3,6.9)]
    for x,y,w,h in panels: box(x,y,w,h,"",fill="246,250,252")
    box(2.35,7.75,4,.62,"1. 姿轨与环境模拟组件",fill="237,246,251",font=.22,bold=True)
    box(8,7.75,6.35,.62,"2. 激光远场模拟组件（核心光学系统）",fill="237,246,251",font=.22,bold=True)
    box(13.65,7.75,4,.62,"3. 激光通信性能测试组件",fill="237,246,251",font=.22,bold=True)
    box(2.35,6.65,3.8,1.25,"▸ 六自由度运动模拟\n▸ 微振动谱 / 轨道相对运动复现\n▸ 冷黑真空热环境模拟",line="246,250,252",fill="246,250,252",font=.17)
    box(8,6.5,6.05,1.55,"▸ 离轴抛物面镜平行光管\n▸ 程控光强衰减 / 波前畸变加载\n▸ 指向抖动模拟\n▸ 短距离 → 等效数万公里远场光斑",line="246,250,252",fill="246,250,252",font=.16)
    box(13.65,6.65,3.8,1.25,"▸ 误码率全自动测试\n▸ 跟瞄精度测试\n▸ 通信速率测试",line="246,250,252",fill="246,250,252",font=.17)
    # Functional blocks in lieu of raster artwork: fully editable Visio primitives.
    box(2.35,3.6,3.2,2.7,"真空热环境\n\n六自由度模拟台\n\n微振动 / 轨道运动",fill="232,243,248",font=.20,bold=True)
    box(5.25,4.0,1.05,.75,"激光终端\n发射端",fill="232,243,248",font=.15,bold=True)
    box(7.1,4.0,.32,2.25,"离轴抛物面镜",fill="234,244,249",font=.13,bold=True)
    box(8.5,4.0,.32,2.6,"离轴抛物面镜",fill="234,244,249",font=.13,bold=True)
    box(9.45,4.0,.85,.7,"程控\n衰减器",fill="255,243,229",line="229,138,50",font=.14,bold=True)
    box(10.45,4.0,.85,.7,"波前畸变\n加载器",fill="240,236,250",line="113,91,163",font=.13,bold=True)
    box(11.2,4.0,.35,2.9,"等效远场光斑",fill="255,244,231",line="229,138,50",font=.14,bold=True)
    line(5.8,4.0,11.0,4.0,color="214,107,50",weight=.018,arrow=False)
    box(13.65,4.0,3.0,2.75,"自动测试结果\n\n误码率：1×10⁻⁹\n跟瞄精度：0.1 μrad\n通信速率：10 Gbps",fill="233,241,245",font=.19,bold=True)
    line(4.5,1.45,5.0,1.45,weight=.04)
    line(11.35,1.45,11.85,1.45,weight=.04)
    box(8,1.45,5.9,.55,"终端状态 → 远场传输 → 性能评估",line="255,255,255",fill="255,255,255",font=.22,bold=True)
    box(8,.55,11.8,.55,"三大组件协同联动，完整构建激光链路地面验证闭环",line="255,255,255",fill="255,255,255",font=.23,bold=True)
    xml='\n'.join(shapes)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<VisioDocument xmlns="http://schemas.microsoft.com/visio/2003/core" xmlns:vx="http://schemas.microsoft.com/visio/2006/extension" xml:space="preserve">
<DocumentProperties><Title>激光通信模拟器框架图</Title><Creator>OpenAI Codex</Creator><Description>激光链路验证闭环的三组件框架图</Description></DocumentProperties>
<Fonts><FontEntry ID="0" Name="Microsoft YaHei" CharSet="134" PitchAndFamily="34" Attributes="0"/></Fonts>
<StyleSheets><StyleSheet ID="0" NameU="No Style" Name="No Style"/></StyleSheets>
<Pages><Page ID="0" NameU="Page-1" Name="激光通信模拟器框架图"><PageSheet><PageProps><PageWidth>16</PageWidth><PageHeight>9</PageHeight><ShdwOffsetX>0.11811</ShdwOffsetX><ShdwOffsetY>-0.11811</ShdwOffsetY><PageScale>1</PageScale><DrawingScale>1</DrawingScale><DrawingSizeType>3</DrawingSizeType><DrawingScaleType>0</DrawingScaleType><InhibitSnap>0</InhibitSnap><UIVisibility>0</UIVisibility></PageProps></PageSheet><Shapes>{xml}</Shapes></Page></Pages>
</VisioDocument>'''


def main():
    (OUT / "laser_communication_simulator_framework.svg").write_text(build_svg(), encoding="utf-8")
    (OUT / "laser_communication_simulator_framework.vdx").write_text(build_vdx(), encoding="utf-8")
    print("Generated SVG and editable Visio VDX files.")

if __name__ == "__main__":
    main()
