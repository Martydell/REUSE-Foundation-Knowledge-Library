# Research Progress

Total unique organisations: 727 (748 rows in original list, 21 duplicates)

- Full V4 profile complete (markdown + sourced + confidence-rated + schema-v2 CSV row): 607
- Remaining (unresearched + partial + deep legacy, combined): 102

Note: from org #398 onward (~Looping/M-names onward), profiles use a leaner format at the
user's request to increase throughput: 1-2 sources per org instead of 2-4, ~50-word overview/
~75-word business model instead of 100/150-200, terser bullet-style sections, 1-2 line
Verification Notes. The "never invent, mark unconfirmed as Not publicly available" rule is
unchanged - only prose depth and source-count were reduced, not verification rigor.

Note: 4 completed profiles (Coca-Cola Returnables, Flo Hygiene, Bio-Home, For Earth's Sake) have corrected
names/spellings vs. the original legacy list (which had typos/wrong countries) — tracked here by their
corrected slug, not the original list's exact string.

Schema: `data/REUSE_V4_Master.csv` uses the expanded 34-column V4 schema (adds GitHub slug, short summary,
logo/featured image URL, SEO description, primary colour, tags, last verified/updated dates, researcher,
source count, overall confidence score, REUSE priority rating, SDGs — see README for full method).
Generated mechanically from each org's markdown profile via `scripts/parse_md_to_csv.py` — free to re-run,
no API calls needed, so CSV regeneration never costs research budget.

## Unresearched organisations (priority batch)

- [x] L'Occitane — global brand; PH listing is a retail market, not a distinct subsidiary; see organisations/l-occitane.md
- [x] Akomeya — see organisations/akomeya.md
- [x] Alima Pure — CEASED (~2025); country corrected US not Canada; see organisations/alima-pure.md
- [x] Allas — Indonesia; NGO-incubated venture (Enviu/Zero Waste Living Lab); see organisations/allas.md
- [x] Almang Market — see organisations/almang-market.md
- [x] Bio C' Bon — Japan; joint venture Aeon/Marne & Finance; see organisations/bio-c-bon.md
- [x] Bio-Home — Singapore; brand of Lam Soon; see organisations/bio-home.md
- [x] Coca-Cola Returnables — Brazil; multi-bottler packaging program, not a standalone company; see organisations/coca-cola-returnables.md
- [x] ECCBC / UNIDO PET pilot — Morocco; recycling/material-recovery pilot, not a reuse programme; see organisations/eccbc-unido-pet-pilot.md
- [x] EcoNowCA — US; active but consolidating locations; see organisations/econowca.md
- [x] Ernie's Zero Waste Shop — UK; independent refill shop, founded 2019; see organisations/ernies-zero-waste-shop.md
- [x] Evy Café — Switzerland; sparse/no verified reuse activity found; see organisations/evy-cafe.md
- [x] Flo Hygiene — Nepal; parent co. TNT Hygiene; see organisations/flo-hygiene.md
- [x] For Earth's Sake — country corrected UK not India; see organisations/for-earths-sake.md
- [x] Green Joy — Vietnam; materials-substitution manufacturer, not core reuse; see organisations/green-joy.md
- [ ] Green Upshot
- [ ] Hoa Đất – Tiêu dùng an lành
- [ ] HRK Group
- [ ] KinkoCare
- [ ] Let’s Get Naked Refill
- [ ] Maria Granel
- [ ] Mi Barrio Sin Residuos (UNDP project)
- [ ] miniml
- [ ] Moon Berry Made
- [ ] Mottainai Refill
- [ ] Mottainai Refill
- [ ] Mottainai Refill
- [x] My Naked Bar — see organisations/my-naked-bar.md
- [x] MyEarth — actually L'earth (S) Pte Ltd, Singapore; bio-composite single-use, low relevance; see organisations/myearth.md
- [x] mymizu — Japan + Philippines chapter (Mymizu PH); see organisations/mymizu.md, organisations/mymizu-ph.md
- [x] Nashonuma — see organisations/nashonuma.md
- [x] Net Zero Co. — see organisations/net-zero-co.md
- [x] O Granel da Sofia — see organisations/o-granel-da-sofia.md
- [x] Ong Hut Co — Vietnam; single-use biodegradable straws, not reuse; see organisations/ong-hut-co.md
- [x] Ozarka — Netherlands; site is live (seed's "broken" note was wrong); see organisations/ozarka.md
- [x] Packaging Cluster / Green Impackt — lead org is Spain-based, Green Impackt is EU-funded Colombia programme; see organisations/packaging-cluster-green-impackt.md
- [x] Pakpet — Pakistan; no dedicated reuse/refill line found, low-confidence inclusion; see organisations/pakpet.md
- [x] Paraguay Sin Basura (“Reduce” guide) — see organisations/paraguay-sin-basura.md
- [x] Pfaffhüsli — see organisations/pfaffhusli.md
- [x] Pizza 4P’s — see organisations/pizza-4ps.md
- [x] PolyLayerTech — see organisations/polylayertech.md
- [x] Rampe5 ZeroWaste Ladencafé — Zurich; see organisations/rampe5-zerowaste-ladencafe.md
- [x] Re-up Refill — merged w/ duplicate seed row "Re up Refills"; see organisations/re-up-refills.md
- [x] Recicla y Reusa Venezuela — no matching org confirmed publicly; thin profile per rules; see organisations/recicla-y-reusa-venezuela.md
- [x] Reciclaje Moreno (AIM2Flourish) — no matching org confirmed publicly; thin profile per rules; see organisations/reciclaje-moreno-aim2flourish.md
- [x] Reciclarte — no matching org confirmed publicly; thin profile per rules; see organisations/reciclarte.md
- [ ] rĒCo Refillery
- [ ] Refill
- [x] Refill H2O – IPVC — Portugal; university IoT refill pilot; see organisations/refill-h2o-ipvc.md
- [x] Refiller Mobile — Malaysia; see organisations/refiller-mobile.md
- [x] Replenish Refillery & Zero Waste Store — Canada; confirmed independent of the similarly-named US company; see organisations/replenish-refillery-canada.md
- [x] Reuso.io — US; see organisations/reuso-io.md
- [x] Sanima — see organisations/sanima.md
- [x] Sankoty Sustainables — see organisations/sankoty-sustainables.md
- [x] Saponetti — merged w/ duplicate seed row "Saponetti Soaps"; see organisations/saponetti.md
- [x] Saponetti Soaps — merged into organisations/saponetti.md
- [x] Savonnerie des Diligences — see organisations/savonnerie-des-diligences.md
- [x] Searious Business – MOSSUP — Morocco pilot; see organisations/searious-business-mossup.md
- [x] Seeker's spirits — see organisations/seekers-spirits.md
- [x] Shuangti — see organisations/shuangti.md
- [x] Slo Store — see organisations/slo-store.md
- [x] SmartFilter — see organisations/smartfilter.md
- [x] SOCSE — see organisations/socse.md
- [x] Solid — see organisations/solid-oral-care.md
- [x] Sonora Reffilery — actual name Sonora Refillery; see organisations/sonora-reffilery.md
- [x] Spruce Refill — merged w/ duplicate seed row "Spruce"; see organisations/spruce.md
- [x] Sun Moon Rain — see organisations/sun-moon-rain.md
- [x] Sunrise Straws — actual name Sunbird Straws; see organisations/sunbird-straws.md
- [x] Sunsilk — Unilever refill programme, Pakistan; see organisations/sunsilk-pakistan-refill.md
- [x] Sustenir — seed miscategorised; actually a vertical-farming co, no reuse activity; see organisations/sustenir.md
- [x] Tạp Hóa Lá Xanh — see organisations/tap-hoa-la-xanh.md
- [x] Tarım Kredi Sıfır Market — see organisations/tarim-kredi-sifir-market.md
- [x] Tetra Pak Paraguay — see organisations/tetra-pak-paraguay.md
- [x] The Ditty Bag — see organisations/the-ditty-bag.md
- [x] The Green Bee — see organisations/the-green-bee.md
- [ ] The Mayan Collective
- [ ] The Nature Masons
- [ ] The Purest Solutions
- [ ] The Refillary Storehouse
- [ ] The Sustainability Project
- [ ] The Tare Market
- [ ] The Unwaste Shop
- [ ] The Wallet Shop
- [ ] The Wally Shop
- [ ] The Waste Free Co.
- [ ] Tip Toe Eco Marketplace
- [ ] TNT Bags
- [ ] Touch the Toes
- [ ] TRAMUCO (via COOPI initiative)
- [ ] Trash Hero Czech Republic 
- [ ] Trashit
- [ ] Unibag
- [ ] Unilever Colombia (FAB, Dirt is Good)
- [ ] Unit Goods
- [ ] Unpackaged Eco (potentially closed?)
- [ ] V’s HOME – Veggie Restaurant & Café
- [ ] Venezolana de Reciclaje, C.A.
- [ ] Venezuela Refill Initiative
- [ ] VerdeMar
- [ ] Vermont Soap
- [ ] Village General Store
- [ ] Wasteupso Zero-Waste Shop
- [ ] Well Spent Grain
- [ ] Wheedle
- [ ] Woosh Water
- [ ] XICLO / Biocírculo
- [ ] XXL Refill
- [ ] Your Sustainable store
- [ ] Zero Waste Harare (women‑led)
- [ ] Zero Waste Reserve
- [ ] Zero Waste Store
- [ ] Zeropolitan
- [ ] Zerosporo
