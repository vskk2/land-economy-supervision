# How big is the Hong Kong–mainland border?

Paper 7 supervision project. Research question: *How large is the "border" between Hong Kong and the mainland in trade terms, compared with McCallum's (1995) US–Canada estimate?*

## Data sources

| File | What it is | Source |
|---|---|---|
| `data/raw/agtpa_yotov2016.csv` | Bilateral manufacturing trade (US$ millions, current) for 69 economies, 1986–2006, **including each economy's domestic trade**. Also population-weighted distance, contiguity, common language, colonial ties, RTA dummies. | Yotov, Piermartini, Monteiro & Larch (2016), *An Advanced Guide to Trade Policy Analysis: The Structural Gravity Model*, WTO/UNCTAD. Extracted from the R package `tradepolicy` (https://github.com/pachadotdev/tradepolicy). |
| `data/raw/worldbank_gdp_current_usd.csv` | GDP, current US$ | World Bank WDI, via https://github.com/datasets/gdp |

Notes on the trade data:
- Hong Kong's **exports** here are domestic exports (goods made in Hong Kong). Re-exports are excluded.
- Hong Kong's **imports** include goods that are later re-exported, which inflates imports from the mainland.
- Hong Kong's distance to "China" is population-weighted, so it is measured to China's population centres (about 1,600 km), not to Shenzhen.
- The sample ends in 2006. Extending it needs UN Comtrade (free API key) plus a source for domestic trade.

## Code

```
pip install pandas numpy statsmodels pyfixest
python code/01_build_and_estimate.py   # builds data/processed/*.csv
python code/02_make_charts.py          # builds charts/*.html
```

## Methods

1. **Simple gravity (Lecture 5 form)**, run for each year and direction on Hong Kong's flows only:
   `ln X = a + b·ln GDP_partner − d·ln dist + γ·Mainland + m·Macau`. The mainland premium is e^γ.
2. **Structural gravity, McCallum-style.** PPML for each year on all 69×69 flows, including domestic trade, with exporter and importer fixed effects:
   `X_ij = exp(FE_i + FE_j + β1 ln dist + β2 contiguity + β3 language + β4 colony + β5 INTL + β6 CAN–US + β7 HK→CN + β8 CN→HK)`.
   Border factor = e^−(β5 + pair coefficient), i.e. how many times more an economy trades with itself than across that border. Canada–US is estimated in the same model as a benchmark against McCallum's ≈22.

## Charts (`charts/`)

1. `1_mainland_share.html` – mainland share of Hong Kong trade
2. `2_gravity_scatter.html` – trade vs distance, year slider
3. `3_mainland_premium.html` – e^γ over time with 95% CIs
4. `4_mccallum_border.html` – border factors vs McCallum
5. `5_partner_residuals.html` – actual ÷ predicted trade by partner

Each is a self-contained HTML file. In Google Sites: **Insert → Embed → Embed code**, paste the whole file, then resize the box.

## References

- Anderson, J. E., & van Wincoop, E. (2003). Gravity with gravitas. *American Economic Review*, 93(1), 170–192.
- McCallum, J. (1995). National borders matter: Canada–U.S. regional trade patterns. *American Economic Review*, 85(3), 615–623.
- Santos Silva, J. M. C., & Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics*, 88(4), 641–658.
- Yotov, Y. V., Piermartini, R., Monteiro, J.-A., & Larch, M. (2016). *An Advanced Guide to Trade Policy Analysis: The Structural Gravity Model*. WTO/UNCTAD.
