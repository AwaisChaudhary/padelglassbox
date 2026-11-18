/* Padel Glass Box interactions */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var D = window.PP || {};
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var t;
  function toast(m) {
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = m; t.classList.add("show"); clearTimeout(t.x); t.x = setTimeout(function () { t.classList.remove("show"); }, 1800);
  }
  var head = $(".head"), bg = $(".burger");
  if (bg) bg.addEventListener("click", function () { var o = head.classList.toggle("open"); bg.setAttribute("aria-expanded", o); });

  function choose(group, cb) {
    $$("button", group).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("button", group).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true"); cb(b.dataset.v);
      });
    });
  }

  /* ---------- racket finder ---------- */
  var RS = {
    round: '<svg class="racket-svg" viewBox="0 0 120 200" aria-hidden="true"><ellipse cx="60" cy="62" rx="50" ry="56" fill="#d4f53c"/><g fill="#0b1530">' + holes(60, 62, 34, 38) + '</g><rect x="52" y="116" width="16" height="70" rx="7" fill="#d4f53c"/></svg>',
    teardrop: '<svg class="racket-svg" viewBox="0 0 120 200" aria-hidden="true"><path d="M60 6 C108 6 114 50 106 78 C98 104 76 118 60 120 C44 118 22 104 14 78 C6 50 12 6 60 6Z" fill="#d4f53c"/><g fill="#0b1530">' + holes(60, 58, 32, 36) + '</g><rect x="52" y="116" width="16" height="70" rx="7" fill="#d4f53c"/></svg>',
    diamond: '<svg class="racket-svg" viewBox="0 0 120 200" aria-hidden="true"><path d="M60 4 C90 4 112 18 112 40 L104 76 C96 100 76 118 60 120 C44 118 24 100 16 76 L8 40 C8 18 30 4 60 4Z" fill="#d4f53c"/><g fill="#0b1530">' + holes(60, 50, 34, 30) + '</g><rect x="52" y="116" width="16" height="70" rx="7" fill="#d4f53c"/></svg>'
  };
  function holes(cx, cy, rx, ry) {
    var s = "";
    for (var y = -ry; y <= ry; y += 12) for (var x = -rx; x <= rx; x += 12) {
      if ((x * x) / (rx * rx) + (y * y) / (ry * ry) <= 1) s += '<circle cx="' + (cx + x) + '" cy="' + (cy + y) + '" r="2.6"/>';
    }
    return s;
  }
  var quiz = $("#quiz");
  if (quiz) {
    var A = { level: "new", style: "control", arm: "no" };
    var out = $("#result");
    var draw = function () {
      var shape, bal, wt, core, face, ctrl, pow, why = [];
      if (A.level === "new") { shape = "round"; why.push("Round rackets have the biggest, most central sweet spot, so mis-hits still go over."); }
      else if (A.level === "improving") { shape = A.style === "control" ? "round" : "teardrop"; why.push(shape === "round" ? "You like control, so a round head still suits you." : "A teardrop mixes control and power while you develop."); }
      else { shape = A.style === "attack" ? "diamond" : A.style === "allround" ? "teardrop" : "round"; why.push(shape === "diamond" ? "Diamond rackets put weight towards the tip for power, but need clean technique." : shape === "teardrop" ? "A teardrop gives an all-court balance of power and control." : "Many top players still pick round rackets for control."); }
      bal = { round: "Low (towards the handle)", teardrop: "Medium", diamond: "High (towards the head)" }[shape];
      var lo = 355, hi = 365;
      if (A.level === "new") { lo = 345; hi = 360; }
      if (A.level === "advanced" && A.style === "attack") { lo = 360; hi = 375; }
      if (A.arm === "yes") { lo -= 10; hi -= 10; why.push("A lighter racket with a soft core is kinder to sore elbows and shoulders."); }
      wt = lo + " to " + hi + " g";
      core = A.arm === "yes" || A.level === "new" ? "Soft foam (comfortable, easy power)" : A.level === "advanced" && A.style === "attack" ? "Harder foam (more control at high speed)" : "Medium foam";
      face = A.arm === "yes" || A.level === "new" ? "Fiberglass (softer, more forgiving)" : A.level === "advanced" ? "Carbon (stiffer, more precise)" : "Fiberglass or a carbon mix";
      ctrl = { round: 90, teardrop: 65, diamond: 40 }[shape]; pow = { round: 45, teardrop: 70, diamond: 92 }[shape];
      out.innerHTML = RS[shape] + '<span class="pill b">Your match</span><h2 style="margin-top:10px">' + shape.charAt(0).toUpperCase() + shape.slice(1) + ' racket</h2>' +
        '<dl class="spec"><dt>Balance</dt><dd>' + bal + "</dd><dt>Weight</dt><dd>" + wt + "</dd><dt>Core</dt><dd>" + core + "</dd><dt>Face</dt><dd>" + face + "</dd></dl>" +
        '<div style="clear:both"></div><div style="display:grid;gap:8px;margin:8px 0 14px"><div><small>Control</small><div class="meter"><i style="width:' + ctrl + '%"></i></div></div><div><small>Power</small><div class="meter"><i style="width:' + pow + '%"></i></div></div></div>' +
        "<p>" + why.join(" ") + "</p>" + '<div class="btns"><button class="btn lime sm" type="button" id="copy-fit">Copy my racket profile</button></div>';
      $("#copy-fit").addEventListener("click", function () {
        var txt = "My padel racket profile: " + shape + " shape, " + bal.toLowerCase() + " balance, " + wt + ", " + core.toLowerCase() + ", " + face.toLowerCase() + ".";
        navigator.clipboard.writeText(txt).then(function () { toast("Profile copied"); }, function () { toast("Copy blocked here"); });
      });
    };
    $$("[data-q]", quiz).forEach(function (g) { choose(g, function (v) { A[g.dataset.q] = v; draw(); }); });
    draw();
  }

  /* ---------- score keeper ---------- */
  var sc = $("#score");
  if (sc) {
    var L = ["0", "15", "30", "40"];
    var S = store.get("pp-score", null) || { p: [0, 0], g: [0, 0], sets: [], srv: 0, mode: "adv", tb: false, done: false, names: ["Team A", "Team B"] };
    var hist = [];
    var save = function () { store.set("pp-score", S); };
    var label = function (i) {
      var me = S.p[i], them = S.p[1 - i];
      if (S.tb) return String(me);
      if (me >= 3 && them >= 3) { if (S.mode === "golden" || me === them) return "40"; return me > them ? "AD" : "40"; }
      return L[Math.min(me, 3)];
    };
    var render = function () {
      [0, 1].forEach(function (i) {
        var b = $('.team[data-i="' + i + '"]', sc);
        $(".pts", b).textContent = label(i);
        $(".gs", b).textContent = "Games " + S.g[i] + (S.sets.length ? " · Sets " + S.sets.filter(function (s) { return s[i] > s[1 - i]; }).length : "");
        $(".srv", b).style.visibility = S.srv === i ? "visible" : "hidden";
        $(".tname", b).textContent = S.names[i];
      });
      $("#sets").innerHTML = S.sets.map(function (s, n) { return "<span>Set " + (n + 1) + ": " + s[0] + "-" + s[1] + "</span>"; }).join("") + (S.done ? "" : "<span>Now: " + S.g[0] + "-" + S.g[1] + (S.tb ? " (tie-break)" : "") + "</span>");
      var m = "";
      if (S.done) m = S.names[S.sets.filter(function (s) { return s[0] > s[1]; }).length >= 2 ? 0 : 1] + " win the match!";
      else if (!S.tb && S.p[0] >= 3 && S.p[1] >= 3 && S.p[0] === S.p[1]) m = S.mode === "golden" ? "Golden point! The receiving pair picks the side." : "Deuce";
      else if (S.tb) m = "Tie-break: first to 7, two clear.";
      $("#msg").textContent = m;
      $$("#mode button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === S.mode); });
      save();
    };
    var winGame = function (i) {
      S.g[i]++; S.p = [0, 0]; S.srv = 1 - S.srv;
      var a = S.g[i], b = S.g[1 - i];
      if (S.tb || (a >= 6 && a - b >= 2)) {
        S.sets.push(S.g.slice()); S.g = [0, 0]; S.tb = false;
        var won = S.sets.filter(function (s) { return s[i] > s[1 - i]; }).length;
        if (won >= 2) S.done = true;
      } else if (S.g[0] === 6 && S.g[1] === 6) { S.tb = true; }
    };
    var point = function (i) {
      if (S.done) return;
      hist.push(JSON.stringify(S));
      S.p[i]++;
      var me = S.p[i], them = S.p[1 - i];
      if (S.tb) { if (me >= 7 && me - them >= 2) winGame(i); }
      else if (S.mode === "golden") { if (me >= 4) winGame(i); }
      else if (me >= 4 && me - them >= 2) winGame(i);
      else if (me >= 4 && them >= 4 && me === them) { S.p = [3, 3]; }
      if (navigator.vibrate) try { navigator.vibrate(15); } catch (e) {}
      render();
    };
    $$(".team", sc).forEach(function (b) { b.addEventListener("click", function () { point(+b.dataset.i); }); });
    $("#undo").addEventListener("click", function () { if (hist.length) { S = JSON.parse(hist.pop()); render(); } else toast("Nothing to undo"); });
    $("#reset").addEventListener("click", function () { hist.push(JSON.stringify(S)); S = { p: [0, 0], g: [0, 0], sets: [], srv: 0, mode: S.mode, tb: false, done: false, names: S.names }; render(); toast("New match"); });
    $("#swap-srv").addEventListener("click", function () { S.srv = 1 - S.srv; render(); });
    $("#rename").addEventListener("click", function () {
      var box = $("#names"); box.hidden = !box.hidden;
      if (!box.hidden) { $("#n0").value = S.names[0]; $("#n1").value = S.names[1]; $("#n0").focus(); }
    });
    $("#names").addEventListener("submit", function (e) { e.preventDefault(); S.names = [$("#n0").value.trim() || "Team A", $("#n1").value.trim() || "Team B"]; $("#names").hidden = true; render(); });
    choose($("#mode"), function (v) { S.mode = v; render(); });
    render();
  }

  /* ---------- rules court ---------- */
  var zp = $("#zpanel");
  if (zp) {
    var Z = D.zones || [];
    var show = function (id) {
      var z = Z.filter(function (x) { return x.id === id; })[0]; if (!z) return;
      $$(".zone").forEach(function (g) { g.classList.toggle("on", g.dataset.id === id); g.setAttribute("aria-pressed", g.dataset.id === id); });
      zp.innerHTML = '<span class="pill i">Court explorer</span><h3 style="margin-top:12px">' + z.name + "</h3><p>" + z.text + '</p><p class="muted" style="margin:0">Tap another part of the court to keep exploring.</p>';
    };
    $$(".zone").forEach(function (g) {
      g.addEventListener("click", function () { show(g.dataset.id); });
      g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(g.dataset.id); } });
    });
    show("court");
  }

  /* ---------- shots filter ---------- */
  var sf = $("#shot-filter");
  if (sf) choose(sf, function (v) { $$(".shot").forEach(function (c) { c.hidden = v !== "all" && c.dataset.level !== v; }); });

  /* ---------- checklist ---------- */
  $$("[data-check]").forEach(function (list) {
    var key = "pp-" + list.dataset.check, done = store.get(key, {}), bar = $("#" + list.dataset.check + "-bar");
    var upd = function () { var all = $$("input", list), n = all.filter(function (x) { return x.checked; }).length; if (bar) bar.style.width = (n / all.length * 100) + "%"; var c = $("#" + list.dataset.check + "-count"); if (c) c.textContent = n + " of " + all.length + " done"; };
    $$("input", list).forEach(function (inp, i) { inp.checked = !!done[i]; inp.addEventListener("change", function () { done[i] = inp.checked; store.set(key, done); upd(); }); });
    upd();
  });

  /* ---------- glossary search ---------- */
  var gs = $("#gsearch");
  if (gs) gs.addEventListener("input", function () {
    var q = gs.value.toLowerCase().trim();
    $$("#glist > div").forEach(function (d) { d.hidden = q && d.textContent.toLowerCase().indexOf(q) === -1; });
  });

  /* ---------- home: live 3D court (canvas). Court in metres: x -5..5, y 0..20 (near to far), z up. ---------- */
  var cv3 = document.getElementById("court3d");
  if (cv3 && cv3.getContext) (function () {
    var ctx = cv3.getContext("2d"), W = 0, H = 0, dpr = 1, fit = null;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var CAM = { y: -6.2, z: 6.4, pitch: 0.4 };
    var cp = Math.cos(CAM.pitch), sp = Math.sin(CAM.pitch);
    function raw(x, y, z) { var dy = y - CAM.y, dz = z - CAM.z, fw = dy * cp - dz * sp, up = dy * sp + dz * cp; return [x / fw, -up / fw, fw]; }
    function P(x, y, z) { var r = raw(x, y, z); return [fit.ox + r[0] * fit.s, fit.oy + r[1] * fit.s, r[2]]; }
    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv3.clientWidth; H = cv3.clientHeight;
      cv3.width = Math.round(W * dpr); cv3.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var pts = [[-5, 0, 0], [5, 0, 0], [-5, 20, 4], [5, 20, 4], [-5, 0, 3], [5, 0, 3], [-5, 20, 0]], minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
      pts.forEach(function (p) { var r = raw(p[0], p[1], p[2]); minx = Math.min(minx, r[0]); maxx = Math.max(maxx, r[0]); miny = Math.min(miny, r[1]); maxy = Math.max(maxy, r[1]); });
      var padX = W * 0.04, padT = H * 0.08, padB = H * 0.02;
      var s = Math.min((W - padX * 2) / (maxx - minx), (H - padT - padB) / (maxy - miny));
      fit = { s: s, ox: W / 2 - (minx + maxx) / 2 * s, oy: padT - miny * s + ((H - padT - padB) - (maxy - miny) * s) };
    }
    function poly(pts, fill, stroke, lw) {
      ctx.beginPath(); pts.forEach(function (p, i) { var q = P(p[0], p[1], p[2]); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); }); ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw || 1; ctx.stroke(); }
    }
    function line(a, b, col, lw) { var p = P(a[0], a[1], a[2]), q = P(b[0], b[1], b[2]); ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.stroke(); }
    function glassWall(pts, alpha) {
      var a = P(pts[0][0], pts[0][1], pts[0][2]), c = P(pts[2][0], pts[2][1], pts[2][2]);
      var g = ctx.createLinearGradient(a[0], a[1], c[0], c[1]);
      g.addColorStop(0, "rgba(190,225,255," + alpha + ")"); g.addColorStop(0.55, "rgba(190,225,255," + alpha * 0.35 + ")"); g.addColorStop(1, "rgba(255,255,255," + alpha * 1.4 + ")");
      poly(pts, g, "rgba(210,235,255," + Math.min(0.9, alpha * 5) + ")", 1.2);
    }
    function mesh(x0, y0, x1, y1, z0, z1) {
      poly([[x0, y0, z0], [x1, y1, z0], [x1, y1, z1], [x0, y0, z1]], "rgba(122,139,168,0.10)", "rgba(160,176,205,0.5)", 1);
      var n = 14; for (var i = 1; i < n; i++) { var t = i / n; line([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z0], [x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z1], "rgba(160,176,205,0.22)", 0.8); }
      for (var j = 1; j < 4; j++) { var zz = z0 + (z1 - z0) * j / 4; line([x0, y0, zz], [x1, y1, zz], "rgba(160,176,205,0.22)", 0.8); }
    }

    /* ---------- rally simulation ---------- */
    var G = 9.81, ball, shots = 0, glass = 0, maxShots = 8, ending = false, restartAt = 0, trail = [], flashes = [], lastSide = 0, bounces = 0, hitCool = 0, finished = false;
    var players = [{ x: -2.4, y: 2.2 }, { x: 2.4, y: 3.2 }, { x: -2.2, y: 16.5 }, { x: 2.2, y: 17.6 }];
    var hudS = document.getElementById("hud-shots"), hudG = document.getElementById("hud-glass");
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function aim(tx, ty, T) {
      var vx = (tx - ball.x) / T, vy = (ty - ball.y) / T, vz = (0 - ball.z + 0.5 * G * T * T) / T;
      var t10 = (10 - ball.y) / vy, z10 = ball.z + vz * t10 - 0.5 * G * t10 * t10;
      if (t10 > 0 && t10 < T && z10 < 1.25) return aim(tx, ty, T + 0.15);
      ball.vx = vx; ball.vy = vy; ball.vz = vz;
    }
    function serve() {
      var sx = Math.random() < 0.5 ? -1 : 1;
      ball = { x: 2.6 * sx, y: 0.6, z: 0.85, vx: 0, vy: 0, vz: 0 };
      shots = 1; glass = 0; maxShots = Math.round(rnd(6, 13)); ending = false; finished = false; trail = []; bounces = 0; lastSide = 0; hitCool = 0.4;
      aim(-sx * rnd(1, 4), rnd(12.5, 16.4), 1.15);
      hud();
    }
    function hud() { if (hudS) hudS.textContent = shots; if (hudG) hudG.textContent = glass; }
    function hit() {
      var side = ball.y < 10 ? 0 : 1;
      shots++; bounces = 0; lastSide = side; hitCool = 0.35;
      var far = side === 0, T, tx = rnd(-4.2, 4.2), ty;
      if (shots >= maxShots) { ending = true; ty = far ? rnd(13, 17) : rnd(3, 7); T = 0.62; ball.z = Math.max(ball.z, 2.4); }
      else if (Math.random() < 0.28) { ty = far ? rnd(17.5, 19.4) : rnd(0.6, 2.5); T = rnd(1.7, 2.1); }
      else { ty = far ? rnd(14, 19.6) : rnd(0.4, 6); T = rnd(0.9, 1.25); }
      aim(tx, ty, T);
      hud();
    }
    function flash(x, y, z) { flashes.push({ x: x, y: y, z: z, t: 0 }); }
    function step(dt) {
      if (finished) { if (performance.now() > restartAt) serve(); return; }
      hitCool -= dt;
      ball.vz -= G * dt; ball.x += ball.vx * dt; ball.y += ball.vy * dt; ball.z += ball.vz * dt;
      if (ball.z < 0.033) { ball.z = 0.033; ball.vz = -ball.vz * 0.7; ball.vx *= 0.88; ball.vy *= 0.88; bounces++;
        if (bounces >= 2 && !ending) { ending = true; } }
      if (ball.z < 4) {
        if (ball.y < 0.04 && ball.vy < 0) { ball.y = 0.04; ball.vy = -ball.vy * 0.62; if (ball.z < 3) { glass++; flash(ball.x, 0, ball.z); hud(); } }
        if (ball.y > 19.96 && ball.vy > 0) { ball.y = 19.96; ball.vy = -ball.vy * 0.62; if (ball.z < 3) { glass++; flash(ball.x, 20, ball.z); hud(); } }
        if (Math.abs(ball.x) > 4.96 && ball.x * ball.vx > 0) { ball.x = 4.96 * Math.sign(ball.x); ball.vx = -ball.vx * 0.6; if (ball.y < 4 || ball.y > 16) { glass++; flash(ball.x, ball.y, ball.z); hud(); } }
      }
      var side = ball.y < 10 ? 0 : 1;
      if (!ending && hitCool <= 0 && side !== lastSide) {
        var deep = side === 0 ? ball.y < 7.5 : ball.y > 12.5;
        var volley = bounces === 0 && Math.abs(ball.y - 10) > 2.2 && Math.abs(ball.y - 10) < 4.5 && ball.z < 1.6 && ball.vz < 0 && Math.random() < 0.02;
        if ((bounces >= 1 && ball.vz < 0 && ball.z < 1.1 && deep) || volley) hit();
      }
      if (ending && (bounces >= 2 || Math.abs(ball.vz) < 0.4 && ball.z < 0.05)) { finished = true; restartAt = performance.now() + 1600; }
      if (ball.y < -2 || ball.y > 22 || Math.abs(ball.x) > 7) { finished = true; restartAt = performance.now() + 900; }
      trail.push([ball.x, ball.y, ball.z]); if (trail.length > 34) trail.shift();
      // players drift towards the ball on their side
      players.forEach(function (p, i) {
        var mySide = i < 2 ? 0 : 1, tx = p.x, ty = p.y;
        if (mySide === (ball.y < 10 ? 0 : 1) && ((i % 2 === 0) === (ball.x < 0))) { tx = ball.x * 0.9; ty = mySide === 0 ? Math.min(Math.max(ball.y, 1), 8) : Math.max(Math.min(ball.y, 19), 12); }
        else { tx = (i % 2 === 0 ? -2.3 : 2.3); ty = mySide === 0 ? 3 : 17; }
        p.x += (tx - p.x) * Math.min(1, dt * 2.2); p.y += (ty - p.y) * Math.min(1, dt * 2.2);
      });
      flashes.forEach(function (f) { f.t += dt; }); flashes = flashes.filter(function (f) { return f.t < 0.9; });
    }

    function drawBall() {
      // trail
      for (var i = 1; i < trail.length; i++) {
        var a = P(trail[i - 1][0], trail[i - 1][1], trail[i - 1][2]), b = P(trail[i][0], trail[i][1], trail[i][2]);
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.strokeStyle = "rgba(232,248,74," + (i / trail.length * 0.55) + ")"; ctx.lineWidth = 2.2 * i / trail.length + 0.4; ctx.stroke();
      }
      var s = P(ball.x, ball.y, 0), r0 = fit.s * 0.07 / s[2];
      ctx.beginPath(); ctx.ellipse(s[0], s[1], Math.max(2, r0 * 1.4 * (1 - Math.min(ball.z, 4) / 8)), Math.max(1, r0 * 0.5 * (1 - Math.min(ball.z, 4) / 8)), 0, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(4,12,40," + (0.45 - Math.min(ball.z, 4) * 0.08) + ")"; ctx.fill();
      var b2 = P(ball.x, ball.y, ball.z), r = Math.max(3, fit.s * 0.11 / b2[2]);
      var g = ctx.createRadialGradient(b2[0] - r * 0.35, b2[1] - r * 0.35, r * 0.1, b2[0], b2[1], r * 1.1);
      g.addColorStop(0, "#fbffd0"); g.addColorStop(0.6, "#e8f84a"); g.addColorStop(1, "#b9c91f");
      ctx.beginPath(); ctx.arc(b2[0], b2[1], r, 0, Math.PI * 2); ctx.fillStyle = g; ctx.shadowColor = "rgba(232,248,74,0.7)"; ctx.shadowBlur = 14; ctx.fill(); ctx.shadowBlur = 0;
    }
    function drawPlayers(far) {
      players.forEach(function (p, i) {
        if ((i >= 2) !== far) return;
        var c = P(p.x, p.y, 0), r = fit.s * 0.3 / c[2];
        ctx.beginPath(); ctx.ellipse(c[0], c[1], r * 1.4, r * 0.55, 0, 0, Math.PI * 2); ctx.fillStyle = "rgba(6,16,52,0.35)"; ctx.fill();
        ctx.beginPath(); ctx.ellipse(c[0], c[1], r * 1.1, r * 0.42, 0, 0, Math.PI * 2); ctx.strokeStyle = i < 2 ? "rgba(255,255,255,0.75)" : "rgba(232,248,74,0.75)"; ctx.lineWidth = 2; ctx.stroke();
        var top = P(p.x, p.y, 1.75);
        var g = ctx.createLinearGradient(c[0], c[1], top[0], top[1]);
        g.addColorStop(0, i < 2 ? "rgba(255,255,255,0.32)" : "rgba(232,248,74,0.3)"); g.addColorStop(1, "rgba(255,255,255,0)");
        ctx.beginPath(); ctx.moveTo(c[0] - r * 0.6, c[1]); ctx.lineTo(top[0] - r * 0.25, top[1]); ctx.lineTo(top[0] + r * 0.25, top[1]); ctx.lineTo(c[0] + r * 0.6, c[1]); ctx.closePath(); ctx.fillStyle = g; ctx.fill();
      });
    }
    function drawFlashes() {
      flashes.forEach(function (f) {
        var c = P(f.x, f.y, f.z), k = f.t / 0.9, r = fit.s * (0.08 + k * 0.7) / c[2];
        ctx.beginPath(); ctx.arc(c[0], c[1], r, 0, Math.PI * 2); ctx.strokeStyle = "rgba(255,255,255," + (1 - k) * 0.9 + ")"; ctx.lineWidth = 2.5 * (1 - k) + 0.5; ctx.stroke();
        var g = ctx.createRadialGradient(c[0], c[1], 0, c[0], c[1], r * 1.6); g.addColorStop(0, "rgba(220,240,255," + (1 - k) * 0.45 + ")"); g.addColorStop(1, "rgba(220,240,255,0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(c[0], c[1], r * 1.6, 0, Math.PI * 2); ctx.fill();
      });
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      // turf
      var a = P(0, 0, 0), b = P(0, 20, 0), tg = ctx.createLinearGradient(0, a[1], 0, b[1]);
      tg.addColorStop(0, "#2350d8"); tg.addColorStop(1, "#1a3fae");
      poly([[-5, 0, 0], [5, 0, 0], [5, 20, 0], [-5, 20, 0]], tg);
      // floodlight pools
      [[-2.5, 6], [2.5, 6], [-2.5, 14], [2.5, 14]].forEach(function (l) { var c = P(l[0], l[1], 0), r = fit.s * 3.2 / c[2]; if (r > W) r = W; var g = ctx.createRadialGradient(c[0], c[1], 0, c[0], c[1], r); g.addColorStop(0, "rgba(255,255,255,0.10)"); g.addColorStop(1, "rgba(255,255,255,0)"); ctx.fillStyle = g; ctx.fillRect(c[0] - r, c[1] - r, r * 2, r * 2); });
      // lines
      var L = "rgba(255,255,255,0.92)";
      [[-5, 0, 5, 0], [-5, 20, 5, 20], [-5, 0, -5, 20], [5, 0, 5, 20], [-5, 3.05, 5, 3.05], [-5, 16.95, 5, 16.95], [0, 3.05, 0, 16.95]].forEach(function (l) { line([l[0], l[1], 0], [l[2], l[3], 0], L, 1.6); });
      // far back wall + mesh above, far side glass
      glassWall([[-5, 20, 0], [5, 20, 0], [5, 20, 3], [-5, 20, 3]], 0.16);
      mesh(-5, 20, 5, 20, 3, 4);
      [-5, 5].forEach(function (x) {
        glassWall([[x, 16, 0], [x, 20, 0], [x, 20, 3], [x, 18, 3], [x, 18, 2], [x, 16, 2]], 0.12);
        mesh(x, 4, x, 16, 0, 3);
      });
      drawPlayers(true);
      if (ball.y >= 10) drawBall();
      // net
      poly([[-5, 10, 0], [5, 10, 0], [5, 10, 0.92], [0, 10, 0.88], [-5, 10, 0.92]], "rgba(10,24,70,0.45)", "rgba(255,255,255,0.35)", 0.8);
      for (var i = -5; i <= 5; i += 0.5) line([i, 10, 0], [i, 10, 0.9], "rgba(255,255,255,0.12)", 0.6);
      line([-5, 10, 0.92], [0, 10, 0.88], "#ffffff", 2.2); line([0, 10, 0.88], [5, 10, 0.92], "#ffffff", 2.2);
      [-5.05, 5.05].forEach(function (x) { line([x, 10, 0], [x, 10, 1.0], "#dfe8f7", 3); });
      drawPlayers(false);
      if (ball.y < 10) drawBall();
      // near side glass and near back glass (we film from behind it)
      [-5, 5].forEach(function (x) { glassWall([[x, 0, 0], [x, 4, 0], [x, 4, 2], [x, 2, 2], [x, 2, 3], [x, 0, 3]], 0.08); });
      glassWall([[-5, 0, 0], [5, 0, 0], [5, 0, 3], [-5, 0, 3]], 0.05);
      line([-5, 0, 3], [5, 0, 3], "rgba(220,240,255,0.55)", 1.5);
      drawFlashes();
    }
    var last = 0, running = true, raf = 0;
    function loop(t) {
      var dt = Math.min(0.033, (t - last) / 1000 || 0); last = t;
      var sub = 3; for (var i = 0; i < sub; i++) step(dt * 0.82 / sub);
      draw();
      if (running) raf = requestAnimationFrame(loop);
    }
    size(); serve();
    if (reduce) {
      for (var k = 0; k < 40; k++) step(0.02);
      draw();
      var hint = document.getElementById("stage-hint"); if (hint) hint.hidden = true;
    } else {
      raf = requestAnimationFrame(loop);
      if ("IntersectionObserver" in window) new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; last = performance.now(); raf = requestAnimationFrame(loop); }
        if (!vis) { running = false; cancelAnimationFrame(raf); }
      }).observe(cv3);
      cv3.addEventListener("click", function () { serve(); var h = document.getElementById("stage-hint"); if (h) h.style.opacity = "0.4"; });
    }
    window.addEventListener("resize", function () { size(); if (reduce) draw(); });
  })();
})();
