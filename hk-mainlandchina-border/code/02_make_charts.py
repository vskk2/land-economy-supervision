"""
Builds five self-contained interactive HTML charts (Plotly.js from CDN) in charts/.
Each file can be pasted into Google Sites via Insert > Embed > Embed code.
Run after 01_build_and_estimate.py.
"""
import json
import pandas as pd

P = "data/processed/"
NAMES = {"ARG": "Argentina", "AUS": "Australia", "AUT": "Austria", "BEL": "Belgium", "BGR": "Bulgaria",
    "BOL": "Bolivia", "BRA": "Brazil", "CAN": "Canada", "CHE": "Switzerland", "CHL": "Chile",
    "CHN": "Mainland China", "CMR": "Cameroon", "COL": "Colombia", "CRI": "Costa Rica", "CYP": "Cyprus",
    "DEU": "Germany", "DNK": "Denmark", "ECU": "Ecuador", "EGY": "Egypt", "ESP": "Spain", "FIN": "Finland",
    "FRA": "France", "GBR": "United Kingdom", "GRC": "Greece", "HKG": "Hong Kong", "HUN": "Hungary",
    "IDN": "Indonesia", "IND": "India", "IRL": "Ireland", "IRN": "Iran", "ISL": "Iceland", "ISR": "Israel",
    "ITA": "Italy", "JOR": "Jordan", "JPN": "Japan", "KEN": "Kenya", "KOR": "South Korea", "KWT": "Kuwait",
    "LKA": "Sri Lanka", "MAC": "Macau", "MAR": "Morocco", "MEX": "Mexico", "MLT": "Malta", "MMR": "Myanmar",
    "MUS": "Mauritius", "MWI": "Malawi", "MYS": "Malaysia", "NER": "Niger", "NGA": "Nigeria",
    "NLD": "Netherlands", "NOR": "Norway", "NPL": "Nepal", "PAN": "Panama", "PHL": "Philippines",
    "POL": "Poland", "PRT": "Portugal", "QAT": "Qatar", "ROM": "Romania", "SEN": "Senegal",
    "SGP": "Singapore", "SWE": "Sweden", "THA": "Thailand", "TTO": "Trinidad and Tobago", "TUN": "Tunisia",
    "TUR": "Turkey", "TZA": "Tanzania", "URY": "Uruguay", "USA": "United States", "ZAF": "South Africa"}

