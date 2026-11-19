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
      else if (!S.tb && S.p[0] >= 3 && S.p[1] >= 3 && S.p[0] === S.p[1]) m = S.mode === "golden" ? "Golden point! The receiving pair picks the side." : S.mode === "star" ? ((S.dc || 1) >= 3 ? "Star Point! Next point wins. The receiving pair picks the side." : (S.dc || 1) === 2 ? "Second deuce. Lose the next advantage and it goes to Star Point." : "Deuce (Star Point format: advantage twice, then a deciding point)") : "Deuce";
      else if (S.tb) m = "Tie-break: first to 7, two clear.";
      $("#msg").textContent = m;
      $$("#mode button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === S.mode); });
      save();
    };
    var winGame = function (i) {
      S.g[i]++; S.p = [0, 0]; S.dc = 0; S.srv = 1 - S.srv;
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
      var gBefore = S.g.join();
      S.p[i]++;
      var me = S.p[i], them = S.p[1 - i];
      if (S.tb) { if (me >= 7 && me - them >= 2) winGame(i); }
      else if (S.mode === "golden") { if (me >= 4) winGame(i); }
      else if (S.mode === "star" && (S.dc || 0) >= 3) winGame(i);
      else if (me >= 4 && me - them >= 2) winGame(i);
      else if (me >= 4 && them >= 4 && me === them) { S.p = [3, 3]; }
      if (!S.tb && S.p[0] === 3 && S.p[1] === 3 && S.g.join() === gBefore) S.dc = (S.dc || 0) + 1;
      if (navigator.vibrate) try { navigator.vibrate(15); } catch (e) {}
      render();
    };
    $$(".team", sc).forEach(function (b) { b.addEventListener("click", function () { point(+b.dataset.i); }); });
    $("#undo").addEventListener("click", function () { if (hist.length) { S = JSON.parse(hist.pop()); render(); } else toast("Nothing to undo"); });
    $("#reset").addEventListener("click", function () { hist.push(JSON.stringify(S)); S = { p: [0, 0], g: [0, 0], dc: 0, sets: [], srv: 0, mode: S.mode, tb: false, done: false, names: S.names }; render(); toast("New match"); });
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
  /* ---------- americano / mexicano draw maker ---------- */
  var mx = $("#mx-setup");
  if (mx) {
    var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var shuffle = function (a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x; } return a; };
    var M = store.get("pp-mx", null);
    var cfg = { fmt: (M && M.fmt) || "americano", pts: (M && M.pts) || 24 };
    var namesEl = $("#mx-names"), courtsEl = $("#mx-courts"), roundsEl = $("#mx-rounds"), err = $("#mx-err");
    var NOTE = { americano: "Partners change every round, planned so everyone mixes as much as possible.", mexicano: "Round one is random. Each next round is made from the leaderboard: 1st and 4th play 2nd and 3rd." };
    var parseNames = function () {
      var seen = {}, out = [];
      namesEl.value.split(/[\n,]+/).forEach(function (n) { n = n.trim().slice(0, 24); if (n && !seen[n.toLowerCase()]) { seen[n.toLowerCase()] = 1; out.push(n); } });
      return out;
    };
    var syncSetup = function (touchCourts) {
      var n = parseNames().length, maxC = Math.max(1, Math.floor(n / 4));
      $("#mx-count").textContent = n ? n + " player" + (n === 1 ? "" : "s") + (n >= 4 ? ", up to " + maxC + " court" + (maxC === 1 ? "" : "s") : ", add at least 4") : "";
      courtsEl.max = Math.min(6, maxC);
      if (touchCourts || +courtsEl.value > maxC) courtsEl.value = Math.min(6, maxC);
      if (touchCourts && cfg.fmt === "americano") roundsEl.value = Math.max(3, Math.min(12, n > 4 ? n - 1 : 3));
      $("#mx-fmt-note").textContent = NOTE[cfg.fmt];
      $("#mx-rounds-q").querySelector("label").textContent = cfg.fmt === "mexicano" ? "Rounds (planned, add more any time)" : "Rounds";
    };
    $$("[data-mx]", mx).forEach(function (g) {
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.v === String(cfg[g.dataset.mx]))); });
      choose(g, function (v) { cfg[g.dataset.mx] = g.dataset.mx === "pts" ? +v : v; syncSetup(false); });
    });
    namesEl.addEventListener("input", function () { syncSetup(true); });
    $("#mx-demo").addEventListener("click", function () { namesEl.value = ["Sam", "Priya", "Omar", "Lucia", "Ben", "Aisha", "Marco", "Hana"].join("\n"); syncSetup(true); });

    var pairCount = function (c, a, b) { return (c[a + "|" + b] || 0); };
    var bump = function (c, a, b) { c[a + "|" + b] = (c[a + "|" + b] || 0) + 1; c[b + "|" + a] = (c[b + "|" + a] || 0) + 1; };
    var history = function () {
      var part = {}, opp = {}, rests = M.names.map(function () { return 0; });
      M.rounds.forEach(function (r) {
        r.rest.forEach(function (i) { rests[i]++; });
        r.matches.forEach(function (m) { bump(part, m.a[0], m.a[1]); bump(part, m.b[0], m.b[1]); m.a.forEach(function (x) { m.b.forEach(function (y) { bump(opp, x, y); }); }); });
      });
      return { part: part, opp: opp, rests: rests };
    };
    var pickRest = function (h, order) {
      var n = M.names.length, k = n - M.courts * 4;
      var last = M.rounds.length ? M.rounds[M.rounds.length - 1].rest : [];
      var ids = shuffle(M.names.map(function (_, i) { return i; }));
      if (order) ids = order.slice().reverse();
      ids.sort(function (x, y) { return (h.rests[x] - h.rests[y]) || ((last.indexOf(x) > -1) - (last.indexOf(y) > -1)); });
      return ids.slice(0, k);
    };
    var standings = function () {
      var P = M.names.map(function (n, i) { return { i: i, name: n, pts: 0, played: 0, won: 0 }; });
      M.rounds.forEach(function (r) { r.matches.forEach(function (m) {
        if (m.sa === null || m.sb === null) return;
        m.a.forEach(function (x) { P[x].pts += m.sa; P[x].played++; if (m.sa > m.sb) P[x].won++; });
        m.b.forEach(function (x) { P[x].pts += m.sb; P[x].played++; if (m.sb > m.sa) P[x].won++; });
      }); });
      var uneven = M.names.length > M.courts * 4 && P.some(function (p) { return p.played !== P[0].played; });
      P.forEach(function (p) { p.avg = p.played ? p.pts / p.played : 0; });
      P.sort(function (a, b) { return (uneven ? b.avg - a.avg : 0) || (b.pts - a.pts) || (b.won - a.won) || a.name.localeCompare(b.name); });
      P.uneven = uneven; return P;
    };
    var makeRound = function () {
      var h = history(), r = { matches: [], rest: [] };
      if (M.fmt === "mexicano" && M.rounds.length) {
        var order = standings().map(function (p) { return p.i; });
        r.rest = pickRest(h, order);
        var act = order.filter(function (i) { return r.rest.indexOf(i) < 0; });
        for (var c = 0; c < M.courts; c++) { var g = act.slice(c * 4, c * 4 + 4); r.matches.push({ a: [g[0], g[3]], b: [g[1], g[2]], sa: null, sb: null }); }
        M.rounds.push(r); return;
      }
      r.rest = pickRest(h);
      var active = M.names.map(function (_, i) { return i; }).filter(function (i) { return r.rest.indexOf(i) < 0; });
      var best = null, bestCost = Infinity;
      for (var t = 0; t < 300 && bestCost > 0; t++) {
        var pool = shuffle(active), pairs = [], cost = 0;
        while (pool.length) {
          var p = pool.shift(), bi = 0, bc = Infinity;
          pool.forEach(function (q, qi) { var cc = pairCount(h.part, p, q); if (cc < bc) { bc = cc; bi = qi; } });
          cost += bc * 100; pairs.push([p, pool.splice(bi, 1)[0]]);
        }
        var ms = [];
        while (pairs.length) {
          var A = pairs.shift(), bj = 0, oc = Infinity;
          pairs.forEach(function (B, k) { var s = 0; A.forEach(function (x) { B.forEach(function (y) { s += pairCount(h.opp, x, y); }); }); if (s < oc) { oc = s; bj = k; } });
          cost += oc * 10; ms.push({ a: A, b: pairs.splice(bj, 1)[0], sa: null, sb: null });
        }
        if (cost < bestCost) { bestCost = cost; best = ms; }
      }
      r.matches = best; M.rounds.push(r);
    };
    var save2 = function () { store.set("pp-mx", M); };
    var nm = function (i) { return esc(M.names[i]); };
    var roundDone = function (r) { return r.matches.every(function (m) { return m.sa !== null && m.sb !== null; }); };
    var drawBoard = function () {
      var P = standings(), any = P.some(function (p) { return p.played; });
      $("#mx-board").innerHTML = "<h2>Leaderboard</h2>" + (any ? "" : "<p>Enter the points after each match. The table updates as you type.</p>") +
        '<table><thead><tr><th>#</th><th>Player</th><th class="num">Points</th><th class="num">Played</th><th class="num">' + (P.uneven ? "Per match" : "Won") + "</th></tr></thead><tbody>" +
        P.map(function (p, k) { return '<tr class="' + (k === 0 && any ? "top" : "") + '"><td>' + (k + 1) + "</td><td>" + esc(p.name) + '</td><td class="num"><b>' + p.pts + '</b></td><td class="num">' + p.played + '</td><td class="num">' + (P.uneven ? p.avg.toFixed(1) : p.won) + "</td></tr>"; }).join("") + "</tbody></table>" +
        (P.uneven ? '<p style="margin:12px 0 0;font-size:.88rem">Players have played different numbers of matches, so the table is sorted by points per match.</p>' : "");
    };
    var drawRounds = function () {
      var html = "";
      M.rounds.forEach(function (r, ri) {
        html += '<div class="card round"><h3>Round ' + (ri + 1) + "<small>" + (roundDone(r) ? "Done" : M.pts + " points per match") + "</small></h3>";
        r.matches.forEach(function (m, mi) {
          var cls = m.sa !== null && m.sb !== null ? (m.sa > m.sb ? " won-a" : m.sb > m.sa ? " won-b" : "") : "";
          html += '<div class="match' + cls + '"><span class="ct">Court ' + (mi + 1) + '</span>' +
            '<div class="pair a"><input type="number" min="0" max="' + M.pts + '" inputmode="numeric" aria-label="Points for ' + nm(m.a[0]) + " and " + nm(m.a[1]) + '" data-r="' + ri + '" data-m="' + mi + '" data-s="a" value="' + (m.sa === null ? "" : m.sa) + '"><span>' + nm(m.a[0]) + " &amp; " + nm(m.a[1]) + "</span></div>" +
            '<span class="vs">vs</span><div class="pair b"><span>' + nm(m.b[0]) + " &amp; " + nm(m.b[1]) + '</span><input type="number" min="0" max="' + M.pts + '" inputmode="numeric" aria-label="Points for ' + nm(m.b[0]) + " and " + nm(m.b[1]) + '" data-r="' + ri + '" data-m="' + mi + '" data-s="b" value="' + (m.sb === null ? "" : m.sb) + '"></div></div>';
        });
        if (r.rest.length) html += '<p class="rest">Resting: ' + r.rest.map(nm).join(", ") + "</p>";
        html += "</div>";
      });
      $("#mx-rounds-list").innerHTML = html;
      var nx = $("#mx-next");
      nx.textContent = M.fmt === "mexicano" ? "Make the next round" : "Add another round";
      nx.disabled = M.fmt === "mexicano" && !roundDone(M.rounds[M.rounds.length - 1]);
      nx.style.opacity = nx.disabled ? ".5" : "1";
      $("#mx-sum").textContent = (M.fmt === "mexicano" ? "Mexicano" : "Americano") + " · " + M.names.length + " players · " + M.courts + " court" + (M.courts === 1 ? "" : "s") + " · " + M.pts + " points";
      drawBoard();
    };
    var show = function (live) { mx.hidden = live; $("#mx-live").hidden = !live; $(".gen").classList.toggle("live", live); };
    $("#mx-rounds-list").addEventListener("input", function (ev) {
      var t = ev.target; if (!t.dataset || t.dataset.s === undefined) return;
      var m = M.rounds[+t.dataset.r].matches[+t.dataset.m], v = t.value === "" ? null : Math.max(0, Math.min(M.pts, Math.round(+t.value)));
      var other = t.dataset.s === "a" ? "b" : "a", oEl = t.parentNode.parentNode.querySelector('input[data-s="' + other + '"]');
      m["s" + t.dataset.s] = v; m["s" + other] = v === null ? null : M.pts - v; oEl.value = v === null ? "" : M.pts - v;
      var row = t.parentNode.parentNode; row.classList.remove("won-a", "won-b");
      if (v !== null) { if (m.sa > m.sb) row.classList.add("won-a"); else if (m.sb > m.sa) row.classList.add("won-b"); }
      save2(); drawBoard();
      var r = M.rounds[+t.dataset.r], sm = row.parentNode.querySelector("h3 small"); if (sm) sm.textContent = roundDone(r) ? "Done" : M.pts + " points per match";
      var nx = $("#mx-next"); nx.disabled = M.fmt === "mexicano" && !roundDone(M.rounds[M.rounds.length - 1]); nx.style.opacity = nx.disabled ? ".5" : "1";
    });
    $("#mx-start").addEventListener("click", function () {
      var names = parseNames(), courts = Math.round(+courtsEl.value) || 1, rounds = Math.round(+roundsEl.value) || 1;
      err.textContent = "";
      if (names.length < 4) { err.textContent = "Add at least 4 players."; return; }
      if (names.length > 24) { err.textContent = "This tool handles up to 24 players."; return; }
      courts = Math.max(1, Math.min(courts, Math.floor(names.length / 4), 6)); rounds = Math.max(1, Math.min(rounds, 30));
      M = { fmt: cfg.fmt, pts: cfg.pts, names: names, courts: courts, rounds: [] };
      var k = M.fmt === "mexicano" ? 1 : rounds;
      for (var i = 0; i < k; i++) makeRound();
      save2(); show(true); drawRounds();
      $("#mx-live").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    $("#mx-next").addEventListener("click", function () { if (this.disabled) return; makeRound(); save2(); drawRounds(); var c = $$(".round"); if (c.length) c[c.length - 1].scrollIntoView({ behavior: "smooth", block: "center" }); });
    $("#mx-new").addEventListener("click", function () {
      if (!confirm("Start a new session? The current scores will be cleared.")) return;
      namesEl.value = M.names.join("\n"); cfg.fmt = M.fmt; cfg.pts = M.pts; M = null; store.set("pp-mx", null); show(false); syncSetup(true);
    });
    $("#mx-copy").addEventListener("click", function () {
      var P = standings(), txt = (M.fmt === "mexicano" ? "Mexicano" : "Americano") + " results\n" + P.map(function (p, k) { return (k + 1) + ". " + p.name + ": " + p.pts + " points (" + p.played + " played)"; }).join("\n");
      navigator.clipboard.writeText(txt).then(function () { toast("Results copied"); }, function () { toast("Copy blocked here"); });
    });
    if (M && M.rounds && M.rounds.length) { show(true); drawRounds(); namesEl.value = M.names.join("\n"); }
    else { M = null; syncSetup(false); }
  }

  /* ---------- court dimensions ---------- */
  var dims = $("#dims");
  if (dims) {
    var unit = "m";
    var fmt = function (m) {
      if (unit === "m") return m < 1 ? Math.round(m * 100) + " cm" : (+m.toFixed(2)) + " m";
      var inch = m / 0.0254;
      if (m < 0.95) return (Math.round(inch * 10) / 10) + " in";
      var ft = Math.floor(inch / 12), r = Math.round(inch - ft * 12);
      if (r === 12) { ft++; r = 0; }
      return ft + " ft" + (r ? " " + r + " in" : "");
    };
    var paint = function () { $$("[data-m]").forEach(function (el) { el.textContent = fmt(+el.dataset.m); }); };
    var INFO = {
      len: ["Length", [20], "The court is 20 m long from back wall to back wall, measured inside the walls. The net splits it into two halves of 10 m."],
      wid: ["Width", [10], "A doubles court is 10 m wide. Each team covers 10 m by 10 m, so each player looks after about 5 m of width."],
      svc: ["Net to service line", [6.95], "The service line is 6.95 m from the net on both sides. The server stands behind it, and the serve must land between the net and this line in the diagonal box."],
      back: ["Service line to back wall", [3.05], "Only 3.05 m sits behind the service line. That short space is why the ball reaches the back glass so often."],
      box: ["Service box width", [5], "The centre line splits each half into two service boxes, each 5 m wide and 6.95 m deep."],
      ext: ["Centre line extension", [0.2], "The centre service line runs from the net to the service line and sticks out 0.2 m past it, so players can see where to stand to serve."],
      glassl: ["Side glass length", [4, 2, 2], "Along each side, glass runs for 4 m from each back wall: 2 m at full height, then 2 m at a lower height. The middle of the side is metal mesh."],
      glass3: ["Glass height", [3], "The back glass is 3 m high, and so is the first 2 m of side glass next to it."],
      step2: ["Side step height", [2], "After the first 2 m, the side glass steps down to 2 m high for another 2 m. Some courts use a variant with taller side glass instead."],
      back4: ["Back wall total", [4, 3, 1], "The back wall is 4 m high in total: 3 m of glass with 1 m of metal mesh on top. A ball that hits the mesh above the glass is treated differently, so check the rules."],
      neth: ["Net height", [0.88, 0.92], "The net is 0.88 m high in the middle and 0.92 m at the posts. It sags a little, so the centre is the lowest place to hit over."],
      netl: ["Net length", [10], "The net crosses the full 10 m width of the court, between posts at each side."]
    };
    var info = $("#dim-info"), cur = null;
    var showInfo = function () {
      if (!cur) { info.innerHTML = '<p class="muted">Pick a measurement above. It lights up on the drawings.</p>'; return; }
      var d = INFO[cur];
      info.innerHTML = '<span class="pill i">' + d[1].map(function (m) { return '<span data-m="' + m + '">' + fmt(m) + "</span>"; }).join(" · ") + "</span><h3 style=\"margin-top:10px;font-size:1.4rem\">" + d[0] + "</h3><p>" + d[2] + "</p>";
    };
    var pick = function (k) {
      cur = cur === k ? null : k;
      $$("#dim-btns button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.k === cur)); });
      $$(".dim", dims).forEach(function (g) { g.classList.toggle("on", g.dataset.k === cur); });
      dims.classList.toggle("focus", !!cur); showInfo();
    };
    $$("#dim-btns button").forEach(function (b) { b.addEventListener("click", function () { pick(b.dataset.k); }); });
    $$(".dim", dims).forEach(function (g) { g.addEventListener("click", function () { pick(g.dataset.k); }); });
    choose($("#unit"), function (u) { unit = u; paint(); });
    showInfo(); paint();
  }
  /* ---------- level calculator ---------- */
  var lq = $("#lvquiz");
  if (lq) {
    var LA = store.get("pp-level", {}) || {};
    var lres = $("#lv-result");
    var groups = $$("[data-lv]", lq);
    var CAP = { social: 3.5, club: 4.5, tour: 5.5, nat: 6, pro: 7 };
    var AREA = {
      rally: ["Consistency", "Rally with a friend at slow pace and count shots. Aim for 20 without a miss before you add speed."],
      serve: ["Serve and return", "Practise the serve to the glass corner and the return low to the feet of the net player. Ten minutes before each game is enough."],
      glass: ["Playing off the glass", "Let the ball pass you, turn sideways and wait for it to come off the back glass. Start with easy feeds and short swings."],
      net: ["Volleys", "Keep the racket up in front of you and block the ball deep. Short, firm volleys beat big swings."],
      over: ["Overheads", "Learn the bandeja: a controlled, sliced overhead that keeps you at the net. Our shot library shows the path."],
      tact: ["Tactics", "Move up and back with your partner, and use the lob to take the net. Play the middle when in doubt."]
    };
    var BAND = function (l) {
      if (l < 3) return ["Beginner", "You are learning the basics: the serve, the score and how the walls work. Short rallies are normal. Play often and you will move up quickly."];
      if (l < 4) return ["Improver", "You can rally and use the glass on easy balls. Now it's about fewer mistakes and moving well with your partner."];
      if (l < 5) return ["Intermediate", "A solid club player. You control the court and know the main shots. Small gains now come from tactics and choosing the right shot."];
      if (l < 6) return ["Advanced", "A tournament player who builds points with a plan. Match play and coaching make the biggest difference from here."];
      return ["Elite", "Semi-professional or professional level. Your ranking says more than any quiz."];
    };
    var lrender = function () {
      groups.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", String(LA[g.dataset.lv] === b.dataset.v)); }); });
      var keys = groups.map(function (g) { return g.dataset.lv; });
      var done = keys.filter(function (k) { return LA[k] !== undefined; }).length;
      if (done < keys.length) {
        lres.innerHTML = '<span class="pill b">' + done + " of " + keys.length + ' answered</span><h2 style="margin-top:10px">Your level</h2><div class="meter" style="margin:6px 0 14px"><i style="width:' + Math.round(done / keys.length * 100) + '%"></i></div><p>Pick the answer that sounds most like you on a normal day, not your best day. Your result appears when all seven are answered.</p>';
        return;
      }
      var skill = keys.filter(function (k) { return k !== "comp"; });
      var sum = 0, low = skill[0], high = skill[0];
      skill.forEach(function (k) { var x = +LA[k]; sum += x; if (x < +LA[low]) low = k; if (x > +LA[high]) high = k; });
      var lv = Math.round(sum / skill.length * 2) / 2;
      lv = Math.max(1, Math.min(lv, CAP[LA.comp]));
      if (LA.comp === "nat") lv = Math.max(lv, 5.5);
      if (LA.comp === "pro") lv = Math.max(lv, 6.5);
      var bd = BAND(lv), lvTxt = lv.toFixed(1);
      var tip = lv >= 6 ? ["Keep competing", "At this level, rated tournament results are your best guide."] : AREA[low];
      lres.innerHTML = '<span class="pill b">Your estimated level</span><div class="lv-num">' + lvTxt + '<small> / 7</small></div><h2>' + bd[0] + '</h2>' +
        '<div class="lv-scale" aria-hidden="true"><i style="left:' + ((lv - 1) / 6 * 100) + '%"></i><span>1</span><span>4</span><span>7</span></div>' +
        "<p>" + bd[1] + "</p>" +
        '<dl class="spec"><dt>Strongest area</dt><dd>' + AREA[high][0] + "</dd><dt>Work on next</dt><dd>" + tip[0] + "</dd></dl>" +
        "<p>" + tip[1] + "</p>" +
        "<p style=\"font-size:.92rem\">Look for games with players around " + Math.max(1, lv - 0.5).toFixed(1) + " to " + Math.min(7, lv + 0.5).toFixed(1) + ". This is an estimate, not an official rating.</p>" +
        '<div class="btns"><button class="btn lime sm" type="button" id="lv-copy">Copy my level</button></div>';
      $("#lv-copy").addEventListener("click", function () {
        var txt = "My estimated padel level: " + lvTxt + " out of 7 (" + bd[0] + "). Working on: " + tip[0].toLowerCase() + ".";
        navigator.clipboard.writeText(txt).then(function () { toast("Level copied"); }, function () { toast("Copy blocked here"); });
      });
    };
    groups.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { LA[g.dataset.lv] = b.dataset.v; store.set("pp-level", LA); lrender(); }); }); });
    $("#lv-reset").addEventListener("click", function () { LA = {}; store.set("pp-level", LA); lrender(); toast("Answers cleared"); });
    lrender();
  }

  /* ---------- deuce simulator ---------- */
  var dz = $("#deuce");
  if (dz) {
    var seq = [];
    var TN = ["A", "B"];
    var sim = function (f) {
      var a = 0, b = 0, deuces = 1, i, w;
      for (i = 0; i < seq.length; i++) {
        w = seq[i];
        if (f === "golden" || (f === "star" && deuces >= 3)) return { win: w, n: i + 1 };
        if (a === b) { if (w === 0) a++; else b++; }
        else if ((a > b) === (w === 0)) return { win: w, n: i + 1 };
        else { a = b = 0; deuces++; }
      }
      return { a: a, b: b, deuces: deuces };
    };
    var drender = function () {
      var all = true;
      $$(".dz", dz).forEach(function (c) {
        var f = c.dataset.f, r = sim(f), s = $(".dz-s", c), m = $(".dz-m", c);
        c.classList.toggle("over", r.win !== undefined);
        if (r.win !== undefined) { s.textContent = "Game " + TN[r.win]; m.textContent = "Decided after " + r.n + (r.n === 1 ? " point" : " points") + " from 40-40"; return; }
        all = false;
        if (r.a !== r.b) { s.textContent = "Ad " + TN[r.a > r.b ? 0 : 1]; m.textContent = f === "star" ? "Advantage " + Math.min(r.deuces, 2) + " of 2" : "Advantage"; }
        else {
          s.textContent = "40-40";
          if (f === "golden") m.textContent = "Next point wins";
          else if (f === "star") m.textContent = r.deuces >= 3 ? "Star Point: next point wins" : r.deuces === 2 ? "Second deuce" : "First deuce";
          else m.textContent = r.deuces > 1 ? "Deuce number " + r.deuces : "Deuce";
        }
      });
      $("#dz-log").textContent = seq.length ? "Points after 40-40: " + seq.map(function (w) { return TN[w]; }).join(" ") : "No points played yet.";
      $$(".dz-btns button", dz).forEach(function (b) { b.disabled = all; });
      return all;
    };
    $$(".dz-btns button", dz).forEach(function (b) { b.addEventListener("click", function () { seq.push(+b.dataset.w); drender(); }); });
    $("#dz-reset").addEventListener("click", function () { seq = []; drender(); });
    $("#dz-rand").addEventListener("click", function () { seq = []; var guard = 0; while (!drender() && guard++ < 40) seq.push(Math.random() < 0.5 ? 0 : 1); drender(); });
    drender();
  }
})();
