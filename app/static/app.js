/* RefundRadar front end. Vanilla JS; everything rendered from the /api report. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const fmt = (n) => "$" + Math.round(n || 0).toLocaleString("en-US");
  const fmt2 = (n) => "$" + (n || 0).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const dateFmt = (iso) => iso ? new Date(iso + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : "";
  const shortDate = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" });

  let report = null;
  let filter = null;
  let shown = 40;

  const GROUPS = [
    { key: "cape_now", label: "File in CBP's refund tool now", tone: "good" },
    { key: "fix_first", label: "Fix, then file", tone: "warn" },
    { key: "protest", label: "Protest before the deadline", tone: "warn" },
    { key: "review", label: "Ask your broker", tone: "warn" },
    { key: "waiting", label: "Waiting on CBP", tone: "neutral" },
    { key: "blocked", label: "Blocked for now", tone: "bad" },
    { key: "litigation", label: "Court route only", tone: "bad" },
    { key: "someone", label: "Someone else holds the claim", tone: "pink" },
    { key: "not_eligible", label: "Not eligible", tone: "neutral" },
  ];
  const groupOf = (r) => (r.holder !== "you" && r.principal > 0 ? "someone" : r.bucket);
  const groupLabel = Object.fromEntries(GROUPS.map((g) => [g.key, g]));

  // ---------- start screen ----------
  $$(".seg").forEach((seg) => seg.addEventListener("click", (e) => {
    const b = e.target.closest("button"); if (!b) return;
    $$("button", seg).forEach((x) => x.classList.toggle("on", x === b));
  }));
  $("#csvInput").addEventListener("change", (e) => {
    const f = e.target.files[0]; const el = $("#csvName");
    el.textContent = f ? f.name : "No file chosen"; el.classList.toggle("set", !!f);
  });
  $("#photoInput").addEventListener("change", (e) => {
    const n = e.target.files.length; const el = $("#photoName");
    el.textContent = n ? `${n} photo${n > 1 ? "s" : ""} chosen` : "No photos chosen"; el.classList.toggle("set", n > 0);
  });

  function profile() {
    const p = { importer_number: $("[name=importer_number]").value.trim() };
    $$(".seg").forEach((seg) => {
      const v = $("button.on", seg)?.dataset.v;
      p[seg.dataset.name] = v === "true" ? true : v === "false" ? false : "unknown";
    });
    return p;
  }

  function showWorking(steps) {
    $("#start").hidden = true; $("#results").hidden = true; $("#working").hidden = false;
    const ol = $("#workSteps"); ol.innerHTML = "";
    steps.forEach((s, i) => {
      const li = document.createElement("li");
      li.className = i === 0 ? "doing" : "";
      li.innerHTML = `<span>${esc(s.label)}</span><span class="m">${esc(s.model || "Rule engine")}</span>`;
      ol.appendChild(li);
    });
    let i = 0;
    return setInterval(() => {
      const lis = $$("li", ol); if (i < lis.length - 1) { lis[i].className = "done"; i++; lis[i].className = "doing"; }
    }, 1400);
  }

  async function run(fetcher, steps) {
    const timer = showWorking(steps);
    try {
      const res = await fetcher();
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong.");
      clearInterval(timer);
      render(data);
    } catch (err) {
      clearInterval(timer);
      $("#working").hidden = true; $("#start").hidden = false;
      alert(err.message);
    }
  }

  $("#sampleBtn").addEventListener("click", () => run(() => fetch("/api/sample"), [
    { label: "Reading the sample ES-003 export" }, { label: "Reading 3 form photos", model: "Nemotron 3.5 Super VL" },
    { label: "Applying CBP's refund rules" },
  ]));

  $("#upload").addEventListener("submit", (e) => {
    e.preventDefault();
    const fd = new FormData();
    const csv = $("#csvInput").files[0]; if (csv) fd.append("csv_file", csv);
    [...$("#photoInput").files].forEach((f) => fd.append("photos", f));
    if (!csv && !$("#photoInput").files.length) { alert("Add an ES-003 export or photos of your entry summaries."); return; }
    fd.append("profile", JSON.stringify(profile()));
    const steps = [];
    if (csv) steps.push({ label: "Reading your spreadsheet" });
    if ($("#photoInput").files.length) steps.push({ label: "Reading your form photos", model: "Nemotron 3.5 Super VL" });
    steps.push({ label: "Applying CBP's refund rules" });
    run(() => fetch("/api/analyze", { method: "POST", body: fd }), steps);
  });

  $("#backBtn").addEventListener("click", () => { $("#results").hidden = true; $("#start").hidden = false; window.scrollTo(0, 0); });

  // ---------- results ----------
  function render(data) {
    report = data; filter = null; shown = 40;
    $("#working").hidden = true; $("#results").hidden = false; window.scrollTo(0, 0);
    $("#demoNote").hidden = !data.demo;
    renderVerdict(); renderStop(); renderRadar(); renderBuckets(); renderBlockers(); renderTable();
    renderPhotos(); renderCosts(); renderDownloads(); renderHow();
    $("#planBody").innerHTML = `<button class="btn ghost" id="planBtn" type="button">Write my plan</button>`;
    $("#planBtn").addEventListener("click", loadPlan);
    if (data.demo) loadPlan();
    $("#offerResult").innerHTML = ""; $("#offerText").value = "";
  }

  function renderVerdict() {
    const h = report.headline;
    let t = `You can claim <span class="amt good">${fmt(h.reachable_now)}</span> now.`;
    if (h.urgent_count) t += ` <span class="amt bad">${fmt(h.urgent_amount)}</span> of it leaves CBP's refund tool within 3 weeks${h.urgent_soonest_days <= 7 ? `, the first in ${h.urgent_soonest_days} day${h.urgent_soonest_days === 1 ? "" : "s"}` : ""}.`;
    if (!h.reachable_now) t = `Nothing on these entries can go through CBP's refund tool today.`;
    $("#verdictText").innerHTML = t;
    const parts = [];
    if (h.protest_amount) parts.push(`${fmt(h.protest_amount)} needs a protest before its deadline`);
    if (h.litigation_amount) parts.push(`${fmt(h.litigation_amount)} can only be recovered in court or through the class action`);
    if (h.someone_else_amount) parts.push(`${fmt(h.someone_else_amount)} sits on entries where someone else was the importer of record`);
    const tail = parts.length ? " " + (parts.length > 1 ? parts.slice(0, -1).join("; ") + "; and " + parts[parts.length - 1] : parts[0]) + "." : "";
    $("#verdictSub").textContent = `Across ${h.entries} entries we found ${fmt(h.total_principal + h.total_interest)} in IEEPA duty and estimated interest.${tail}`;
  }

  function renderStop() {
    const ach = report.blockers.find((b) => b.key === "ach");
    const el = $("#stopBanner");
    if (!ach) { el.hidden = true; return; }
    el.hidden = false;
    el.innerHTML = `<span class="stamp">HOLD</span><strong>${esc(ach.title)}</strong><p>${esc(ach.detail)} ${esc(ach.fix)}</p>`;
  }

  // Deadline radar: weekly bars for CAPE-window closings and protest deadlines; court decision point as a marker.
  function renderRadar() {
    const weeks = report.radar.weeks;
    const today = new Date(report.today + "T12:00:00");
    const monday = (d) => { const x = new Date(d); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; };
    const start = monday(today);
    const endDate = new Date("2027-02-08T12:00:00");
    const nWeeks = Math.max(8, Math.ceil((endDate - start) / (7 * 864e5)) + 1);
    const byWeek = Object.fromEntries(weeks.map((w) => [w.week_of, w]));
    const cols = [];
    for (let i = 0; i < nWeeks; i++) {
      const d = new Date(start); d.setDate(d.getDate() + 7 * i);
      const key = d.toISOString().slice(0, 10);
      const w = byWeek[key] || { CAPE_80: [0, 0], PROTEST_180: [0, 0], CIT_2YR: [0, 0] };
      cols.push({ key, d, cape: w.CAPE_80, protest: w.PROTEST_180, cit: w.CIT_2YR });
    }
    const maxV = Math.max(1, ...cols.map((c) => c.cape[1] + c.protest[1]));
    const W = 960, H = 260, L = 56, R = 16, T = 18, B = 40, bw = (W - L - R) / nWeeks;
    const y = (v) => T + (H - T - B) * (1 - v / maxV);
    const step = niceStep(maxV);
    let svg = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">`;
    for (let v = 0; v <= maxV + 1; v += step) svg += `<line class="axis" x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke-opacity="${v ? .35 : 1}"/><text x="${L - 8}" y="${y(v) + 4}" text-anchor="end">${v >= 1000 ? "$" + Math.round(v / 1000) + "k" : "$" + v}</text>`;
    cols.forEach((c, i) => {
      const x = L + i * bw + bw * 0.16, w = bw * 0.68;
      const hc = (H - T - B) * c.cape[1] / maxV, hp = (H - T - B) * c.protest[1] / maxV;
      const base = H - B;
      if (c.protest[1]) svg += `<rect class="bar grow" data-i="${i}" x="${x}" y="${base - hc - hp}" width="${w}" height="${hp}" fill="var(--canary)" style="animation-delay:${i * 30}ms"/>`;
      if (c.cape[1]) svg += `<rect class="bar grow" data-i="${i}" x="${x}" y="${base - hc}" width="${w}" height="${hc}" fill="var(--stamp)" style="animation-delay:${i * 30}ms"/>`;
      svg += `<rect class="bar" data-i="${i}" x="${L + i * bw}" y="${T}" width="${bw}" height="${H - T - B}" fill="transparent"/>`;
      if (i % 2 === 0) svg += `<text x="${L + i * bw + bw / 2}" y="${H - B + 18}" text-anchor="middle">${shortDate(c.key)}</text>`;
    });
    // today + milestones
    svg += `<line class="today" x1="${L + bw * ((today - start) / (7 * 864e5))}" x2="${L + bw * ((today - start) / (7 * 864e5))}" y1="${T - 6}" y2="${H - B}"/><text x="${L + 4}" y="${T - 4}">Today</text>`;
    report.radar.milestones.forEach((m) => {
      const d = new Date(m.date + "T12:00:00"); const xi = (d - start) / (7 * 864e5);
      if (xi < 0 || xi > nWeeks) return;
      const x = L + bw * xi;
      svg += `<line class="ms" x1="${x}" x2="${x}" y1="${T}" y2="${H - B}"/>`;
    });
    const citCol = cols.findIndex((c) => c.cit[1] > 0);
    if (citCol >= 0) {
      const x = L + citCol * bw + bw / 2;
      svg += `<circle cx="${x}" cy="${y(maxV * 0.62)}" r="7" fill="var(--slate)"/><text x="${x - 10}" y="${y(maxV * 0.62) - 14}" text-anchor="end">${fmt(cols[citCol].cit[1])} court-only</text>`;
    }
    svg += `</svg>`;
    const chart = $("#radarChart");
    chart.innerHTML = svg;
    const capeTotal = cols.reduce((s, c) => s + c.cape[1], 0);
    chart.setAttribute("aria-label", `Deadline radar: ${fmt(capeTotal)} leaves the CAPE window between now and February 2027.`);
    const readout = (i) => {
      const c = cols[i]; const bits = [];
      if (c.cape[0]) bits.push(`${c.cape[0]} entr${c.cape[0] > 1 ? "ies" : "y"} (${fmt(c.cape[1])}) leave the refund tool window`);
      if (c.protest[0]) bits.push(`${c.protest[0]} reach${c.protest[0] > 1 ? "" : "es"} the protest deadline (${fmt(c.protest[1])})`);
      if (c.cit[0]) bits.push(`court-filing decision point for ${c.cit[0]} entries (${fmt(c.cit[1])})`);
      $("#radarReadout").textContent = `Week of ${dateFmt(c.key)}: ` + (bits.join("; ") || "nothing due.");
      $$(".bar", chart).forEach((b) => b.classList.toggle("sel", +b.dataset.i === i));
    };
    $$(".bar", chart).forEach((b) => { b.addEventListener("mouseenter", () => readout(+b.dataset.i)); b.addEventListener("click", () => readout(+b.dataset.i)); });
    const first = cols.findIndex((c) => c.cape[0] || c.protest[0]);
    readout(first >= 0 ? first : 0);
  }
  function niceStep(max) { const raw = max / 4; const p = 10 ** Math.floor(Math.log10(raw)); return [1, 2, 2.5, 5, 10].map((m) => m * p).find((s) => s >= raw); }

  function groups() {
    const g = {};
    report.routes.forEach((r) => { const k = groupOf(r); g[k] = g[k] || { count: 0, amount: 0 }; g[k].count++; if (k !== "not_eligible") g[k].amount += r.principal + r.interest; });
    return g;
  }

  function renderBuckets() {
    const g = groups();
    const total = Object.values(g).reduce((s, x) => s + x.amount, 0) || 1;
    $("#bucketBar").innerHTML = GROUPS.filter((x) => g[x.key]?.amount > 0)
      .map((x) => `<span class="c-${x.key}" style="width:${(100 * g[x.key].amount / total).toFixed(2)}%" title="${esc(x.label)}: ${fmt(g[x.key].amount)}"></span>`).join("");
    const meta = report.bucket_meta;
    $("#bucketList").innerHTML = GROUPS.filter((x) => g[x.key]).map((x) => `
      <button type="button" class="bucket-item" data-k="${x.key}" aria-pressed="false">
        <span class="sw c-${x.key}"></span><span class="bl">${esc(x.label)}</span><span class="ba">${x.key === "not_eligible" ? "" : fmt(g[x.key].amount)}</span>
        <span class="bd">${g[x.key].count} entr${g[x.key].count > 1 ? "ies" : "y"}. ${esc(x.key === "someone" ? "The refund belongs to your courier, forwarder or supplier." : meta[x.key]?.blurb || "")}</span>
      </button>`).join("");
    $$(".bucket-item").forEach((b) => b.addEventListener("click", () => {
      filter = filter === b.dataset.k ? null : b.dataset.k; shown = 40;
      $$(".bucket-item").forEach((x) => { x.classList.toggle("sel", x.dataset.k === filter); x.setAttribute("aria-pressed", x.dataset.k === filter); });
      renderTable(); $("#entriesTitle").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
    }));
  }

  function renderBlockers() {
    const list = report.blockers;
    $("#blockerList").innerHTML = list.length ? list.map((b) => `<li class="${b.severity}"><strong>${esc(b.title)}</strong><p>${esc(b.detail)}</p><p class="fix">${esc(b.fix)}</p></li>`).join("")
      : `<li><strong>Nothing found</strong><p>No blockers in what you uploaded. Still confirm your refund bank details in ACE.</p></li>`;
  }

  async function loadPlan() {
    const body = $("#planBody");
    body.innerHTML = `<div class="skeleton" style="width:90%"></div><div class="skeleton" style="width:75%"></div><div class="skeleton" style="width:82%"></div>`;
    try {
      const res = await fetch("/api/plan", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ report_id: report.report_id }) });
      const p = await res.json();
      if (!res.ok) throw new Error(p.detail);
      $("#planMeta").textContent = p.fallback ? "Built from the rules (AI plan unavailable right now)." : "Written by Nemotron 3 Ultra from the numbers above. Check anything that matters with your broker.";
      body.innerHTML = `<p class="summary">${esc(p.summary)}</p><ol class="steps">${p.steps.map((s) => `
        <li><span class="when">${esc(s.when)}<span class="who">${esc(s.who)}</span></span><span class="do">${esc(s.do)}</span><span class="why">${esc(s.why)}</span></li>`).join("")}</ol>
        ${p.watch_outs?.length ? `<ul class="watch">${p.watch_outs.map((w) => `<li>${esc(w)}</li>`).join("")}</ul>` : ""}`;
    } catch (e) { body.innerHTML = `<p>Couldn't write the plan: ${esc(e.message)}</p><button class="btn ghost" id="planBtn" type="button">Try again</button>`; $("#planBtn").addEventListener("click", loadPlan); }
  }

  function renderTable() {
    const q = ($("#entrySearch").value || "").replace(/[^0-9a-z]/gi, "").toUpperCase();
    let rows = report.routes.filter((r) => (!filter || groupOf(r) === filter) && (!q || r.entry_number.replace(/-/g, "").includes(q)));
    $("#clearFilter").hidden = !filter;
    $("#entriesMeta").textContent = filter ? `${rows.length} entries · ${groupLabel[filter].label}` : `${rows.length} entries, most urgent first`;
    const tb = $("#entryTable tbody");
    tb.innerHTML = rows.slice(0, shown).map((r) => {
      const g = groupLabel[groupOf(r)];
      const soon = r.days_left !== null && r.days_left <= 14 && r.days_left >= 0;
      const dl = r.deadline ? `<span class="${soon ? "dl-soon" : ""}">${dateFmt(r.deadline)}</span><br><small>${r.days_left >= 0 ? r.days_left + " days left" : "passed"}${r.liquidation_estimated ? " · estimated" : ""}</small>` : "—";
      return `<tr tabindex="0" data-e="${esc(r.entry_number)}"><td><span class="en">${esc(r.entry_number)}</span>${r.source?.startsWith?.("photo") ? '<br><span class="tag neutral">from photo</span>' : ""}</td>
        <td>${esc(r.title)}<br><span class="tag ${g.tone}">${esc(g.label)}</span></td><td class="num">${fmt2(r.principal)}</td><td class="num">${fmt2(r.interest)}</td><td>${dl}</td></tr>`;
    }).join("");
    $("#moreRows").hidden = rows.length <= shown;
    $$("#entryTable tbody tr").forEach((tr) => {
      tr.addEventListener("click", () => openEntry(tr.dataset.e));
      tr.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openEntry(tr.dataset.e); } });
    });
  }
  $("#entrySearch").addEventListener("input", () => { shown = 40; renderTable(); });
  $("#clearFilter").addEventListener("click", () => { filter = null; $$(".bucket-item").forEach((x) => x.classList.remove("sel")); renderTable(); });
  $("#moreRows").addEventListener("click", () => { shown += 60; renderTable(); });

  function openEntry(num) {
    const r = report.routes.find((x) => x.entry_number === num); if (!r) return;
    const g = groupLabel[groupOf(r)];
    $("#drawerBody").innerHTML = `
      <span class="tag ${g.tone}">${esc(g.label)}</span>
      <h3>${esc(r.title)}</h3>
      <p>${esc(r.action)}</p>
      <dl class="kv">
        <dt>Entry</dt><dd class="en">${esc(r.entry_number)}</dd>
        <dt>IEEPA duty (est.)</dt><dd>${fmt2(r.principal)}</dd>
        <dt>Interest (est.)</dt><dd>${fmt2(r.interest)}</dd>
        <dt>Tariff programs</dt><dd>${esc(r.programs.join(", ") || "—")}</dd>
        <dt>Liquidated</dt><dd>${r.liquidation_date ? dateFmt(r.liquidation_date) + (r.liquidation_estimated ? " (estimated)" : "") : "Not yet"}</dd>
        <dt>Deadline</dt><dd>${r.deadline ? dateFmt(r.deadline) + ` (${r.days_left} days)` : "—"}</dd>
        <dt>Rule</dt><dd>${esc(r.rule_id)} · confidence ${esc({ P: "primary source", S: "secondary source", U: "unconfirmed" }[r.tag])}</dd>
      </dl>
      ${r.notes.length ? `<ul>${r.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>` : ""}
      ${r.entry_problems.length ? `<p class="dl-soon">${r.entry_problems.map(esc).join(". ")}</p>` : ""}
      <div class="explain" id="explainBox"><button class="btn ghost" id="explainBtn" type="button">Explain this in plain English</button></div>
      <p class="src">Sources: ${esc(r.sources.join("; "))}</p>`;
    $("#explainBtn").addEventListener("click", async () => {
      const box = $("#explainBox"); box.innerHTML = `<div class="skeleton"></div><div class="skeleton" style="width:70%"></div>`;
      const res = await fetch("/api/explain", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ report_id: report.report_id, entry_number: num }) });
      const d = await res.json();
      box.innerHTML = `<p>${esc(d.text || d.detail)}</p><p class="src">${d.fallback ? "From the rule catalog (AI unavailable)." : "Nemotron 3 Ultra, from this entry's facts and rule."}</p>`;
    });
    $("#drawer").showModal();
  }

  function renderPhotos() {
    const grid = report.review_grid || [];
    $("#photosSec").hidden = !grid.length;
    const mine = (report.profile?.importer_number || "").replace(/[^0-9A-Z]/gi, "").toUpperCase();
    $("#photoGrid").innerHTML = grid.map((p) => {
      const f = p.fields; const theirs = (f.importer_number || "").replace(/[^0-9A-Z]/gi, "").toUpperCase();
      const other = mine && theirs && mine !== theirs;
      const lineTxt = (f.lines || []).map((l) => l.hts_numbers.map((h, i) => `${h} · ${fmt2(l.duties[i] || 0)}`).join("<br>")).join("<br>");
      return `<article class="photo-card">${p.url ? `<img src="${p.url}" alt="Photo of entry summary ${esc(f.entry_number)}" loading="lazy">` : `<div></div>`}
        <div class="form-fields">
          <div class="ff"><span>1. Entry no.</span><b>${esc(f.entry_number)}</b></div>
          <div class="ff"><span>2. Entry type</span><b>${esc(f.entry_type)}</b></div>
          <div class="ff"><span>7. Entry date</span><b>${esc(f.entry_date)}</b></div>
          <div class="ff ${other ? "alert" : ""}"><span>23. Importer no.</span><b>${esc(f.importer_number)}</b></div>
          <div class="ff ${other ? "alert" : ""}"><span>26. Importer of record</span><b>${esc(f.importer_name)}</b></div>
          <div class="ff wide"><span>29 / 34. Tariff lines and duty</span><b>${lineTxt}</b></div>
          <div class="ff"><span>37. Duty total</span><b>${fmt2(f.total_duty)}</b></div>
          ${other ? `<p class="holder-note">The importer of record here is <strong>${esc(f.importer_name)}</strong>, not you, so this refund belongs to them. Ask them to file and pass it through.</p>` : ""}
        </div></article>`;
    }).join("");
  }

  function renderCosts() {
    const h = report.headline;
    $("#costMeta").textContent = h.reachable_now_count
      ? `For the ${h.reachable_now_count} entries you can file now (about ${fmt(h.reachable_now)} with interest).`
      : "No entries can be filed in CBP's refund tool right now.";
    const maxPct = Math.max(...report.costs.map((c) => c.effective_pct));
    $("#costTable tbody").innerHTML = report.costs.map((c) => `<tr class="${c.key === "self" ? "best" : c.effective_pct === maxPct ? "worst" : ""}">
      <td><strong>${esc(c.label)}</strong><br><small>${esc(c.caveat)}</small></td><td>${esc(c.how)}</td>
      <td class="num">${fmt(c.fee)}</td><td class="num">${fmt(c.net)}</td><td class="num">${c.effective_pct}%</td></tr>`).join("");
  }

  // ---------- offer check ----------
  $("#offerSample").addEventListener("click", async () => {
    const t = await (await fetch("/api/sample/files/refund_offer_email.txt")).text();
    $("#offerText").value = t; $("#offerText").dataset.sample = "1";
  });
  $("#offerText").addEventListener("input", () => { delete $("#offerText").dataset.sample; });
  $("#offerBtn").addEventListener("click", async () => {
    const text = $("#offerText").value.trim(); const out = $("#offerResult");
    if (text.length < 20) { out.innerHTML = "<p>Paste the offer text first.</p>"; return; }
    $("#offerBtn").disabled = true; out.innerHTML = `<div class="skeleton"></div><div class="skeleton" style="width:60%"></div>`;
    try {
      const res = await fetch("/api/offer", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ report_id: report.report_id, text, use_sample: !!$("#offerText").dataset.sample }) });
      const d = await res.json(); if (!res.ok) throw new Error(d.detail);
      const stamp = { likely_scam: "LIKELY SCAM", expensive: "EXPENSIVE", reasonable: "LOOKS FAIR", unclear: "UNCLEAR" }[d.verdict] || "UNCLEAR";
      const flagNames = { asks_for_ace_login: "Asks for your ACE login", asks_for_bank_details: "Asks for your bank details", claims_to_be_cbp_or_government: "Implies it acts for CBP or the government",
        unsolicited_contact: "Unsolicited contact", urgency_pressure: "Pressure to act fast", upfront_payment: "Upfront fee", guarantees_refund: "Guarantees a refund",
        vague_fees: "Vague fees", processes_refunds_outside_ace: "Claims to process refunds outside ACE", qr_code_or_link_to_pay: "QR code or payment link", other: "Other concern" };
      out.innerHTML = `<div class="offer-verdict ${esc(d.verdict)}"><span class="stamp">${stamp}</span>
        <strong>On your numbers this offer would cost ${fmt(d.cost_on_your_numbers)} (${d.effective_pct}% of your claimable refund).</strong>
        <p>${esc(d.advice)}</p>
        <div>${d.red_flags?.length ? `<ul class="flags">${d.red_flags.map((f) => `<li><strong>${esc(flagNames[f.flag] || f.flag)}</strong>${f.evidence ? ` — <q>${esc(f.evidence)}</q>` : ""}</li>`).join("")}</ul>` : "<p>No red flags found.</p>"}
        ${d.web_results?.length ? `<p class="web">What the web says about ${esc(d.company_name)} (Tavily): ${d.web_results.slice(0, 3).map((w) => `<a href="${esc(w.url)}" target="_blank" rel="noopener">${esc(w.title)}</a>`).join(" · ")}</p>`
          : d.company_name ? `<p class="web">Tavily found no independent record of ${esc(d.company_name)}.</p>` : ""}
        ${d.fallback ? `<p class="web">Pattern check only; AI review unavailable right now.</p>` : ""}</div></div>`;
    } catch (e) { out.innerHTML = `<p>Couldn't check the offer: ${esc(e.message)}</p>`; }
    $("#offerBtn").disabled = false;
  });

  function renderDownloads() {
    const base = `/api/export/${report.report_id}/`;
    $("#dlList").href = base + "broker_entry_list.csv"; $("#dlSheet").href = base + "worksheet.csv"; $("#dlIcs").href = base + "deadlines.ics";
  }

  function renderHow() {
    const calls = report.calls || [];
    const steps = report.pipeline || [];
    $("#howBody").innerHTML = `
      <table><thead><tr><th>Step</th><th>Detail</th><th>Done by</th></tr></thead><tbody>
        ${steps.map((s) => `<tr><td>${esc(s.step)}</td><td>${esc(s.detail)}</td><td>${esc(s.model || "Rule engine (no AI)")}</td></tr>`).join("")}
      </tbody></table>
      ${calls.length ? `<table><thead><tr><th>Model call</th><th>Model</th><th class="num">Seconds</th><th class="num">Tokens in/out</th><th class="num">Cost</th></tr></thead><tbody>
        ${calls.map((c) => `<tr><td>${esc(c.purpose)}</td><td>${esc(c.model_id)}</td><td class="num">${c.seconds}</td><td class="num">${c.tokens_in}/${c.tokens_out}</td><td class="num">$${c.cost_usd.toFixed(4)}</td></tr>`).join("")}
      </tbody></table>` : ""}
      <p>Routes, deadlines and amounts come from a tested rule engine (21 routing rules from CBP CSMS messages, CBP's CAPE guide, court orders and statutes, each tagged by confidence). AI models read documents, write the plan and explanations, and check offers; they never set amounts or deadlines. Rules verified ${dateFmt(report.rules_verified_as_of)}.</p>
      <p>Interest is estimated at CBP's quarterly overpayment rate, compounded daily, from an estimated deposit date to the expected liquidation date. Confirm amounts in ACE reports ES-022 and REV-603.</p>`;
  }

  // ---------- rules freshness ----------
  fetch("/api/freshness").then((r) => r.json()).then((f) => {
    const b = $("#freshBtn");
    if (f.checked && f.changed) { b.classList.add("changed"); b.textContent = "CBP guidance may have changed"; }
    else if (f.checked) { b.classList.add("ok"); b.textContent = "Rules checked today"; }
    b.addEventListener("click", () => {
      $("#drawerBody").innerHTML = `<h3>Is the rule set current?</h3>
        <p>Our routing rules were verified against CBP and court sources on ${dateFmt(f.rules_verified_as_of)}. ${f.checked ? "Today Tavily searched recent news and Nemotron Nano checked it for changes." : "Live checking isn't available right now."}</p>
        ${f.items?.length ? `<ul>${f.items.map((i) => `<li><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.what)}</a> <small>${esc(i.date)}</small></li>`).join("")}</ul>` : f.checked ? "<p>No changes found since then.</p>" : ""}
        <p class="src">Pending: CBP status report (Oct 26), settlement conference (Oct 27), class scheduling order (Nov 5), Federal Circuit appeal.</p>`;
      $("#drawer").showModal();
    });
  }).catch(() => {});
})();