SOURCE = ("Data: Yotov et al. (2016), <i>An Advanced Guide to Trade Policy Analysis</i>, WTO/UNCTAD "
          "(manufacturing trade, 69 economies); World Bank GDP. Code and data in the project repository.")

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {{ --surface:#ffffff; --ink:#0b0b0b; --ink2:#52514e; --muted:#8a8984; --grid:#ececea;
          --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --ref:#8a8984; }}
  html,body {{ margin:0; background:var(--surface); color:var(--ink);
              font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; }}
  .wrap {{ max-width:900px; margin:0 auto; padding:12px 16px 8px; box-sizing:border-box; }}
  h1 {{ font-size:18px; font-weight:600; margin:0 0 4px; line-height:1.3; }}
  .sub {{ font-size:13px; color:var(--ink2); margin:0 0 10px; line-height:1.45; }}
  .controls {{ display:flex; flex-wrap:wrap; gap:12px 20px; align-items:center; font-size:13px;
              color:var(--ink2); margin-bottom:4px; }}
  .controls label {{ display:flex; align-items:center; gap:8px; }}
  select, input[type=range] {{ font:inherit; }}
  select {{ padding:4px 6px; border:1px solid #d4d3cf; border-radius:6px; background:#fff; color:var(--ink); }}
  input[type=range] {{ width:220px; accent-color:var(--s1); }}
  .yr {{ font-variant-numeric:tabular-nums; font-weight:600; color:var(--ink); min-width:3em; }}
  #chart {{ width:100%; height:{height}px; }}
  .src {{ font-size:11px; color:var(--muted); margin:4px 0 0; line-height:1.4; }}
  details {{ font-size:12px; color:var(--ink2); margin-top:6px; }}
  table {{ border-collapse:collapse; font-size:12px; margin-top:6px; font-variant-numeric:tabular-nums; }}
  td,th {{ padding:2px 10px 2px 0; text-align:right; }} th {{ font-weight:600; }}
  td:first-child, th:first-child {{ text-align:left; }}
</style></head>
<body><div class="wrap">
<h1>{title}</h1>
<p class="sub">{subtitle}</p>
{controls}
<div id="chart"></div>
<p class="src">{note}<br>{source}</p>
<details><summary>Show data table</summary><div id="tbl"></div></details>
</div>
<script>
const DATA = {data};
const CSS = getComputedStyle(document.documentElement);
const C = n => CSS.getPropertyValue(n).trim();
const BASE = {{
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{{family:'Helvetica Neue, Helvetica, Arial, sans-serif', size:12, color:C('--ink2')}},
  margin:{{l:64, r:24, t:16, b:56}}, hovermode:'closest',
  hoverlabel:{{bgcolor:'#ffffff', bordercolor:'#d4d3cf', font:{{color:C('--ink'), size:12}}}},
  legend:{{orientation:'h', y:-0.18, x:0, font:{{size:12, color:C('--ink2')}}}},
  xaxis:{{gridcolor:C('--grid'), zeroline:false, linecolor:'#d4d3cf', ticks:'outside', tickcolor:'#d4d3cf'}},
  yaxis:{{gridcolor:C('--grid'), zeroline:false, linecolor:'#d4d3cf'}}
}};
const CFG = {{displaylogo:false, responsive:true,
  modeBarButtonsToRemove:['lasso2d','select2d','autoScale2d']}};
function table(rows, cols) {{
  let h = '<table><tr>' + cols.map(c=>'<th>'+c[1]+'</th>').join('') + '</tr>';
  rows.forEach(r => h += '<tr>' + cols.map(c=>'<td>'+(c[2]?c[2](r[c[0]]):r[c[0]])+'</td>').join('') + '</tr>');
  document.getElementById('tbl').innerHTML = h + '</table>';
}}
{js}
</script></body></html>
"""


def write(fname, title, subtitle, note, data, js, controls="", height=460):
    html = TEMPLATE.format(title=title, subtitle=subtitle, note=note, source=SOURCE,
                           data=json.dumps(data, separators=(",", ":")), js=js,
                           controls=controls, height=height)
    open("charts/" + fname, "w").write(html)
    print("wrote", fname, round(len(html) / 1024), "KB")


YEAR_CTRL = """<div class="controls">
  <label>Flow <select id="dir"><option value="HK exports">Hong Kong exports to partner</option>
  <option value="HK imports">Hong Kong imports from partner</option></select></label>
  <label>Year <input id="yr" type="range" min="1986" max="2006" step="1" value="{v}"><span class="yr" id="yrv">{v}</span></label>
</div>"""

# ------------------------------------------------------------------ 1. mainland share
sh = pd.read_csv(P + "mainland_share.csv")
d1 = {k: {"year": g.year.tolist(), "v": g.mainland_share_pct.round(1).tolist()}
      for k, g in sh.groupby("direction")}
write("1_mainland_share.html",
      "How much of Hong Kong's trade is with the mainland?",
      "Mainland China's share of Hong Kong's manufacturing trade with the 68 other economies in the sample, 1986&ndash;2006.",
      "Exports are Hong Kong's domestic exports (goods made in Hong Kong); imports include goods later re-exported.",
      d1, """
const tr = [['HK imports','Imports from the mainland',C('--s2')],['HK exports','Exports to the mainland',C('--s1')]].map(([k,n,c]) => ({
  x:DATA[k].year, y:DATA[k].v, name:n, mode:'lines+markers', line:{color:c,width:2}, marker:{size:7,color:c},
  hovertemplate:'%{x}<br>'+n+': <b>%{y:.1f}%</b><extra></extra>'}));
const L = JSON.parse(JSON.stringify(BASE)); L.hovermode='x unified';
L.yaxis.title={text:'Share of Hong Kong trade (%)'}; L.yaxis.rangemode='tozero'; L.yaxis.ticksuffix='%';
L.xaxis.dtick=2;
L.shapes=[1997,2001,2003].map(x=>({type:'line',x0:x,x1:x,y0:0,y1:1,yref:'paper',line:{color:C('--ref'),width:1,dash:'dot'}}));
L.annotations=[[1997,'Handover'],[2001,'WTO'],[2003,'CEPA']].map(([x,t])=>({x:x,y:1,yref:'paper',text:t,showarrow:false,
  yanchor:'bottom',font:{size:11,color:C('--muted')}}));
L.margin.t=28;
Plotly.newPlot('chart', tr, L, CFG);
table(DATA['HK exports'].year.map((y,i)=>({y:y,e:DATA['HK exports'].v[i],m:DATA['HK imports'].v[i]})),
  [['y','Year'],['e','Exports to mainland (%)'],['m','Imports from mainland (%)']]);
""")

# ------------------------------------------------------------------ 2. gravity scatter
res = pd.read_csv(P + "hk_partner_residuals.csv")
simple = pd.read_csv(P + "simple_gravity_by_year.csv")
d2 = {"pts": {}, "fit": {}}
for (yr, dirn), g in res.groupby(["year", "direction"]):
    key = f"{dirn}|{yr}"
    d2["pts"][key] = [[NAMES[p], round(x, 3), round(y, 3), round(t, 1)]
                      for p, x, y, t in zip(g.partner, g.ln_dist, g.y_adj, g.trade)]
    s = simple[(simple.year == yr) & (simple.direction == dirn)].iloc[0]
    a = s.a   # OLS intercept: the line is the prediction for a partner with no dummies
    d2["fit"][key] = [round(s.b_dist, 3), round(a, 3), round(s.gamma, 3)]
write("2_gravity_scatter.html",
      "Hong Kong's trade and distance: where does the mainland sit?",
      "Each bubble is a trading partner. The y-axis removes the effect of partner size (the same distance-decay idea as the Munich wage-shock chart in Lectures 5&ndash;6); "
      "bubbles above the line trade more than gravity predicts. Bubble area is proportional to trade value.",
      "y = ln(trade) &minus; b&middot;ln(partner GDP), with b estimated each year. Line: fitted distance effect. Distance is population-weighted (CEPII).",
      d2, """
const dirEl=document.getElementById('dir'), yrEl=document.getElementById('yr'), yrv=document.getElementById('yrv');
function draw(){
  const k = dirEl.value+'|'+yrEl.value; yrv.textContent=yrEl.value;
  const pts = DATA.pts[k], [b,a,g] = DATA.fit[k];
  const maxT = Math.max(...pts.map(p=>p[3]));
  const grp = (f,n,c) => { const s=pts.filter(f); return {x:s.map(p=>p[1]), y:s.map(p=>p[2]), text:s.map(p=>p[0]),
     customdata:s.map(p=>p[3]), name:n, mode:'markers',
     marker:{size:s.map(p=>Math.max(8, 46*Math.sqrt(p[3]/maxT))), color:c, opacity:0.75, line:{color:'#ffffff',width:2}},
     hovertemplate:'<b>%{text}</b><br>Trade: US$%{customdata:,.0f}m<br>ln distance: %{x:.2f}<extra></extra>'}; };
  const xs=pts.map(p=>p[1]), x0=Math.min(...xs), x1=Math.max(...xs);
  const tr=[grp(p=>p[0]!=='Mainland China'&&p[0]!=='Macau','Other partners',C('--s1')),
            grp(p=>p[0]==='Macau','Macau',C('--s3')),
            grp(p=>p[0]==='Mainland China','Mainland China',C('--s2')),
            {x:[x0,x1], y:[a+b*x0, a+b*x1], mode:'lines', name:'Gravity prediction', line:{color:C('--ink2'),width:2,dash:'dash'}, hoverinfo:'skip'}];
  const L = JSON.parse(JSON.stringify(BASE));
  L.xaxis.title={text:'ln(distance from Hong Kong, km)'}; L.yaxis.title={text:'ln(trade) adjusted for partner size'};
  L.annotations=[{x:0.99,y:0.98,xref:'paper',yref:'paper',xanchor:'right',showarrow:false,align:'right',
     text:'Distance elasticity: '+b.toFixed(2)+'<br>Mainland premium: ×'+Math.exp(g).toFixed(1),font:{size:12,color:C('--ink')}}];
  Plotly.react('chart', tr, L, CFG);
  table(pts.slice().sort((p,q)=>q[3]-p[3]), [[0,'Partner'],[3,'Trade (US$m)',v=>Math.round(v).toLocaleString()],[1,'ln distance'],[2,'Size-adjusted ln trade']]);
}
dirEl.onchange=draw; yrEl.oninput=draw; draw();
""", controls=YEAR_CTRL.format(v=2006), height=500)

# ------------------------------------------------------------------ 3. mainland premium (simple OLS)
d3 = {k: {"year": g.year.tolist(), "f": g.mainland_factor.round(2).tolist(),
          "lo": g.factor_lo.round(2).tolist(), "hi": g.factor_hi.round(2).tolist(),
          "dist": g.b_dist.round(2).tolist(), "n": g.n.tolist()}
      for k, g in simple.groupby("direction")}
write("3_mainland_premium.html",
      "The mainland premium: how much more does Hong Kong trade with the mainland than gravity predicts?",
      "Estimated each year from ln(trade) = a + b&middot;ln(GDP) &minus; d&middot;ln(distance) + &gamma;&middot;Mainland + Macau dummy. "
      "The line shows e<sup>&gamma;</sup>: a value of 3 means three times the trade a partner of the mainland's size and distance would normally have. "
      "Shaded bands are 95% confidence intervals.",
      "Values above the dotted line at 1 mean extra trade; below 1 would mean a border penalty. Log scale. Robust (HC1) standard errors.",
      d3, """
const series=[['HK exports','Hong Kong exports to the mainland',C('--s1'),'rgba(42,120,214,0.14)'],
              ['HK imports','Hong Kong imports from the mainland',C('--s2'),'rgba(235,104,52,0.14)']];
let tr=[];
series.forEach(([k,n,c,f])=>{ const D=DATA[k];
  tr.push({x:D.year.concat(D.year.slice().reverse()), y:D.hi.concat(D.lo.slice().reverse()), fill:'toself', fillcolor:f,
           line:{width:0}, hoverinfo:'skip', showlegend:false, legendgroup:k});
  tr.push({x:D.year, y:D.f, name:n, legendgroup:k, mode:'lines+markers', line:{color:c,width:2}, marker:{size:7,color:c},
           customdata:D.year.map((_,i)=>[D.lo[i],D.hi[i]]),
           hovertemplate:'%{x} · '+n+'<br>Premium: <b>×%{y:.2f}</b> (95% CI %{customdata[0]:.2f}–%{customdata[1]:.2f})<extra></extra>'});});
const L = JSON.parse(JSON.stringify(BASE));
L.yaxis.type='log'; L.yaxis.tickvals=[0.5,1,2,5,10,20]; L.yaxis.ticktext=['0.5','1','2','5','10','20']; L.yaxis.title={text:'Mainland premium, e^γ (log scale)'}; L.xaxis.dtick=2;
L.shapes=[{type:'line',xref:'paper',x0:0,x1:1,y0:1,y1:1,line:{color:C('--ink2'),width:1.5,dash:'dot'}}]
  .concat([1997,2001,2003].map(x=>({type:'line',x0:x,x1:x,y0:0,y1:1,yref:'paper',line:{color:C('--ref'),width:1,dash:'dot'}})));
L.annotations=[[1997,'Handover'],[2001,'WTO'],[2003,'CEPA']].map(([x,t])=>({x:x,y:1,yref:'paper',text:t,showarrow:false,
  yanchor:'bottom',font:{size:11,color:C('--muted')}})).concat([{x:1986,y:0,xanchor:'left',yanchor:'top',text:'No premium',
  showarrow:false,font:{size:11,color:C('--muted')}}]);
L.margin.t=28;
Plotly.newPlot('chart', tr, L, CFG);
const E=DATA['HK exports'], M=DATA['HK imports'];
table(E.year.map((y,i)=>({y:y,e:E.f[i],el:E.lo[i]+'–'+E.hi[i],m:M.f[i],ml:M.lo[i]+'–'+M.hi[i],de:E.dist[i],dm:M.dist[i]})),
  [['y','Year'],['e','Exports premium'],['el','95% CI'],['m','Imports premium'],['ml','95% CI'],['de','Distance coef. (exports)'],['dm','Distance coef. (imports)']]);
""")

# ------------------------------------------------------------------ 4. McCallum comparison (structural PPML)
st = pd.read_csv(P + "structural_border_by_year.csv")
order = ["Average international border", "Canada - US", "Hong Kong to mainland", "Mainland to Hong Kong"]
d4 = {k: {"year": st[st.series == k].year.tolist(),
          "f": st[st.series == k].border_factor.round(2).tolist(),
          "lo": st[st.series == k].lo.round(2).tolist(),
          "hi": st[st.series == k].hi.round(2).tolist()} for k in order}
write("4_mccallum_border.html",
      "How big is the Hong Kong&ndash;mainland border, compared with McCallum's US&ndash;Canada border?",
      "Each line shows how many times more an economy trades with <i>itself</i> than across that border, after controlling for distance, "
      "a shared border, a common language and colonial ties. McCallum (1995) found about 22 for Canada and the US (1988 data). "
      "Higher means a thicker border; 1 would mean the border makes no difference.",
      "Structural gravity, estimated by PPML each year with exporter and importer fixed effects and domestic trade flows "
      "(Yotov et al., 2016, ch. 1). Border factor = e<sup>&minus;(international + pair-specific coefficient)</sup>. "
      "95% CIs (delta method, pair-clustered) shown on hover. Log scale.",
      d4, """
const cols=['#8a8984',C('--s4'),C('--s1'),C('--s2')], dash=['solid','solid','solid','solid'];
const tr=Object.keys(DATA).map((k,i)=>({x:DATA[k].year, y:DATA[k].f, name:k.replace(' - ','–'), mode:'lines+markers',
  line:{color:cols[i],width:2}, marker:{size:7,color:cols[i],symbol:['circle','square','diamond','triangle-up'][i]},
  customdata:DATA[k].year.map((_,j)=>[DATA[k].lo[j],DATA[k].hi[j]]),
  hovertemplate:'%{x} · '+k.replace(' - ','–')+'<br>Border factor: <b>%{y:.1f}</b> (95% CI %{customdata[0]:.1f}–%{customdata[1]:.1f})<extra></extra>'}));
const L = JSON.parse(JSON.stringify(BASE));
L.yaxis.type='log'; L.yaxis.tickvals=[1,2,5,10,20,50]; L.yaxis.ticktext=['1','2','5','10','20','50']; L.yaxis.title={text:'Domestic trade ÷ cross-border trade (log scale)'}; L.xaxis.dtick=2;
L.shapes=[{type:'line',xref:'paper',x0:0,x1:1,y0:22,y1:22,line:{color:C('--ink2'),width:1.5,dash:'dash'}},
          {type:'line',xref:'paper',x0:0,x1:1,y0:1,y1:1,line:{color:C('--ref'),width:1,dash:'dot'}}];
L.annotations=[{xref:'paper',x:1,y:Math.log10(22),xanchor:'right',yanchor:'bottom',text:'McCallum (1995): ≈22',showarrow:false,font:{size:11,color:C('--ink2')}},
               {xref:'paper',x:1,y:0,xanchor:'right',yanchor:'top',text:'No border effect',showarrow:false,font:{size:11,color:C('--muted')}}];
L.legend.y=-0.2;
Plotly.newPlot('chart', tr, L, CFG);
const K=Object.keys(DATA);
table(DATA[K[0]].year.map((y,i)=>Object.assign({y:y},...K.map((k,j)=>({['s'+j]:DATA[k].f[i]})))),
  [['y','Year']].concat(K.map((k,j)=>['s'+j,k.replace(' - ','–')])));
""", height=500)

# ------------------------------------------------------------------ 5. partner residuals
d5 = {}
for (yr, dirn), g in res.groupby(["year", "direction"]):
    g = g.sort_values("ratio")
    d5[f"{dirn}|{yr}"] = [[NAMES[p], round(r, 3), round(t, 1), round(pr, 1)]
                          for p, r, t, pr in zip(g.partner, g.ratio, g.trade, g.predicted)]
write("5_partner_residuals.html",
      "Which partners trade more, or less, with Hong Kong than gravity predicts?",
      "Actual trade divided by the trade a plain gravity model (partner GDP and distance only) would predict. "
      "Showing the 12 partners furthest above and below the prediction, plus the mainland and Macau. Is the mainland unusual, or one of many outliers?",
      "Values above 1 mean more trade than predicted (log scale). Predictions exclude the mainland and Macau dummies.",
      d5, """
const dirEl=document.getElementById('dir'), yrEl=document.getElementById('yr'), yrv=document.getElementById('yrv');
function draw(){
  const k=dirEl.value+'|'+yrEl.value; yrv.textContent=yrEl.value;
  const all=DATA[k]; const keep=new Set(all.slice(0,12).concat(all.slice(-12)).map(p=>p[0]).concat(['Mainland China','Macau']));
  const sel=all.filter(p=>keep.has(p[0]));
  const col=sel.map(p=>p[0]==='Mainland China'?C('--s2'):(p[0]==='Macau'?C('--s3'):(p[1]>=1?C('--s1'):'#86b6ef')));
  const tr=[{type:'bar', orientation:'h', y:sel.map(p=>p[0]), x:sel.map(p=>p[1]-1), base:1,
    marker:{color:col, line:{color:'#ffffff',width:1}}, customdata:sel.map(p=>[p[2],p[3],p[1]]),
    hovertemplate:'<b>%{y}</b><br>Actual ÷ predicted: <b>%{customdata[2]:.2f}</b><br>Actual: US$%{customdata[0]:,.0f}m<br>Predicted: US$%{customdata[1]:,.0f}m<extra></extra>'}];
  const L=JSON.parse(JSON.stringify(BASE));
  L.xaxis.type='log'; L.xaxis.tickvals=[0.01,0.03,0.1,0.3,1,3,10,30,100]; L.xaxis.ticktext=['0.01','0.03','0.1','0.3','1','3','10','30','100']; L.xaxis.title={text:'Actual trade ÷ gravity prediction (log scale)'};
  L.yaxis.automargin=true; L.yaxis.gridcolor='rgba(0,0,0,0)'; L.margin.l=140; L.showlegend=false; L.bargap=0.25;
  L.shapes=[{type:'line',x0:1,x1:1,y0:0,y1:1,yref:'paper',line:{color:C('--ink2'),width:1.5,dash:'dot'}}];
  const rank=all.length-all.findIndex(p=>p[0]==='Mainland China');
  L.annotations=[{xref:'paper',yref:'paper',x:0,y:1.02,xanchor:'left',yanchor:'bottom',showarrow:false,
     text:'Mainland China ranks <b>'+rank+'</b> of '+all.length+' partners', font:{size:12,color:C('--ink')}}];
  L.margin.t=30;
  Plotly.react('chart', tr, L, CFG);
  table(all.slice().reverse(), [[0,'Partner'],[1,'Actual ÷ predicted',v=>v.toFixed(2)],[2,'Actual (US$m)',v=>Math.round(v).toLocaleString()],[3,'Predicted (US$m)',v=>Math.round(v).toLocaleString()]]);
}
dirEl.onchange=draw; yrEl.oninput=draw; draw();
""", controls=YEAR_CTRL.format(v=2006), height=620)
