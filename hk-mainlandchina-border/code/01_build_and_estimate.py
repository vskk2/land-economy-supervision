"""
Hong Kong - mainland border effect: data build and estimation.

Research question: How large is the "border" between Hong Kong and the
mainland in trade terms, compared with McCallum's (1995) US-Canada estimate?

Inputs (data/raw/):
  agtpa_yotov2016.csv          Yotov, Piermartini, Monteiro & Larch (2016),
                               "An Advanced Guide to Trade Policy Analysis",
                               WTO/UNCTAD. 69 economies, 1986-2006, manufacturing
                               trade in millions of current USD, INCLUDING each
                               economy's domestic (internal) trade. Distances are
                               population-weighted (CEPII). Extracted from the
                               R package `tradepolicy` (github.com/pachadotdev/tradepolicy).
  worldbank_gdp_current_usd.csv  World Bank WDI GDP (current USD), via
                               github.com/datasets/gdp.

Outputs (data/processed/):
  hk_flows.csv                 Every HK export/import flow with partner GDP.
  simple_gravity_by_year.csv   Lecture-style OLS: ln X = a + b lnGDP - d lnDist
                               + g*Mainland + m*Macau, by year and direction.
  structural_border_by_year.csv  PPML with exporter & importer fixed effects and
                               domestic flows: McCallum-style border factors.
  hk_partner_residuals.csv     Actual vs gravity-predicted trade, by partner.
  mainland_share.csv           Mainland share of HK trade, by year.

Run:  python code/01_build_and_estimate.py   (from the project folder)
Needs: pandas, numpy, statsmodels, pyfixest
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import pyfixest as pf

RAW, OUT = "data/raw/", "data/processed/"

# ---------------------------------------------------------------- 1. load
d = pd.read_csv(RAW + "agtpa_yotov2016.csv")
d["year"] = d["year"].astype(int)
gdp = pd.read_csv(RAW + "worldbank_gdp_current_usd.csv")
gdp = gdp.rename(columns={"Country Code": "iso", "Year": "year", "Value": "gdp"})
gdp["iso"] = gdp["iso"].replace({"ROU": "ROM"})   # Yotov uses the old Romania code
gdp = gdp[["iso", "year", "gdp"]]

# ---------------------------------------------------------------- 2. HK flows
hk = d[((d.exporter == "HKG") | (d.importer == "HKG")) & (d.exporter != d.importer)].copy()
hk["direction"] = np.where(hk.exporter == "HKG", "HK exports", "HK imports")
hk["partner"] = np.where(hk.exporter == "HKG", hk.importer, hk.exporter)
hk = hk.merge(gdp, left_on=["partner", "year"], right_on=["iso", "year"], how="left").drop(columns="iso")
hk["mainland"] = (hk.partner == "CHN").astype(int)
hk["macau"] = (hk.partner == "MAC").astype(int)
hk = hk[(hk.trade > 0) & hk.gdp.notna()].copy()
hk["ln_trade"] = np.log(hk.trade)
hk["ln_gdp"] = np.log(hk.gdp / 1e9)          # GDP in USD billions
hk["ln_dist"] = np.log(hk.dist)
hk[["year", "direction", "partner", "trade", "gdp", "dist", "cntg", "lang", "clny", "rta",
    "mainland", "macau"]].to_csv(OUT + "hk_flows.csv", index=False)

# ---------------------------------------------------------------- 3. simple OLS gravity (Lecture 5 form)
rows, resid_rows = [], []
for (yr, dirn), g in hk.groupby(["year", "direction"]):
    m = smf.ols("ln_trade ~ ln_gdp + ln_dist + mainland + macau", data=g).fit(cov_type="HC1")
    b, se = m.params, m.bse
    rows.append(dict(year=yr, direction=dirn, n=int(m.nobs), r2=m.rsquared, a=b.Intercept, b_macau=b.macau,
                     b_gdp=b.ln_gdp, b_dist=b.ln_dist,
                     gamma=b.mainland, gamma_se=se.mainland,
                     mainland_factor=np.exp(b.mainland),
                     factor_lo=np.exp(b.mainland - 1.96 * se.mainland),
                     factor_hi=np.exp(b.mainland + 1.96 * se.mainland)))
    # prediction WITHOUT the mainland/macau dummies = "what plain gravity expects"
    pred = b.Intercept + b.ln_gdp * g.ln_gdp + b.ln_dist * g.ln_dist
    resid_rows.append(pd.DataFrame(dict(
        year=yr, direction=dirn, partner=g.partner, trade=g.trade,
        predicted=np.exp(pred), ln_dist=g.ln_dist, ln_gdp=g.ln_gdp,
        y_adj=g.ln_trade - b.ln_gdp * g.ln_gdp,         # size-adjusted trade (y-axis of scatter)
        ratio=g.trade / np.exp(pred))))
simple = pd.DataFrame(rows)
simple.to_csv(OUT + "simple_gravity_by_year.csv", index=False)
pd.concat(resid_rows).to_csv(OUT + "hk_partner_residuals.csv", index=False)

# ---------------------------------------------------------------- 4. structural PPML (McCallum-style)
s = d.copy()
s["ln_dist"] = np.log(s.dist)
s["intl"] = (s.exporter != s.importer).astype(int)
pair = lambda a, b_: ((s.exporter == a) & (s.importer == b_)).astype(int)
s["canus"] = pair("CAN", "USA") + pair("USA", "CAN")
s["hk2cn"] = pair("HKG", "CHN")
s["cn2hk"] = pair("CHN", "HKG")
s["exp_id"], s["imp_id"] = s.exporter, s.importer

def border(coefs, V, names):
    """Border factor = exp(-(sum of coefs)); 95% CI by delta method on the sum."""
    est = sum(coefs[n] for n in names)
    var = sum(V.loc[a, b_] for a in names for b_ in names)
    sd = np.sqrt(var)
    return np.exp(-est), np.exp(-(est + 1.96 * sd)), np.exp(-(est - 1.96 * sd))

srows = []
for yr, g in s.groupby("year"):
    fit = pf.fepois("trade ~ ln_dist + cntg + lang + clny + intl + canus + hk2cn + cn2hk | exp_id + imp_id",
                    data=g, vcov={"CRV1": "pair_id"})
    c, V = fit.coef(), fit._vcov
    V = pd.DataFrame(V, index=c.index, columns=c.index)
    for label, names in [("Average international border", ["intl"]),
                         ("Canada - US", ["intl", "canus"]),
                         ("Hong Kong to mainland", ["intl", "hk2cn"]),
                         ("Mainland to Hong Kong", ["intl", "cn2hk"])]:
        f, lo, hi = border(c, V, names)
        srows.append(dict(year=yr, series=label, border_factor=f, lo=lo, hi=hi))
    print(yr, "dist", round(c.ln_dist, 3), "intl", round(c.intl, 3),
          "hk2cn", round(c.hk2cn, 3), "cn2hk", round(c.cn2hk, 3))
pd.DataFrame(srows).to_csv(OUT + "structural_border_by_year.csv", index=False)

# ---------------------------------------------------------------- 5. descriptive shares
# Shares use ALL partners (no GDP needed), so no partner is dropped here.
allhk = d[((d.exporter == "HKG") | (d.importer == "HKG")) & (d.exporter != d.importer)].copy()
allhk["direction"] = np.where(allhk.exporter == "HKG", "HK exports", "HK imports")
allhk["partner"] = np.where(allhk.exporter == "HKG", allhk.importer, allhk.exporter)
tot = allhk.groupby(["year", "direction"]).trade.sum()
cn = allhk[allhk.partner == "CHN"].groupby(["year", "direction"]).trade.sum()
(cn / tot * 100).rename("mainland_share_pct").reset_index().to_csv(OUT + "mainland_share.csv", index=False)
print(simple[["year", "direction", "mainland_factor", "factor_lo", "factor_hi", "b_dist"]].round(2).to_string())
