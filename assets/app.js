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
        "<p>" + why.join(" ") + "</p>" + '<div class="btns"><button class="btn lime sm" type="button" id="copy-fit">Copy my racket profile</button><a class="btn sm" href="/go/padel-' + shape + '-rackets" rel="sponsored nofollow noopener" target="_blank">Shop ' + shape + ' rackets</a></div><p class="aff-note">We may earn a commission if you buy through this link, at no extra cost to you.</p>';
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
  if (gs) (function () {
    var cat = "", gc = $("#gcat"), cnt = $("#gcount");
    var norm = function (x) { return x.toLowerCase().normalize ? x.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") : x.toLowerCase(); };
    var run = function () {
      var q = norm(gs.value.trim()), n = 0, all = $$("#glist > div");
      all.forEach(function (d) { var h = (q && norm(d.textContent).indexOf(q) === -1) || (cat && d.dataset.cat !== cat); d.hidden = h; if (!h) n++; });
      if (cnt) cnt.textContent = n === all.length ? all.length + " terms" : n ? "Showing " + n + " of " + all.length + " terms" : "No match. Try a shorter word, or check the spelling.";
    };
    gs.addEventListener("input", run);
    if (gc) choose(gc, function (v) { cat = v; run(); });
    run();
  })();

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

  /* ---------- positioning court ---------- */
  var pc = $("#pos-court");
  if (pc) {
    var NS = "http://www.w3.org/2000/svg";
    var px = function (x) { return 20 + x * 30; }, py = function (y) { return 20 + y * 30; };
    var el = function (tag, a) { var n = document.createElementNS(NS, tag); for (var k in a) n.setAttribute(k, a[k]); return n; };
    // Positions in metres: x 0-10 (left to right), y 0-20 (opponents' glass to yours). Net at y 10.
    // p: [you, partner, opponent left, opponent right]; ball: [x, y]; ar: arrows [x1,y1,x2,y2]
    var SC = {
      serve: { t: "Your team serves", p: [[3, 12.4], [7, 18.1], [2.6, 1.2], [7.2, 4.2]], ball: [3, 2.2], ar: [[7, 18.1, 7.2, 13.2]],
        d: "Your partner serves from the right, behind the service line, aimed diagonally at the opponent on the left. You wait at the net on the other half.",
        tips: ["The server bounces the ball, serves, then moves forward to join the partner at the net.", "The partner at the net stands about 2 metres from it, ready to volley the return.", "Aim the serve deep, so the ball comes off the back glass and the return is harder."], warn: "" },
      receive: { t: "You receive", p: [[2.8, 19], [7.2, 16.2], [7.2, 1.9], [2.6, 7.6]], ball: [2.8, 18.2], ar: [],
        d: "The server on the far side serves diagonally to you, and their partner waits at the net. You stand about 1 metre in front of your back glass. Your partner waits further forward on the other half.",
        tips: ["Stand about 1 metre off the glass so a deep serve can come off the glass and you still have room.", "Let the serve bounce. You may not volley it.", "A good return is a low ball at the feet of the player coming to the net, or a lob over the net player."], warn: "" },
      net: { t: "Both at the net", p: [[2.8, 12.2], [7.2, 12.6], [2.8, 1.2], [7.2, 1.1]], ball: [2.6, 1.6], ar: [], side: true,
        d: "You and your partner both stand about 2 to 2.5 metres from the net. This is the strongest place to be: most points are won from here.",
        tips: ["The player on the ball's side stays a little closer and covers the line.", "The other player is half a step back and closer to the middle, watching for the lob.", "Keep your racket up and in front of you, ready for a volley."], warn: "" },
      back: { t: "Both at the back", p: [[2.8, 18.9], [7.2, 18.6], [2.9, 7.7], [7.1, 7.9]], ball: [3.3, 8.2], ar: [], side: true,
        d: "The opponents hold the net, so you both defend about 1 metre in front of your back glass, side by side.",
        tips: ["Give the ball room to come off the glass rather than rushing it.", "The player on the ball's side covers the line, the other covers the middle.", "Look for a good lob or a low chiquita, then move up together."], warn: "" },
      lob: { t: "Lobbed at the net", p: [[2.8, 12.3], [7.2, 12.5], [2.8, 1.2], [7.2, 1.3]], ball: [3.3, 17.6], ar: [[2.8, 12.3, 3.1, 17.4], [7.2, 12.5, 6.8, 17.6]],
        d: "A lob has gone over you. Both of you turn and go back together, so you can defend side by side.",
        tips: ["Turn side-on and run back, don't back-pedal facing the net.", "Let the ball come off the glass if you can't reach it before it bounces.", "Play a safe ball, then move back up to the net as a pair."], warn: "" },
      split: { t: "One up, one back", p: [[2.8, 12.3], [7.2, 18.9], [2.8, 1.2], [7.2, 7.7]], ball: [7, 8.1], ar: [], gap: true,
        d: "One player at the net and one at the back leaves a big diagonal gap between you. Good opponents hit the ball straight through it or at the net player's feet.",
        tips: ["If your partner goes up, go up with them.", "If one of you is pushed back, both go back.", "Think of an invisible rope of about 3 metres joining you."], warn: "Avoid this formation." }
    };
    var cur = "serve", side = "L", gZ = $("#pos-zones"), gA = $("#pos-arrows"), gP = $("#pos-players"), panel = $("#pos-panel"), sideBar = $("#pos-side-bar");
    var COL = ["#e8f84a", "#ffffff", "#ff8a5c", "#ff8a5c"], LAB = ["You", "Partner", "", ""], nodes = [];
    for (var i = 0; i < 4; i++) {
      var g = el("g", { "class": "pl" });
      g.appendChild(el("circle", { r: 13, fill: COL[i], stroke: "#0b1530", "stroke-width": 2.5 }));
      if (LAB[i]) { var tx = el("text", { y: 30, "text-anchor": "middle", fill: "#fff", "font-family": "sans-serif", "font-size": 12, "font-weight": 700 }); tx.textContent = LAB[i]; g.appendChild(tx); }
      gP.appendChild(g); nodes.push(g);
    }
    var ballN = el("circle", { r: 6, fill: "#e8f84a", stroke: "#fff", "stroke-width": 2, "class": "pl" }); gP.appendChild(ballN);
    var prender = function () {
      var s = SC[cur], pts = s.p.map(function (q) { return q.slice(); }), b = s.ball.slice();
      if (s.side && side === "R") {
        // mirror the scene left-right so the ball is on your partner's side
        pts = [[10 - pts[1][0], pts[1][1]], [10 - pts[0][0], pts[0][1]], [10 - pts[3][0], pts[3][1]], [10 - pts[2][0], pts[2][1]]];
        b[0] = 10 - b[0];
      }
      pts.forEach(function (q, i) { nodes[i].setAttribute("transform", "translate(" + px(q[0]) + " " + py(q[1]) + ")"); });
      ballN.setAttribute("transform", "translate(" + px(b[0]) + " " + py(b[1]) + ")");
      gA.textContent = ""; gZ.textContent = "";
      (s.ar || []).forEach(function (a) { gA.appendChild(el("line", { x1: px(a[0]), y1: py(a[1]), x2: px(a[2]), y2: py(a[3]), stroke: "#e8f84a", "stroke-width": 3, "stroke-dasharray": "6 6", "marker-end": "url(#pos-ar)" })); });
      if (s.gap) [[4.6, 11.6, 5.1, 5.4], [0.3, 15.2, 4.4, 4.5]].forEach(function (r) { gZ.appendChild(el("rect", { x: px(r[0]), y: py(r[1]), width: r[2] * 30, height: r[3] * 30, rx: 10, fill: "rgba(255,138,92,0.28)", stroke: "#ff8a5c", "stroke-width": 2, "stroke-dasharray": "5 5" })); });
      else if (cur !== "serve" && cur !== "receive") {
        var near = pts[0][1] > 15;
        gZ.appendChild(el("rect", { x: px(0.3), y: py(near ? 17.6 : 11.3), width: 9.4 * 30, height: (near ? 2.1 : 2.2) * 30, rx: 10, fill: "rgba(232,248,74,0.12)", stroke: "rgba(232,248,74,0.5)", "stroke-dasharray": "4 6" }));
      }
      sideBar.hidden = !s.side;
      panel.innerHTML = "<h3>" + s.t + "</h3><p>" + s.d + "</p><ul class=\"pos-tips\">" + s.tips.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>" + (s.warn ? "<p class=\"pos-warn\">" + s.warn + "</p>" : "");
      $$("#pos-pick .opt").forEach(function (o) { o.setAttribute("aria-pressed", o.dataset.s === cur ? "true" : "false"); });
      $$("#pos-side button").forEach(function (o) { o.setAttribute("aria-pressed", o.dataset.v === side ? "true" : "false"); });
    };
    $$("#pos-pick .opt").forEach(function (o) { o.addEventListener("click", function () { cur = o.dataset.s; prender(); }); });
    $$("#pos-side button").forEach(function (o) { o.addEventListener("click", function () { side = o.dataset.v; prender(); }); });
    prender();
  }

  /* ---------- serve checker ---------- */
  var svc = $("#svc");
  if (svc) {
    var A = {}, out = $("#sv-out"), aft = $("#sv-after");
    var ORDER = ["try", "bounce", "feet", "ground", "waist", "own", "land", "after"];
    var verdict = function () {
      var second = A["try"] === "2", F = function (why) { return { c: "fault", h: second ? "Double fault" : "Fault", p: why + (second ? " That was the second serve, so the receiving pair wins the point." : " The server has one more try: the second serve.") }; };
      if (A.land === "miss") return F("Swinging and missing counts as a serve.");
      if (A.bounce === "n") return F("The ball must bounce behind the service line, in the server's own half, before it is hit.");
      if (A.feet === "n") return F("The server's feet may not touch the service line or the centre line extension.");
      if (A.ground === "n") return F("At least one foot must be on the ground when the ball is hit. No jump serves.");
      if (A.waist === "n") return F("Contact must be at or below waist height.");
      if (A.own === "y") return F("The serve may not touch the server, their partner or anything on their side before crossing the net.");
      if (!A.land) return null;
      if (A.land === "out") return F("The ball must land in the service box diagonally opposite. Lines count as in.");
      if (A.land === "netout") return F("A net touch is only a let if the ball still lands in the correct box.");
      if (A.land === "body") return { c: "good", h: "Point to the server", p: "The serve hit the receiver before it bounced, so the serving pair wins the point." };
      if (!A.after) return null;
      if (A.after === "fence") return F("After bouncing in the box, the serve hit the metal fence before a second bounce.");
      if (A.land === "netin") return { c: "let", h: "Let: replay the serve", p: "The ball touched the net and landed in the right box without touching the fence. Replay " + (second ? "the second serve only." : "the first serve.") };
      return { c: "good", h: "Good serve", p: A.after === "glass" ? "It bounced in the box and then hit the glass, which is fine. Play on: the receiver can play it off the glass." : "A legal serve. Play on." };
    };
    var srender = function () {
      var needAfter = A.land === "in" || A.land === "netin";
      aft.classList.toggle("off", !needAfter);
      $$(".sv-q", svc).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.setAttribute("aria-pressed", A[q.dataset.q] === o.dataset.v ? "true" : "false"); }); });
      var r = verdict();
      out.className = "result" + (r ? " " + r.c : "");
      out.innerHTML = r ? "<h2>" + r.h + "</h2><p>" + r.p + "</p>" : "<h2>Make the call</h2><p>" + (A.land && needAfter && !A.after ? "One more: what did the ball hit after bouncing in the box?" : "Answer the questions and the verdict appears here.") + "</p>";
    };
    $$(".sv-q", svc).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.addEventListener("click", function () { A[q.dataset.q] = o.dataset.v; if (q.dataset.q === "land" && o.dataset.v !== "in" && o.dataset.v !== "netin") delete A.after; srender(); }); }); });
    $("#sv-reset").addEventListener("click", function () { A = {}; srender(); });
    srender();
  }

  /* ---------- warm-up timer ---------- */
  var wu = $("#wu");
  if (wu && window.WU) {
    var W = { len: store.get("pp-wu-len", "q"), snd: store.get("pp-wu-snd", "on"), i: 0, left: 0, run: false }, tick = null, ac = null, lock = null;
    var steps = function () { return window.WU[W.len] || window.WU.q; };
    var fmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var beep = function (f, d) {
      if (W.snd !== "on") return;
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = f; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.18, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d); o.start(); o.stop(ac.currentTime + d); } catch (e) {}
    };
    var wake = function (on) {
      try { if (on && navigator.wakeLock && !lock) navigator.wakeLock.request("screen").then(function (l) { lock = l; l.addEventListener("release", function () { lock = null; }); }, function () {}); else if (!on && lock) { lock.release(); lock = null; } } catch (e) {}
    };
    var list = $("#wu-list");
    var buildList = function () {
      list.innerHTML = steps().map(function (s, n) { return '<li data-n="' + n + '"><b>' + (n + 1) + ". " + s.n + '</b><span class="pill">' + s.ph + '</span><span class="wu-t">' + fmt(s.t) + "</span><p>" + s.d + "</p></li>"; }).join("");
      $$("li", list).forEach(function (li) { li.addEventListener("click", function () { go(+li.dataset.n); }); });
    };
    var total = function () { return steps().reduce(function (a, s) { return a + s.t; }, 0); };
    var wrender = function () {
      var S = steps(), s = S[W.i], done = 0;
      for (var k = 0; k < W.i; k++) done += S[k].t;
      done += s.t - W.left;
      $("#wu-clock").textContent = fmt(W.left);
      $("#wu-of").textContent = "Step " + (W.i + 1) + " of " + S.length;
      $("#wu-ph").textContent = s.ph; $("#wu-name").textContent = s.n; $("#wu-how").textContent = s.d;
      $("#wu-next").textContent = W.i + 1 < S.length ? "Next: " + S[W.i + 1].n : "Last step. Then play!";
      $("#wu-arc").setAttribute("stroke-dashoffset", (326.7 * (1 - W.left / s.t)).toFixed(1));
      $("#wu-prog").style.width = (done / total() * 100) + "%";
      $("#wu-left").textContent = fmt(total() - done) + " left in total";
      $("#wu-go").textContent = W.run ? "Pause" : (W.left < s.t || W.i ? "Resume" : "Start");
      $$("li", list).forEach(function (li, n) { li.classList.toggle("on", n === W.i); li.classList.toggle("done", n < W.i); });
      $$("#wu-len button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === W.len ? "true" : "false"); });
      $$("#wu-snd button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === W.snd ? "true" : "false"); });
    };
    var stop = function () { W.run = false; clearInterval(tick); tick = null; wake(false); };
    var finish = function () {
      stop(); beep(880, 0.6);
      $("#wu-clock").textContent = "0:00"; $("#wu-name").textContent = "Warm-up done. Enjoy the match!"; $("#wu-how").textContent = "Remember your three goals, and save the long, held stretches for after you play.";
      $("#wu-next").textContent = ""; $("#wu-prog").style.width = "100%"; $("#wu-left").textContent = ""; $("#wu-go").textContent = "Start again";
      $$("li", list).forEach(function (li) { li.classList.remove("on"); li.classList.add("done"); });
      W.i = 0; W.left = steps()[0].t; W.end = true;
    };
    var go = function (n) { var S = steps(); W.end = false; W.i = Math.max(0, Math.min(S.length - 1, n)); W.left = S[W.i].t; W.last = Date.now(); wrender(); };
    var step = function () {
      var now = Date.now(); W.left -= (now - W.last) / 1000; W.last = now;
      var c = Math.ceil(W.left);
      if (c !== W.shown && c <= 3 && c > 0) beep(660, 0.12);
      W.shown = c;
      if (W.left <= 0) { if (W.i + 1 >= steps().length) return finish(); beep(990, 0.35); go(W.i + 1); return; }
      wrender();
    };
    $("#wu-go").addEventListener("click", function () {
      if (W.run) { stop(); wrender(); return; }
      if (W.end) go(0);
      W.run = true; W.last = Date.now(); beep(990, 0.2); wake(true); tick = setInterval(step, 250); wrender();
    });
    $("#wu-skip").addEventListener("click", function () { if (W.i + 1 >= steps().length) finish(); else go(W.i + 1); });
    $("#wu-back").addEventListener("click", function () { go(W.left < steps()[W.i].t - 2 ? W.i : W.i - 1); });
    $$("#wu-len button").forEach(function (b) { b.addEventListener("click", function () { if (b.dataset.v === W.len) return; stop(); W.len = b.dataset.v; store.set("pp-wu-len", W.len); buildList(); go(0); }); });
    $$("#wu-snd button").forEach(function (b) { b.addEventListener("click", function () { W.snd = b.dataset.v; store.set("pp-wu-snd", W.snd); wrender(); }); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden && W.run) wake(true); });
    buildList(); go(0);
  }

  /* ---------- dead ball checker ---------- */
  var bchk = $("#bchk");
  if (bchk) {
    var B = {}, bout = $("#b-out"), BQ = ["use", "squeeze", "drop", "glass", "felt", "sound"];
    var WHY = { use: ["", "It has been used once or twice.", "The can has had several sessions.", "The can has had a lot of use."], squeeze: ["", "It feels a little soft.", "", "It squashes easily: the air is going."], drop: ["", "It bounces a bit lower than a new ball.", "", "It bounces much lower than a new ball."], glass: ["", "It comes back short off the glass.", "", "It dies in the corner off the glass."], felt: ["", "The felt is flat in places.", "The felt is bald, dirty or heavy."], sound: ["", "It sounds duller than a new ball."] };
    var brender = function () {
      $$(".bq", bchk).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.setAttribute("aria-pressed", B[q.dataset.q] === o.dataset.v ? "true" : "false"); }); });
      var n = BQ.filter(function (k) { return B[k] !== undefined; }).length;
      if (n < BQ.length) { bout.className = "result"; bout.innerHTML = "<h2>Check your ball</h2><p>" + (n ? (BQ.length - n) + " more to go." : "Answer the questions and the verdict appears here.") + "</p>"; return; }
      var sc = 0, max = 0, why = [];
      BQ.forEach(function (k) { var v = B[k]; if (v === "x") return; v = +v; sc += v; if (WHY[k][v]) why.push(WHY[k][v]); if (v > max) max = v; });
      var r;
      if (sc <= 2 && max <= 1) r = { c: "good", h: "Good for a match", p: "This ball still has its bounce. Use it for your next game." };
      else if (sc <= 6 && max < 3) r = { c: "mid", h: "Fine for practice", p: "It's losing pressure. Keep it for drills, warm-ups and practice serves, and open a new can for matches." };
      else r = { c: "fault", h: "Time for new balls", p: "This ball is dead or close to it. It will make rallies off the glass short and frustrating." };
      bout.className = "result " + r.c;
      bout.innerHTML = "<h2>" + r.h + "</h2><p>" + r.p + "</p>" + (why.length ? '<ul class="b-why">' + why.map(function (w) { return "<li>" + w + "</li>"; }).join("") + "</ul>" : "");
    };
    $$(".bq", bchk).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.addEventListener("click", function () { B[q.dataset.q] = o.dataset.v; brender(); }); }); });
    $("#b-reset").addEventListener("click", function () { B = {}; brender(); });
    brender();
  }

  /* ---------- wall and fence checker ---------- */
  var wr = $("#wr");
  if (wr && window.WR) {
    var WA = {}, wtxt = $("#wr-txt"), wout = $("#wr-out"), wpath = $("#wr-path"), wball = $("#wr-ball"), wmarks = $("#wr-marks"), wraf = null;
    var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var NEED2 = { a: 1, c: 1, e: 1 };
    var draw = function (pts) {
      if (wraf) cancelAnimationFrame(wraf);
      wmarks.innerHTML = "";
      if (!pts) { wpath.setAttribute("points", ""); wball.setAttribute("cx", 70); wball.setAttribute("cy", 110); return; }
      pts.slice(1, -1).forEach(function (p) { var c = document.createElementNS("http://www.w3.org/2000/svg", "circle"); c.setAttribute("cx", p[0]); c.setAttribute("cy", p[1]); c.setAttribute("r", 3.5); c.setAttribute("fill", "none"); c.setAttribute("stroke", "#fff"); c.setAttribute("stroke-width", 1.5); wmarks.appendChild(c); });
      var lens = [], tot = 0;
      for (var i = 1; i < pts.length; i++) { var l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); lens.push(l); tot += l; }
      var at = function (d) {
        var shown = [pts[0]];
        for (var j = 0; j < lens.length; j++) {
          if (d >= lens[j]) { d -= lens[j]; shown.push(pts[j + 1]); continue; }
          var f = d / lens[j]; shown.push([pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f]); break;
        }
        var last = shown[shown.length - 1];
        wpath.setAttribute("points", shown.map(function (p) { return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" "));
        wball.setAttribute("cx", last[0]); wball.setAttribute("cy", last[1]);
      };
      if (still) { at(tot); return; }
      var t0 = null, dur = Math.min(2200, 500 + tot * 2.6);
      var step = function (t) { if (t0 === null) t0 = t; var k = Math.min(1, (t - t0) / dur); at(tot * k); if (k < 1) wraf = requestAnimationFrame(step); };
      wraf = requestAnimationFrame(step);
    };
    var wrender = function (animate) {
      $$(".wr-q", wr).forEach(function (q) {
        var id = q.dataset.q;
        if (id !== "first") q.classList.toggle("off", WA.first !== id);
        q.hidden = id !== "first" && NEED2[WA.first] && WA.first !== id;
        $$(".opt", q).forEach(function (o) { o.setAttribute("aria-pressed", WA[id] === o.dataset.v ? "true" : "false"); });
      });
      var key = null;
      if (WA.first) key = NEED2[WA.first] ? (WA[WA.first] ? WA.first + "_" + WA[WA.first] : null) : WA.first;
      var r = key && window.WR[key];
      var cls = r ? (r[0] === "lose" ? "fault" : r[0] === "win" ? "good" : "let") : "";
      wout.className = "result" + (cls ? " " + cls : "");
      if (r) {
        wtxt.innerHTML = "<h2>" + r[1] + "</h2><p>" + r[2] + "</p><p class=\"wr-src\">Based on " + r[3] + ".</p>";
        if (animate) draw(r[4]);
      } else {
        if (animate) draw(null);
        if (WA.first) wtxt.innerHTML = "<h2>One more</h2><p>What happened next? Pick an answer in step 2.</p>";
      }
    };
    $$(".wr-q", wr).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.addEventListener("click", function () {
      var id = q.dataset.q;
      if (id === "first") { WA = { first: o.dataset.v }; } else { WA[id] = o.dataset.v; }
      wrender(true);
    }); }); });
    $("#wr-reset").addEventListener("click", function () { WA = {}; wrender(true); wtxt.innerHTML = "<h2>Make the call</h2><p>Tap what the ball touched and the verdict appears here.</p>"; });
    wrender(false);
  }

  /* ---------- padel vs tennis vs pickleball ---------- */
  var vsb = $("#vs");
  if (vsb && window.VS) {
    var VC = window.VS.c, vsShow = "all", vsUnit = "m", vinfo = $("#vs-info");
    var fmt = function (n) { return (+n.toFixed(2)) + (vsUnit === "m" ? " m" : " ft"); };
    var area = function (k) { var d = VC[k][vsUnit]; return Math.round(d[0] * d[1]).toLocaleString("en-GB") + (vsUnit === "m" ? " m²" : " sq ft"); };
    var share = function (k) { var a = VC[k].m[0] * VC[k].m[1], t = VC.t.m[0] * VC.t.m[1]; return Math.round(a / t * 100); };
    var vpaint = function () {
      $$(".vs-g", vsb).forEach(function (g) { g.classList.toggle("dim", vsShow !== "all" && g.dataset.s !== vsShow); g.classList.toggle("on", g.dataset.s === vsShow); });
      if (vsShow === "all") {
        vinfo.innerHTML = "<h2 style=\"font-size:1.4rem\">Three courts, one scale</h2><dl class=\"vs-dl\">" + ["t", "p", "k"].map(function (k) {
          var d = VC[k][vsUnit]; return "<dt>" + VC[k].name + "</dt><dd>" + fmt(d[0]) + " × " + fmt(d[1]) + "<span>" + area(k) + "</span></dd>";
        }).join("") + "</dl><p class=\"muted\" style=\"margin:0\">A padel court covers about " + share("p") + "% of a tennis doubles court, and a pickleball court about " + share("k") + "%. Tap a sport to see its court on its own.</p>";
        return;
      }
      var c = VC[vsShow], d = c[vsUnit];
      vinfo.innerHTML = "<h2 style=\"font-size:1.4rem\">" + c.name + "</h2><dl class=\"vs-dl\"><dt>Size</dt><dd>" + fmt(d[0]) + " × " + fmt(d[1]) + "</dd><dt>Area</dt><dd>" + area(vsShow) + (vsShow !== "t" ? "<span>About " + share(vsShow) + "% of a tennis doubles court</span>" : "") + "</dd><dt>Net</dt><dd>" + c.net + "</dd><dt>Walls</dt><dd>" + c.walls + "</dd></dl><p class=\"muted\" style=\"margin:0\">" + c.note + "</p>";
    };
    choose($("#vs-show"), function (v) { vsShow = v; vpaint(); });
    choose($("#vs-unit"), function (v) { vsUnit = v; vpaint(); });
    vpaint();
  }
  var vsq = $("#vsq");
  if (vsq && window.VS) {
    var VQ = window.VS.q, VA = {}, vout = $("#vsq-out"), NAMES = { t: "Tennis", p: "Padel", k: "Pickleball" };
    var vqrender = function () {
      $$(".vsq", vsq).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.setAttribute("aria-pressed", VA[q.dataset.q] === o.dataset.v ? "true" : "false"); }); });
      var keys = Object.keys(VA), tot = { t: 0, p: 0, k: 0 };
      if (!keys.length) { vout.innerHTML = "<h2>Your match</h2><p>Answer the questions and your best fit appears here. You can change any answer.</p>"; return; }
      keys.forEach(function (q) { var s = VQ[q][VA[q]]; tot.t += s[0]; tot.p += s[1]; tot.k += s[2]; });
      var order = ["p", "k", "t"].sort(function (a, b) { return tot[b] - tot[a]; });
      var max = Math.max(1, tot[order[0]]), left = 5 - keys.length;
      var tie = tot[order[0]] === tot[order[1]];
      vout.innerHTML = "<h2>" + (tie ? NAMES[order[0]] + " or " + NAMES[order[1]] : NAMES[order[0]]) + "</h2><p>" + window.VS.why[order[0]] + "</p><ul class=\"vs-bars\">" + order.map(function (k) {
        return "<li><span>" + NAMES[k] + "</span><i><b style=\"width:" + Math.round(tot[k] / max * 100) + "%\"></b></i><em>" + tot[k] + "</em></li>";
      }).join("") + "</ul><p style=\"margin-bottom:0\">" + (left ? left + (left === 1 ? " question" : " questions") + " left for a better match." : (tie ? "A tie: try a session of each and see which you enjoy most." : "Just for fun, not a test. The best sport is the one you'll keep playing.")) + "</p>";
    };
    $$(".vsq", vsq).forEach(function (q) { $$(".opt", q).forEach(function (o) { o.addEventListener("click", function () { VA[q.dataset.q] = o.dataset.v; vqrender(); }); }); });
    $("#vsq-reset").addEventListener("click", function () { VA = {}; vqrender(); });
  }
  /* ---------- racket weight and balance decoder ---------- */
  var rbEl = $("#rb");
  if (rbEl && window.RB) {
    var RBP = window.RB, rbSvg = $("#rb-svg"), rbTxt = $("#rb-txt");
    var RBS = store.get("pp-rb", { A: { w: 355, b: 255, s: "round" }, B: { w: 368, b: 275, s: "diamond" } });
    var rbClamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
    var rbHead = {
      round: function (c) { return "M" + c + " 20 C" + (c + 70) + " 20 " + (c + 126) + " 70 " + (c + 126) + " 160 C" + (c + 126) + " 240 " + (c + 80) + " 300 " + c + " 305 C" + (c - 80) + " 300 " + (c - 126) + " 240 " + (c - 126) + " 160 C" + (c - 126) + " 70 " + (c - 70) + " 20 " + c + " 20Z"; },
      teardrop: function (c) { return "M" + c + " 20 C" + (c + 112) + " 20 " + (c + 130) + " 90 " + (c + 124) + " 160 C" + (c + 114) + " 245 " + (c + 54) + " 298 " + c + " 305 C" + (c - 54) + " 298 " + (c - 114) + " 245 " + (c - 124) + " 160 C" + (c - 130) + " 90 " + (c - 112) + " 20 " + c + " 20Z"; },
      diamond: function (c) { return "M" + c + " 20 C" + (c + 84) + " 20 " + (c + 130) + " 44 " + (c + 130) + " 96 L" + (c + 114) + " 178 C" + (c + 96) + " 250 " + (c + 50) + " 298 " + c + " 305 C" + (c - 50) + " 298 " + (c - 96) + " 250 " + (c - 114) + " 178 L" + (c - 130) + " 96 C" + (c - 130) + " 44 " + (c - 84) + " 20 " + c + " 20Z"; }
    };
    var RBSS = { round: [165, 70, 74], teardrop: [140, 62, 62], diamond: [108, 50, 48] };
    var bBand = function (b) { return b < 260 ? ["Low balance", "head-light"] : b <= 270 ? ["Medium balance", "even"] : ["High balance", "head-heavy"]; };
    var wBand = function (w) { return w < 355 ? "light" : w < 370 ? "medium weight" : "heavy"; };
    function rbFeel(r) {
      var wx = (r.w - 330) / 60, bx = (r.b - 248) / 34;
      return { power: Math.round(rbClamp(10 + wx * 45 + bx * 45, 5, 98)), speed: Math.round(rbClamp(95 - wx * 50 - bx * 40, 5, 98)), arm: Math.round(rbClamp(8 + wx * 40 + bx * 52, 5, 98)) };
    }
    function rbSuits(r) {
      var lo = r.b < 260, hi = r.b > 270, lt = r.w < 355, hv = r.w >= 370;
      if (lo && !hv) return "Beginners, players with sore elbows or shoulders, and anyone who wants control and fast hands at the net.";
      if (hi && !lt) return "Experienced attackers who hit hard and want power on smashes, and have the technique and fitness to handle it.";
      if (hi && lt) return "Players who want some extra head weight for power but still want a light racket overall.";
      if (lo && hv) return "Strong players who want a solid, stable feel but still like the weight close to the hand.";
      return "Improving players who want a mix of control and power: an all-round set-up.";
    }
    function rbRacket(c, r, col, key) {
      var y = 475 - r.b, ss = RBSS[r.s], o = "";
      o += '<rect x="' + (c - 18) + '" y="300" width="36" height="175" rx="12" fill="' + col + '"/>';
      o += '<path d="' + rbHead[r.s](c) + '" fill="' + col + '"/>';
      o += '<ellipse cx="' + c + '" cy="' + ss[0] + '" rx="' + ss[1] + '" ry="' + ss[2] + '" fill="#1e46c8" fill-opacity=".28" stroke="#0e2468" stroke-width="2" stroke-dasharray="6 5"/>';
      o += '<text x="' + c + '" y="' + (ss[0] + 6) + '" text-anchor="middle" font-size="17" font-weight="700" fill="#0e2468" font-family="Onest, sans-serif">Sweet spot</text>';
      o += '<path d="M' + (c - 140) + ' ' + y + 'h280" stroke="#ff6b4a" stroke-width="4"/>';
      o += '<circle cx="' + c + '" cy="' + y + '" r="11" fill="#ff6b4a" stroke="#fff" stroke-width="3"/>';
      o += '<text x="' + c + '" y="' + (y - 20) + '" text-anchor="middle" font-size="20" font-weight="800" fill="#fff" stroke="#0b1530" stroke-width="5" paint-order="stroke" font-family="Unbounded, sans-serif">' + key + " " + r.b + " mm</text>";
      return o;
    }
    function rbDraw() {
      var o = '<rect width="600" height="520" rx="16" fill="#0b1c55"/>';
      var my = 475 - 227.5;
      o += rbRacket(150, RBS.A, "#e8f84a", "A") + rbRacket(450, RBS.B, "#f4f6f1", "B");
      o += '<path d="M8 ' + my + 'h584" stroke="#9cc4ea" stroke-width="2" stroke-dasharray="8 7"/>';
      for (var m = 0; m <= 450; m += 50) {
        var ty = 475 - m;
        o += '<path d="M292 ' + ty + 'h16" stroke="#9fb0e0" stroke-width="2"/><text x="300" y="' + (ty - 5) + '" text-anchor="middle" font-size="13" fill="#9fb0e0" font-family="Onest, sans-serif">' + m + "</text>";
      }
      o += '<path d="M300 25V475" stroke="#9fb0e0" stroke-width="1.5" opacity=".5"/><text x="300" y="505" text-anchor="middle" font-size="14" fill="#c9d6fb" font-family="Onest, sans-serif">mm from the bottom of the handle</text>';
      rbSvg.innerHTML = o;
    }
    function rbBars(f) {
      return '<ul class="vs-bars">' + [["Power", f.power], ["Speed at the net", f.speed], ["Load on the arm", f.arm]].map(function (x) {
        return "<li><span>" + x[0] + '</span><i><b style="width:' + x[1] + '%"></b></i><em>' + x[1] + "</em></li>";
      }).join("") + "</ul>";
    }
    function rbCmp() {
      var A = RBS.A, B = RBS.B, dw = B.w - A.w, db = B.b - A.b, parts = [];
      if (dw === 0 && db === 0) return "Both rackets have the same weight and balance, so any difference you feel comes from the shape, core, face and stiffness.";
      if (dw) parts.push(Math.abs(dw) + " g " + (dw > 0 ? "heavier" : "lighter"));
      if (db) parts.push(Math.abs(db) + " mm " + (db > 0 ? "more head-heavy" : "more head-light"));
      var p = dw * 1 + db * 1.4, s = "Racket B is " + parts.join(" and ") + " than racket A. ";
      if (Math.abs(p) < 4) s += "That is a small change: they should feel quite similar to swing.";
      else if (p > 0) s += "Expect B to hit a little harder on smashes and feel more solid, but slower in fast exchanges at the net and harder on the arm.";
      else s += "Expect B to feel quicker and easier to control at the net, with a little less free power on smashes.";
      return s;
    }
    function rbRender() {
      ["A", "B"].forEach(function (k) {
        var r = RBS[k], box = $('.rb-r[data-r="' + k + '"]', rbEl);
        $$("input", box).forEach(function (i) { if (document.activeElement !== i) i.value = r[i.dataset.f]; });
        $("#rb-wo-" + k).textContent = r.w + " g"; $("#rb-bo-" + k).textContent = r.b + " mm";
        $$(".rb-shape .opt", box).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === r.s ? "true" : "false"); });
      });
      rbDraw();
      rbTxt.innerHTML = ["A", "B"].map(function (k) {
        var r = RBS[k], bb = bBand(r.b);
        return '<div class="rb-res"><h3><i class="rb-dot rb-' + k.toLowerCase() + '"></i>Racket ' + k + ": " + bb[0] + ", " + wBand(r.w) + "</h3><p>" + r.w + " g, balance " + r.b + " mm (" + bb[1] + "), " + r.s + " shape. Suits: " + rbSuits(r) + "</p>" + rbBars(rbFeel(r)) + "</div>";
      }).join("") + '<p class="rb-cmp">' + rbCmp() + "</p>";
      store.set("pp-rb", RBS);
    }
    $$(".rb-r", rbEl).forEach(function (box) {
      var k = box.dataset.r;
      $$("input", box).forEach(function (i) {
        i.addEventListener("input", function () {
          var v = parseInt(i.value, 10); if (isNaN(v)) return;
          RBS[k][i.dataset.f] = rbClamp(v, parseInt(i.min, 10), parseInt(i.max, 10)); rbRender();
        });
        i.addEventListener("change", function () { rbRender(); i.value = RBS[k][i.dataset.f]; });
      });
      $$(".rb-shape .opt", box).forEach(function (b) { b.addEventListener("click", function () { RBS[k].s = b.dataset.v; rbRender(); }); });
      $$("[data-p]", box).forEach(function (b) { b.addEventListener("click", function () { var p = RBP[b.dataset.p]; RBS[k] = { w: p[0], b: p[1], s: p[2] }; rbRender(); }); });
    });
    $("#rb-copy").addEventListener("click", function () {
      var t = ["A", "B"].map(function (k) { var r = RBS[k]; return "Racket " + k + ": " + r.w + " g, " + r.b + " mm (" + bBand(r.b)[1] + "), " + r.s; }).join("\n") + "\n" + rbCmp() + "\nhttps://padelglassbox.com/racket-balance";
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { toast("Copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    rbRender();
  }

  /* ---------- round robin (fixed pairs) ---------- */
  var rr = $("#rr-setup");
  if (rr) (function () {
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var FMT = { set: { max: 7, note: "Enter games won, for example 6-3 or 7-6. Draws aren't possible." }, race: { max: 4, note: "First pair to 4 games wins, for example 4-2. Quick enough for big groups." }, free: { max: 99, note: "Play for a set time and enter the games or points each pair won. Draws count." } };
    var cfg = store.get("pp-rr-cfg", { fmt: "set", pts: "w" }), R = store.get("pp-rr", null);
    var namesEl = $("#rr-names"), courtsEl = $("#rr-courts"), legsEl = $("#rr-legs"), err = $("#rr-err");
    var parse = function () { return namesEl.value.split(/\n/).map(function (x) { return x.trim(); }).filter(Boolean).slice(0, 40); };
    var sync = function () {
      $$("[data-rr] button", rr).forEach(function (b) { var g = b.parentNode.dataset.rr; b.setAttribute("aria-pressed", String(cfg[g] === b.dataset.v)); });
      $("#rr-fmt-note").textContent = FMT[cfg.fmt].note;
      var n = parse().length, m = n * (n - 1) / 2;
      $("#rr-count").textContent = n ? n + " pair" + (n === 1 ? "" : "s") + (n >= 3 ? ": " + m + " matches over " + (n % 2 ? n : n - 1) + " rounds" + (legsEl.value === "2" ? " (twice that if you play each pair twice)" : "") : ", add at least 3") : "";
    };
    $$("[data-rr]", rr).forEach(function (g) { choose(g, function (v) { cfg[g.dataset.rr] = v; store.set("pp-rr-cfg", cfg); sync(); }); });
    namesEl.addEventListener("input", sync); legsEl.addEventListener("change", sync);
    $("#rr-demo").addEventListener("click", function () { namesEl.value = ["Sam & Priya", "Omar & Lucia", "Ben & Aisha", "Marta & Jon", "Leo & Fatima", "Chris & Noor"].join("\n"); sync(); });
    // circle method: fix team 0, rotate the rest
    var schedule = function (n, legs) {
      var ids = []; for (var i = 0; i < n; i++) ids.push(i);
      if (n % 2) ids.push(-1);
      var k = ids.length, rounds = [];
      for (var r = 0; r < k - 1; r++) {
        var ms = [], rest = [];
        for (var j = 0; j < k / 2; j++) {
          var a = ids[j], b = ids[k - 1 - j];
          if (a < 0 || b < 0) { rest.push(a < 0 ? b : a); continue; }
          ms.push(r % 2 && j === 0 ? { a: b, b: a, sa: null, sb: null } : { a: a, b: b, sa: null, sb: null });
        }
        rounds.push({ m: ms, rest: rest });
        ids = [ids[0]].concat([ids[k - 1]], ids.slice(1, k - 1));
      }
      if (legs === 2) rounds = rounds.concat(rounds.map(function (x) { return { m: x.m.map(function (y) { return { a: y.b, b: y.a, sa: null, sb: null }; }), rest: x.rest.slice() }; }));
      return rounds;
    };
    var done = function (m) { return m.sa !== null && m.sb !== null; };
    var table = function () {
      var P = R.names.map(function (n, i) { return { i: i, name: n, p: 0, w: 0, d: 0, l: 0, gf: 0, ga: 0 }; });
      R.rounds.forEach(function (r) { r.m.forEach(function (m) {
        if (!done(m)) return; var A = P[m.a], B = P[m.b]; A.p++; B.p++; A.gf += m.sa; A.ga += m.sb; B.gf += m.sb; B.ga += m.sa;
        if (m.sa > m.sb) { A.w++; B.l++; } else if (m.sb > m.sa) { B.w++; A.l++; } else { A.d++; B.d++; }
      }); });
      var key = function (x) { return R.pts === "3" ? x.w * 3 + x.d : x.w + x.d * 0.5; };
      var h2h = function (x, y) { var s = 0; R.rounds.forEach(function (r) { r.m.forEach(function (m) { if (!done(m)) return; if (m.a === x.i && m.b === y.i) s += m.sa - m.sb; if (m.a === y.i && m.b === x.i) s += m.sb - m.sa; }); }); return s; };
      P.sort(function (x, y) { return key(y) - key(x) || (y.gf - y.ga) - (x.gf - x.ga) || y.gf - x.gf || h2h(y, x) || x.i - y.i; });
      P.key = key; return P;
    };
    var draw = function () {
      var P = table(), any = P.some(function (x) { return x.p; }), total = 0, played = 0;
      R.rounds.forEach(function (r) { r.m.forEach(function (m) { total++; if (done(m)) played++; }); });
      $("#rr-board").innerHTML = "<h2>Standings</h2>" + (any ? "" : "<p>Enter the games after each match. The table updates as you type.</p>") +
        '<table><thead><tr><th>#</th><th>Pair</th><th class="num">P</th><th class="num">W</th>' + (R.fmt === "free" ? '<th class="num">D</th>' : "") + '<th class="num">L</th><th class="num">+/-</th>' + (R.pts === "3" ? '<th class="num">Pts</th>' : "") + "</tr></thead><tbody>" +
        P.map(function (x, k) { var gd = x.gf - x.ga; return '<tr class="' + (k === 0 && any ? "top" : "") + '"><td>' + (k + 1) + "</td><td>" + esc(x.name) + '</td><td class="num">' + x.p + '</td><td class="num">' + (R.pts === "3" ? x.w : "<b>" + x.w + "</b>") + "</td>" + (R.fmt === "free" ? '<td class="num">' + x.d + "</td>" : "") + '<td class="num">' + x.l + '</td><td class="num">' + (gd > 0 ? "+" : "") + gd + "</td>" + (R.pts === "3" ? '<td class="num"><b>' + P.key(x) + "</b></td>" : "") + "</tr>"; }).join("") + "</tbody></table>" +
        '<p style="margin:12px 0 0;font-size:.88rem">' + played + " of " + total + " matches played. " + (played === total && any ? "<b>" + esc(P[0].name) + "</b> top the table. Play a final with the <a href=\"score.html\" style=\"color:#e8f84a\">score keeper</a>?" : "Sorted by " + (R.pts === "3" ? "points" : "wins") + ", then game difference, then games won, then head-to-head.") + "</p>";
      var a = $("#rr-board a"); if (a && location.protocol !== "file:") a.setAttribute("href", "/score");
    };
    var nm = function (i) { return esc(R.names[i]); };
    var drawList = function () {
      var html = "", mx = FMT[R.fmt].max;
      R.rounds.forEach(function (r, ri) {
        var all = r.m.every(done);
        html += '<div class="card round"><h3>Round ' + (ri + 1) + "<small>" + (all ? "Done" : r.m.length + " match" + (r.m.length === 1 ? "" : "es")) + "</small></h3>";
        r.m.forEach(function (m, mi) {
          var slot = Math.floor(mi / R.courts), ct = (mi % R.courts) + 1;
          var lab = R.courts < r.m.length ? "Slot " + (slot + 1) + " · Court " + ct : "Court " + ct;
          var cls = done(m) ? (m.sa > m.sb ? " won-a" : m.sb > m.sa ? " won-b" : "") : "";
          html += '<div class="match' + cls + '"><span class="ct">' + lab + "</span>" +
            '<div class="pair a"><input type="number" min="0" max="' + mx + '" inputmode="numeric" aria-label="Games for ' + nm(m.a) + '" data-r="' + ri + '" data-m="' + mi + '" data-s="a" value="' + (m.sa === null ? "" : m.sa) + '"><span>' + nm(m.a) + "</span></div>" +
            '<span class="vs">vs</span><div class="pair b"><span>' + nm(m.b) + '</span><input type="number" min="0" max="' + mx + '" inputmode="numeric" aria-label="Games for ' + nm(m.b) + '" data-r="' + ri + '" data-m="' + mi + '" data-s="b" value="' + (m.sb === null ? "" : m.sb) + '"></div></div>';
        });
        if (r.rest.length) html += '<p class="rest">Resting: ' + r.rest.map(nm).join(", ") + "</p>";
        html += "</div>";
      });
      $("#rr-list").innerHTML = html;
      var tm = 0; R.rounds.forEach(function (r) { tm += r.m.length; });
      $("#rr-sum").textContent = R.names.length + " pairs · " + R.rounds.length + " rounds · " + tm + " matches · " + R.courts + " court" + (R.courts === 1 ? "" : "s");
      draw();
    };
    var show = function (live) { rr.hidden = live; $("#rr-live").hidden = !live; $(".gen").classList.toggle("live", live); };
    $("#rr-list").addEventListener("input", function (ev) {
      var t = ev.target; if (!t.dataset || t.dataset.s === undefined) return;
      var m = R.rounds[+t.dataset.r].m[+t.dataset.m], v = t.value === "" ? null : Math.max(0, Math.min(FMT[R.fmt].max, Math.round(+t.value)));
      m["s" + t.dataset.s] = v;
      var row = t.parentNode.parentNode; row.classList.remove("won-a", "won-b");
      if (done(m)) { if (m.sa > m.sb) row.classList.add("won-a"); else if (m.sb > m.sa) row.classList.add("won-b"); }
      var r = R.rounds[+t.dataset.r], sm = row.parentNode.querySelector("h3 small"); if (sm) sm.textContent = r.m.every(done) ? "Done" : r.m.length + " match" + (r.m.length === 1 ? "" : "es");
      store.set("pp-rr", R); draw();
    });
    $("#rr-start").addEventListener("click", function () {
      var names = parse(), courts = Math.round(+courtsEl.value) || 1; err.textContent = "";
      if (names.length < 3) { err.textContent = "Add at least 3 pairs, one per line."; return; }
      if (names.length > 16) { err.textContent = "This tool handles up to 16 pairs."; return; }
      courts = Math.max(1, Math.min(courts, 8, Math.floor(names.length / 2)));
      R = { names: names, courts: courts, fmt: cfg.fmt, pts: cfg.pts, rounds: schedule(names.length, +legsEl.value) };
      store.set("pp-rr", R); show(true); drawList();
      $("#rr-live").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    $("#rr-new").addEventListener("click", function () {
      if (!confirm("Start a new round robin? The current scores will be cleared.")) return;
      namesEl.value = R.names.join("\n"); R = null; store.set("pp-rr", null); show(false); sync();
    });
    $("#rr-copy").addEventListener("click", function () {
      var P = table(), txt = "Round robin standings\n" + P.map(function (x, k) { return (k + 1) + ". " + x.name + "  W" + x.w + (R.fmt === "free" ? " D" + x.d : "") + " L" + x.l + "  games " + x.gf + "-" + x.ga + (R.pts === "3" ? "  " + P.key(x) + " pts" : ""); }).join("\n") + "\n\nResults\n";
      R.rounds.forEach(function (r, ri) { r.m.forEach(function (m) { if (done(m)) txt += "R" + (ri + 1) + ": " + R.names[m.a] + " " + m.sa + "-" + m.sb + " " + R.names[m.b] + "\n"; }); });
      txt += "\nMade with padelglassbox.com/round-robin";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    sync();
    if (R && R.rounds) { show(true); drawList(); }
  })();

  /* ---------- padel shoes finder ---------- */
  var sh = $("#shoe");
  if (sh) (function () {
    var A = store.get("pp-shoe", {}), out = $("#shoe-out");
    var SOLE = {
      sand: ["Herringbone", "Your courts are sandy, so look for a full zig-zag (herringbone) sole. The grooves let the sand through, so you can stop and turn without sliding too far."],
      low: ["Omni or hybrid", "On courts with little sand, a herringbone sole can feel too sticky or skate on the turf. An omni sole (small studs) or a hybrid grips better here."],
      mix: ["Hybrid", "You play on different courts, so a hybrid sole (zig-zag on the outside, studs in the middle) is the safest all-round choice."],
      dk: ["Herringbone or hybrid", "Most padel courts are artificial grass with sand, so herringbone is the usual pick. If you aren't sure, a hybrid sole copes with most courts. Look at the court surface next time you play."]
    };
    var render = function () {
      $$(".sh-q", sh).forEach(function (q) { $$("button", q).forEach(function (b) { b.setAttribute("aria-pressed", String(A[q.dataset.q] === b.dataset.v)); }); });
      var left = ["court", "often", "now", "feel"].filter(function (k) { return !A[k]; }).length;
      if (!A.court) { out.innerHTML = "<h2>Your shoe match</h2><p>Start with your courts: the surface decides the sole.</p>"; return; }
      var s = SOLE[A.court], tips = [];
      if (A.now === "run") tips.push("Swap your running shoes before your next game. They are made for going forward, with little side support, so it is easy to slip or roll an ankle.");
      if (A.now === "ten") tips.push("Tennis shoes are OK to start. If you play every week, padel shoes will grip the turf better.");
      if (A.now === "none") tips.push("For a first try, tennis shoes are fine. Buy padel shoes once you know you'll keep playing.");
      if (A.feel === "grip") tips.push(A.now === "pad" ? "Slipping in padel shoes often means a worn sole, or a sole that doesn't match the court. Check the wear list below." : "More grip is the main reason to buy padel shoes. Match the sole to the court.");
      if (A.feel === "soft" || A.often === "3") tips.push("Look for more cushioning in the heel and forefoot. The more you play, the more it matters.");
      if (A.feel === "stab") tips.push("Choose a shoe that feels stable through the middle of the foot, with a firm heel. If your ankle keeps rolling, see a physio.");
      var life = A.often === "3" ? "about every 4 months" : A.often === "2" ? "about every 4 to 6 months" : A.often === "1" ? "after a year or more" : "about every 4 to 6 months if you play weekly";
      out.innerHTML = '<span class="pill b">Look for</span><h2 style="margin-top:8px">' + s[0] + "</h2>" + '<div class="sole-mini">' + (A.court === "sand" ? window.SOLES.herring : A.court === "low" ? window.SOLES.omni : window.SOLES.hybrid) + "</div><p>" + s[1] + "</p>" +
        (tips.length ? '<ul class="b-why">' + tips.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>" : "") +
        "<p><b>Replace them:</b> " + life + ", or sooner if the sole is worn smooth.</p>" +
        (left ? '<p class="wr-src">' + left + " more question" + (left === 1 ? "" : "s") + " for better tips.</p>" : '<p class="wr-src">General guidance from padel shoe guides, not medical advice.</p>');
    };
    $$(".sh-q", sh).forEach(function (q) { $$("button", q).forEach(function (b) { b.addEventListener("click", function () { A[q.dataset.q] = b.dataset.v; store.set("pp-shoe", A); render(); }); }); });
    $("#shoe-reset").addEventListener("click", function () { A = {}; store.set("pp-shoe", A); render(); });
    render();
    var wl = $("#shoe-wear"), wv = $("#shoe-wv");
    if (wl) wl.addEventListener("change", function () {
      var sc = 0, n = 0; $$("input", wl).forEach(function (c) { if (c.checked) { sc += +c.dataset.w; n++; } });
      wv.className = "shoe-wv" + (sc >= 3 ? " bad" : sc ? " mid" : "");
      wv.textContent = !n ? "Tick anything that sounds like your shoes." : sc >= 3 ? "Time for new shoes. Worn soles and flat cushioning make slips and sore legs more likely." : "Not yet, but keep an eye on them. Check again in a few weeks.";
    });
  })();
  /* ---------- padel calories calculator ---------- */
  var cal = $("#cal");
  if (cal) (function () {
    var C = window.CAL || {}, S = store.get("pp-cal", { w: 75, unit: "kg", t: 90, lv: "club", s: 2 });
    var wEl = $("#cal-w"), tEl = $("#cal-t"), sEl = $("#cal-s"), out = $("#cal-out");
    wEl.value = S.w; tEl.value = S.t; sEl.value = S.s;
    var kcal = function (met, kg, min) { return met * 3.5 * kg / 200 * min; };
    var r10 = function (x) { return Math.round(x / 5) * 5; };
    var render = function () {
      $$("[data-cal] button", cal).forEach(function (b) { b.setAttribute("aria-pressed", String(S[b.parentNode.dataset.cal] === b.dataset.v)); });
      $("#cal-tv").textContent = S.t + " min"; $("#cal-sv").textContent = S.s;
      $("#cal-lv-note").textContent = "Uses " + C[S.lv][1] + " METs. " + C[S.lv][2] + ".";
      var w = +S.w, kg = S.unit === "lb" ? w / 2.20462 : w;
      if (!(kg >= 25 && kg <= 200)) { out.innerHTML = "<h2>Your estimate</h2><p>Enter a body weight between " + (S.unit === "lb" ? "55 and 440 lb" : "25 and 200 kg") + ".</p>"; return; }
      var met = C[S.lv][1], one = kcal(met, kg, S.t), hr = kcal(met, kg, 60), wk = one * S.s;
      var vig = met >= 6, mins = S.t * S.s, eq = vig ? mins * 2 : mins, pct = Math.round(eq / 150 * 100);
      var bars = ["easy", "club", "hard"].map(function (k) { var v = kcal(C[k][1], kg, S.t), mx = kcal(C.hard[1], kg, S.t); return "<dt>" + C[k][0] + "</dt><dd>" + r10(v) + ' kcal<div class="meter"><i style="width:' + Math.round(v / mx * 100) + '%"></i></div></dd>'; }).join("");
      out.innerHTML = '<span class="pill b">' + C[S.lv][0] + " · " + S.t + " min</span>" +
        '<p class="cal-big"><b>' + r10(one) + "</b> kcal</p><p>About " + r10(hr * 0.85) + " to " + r10(hr * 1.15) + " kcal per hour for you at this effort, give or take.</p>" +
        '<dl class="spec">' + bars + "</dl>" +
        "<p><b>Each week:</b> about " + (Math.round(wk / 50) * 50).toLocaleString("en-GB") + " kcal from " + S.s + " session" + (S.s > 1 ? "s" : "") + " (" + mins + " min, " + (vig ? "vigorous" : "moderate") + ").</p>" +
        "<p><b>Weekly activity target:</b> " + pct + "% of the NHS and WHO minimum" + (vig ? " (vigorous minutes count double)" : "") + ".</p>" +
        '<div class="meter"><i style="width:' + Math.min(100, pct) + '%"></i></div>' +
        '<div class="btns" style="margin-top:16px"><button class="btn lime sm" type="button" id="cal-copy">Copy result</button></div>' +
        '<p class="wr-src">Estimate based on tennis METs from the Compendium of Physical Activities. Not medical advice.</p>';
      $("#cal-copy").addEventListener("click", function () {
        var txt = "Padel calories: about " + r10(one) + " kcal for " + S.t + " min (" + C[S.lv][0].toLowerCase() + "), about " + (Math.round(wk / 50) * 50) + " kcal a week. padelglassbox.com/padel-calories";
        if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
      });
    };
    var save = function () { store.set("pp-cal", S); render(); };
    $$("[data-cal]", cal).forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () {
      var k = g.dataset.cal, v = b.dataset.v;
      if (k === "unit" && v !== S.unit && +S.w) { S.w = Math.round(v === "lb" ? S.w * 2.20462 : S.w / 2.20462); wEl.value = S.w; }
      S[k] = v; save(); }); }); });
    wEl.addEventListener("input", function () { S.w = wEl.value; save(); });
    tEl.addEventListener("input", function () { S.t = +tEl.value; save(); });
    sEl.addEventListener("input", function () { S.s = +sEl.value; save(); });
    render();
  })();

  /* ---------- padel ladder tracker ---------- */
  var ld = $("#ld-setup");
  if (ld) (function () {
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var cfg = store.get("pp-ld-cfg", { who: "pairs", range: "3", move: "swap" }), L = store.get("pp-ld", null), win = null;
    var namesEl = $("#ld-names"), err = $("#ld-err"), chEl = $("#ld-ch"), dfEl = $("#ld-df");
    var MOVE = { swap: "The winner and the loser swap places. Nobody else moves.", jump: "The winner takes the loser's place. The loser and everyone in between move down one." };
    var parse = function () { var seen = {}; return namesEl.value.split("\n").map(function (x) { return x.trim().slice(0, 60); }).filter(function (x) { if (!x || seen[x.toLowerCase()]) return false; seen[x.toLowerCase()] = 1; return true; }); };
    var sync = function () {
      $$("[data-ld] button", ld).forEach(function (b) { b.setAttribute("aria-pressed", String(cfg[b.parentNode.dataset.ld] === b.dataset.v)); });
      $("#ld-move-note").textContent = MOVE[cfg.move];
      var n = parse().length, w = cfg.who === "pairs" ? "pair" : "player";
      $("#ld-count").textContent = n ? n + " " + w + (n === 1 ? "" : "s") + (n < 4 ? ", add at least 4" : "") : "";
      namesEl.placeholder = cfg.who === "pairs" ? "Sam & Priya\nOmar & Lucia\nBen & Aisha\n..." : "Sam\nPriya\nOmar\n...";
    };
    $$("[data-ld]", ld).forEach(function (g) { choose(g, function (v) { cfg[g.dataset.ld] = v; store.set("pp-ld-cfg", cfg); sync(); }); });
    namesEl.addEventListener("input", sync);
    $("#ld-demo").addEventListener("click", function () { namesEl.value = (cfg.who === "pairs" ? ["Sam & Priya", "Omar & Lucia", "Ben & Aisha", "Marta & Jon", "Leo & Fatima", "Chris & Noor", "Ana & Raj", "Tom & Mei"] : ["Sam", "Priya", "Omar", "Lucia", "Ben", "Aisha", "Marta", "Jon"]).join("\n"); sync(); });
    var byId = function (id) { for (var i = 0; i < L.p.length; i++) if (L.p[i].id === id) return L.p[i]; };
    var pos = function (id) { return L.order.indexOf(id); };
    var fillSel = function () {
      var keep = chEl.value;
      chEl.innerHTML = L.order.slice(1).map(function (id) { return '<option value="' + id + '">' + (pos(id) + 1) + ". " + esc(byId(id).n) + "</option>"; }).join("");
      if (keep && pos(+keep) > 0) chEl.value = keep;
      fillDf();
    };
    var fillDf = function () {
      var c = pos(+chEl.value), rg = +L.range, keep = dfEl.value, opts = [];
      for (var i = Math.max(0, c - rg); i < c; i++) opts.push('<option value="' + L.order[i] + '">' + (i + 1) + ". " + esc(byId(L.order[i]).n) + "</option>");
      dfEl.innerHTML = opts.reverse().join("");
      if (keep && opts.join("").indexOf('value="' + keep + '"') > -1) dfEl.value = keep;
    };
    chEl.addEventListener("change", fillDf);
    var draw = function () {
      var w = L.who === "pairs" ? "pairs" : "players";
      $("#ld-sum").textContent = L.order.length + " " + w + " · challenge up to " + (L.range === "99" ? "anyone above" : L.range + " places") + " · " + L.h.length + " match" + (L.h.length === 1 ? "" : "es");
      $("#ld-board").innerHTML = "<h2>The ladder</h2><table><thead><tr><th>#</th><th>" + (L.who === "pairs" ? "Pair" : "Player") + '</th><th class="num">W-L</th><th class="num">Last move</th></tr></thead><tbody>' +
        L.order.map(function (id, i) { var x = byId(id), mv = x.mv || 0; return "<tr" + (i === 0 ? ' class="top"' : "") + "><td>" + (i + 1) + "</td><td>" + esc(x.n) + '</td><td class="num">' + x.w + "-" + x.l + '</td><td class="num ld-mv' + (mv > 0 ? " up" : mv < 0 ? " dn" : "") + '">' + (mv > 0 ? "▲" + mv : mv < 0 ? "▼" + (-mv) : "–") + "</td></tr>"; }).join("") + "</tbody></table>" +
        (L.h.length ? "" : "<p style=\"margin-top:12px\">Record the first challenge to start moving the ladder.</p>");
      $("#ld-hist").innerHTML = L.h.length ? L.h.slice().reverse().map(function (m) { return "<li><b>" + esc(m.wn) + "</b> beat " + esc(m.ln) + (m.sc ? " (" + esc(m.sc) + ")" : "") + '<span class="muted"> · ' + (m.up ? "moved up to #" + (m.to + 1) : "no change") + " · " + m.d + "</span></li>"; }).join("") : '<li class="muted">No matches yet.</li>';
      fillSel();
    };
    var show = function (live) { ld.hidden = live; $("#ld-live").hidden = !live; $(".gen").classList.toggle("live", live); };
    var save = function () { store.set("pp-ld", L); draw(); };
    $("#ld-start").addEventListener("click", function () {
      var names = parse(); err.textContent = "";
      if (names.length < 4) { err.textContent = "Add at least 4 names, one per line."; return; }
      if (names.length > 40) { err.textContent = "This tool handles up to 40 names."; return; }
      L = { who: cfg.who, range: cfg.range, move: cfg.move, p: names.map(function (n, i) { return { id: i + 1, n: n, w: 0, l: 0, mv: 0 }; }), h: [], snap: [] };
      L.order = L.p.map(function (x) { return x.id; }); L.next = names.length + 1;
      show(true); save();
      $("#ld-live").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    choose($("#ld-win"), function (v) { win = v; });
    $("#ld-save").addEventListener("click", function () {
      var re = $("#ld-rerr"), c = +chEl.value, d = +dfEl.value; re.textContent = "";
      if (!c || !d) { re.textContent = "Pick the challenger and who they challenged."; return; }
      if (!win) { re.textContent = "Pick who won."; return; }
      L.snap.push(JSON.stringify({ order: L.order, p: L.p })); if (L.snap.length > 30) L.snap.shift();
      var pc = pos(c), pd = pos(d), C = byId(c), Dd = byId(d), up = win === "c";
      var before = L.order.slice();
      if (up) {
        if (L.move === "swap") { L.order[pd] = c; L.order[pc] = d; }
        else { L.order.splice(pc, 1); L.order.splice(pd, 0, c); }
        C.w++; Dd.l++;
      } else { Dd.w++; C.l++; }
      L.p.forEach(function (x) { var b0 = before.indexOf(x.id), a0 = pos(x.id); if (b0 !== a0) x.mv = b0 - a0; });
      var dt = new Date();
      L.h.push({ wn: up ? C.n : Dd.n, ln: up ? Dd.n : C.n, sc: $("#ld-sc").value.trim().slice(0, 40), up: up, to: up ? pd : pd, d: dt.getDate() + " " + ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.getMonth()] });
      $("#ld-sc").value = ""; win = null; $$("#ld-win button").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
      save(); toast(up ? C.n + " move up to #" + (pd + 1) : Dd.n + " hold their place");
    });
    $("#ld-undo").addEventListener("click", function () {
      if (!L.h.length || !L.snap.length) { toast("Nothing to undo"); return; }
      var s = JSON.parse(L.snap.pop()); L.order = s.order; L.p = s.p; L.h.pop(); save(); toast("Last result undone");
    });
    $("#ld-addb").addEventListener("click", function () {
      var a = $("#ld-add"), n = a.value.trim().slice(0, 60);
      if (!n) return;
      if (L.p.some(function (x) { return x.n.toLowerCase() === n.toLowerCase(); })) { toast("That name is already on the ladder"); return; }
      if (L.order.length >= 40) { toast("The ladder is full (40)"); return; }
      L.p.push({ id: L.next, n: n, w: 0, l: 0, mv: 0 }); L.order.push(L.next); L.next++; a.value = ""; save(); toast("Added at #" + L.order.length);
    });
    $("#ld-new").addEventListener("click", function () {
      if (!confirm("Start a new ladder? The current one will be cleared from this device.")) return;
      namesEl.value = L.order.map(function (id) { return byId(id).n; }).join("\n"); L = null; store.set("pp-ld", null); show(false); sync();
    });
    $("#ld-copy").addEventListener("click", function () {
      var txt = "Padel ladder\n" + L.order.map(function (id, i) { var x = byId(id); return (i + 1) + ". " + x.n + "  (" + x.w + "-" + x.l + ")"; }).join("\n") + "\n\nMade with padelglassbox.com/ladder";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Ladder copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    sync();
    if (L && L.order) { show(true); draw(); }
  })();

  /* ---------- net rules checker ---------- */
  var nt = $("#nt");
  if (nt && window.NT) {
    var ntxt = $("#nt-txt"), nout = $("#nt-out"), nball = $("#nt-ball"), nring = $("#nt-ring");
    var nshow = function (k) {
      $$(".nt-q .opt", nt).forEach(function (o) { o.setAttribute("aria-pressed", o.dataset.v === k ? "true" : "false"); });
      var r = k && window.NT[k];
      nout.className = "result" + (r ? (r[0] === "lose" ? " fault" : r[0] === "let" ? " let" : " good") : "");
      if (!r) {
        nball.setAttribute("cx", 110); nball.setAttribute("cy", 132); nring.setAttribute("opacity", 0);
        ntxt.innerHTML = "<h2>Make the call</h2><p>Tap a situation and the verdict appears here.</p>"; return;
      }
      nball.setAttribute("cx", r[4][0]); nball.setAttribute("cy", r[4][1]);
      nring.setAttribute("cx", r[4][0]); nring.setAttribute("cy", r[4][1]); nring.setAttribute("opacity", 1);
      ntxt.innerHTML = "<h2>" + r[1] + "</h2><p>" + r[2] + "</p><p class=\"wr-src\">Based on " + r[3] + ".</p>";
    };
    $$(".nt-q .opt", nt).forEach(function (o) { o.addEventListener("click", function () { nshow(o.dataset.v); }); });
    $("#nt-reset").addEventListener("click", function () { nshow(null); });
  }

  /* ---------- out-of-court play checker ---------- */
  var oc = $("#oc");
  if (oc && window.OC) {
    var otxt = $("#oc-txt"), oout = $("#oc-out"), oball = $("#oc-ball"), oring = $("#oc-ring");
    var omode = store.get("pp-oc-mode", "y"), okey = null;
    if (omode !== "y" && omode !== "n") omode = "y";
    var orender = function () {
      $$("#oc-mode button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === omode ? "true" : "false"); });
      $$(".oc-q .opt", oc).forEach(function (o) { o.setAttribute("aria-pressed", o.dataset.v === okey ? "true" : "false"); });
      var d = okey && window.OC[okey], r = d && d[omode];
      oout.className = "result" + (r ? (r[0] === "lose" ? " fault" : r[0] === "let" ? " let" : " good") : "");
      if (!r) {
        oball.setAttribute("cx", 130); oball.setAttribute("cy", 130); oring.setAttribute("opacity", 0);
        otxt.innerHTML = "<h2>Make the call</h2><p>" + (omode === "y" ? "Court with out-of-court play. " : "Court without out-of-court play. ") + "Tap a situation and the verdict appears here.</p>"; return;
      }
      oball.setAttribute("cx", d.p[0]); oball.setAttribute("cy", d.p[1]);
      oring.setAttribute("cx", d.p[0]); oring.setAttribute("cy", d.p[1]); oring.setAttribute("opacity", 1);
      otxt.innerHTML = "<h2>" + r[1] + "</h2><p>" + r[2] + "</p><p class=\"wr-src\">Based on " + r[3] + ". Court: " + (omode === "y" ? "out-of-court play allowed" : "out-of-court play not allowed") + ".</p>";
    };
    $$("#oc-mode button").forEach(function (b) { b.addEventListener("click", function () { omode = b.dataset.v; store.set("pp-oc-mode", omode); orender(); }); });
    $$(".oc-q .opt", oc).forEach(function (o) { o.addEventListener("click", function () { okey = o.dataset.v; orender(); if (window.innerWidth < 860 && oout.scrollIntoView) oout.scrollIntoView({ behavior: "smooth", block: "center" }); }); });
    $("#oc-reset").addEventListener("click", function () { okey = null; orender(); });
    orender();
  }
  var occ = $("#occ");
  if (occ) {
    var obox = $$("#occ-list input"), oco = $("#occ-out");
    var osaved = store.get("pp-occ", []);
    obox.forEach(function (b) { b.checked = osaved.indexOf(b.dataset.k) > -1; });
    var crender = function () {
      var on = obox.filter(function (b) { return b.checked; }).map(function (b) { return b.dataset.k; });
      store.set("pp-occ", on);
      var build = ["door", "zone", "high", "pad", "pole"], miss = build.filter(function (k) { return on.indexOf(k) < 0; });
      var club = on.indexOf("club") > -1, h, p, cls;
      if (!on.length) { cls = ""; h = "Court check"; p = "Tick what you can see at your court and the answer appears here."; }
      else if (!miss.length && club) { cls = " good"; h = "Out-of-court play is on"; p = "The court looks built for it and the club allows it. If the ball bounces in your court and goes out, chase it and hit it before the second bounce."; }
      else if (!miss.length) { cls = " let"; h = "Built for it: ask the club"; p = "The court looks right for out-of-court play. Check with the club or your opponents that it is allowed before you start."; }
      else if (club) { cls = " let"; h = "Allowed, but be careful"; p = "The club allows it, but " + miss.length + " of the FIP safety points " + (miss.length === 1 ? "is" : "are") + " not ticked. Only run out where the area is clear."; }
      else { cls = " fault"; h = "Probably not allowed"; p = miss.length + " of the 5 FIP court points " + (miss.length === 1 ? "is" : "are") + " missing. Treat it as a normal court: a ball that bounces in your court and leaves it wins the point for the other team."; }
      oco.className = "result" + cls;
      oco.innerHTML = "<h2>" + h + "</h2><p>" + p + "</p>" + (on.length ? "<p class=\"wr-src\">Next: try the call checker above with the matching court type.</p>" : "");
    };
    obox.forEach(function (b) { b.addEventListener("change", crender); });
    $("#occ-reset").addEventListener("click", function () { obox.forEach(function (b) { b.checked = false; }); crender(); });
    crender();
  }

  /* ---------- racket health check ---------- */
  var rc = $("#rc");
  if (rc) {
    var rcl = $("#rc-list"), rco = $("#rc-out"), rboxes = $$("input", rcl);
    var rsaved = store.get("pp-rc", []);
    rboxes.forEach(function (b, i) { b.checked = rsaved.indexOf(i) > -1; });
    var FIX = {
      tape: "Put on new protector tape: remove the old tape, clean and dry the frame, then apply the new strip from the middle outwards.",
      grip: "Fit a new overgrip. A slippery grip makes you squeeze harder, which tires your forearm.",
      cord: "Replace the wrist cord. If it breaks or you drop the racket during a point, your pair loses the point, and a flying racket can hurt someone.",
      heat: "Heat can soften the foam core. If it now feels different, that may not come back. From now on, keep it out of the car and the sun."
    };
    var rrender = function () {
      var on = rboxes.filter(function (b) { return b.checked; });
      store.set("pp-rc", rboxes.map(function (b, i) { return b.checked ? i : -1; }).filter(function (i) { return i > -1; }));
      var sc = 0, crack = false, inside = false, fixes = [];
      on.forEach(function (b) { sc += +b.dataset.w; if (b.dataset.c === "crack") crack = true; if (b.dataset.c === "in") inside = true; if (FIX[b.dataset.c] && fixes.indexOf(FIX[b.dataset.c]) < 0) fixes.push(FIX[b.dataset.c]); });
      var h, p, cls;
      if (!on.length) { cls = ""; h = "Your racket check"; p = "Tick what you notice and the verdict and fixes appear here. Nothing ticked? Your racket sounds healthy: keep up the care routine below."; }
      else if (crack || sc >= 4) { cls = " fault"; h = "Get it checked"; p = (crack ? "Cracks tend to grow, and they let water into the core. " : "Together these signs point to damage inside the racket. ") + "Play gently until a shop or the brand has looked at it, and check whether it is still under warranty. It may be time for a new racket."; }
      else if (inside || sc >= 2) { cls = " mid"; h = "Keep an eye on it"; p = "These can be early signs of wear inside the racket. Check the frame and faces closely for small cracks, and test it against a friend's racket. If it gets worse, have it checked."; }
      else { cls = " good"; h = "Quick fixes only"; p = "Nothing serious. A few small jobs will keep it in good shape."; }
      rco.className = "result" + cls;
      rco.innerHTML = "<h2>" + h + "</h2><p>" + p + "</p>" + (fixes.length ? '<ul class="b-why">' + fixes.map(function (f) { return "<li>" + f + "</li>"; }).join("") + "</ul>" : "") +
        (on.length ? '<p class="wr-src">General care guidance, not a substitute for a check by the shop or brand. Ready for a new one? Try the <a href="' + (location.protocol === "file:" ? "racket-finder.html" : "/racket-finder") + '" style="color:#e8f84a">racket finder</a>.</p>' : "");
    };
    rboxes.forEach(function (b) { b.addEventListener("change", rrender); });
    $("#rc-reset").addEventListener("click", function () { rboxes.forEach(function (b) { b.checked = false; }); rrender(); });
    rrender();
  }

  /* ---------- drills session planner ---------- */
  var drs = $("#dr-setup");
  if (drs && window.DRL) (function () {
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var cfg = store.get("pp-dr-cfg", { who: "2", len: "30", lv: "b", focus: "mix" }), pb = store.get("pp-dr-pb", {});
    var by = {}; window.DRL.forEach(function (d) { by[d.id] = d; });
    var TIP = { b: "Keep it slow and steady. Aim for about 20 clean shots before you add movement.", i: "Add movement: get back to your spot after every shot.", a: "Add pressure: smaller targets, more pace, or no second chances." };
    var FN = { mix: "a bit of everything", cons: "keeping the ball in play", wall: "playing off the glass", net: "volleys at the net", over: "lobs and overheads", serve: "serve and return" };
    var fmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var plan = [];
    var build = function () {
      var who = +cfg.who, len = +cfg.len, wu = len <= 30 ? 5 : 10;
      var ok = window.DRL.filter(function (d) { return d.who.indexOf(who) > -1 && d.f.indexOf("game") < 0; });
      var game = who > 1 && len >= 30 ? by.cards : null, gm = game ? (len >= 45 ? 10 : 6) : 0;
      var rest = len - wu - gm, bl = len <= 30 ? 5 : (cfg.lv === "a" ? 8 : 7), n = Math.max(1, Math.floor(rest / bl));
      var pri = ok.filter(function (d) { return cfg.focus !== "mix" && d.f.indexOf(cfg.focus) > -1; });
      var oth = ok.filter(function (d) { return pri.indexOf(d) < 0 && d.id !== "feet"; });
      var pick = [];
      if (cfg.focus === "mix") pick = oth.slice(0, n);
      else { var nf = Math.min(Math.ceil(n * 0.6), pri.length * 2), j = 0; for (var k = 0; k < nf; k++) pick.push(pri[k % pri.length]); while (pick.length < n && j < oth.length) pick.push(oth[j++]); }
      while (pick.length < n) pick.push(ok[pick.length % ok.length]);
      var mins = pick.map(function () { return Math.floor(rest / n); }), extra = rest - Math.floor(rest / n) * n;
      for (var x = 0; x < extra; x++) mins[x % n]++;
      plan = [{ id: "", n: "Warm-up", ph: "Warm up", t: wu * 60, d: "Easy jog, side steps and moving stretches, then soft mini rallies close to the net. Want a full routine? Use the warm-up timer." }];
      pick.forEach(function (d, i) { var again = pick.indexOf(d) < i; plan.push({ id: d.id, n: d.n + (again ? " (again)" : ""), ph: "Drill", t: mins[i] * 60, d: d.d + " " + TIP[cfg.lv], g: d.g }); });
      if (game) plan.push({ id: game.id, n: game.n, ph: "Game", t: gm * 60, d: game.d, g: game.g });
      var sum = { 1: "Just you", 2: "Two players", 4: "Four players" }[cfg.who] + ", " + len + " minutes, focus on " + FN[cfg.focus] + ".";
      $("#dr-sum").textContent = sum + (who === 4 ? " With four players, split into two pairs and use one half of the court each." : "");
      $("#dr-plan").innerHTML = "<h2>Your session</h2><p>" + esc(sum) + "</p><table><tbody>" + plan.map(function (b, i) { return '<tr><td>' + (i + 1) + "</td><td>" + esc(b.n) + '</td><td class="num"><b>' + Math.round(b.t / 60) + " min</b></td></tr>"; }).join("") + '</tbody></table><p style="margin-top:12px">Run it with the timer below.</p>';
      $("#dr-tot").textContent = len + " minute session";
      stop(); buildList(); go(0);
    };
    $$("[data-dr]", drs).forEach(function (g) {
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", String(cfg[g.dataset.dr] === b.dataset.v)); });
      choose(g, function (v) { cfg[g.dataset.dr] = v; store.set("pp-dr-cfg", cfg); build(); });
    });
    /* timer */
    var T = { i: 0, left: 0, run: false, snd: store.get("pp-dr-snd", "on") }, tick = null, ac = null, lock = null, list = $("#dr-list");
    var beep = function (f, d) {
      if (T.snd !== "on") return;
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = f; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.18, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d); o.start(); o.stop(ac.currentTime + d); } catch (e) {}
    };
    var wake = function (on) { try { if (on && navigator.wakeLock && !lock) navigator.wakeLock.request("screen").then(function (l) { lock = l; l.addEventListener("release", function () { lock = null; }); }, function () {}); else if (!on && lock) { lock.release(); lock = null; } } catch (e) {} };
    var total = function () { return plan.reduce(function (a, s) { return a + s.t; }, 0); };
    function buildList() {
      list.innerHTML = plan.map(function (s, n) { return '<li data-n="' + n + '"><b>' + (n + 1) + ". " + esc(s.n) + '</b><span class="pill">' + s.ph + '</span><span class="wu-t">' + fmt(s.t) + "</span><p>" + esc(s.d) + "</p></li>"; }).join("");
      $$("li", list).forEach(function (li) { li.addEventListener("click", function () { go(+li.dataset.n); }); });
    }
    function render() {
      var s = plan[T.i], done = 0;
      for (var k = 0; k < T.i; k++) done += plan[k].t;
      done += s.t - T.left;
      $("#dr-clock").textContent = fmt(T.left);
      $("#dr-of").textContent = "Block " + (T.i + 1) + " of " + plan.length;
      $("#dr-ph").textContent = s.ph; $("#dr-name").textContent = s.n; $("#dr-how").textContent = s.d;
      $("#dr-best").textContent = s.g ? "Count: " + s.g + (pb[s.id] ? " Your best: " + pb[s.id] + "." : "") : "";
      $("#dr-next").textContent = T.i + 1 < plan.length ? "Next: " + plan[T.i + 1].n : "Last block.";
      $("#dr-arc").setAttribute("stroke-dashoffset", (326.7 * (1 - T.left / s.t)).toFixed(1));
      $("#dr-prog").style.width = (done / total() * 100) + "%";
      $("#dr-left").textContent = fmt(total() - done) + " left in total";
      $("#dr-go").textContent = T.run ? "Pause" : (T.left < s.t || T.i ? "Resume" : "Start");
      $$("li", list).forEach(function (li, n) { li.classList.toggle("on", n === T.i); li.classList.toggle("done", n < T.i); });
      $$("#dr-snd button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.v === T.snd)); });
    }
    function stop() { T.run = false; clearInterval(tick); tick = null; wake(false); }
    function finish() {
      stop(); beep(880, 0.6);
      $("#dr-clock").textContent = "0:00"; $("#dr-name").textContent = "Session done. Nice work!"; $("#dr-how").textContent = "Log your best numbers in the drill list below, then stretch gently.";
      $("#dr-best").textContent = ""; $("#dr-next").textContent = ""; $("#dr-prog").style.width = "100%"; $("#dr-left").textContent = ""; $("#dr-go").textContent = "Start again";
      $$("li", list).forEach(function (li) { li.classList.remove("on"); li.classList.add("done"); });
      T.i = 0; T.left = plan[0].t; T.end = true;
    }
    function go(n) { T.end = false; T.i = Math.max(0, Math.min(plan.length - 1, n)); T.left = plan[T.i].t; T.last = Date.now(); render(); }
    var stepT = function () {
      var now = Date.now(); T.left -= (now - T.last) / 1000; T.last = now;
      var c = Math.ceil(T.left);
      if (c !== T.shown && c <= 3 && c > 0) beep(660, 0.12);
      T.shown = c;
      if (T.left <= 0) { if (T.i + 1 >= plan.length) return finish(); beep(990, 0.35); go(T.i + 1); return; }
      render();
    };
    $("#dr-go").addEventListener("click", function () {
      if (T.run) { stop(); render(); return; }
      if (T.end) go(0);
      T.run = true; T.last = Date.now(); beep(990, 0.2); wake(true); tick = setInterval(stepT, 250); render();
    });
    $("#dr-skip").addEventListener("click", function () { if (T.i + 1 >= plan.length) finish(); else go(T.i + 1); });
    $("#dr-back").addEventListener("click", function () { go(T.left < plan[T.i].t - 2 ? T.i : T.i - 1); });
    $$("#dr-snd button").forEach(function (b) { b.addEventListener("click", function () { T.snd = b.dataset.v; store.set("pp-dr-snd", T.snd); render(); }); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden && T.run) wake(true); });
    /* library: filter and personal bests */
    $$("[data-pb]").forEach(function (inp) {
      if (pb[inp.dataset.pb]) inp.value = pb[inp.dataset.pb];
      inp.addEventListener("change", function () { var v = parseInt(inp.value, 10); if (v > 0) pb[inp.dataset.pb] = Math.min(v, 9999); else delete pb[inp.dataset.pb]; store.set("pp-dr-pb", pb); if (!T.run) render(); toast("Saved on this device"); });
    });
    var flt = $("#dr-filter");
    if (flt) choose(flt, function (v) { $$(".dr-card").forEach(function (c) { c.hidden = v !== "all" && c.dataset.who.split(" ").indexOf(v) < 0; }); });
    build();
  })();

  /* ---------- King of the Court ---------- */
  var kcs = $("#kc-setup");
  if (kcs) (function () {
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var cfg = store.get("pp-kc-cfg", { mode: "split", champ: "top", len: "10" }), K = store.get("pp-kc", null);
    var namesEl = $("#kc-names"), err = $("#kc-err");
    var NOTE = { split: "The two pairs that arrive on a court split up, so you get a new partner every round.", fixed: "Pairs stay together all night. Type names in pairs: lines 1 and 2 are a pair, lines 3 and 4, and so on." };
    var parse = function () { var seen = {}; return namesEl.value.split("\n").map(function (x) { return x.trim().slice(0, 40); }).filter(function (x) { if (!x || seen[x.toLowerCase()]) return false; seen[x.toLowerCase()] = 1; return true; }); };
    var sync = function () {
      $$("[data-kc] button", kcs).forEach(function (b) { b.setAttribute("aria-pressed", String(cfg[b.parentNode.dataset.kc] === b.dataset.v)); });
      $("#kc-mode-note").textContent = NOTE[cfg.mode];
      var n = parse().length;
      $("#kc-count").textContent = n ? n + " player" + (n === 1 ? "" : "s") + (n < 8 ? ", add at least 8" : n % 4 ? ", needs a multiple of 4 (add " + (4 - n % 4) + " or remove " + (n % 4) + ")" : "") : "";
      $("#kc-courts").textContent = n >= 8 && n % 4 === 0 ? (n / 4) + " courts" : "Add players to see";
    };
    $$("[data-kc]", kcs).forEach(function (g) { choose(g, function (v) { cfg[g.dataset.kc] = v; store.set("pp-kc-cfg", cfg); sync(); if (K) { K.champ = cfg.champ; save(); draw(); } }); });
    namesEl.addEventListener("input", sync);
    $("#kc-demo").addEventListener("click", function () { namesEl.value = ["Sam", "Priya", "Omar", "Lucia", "Ben", "Aisha", "Marta", "Jon", "Leo", "Fatima", "Chris", "Noor"].join("\n"); sync(); });
    var save = function () { store.set("pp-kc", K); };
    var shuffle = function (a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x; } return a; };
    var nm = function (i) { return K.p[i]; };
    var pairTxt = function (pr) { return esc(nm(pr[0])) + " &amp; " + esc(nm(pr[1])); };
    var stats = function () {
      var S = K.p.map(function (n, i) { return { i: i, n: n, pl: 0, w: 0, top: 0, pos: 99 }; });
      K.r.forEach(function (rd) { rd.forEach(function (m, c) {
        m.a.concat(m.b).forEach(function (i) { S[i].pl += m.w ? 1 : 0; if (c === 0 && m.w) S[i].top++; });
        if (m.w) (m.w === "a" ? m.a : m.b).forEach(function (i) { S[i].w++; });
      }); });
      var last = null; for (var r = K.r.length - 1; r >= 0; r--) { if (K.r[r].every(function (m) { return m.w; })) { last = K.r[r]; break; } }
      if (last) last.forEach(function (m, c) { (m.w === "a" ? m.a : m.b).forEach(function (i) { S[i].pos = c * 2; }); (m.w === "a" ? m.b : m.a).forEach(function (i) { S[i].pos = c * 2 + 1; }); });
      var key = { top: function (x, y) { return y.top - x.top || y.w - x.w || x.pos - y.pos; }, wins: function (x, y) { return y.w - x.w || y.top - x.top || x.pos - y.pos; }, last: function (x, y) { return x.pos - y.pos || y.w - x.w || y.top - x.top; } }[K.champ || "top"];
      return S.sort(function (x, y) { return key(x, y) || x.n.localeCompare(y.n); });
    };
    var next = function () {
      var rd = K.r[K.r.length - 1], C = rd.length, out = [], ri = K.r.length;
      var W = function (c) { return rd[c].w === "a" ? rd[c].a : rd[c].b; }, L = function (c) { return rd[c].w === "a" ? rd[c].b : rd[c].a; };
      for (var c = 0; c < C; c++) {
        var X = c === 0 ? W(0) : L(c - 1), Y = c === 0 ? W(1) : (c === C - 1 ? L(C - 1) : W(c + 1));
        if (K.mode === "fixed") out.push({ a: X.slice(), b: Y.slice(), w: null });
        else if (ri % 2) out.push({ a: [X[0], Y[1]], b: [X[1], Y[0]], w: null });
        else out.push({ a: [X[0], Y[0]], b: [X[1], Y[1]], w: null });
      }
      return out;
    };
    var show = function (on) { $("#kc-setup").hidden = on; $("#kc-live").hidden = !on; };
    var draw = function () {
      var rn = K.r.length, rd = K.r[rn - 1], done = rd.every(function (m) { return m.w; });
      $("#kc-sum").textContent = "Round " + rn + " of " + K.n + ", " + rd.length + " courts, " + K.p.length + " players";
      $("#kc-round").innerHTML = '<div class="card"><h2 style="font-size:1.4rem">Round ' + rn + ': tap the winning pair on each court</h2>' + rd.map(function (m, c) {
        return '<div class="match kc-m' + (m.w ? " won-" + m.w : "") + '"><span class="ct">' + (c === 0 ? "Court 1, king court" : "Court " + (c + 1)) + '</span><button type="button" class="kc-pick pair a" data-c="' + c + '" data-w="a" aria-pressed="' + (m.w === "a") + '">' + pairTxt(m.a) + '</button><span class="vs">vs</span><button type="button" class="kc-pick pair b" data-c="' + c + '" data-w="b" aria-pressed="' + (m.w === "b") + '">' + pairTxt(m.b) + "</button></div>";
      }).join("") + "</div>";
      $$(".kc-pick").forEach(function (b) { b.addEventListener("click", function () { var m = K.r[K.r.length - 1][+b.dataset.c]; m.w = m.w === b.dataset.w ? null : b.dataset.w; $("#kc-rerr").textContent = ""; save(); draw(); }); });
      $("#kc-next").textContent = rn >= K.n ? (done ? "Play an extra round" : "Tap the winners to finish") : "Make round " + (rn + 1);
      $("#kc-undo").hidden = rn < 2;
      $("#kc-hist").innerHTML = rn < 2 ? '<p class="muted">Finished rounds appear here.</p>' : K.r.slice(0, -1).map(function (r, i) { return "<p><b>Round " + (i + 1) + "</b><br>" + r.map(function (m, c) { var w = m.w === "a" ? m.a : m.b, l = m.w === "a" ? m.b : m.a; return "Court " + (c + 1) + ": " + pairTxt(w) + " beat " + pairTxt(l); }).join("<br>") + "</p>"; }).reverse().join("");
      var S = stats(), fin = rn >= K.n && done, lbl = { top: "Most rounds on court 1", last: "Court 1 winners in the last round", wins: "Most wins" }[K.champ || "top"];
      $("#kc-board").innerHTML = "<h2>" + (fin ? "King: " + esc(S[0].n) + (K.champ === "last" ? " &amp; " + esc(S[1].n) : "") : "The table") + "</h2><p>Ranked by: " + lbl + '.</p><table><thead><tr><th scope="col">#</th><th scope="col">Player</th><th scope="col" class="num">Court 1</th><th scope="col" class="num">Won</th><th scope="col" class="num">Played</th></tr></thead><tbody>' + S.map(function (x, i) { return '<tr class="' + (i < (K.champ === "last" ? 2 : 1) && x.pl ? "top" : "") + '"><td>' + (i + 1) + "</td><td>" + esc(x.n) + '</td><td class="num"><b>' + x.top + '</b></td><td class="num">' + x.w + '</td><td class="num">' + x.pl + "</td></tr>"; }).join("") + "</tbody></table>";
    };
    $("#kc-start").addEventListener("click", function () {
      var p = parse(), n = p.length, rounds = Math.max(2, Math.min(20, parseInt($("#kc-rounds").value, 10) || 8));
      if (n < 8) { err.textContent = "Add at least 8 players (2 courts)."; return; }
      if (n > 28) { err.textContent = "28 players (7 courts) is the most this tool handles."; return; }
      if (n % 4) { err.textContent = "You need a multiple of 4 players: 4 per court. With " + n + " players, try the Americano draw maker, which handles rests."; return; }
      err.textContent = "";
      var idx = p.map(function (x, i) { return i; }), r1 = [];
      if (cfg.mode === "fixed") { var prs = []; for (var i = 0; i < n; i += 2) prs.push([i, i + 1]); prs = shuffle(prs); for (var c = 0; c < n / 4; c++) r1.push({ a: prs[c * 2], b: prs[c * 2 + 1], w: null }); }
      else { idx = shuffle(idx); for (var c2 = 0; c2 < n / 4; c2++) r1.push({ a: [idx[c2 * 4], idx[c2 * 4 + 1]], b: [idx[c2 * 4 + 2], idx[c2 * 4 + 3]], w: null }); }
      K = { p: p, mode: cfg.mode, champ: cfg.champ, len: +cfg.len, n: rounds, r: [r1] }; save(); show(true); resetT(); draw();
    });
    $("#kc-next").addEventListener("click", function () {
      var rd = K.r[K.r.length - 1];
      if (!rd.every(function (m) { return m.w; })) { $("#kc-rerr").textContent = "Tap the winning pair on every court first."; return; }
      if (K.r.length >= K.n) K.n = K.r.length + 1;
      K.r.push(next()); save(); resetT(); draw(); window.scrollTo({ top: $("#kc-live").offsetTop - 80, behavior: "smooth" });
    });
    $("#kc-undo").addEventListener("click", function () { if (K.r.length < 2) return; if (!confirm("Remove the last round and go back?")) return; K.r.pop(); save(); draw(); });
    $("#kc-new").addEventListener("click", function () {
      if (!confirm("Start a new event? This one will be cleared from this device.")) return;
      namesEl.value = K.p.join("\n"); K = null; store.set("pp-kc", null); stopT(); show(false); sync();
    });
    $("#kc-copy").addEventListener("click", function () {
      var S = stats(), txt = "King of the Court, after round " + K.r.length + "\n" + S.map(function (x, i) { return (i + 1) + ". " + x.n + "  court 1: " + x.top + ", won " + x.w + "/" + x.pl; }).join("\n") + "\n\nMade with padelglassbox.com/king-of-the-court";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Table copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    /* round timer */
    var TT = { left: 600, run: false }, tk = null, ac = null;
    var tfmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var tb = function (f, d) { try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = f; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.2, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d); o.start(); o.stop(ac.currentTime + d); } catch (e) {} };
    var tdraw = function () { $("#kc-clock").textContent = tfmt(TT.left); $("#kc-tgo").textContent = TT.run ? "Pause" : (TT.left < (K ? K.len : 10) * 60 && TT.left > 0 ? "Resume" : "Start timer"); };
    function stopT() { TT.run = false; clearInterval(tk); tk = null; }
    function resetT() { stopT(); TT.left = (K ? K.len : +cfg.len) * 60; tdraw(); }
    $("#kc-tgo").addEventListener("click", function () {
      if (TT.run) { stopT(); tdraw(); return; }
      if (TT.left <= 0) TT.left = K.len * 60;
      TT.run = true; TT.last = Date.now(); tb(990, 0.2);
      tk = setInterval(function () { var now = Date.now(); TT.left -= (now - TT.last) / 1000; TT.last = now; if (TT.left <= 0) { TT.left = 0; stopT(); tb(880, 0.8); toast("Time! Tap the winners."); } tdraw(); }, 250); tdraw();
    });
    $("#kc-treset").addEventListener("click", resetT);
    sync();
    if (K && K.r) { show(true); resetT(); draw(); }
  })();

  /* ---------- tie-break tracker ---------- */
  var tbe = $("#tb");
  if (tbe) {
    var TS = store.get("pgb-tb", null) || {};
    if (!TS.t) TS.t = 7; if (!TS.n) TS.n = ["", "", "", ""]; if (!TS.p) TS.p = [];
    var tbSave = function () { store.set("pgb-tb", TS); };
    var nm = function (i) { return (TS.n[i] || "").trim() || "Player " + (i + 1); };
    var tname = function (k) { return "Team " + (k ? "B" : "A") + " (" + nm(k) + " & " + nm(k + 2) + ")"; };
    var tcount = function (p) {
      var a = 0, b = 0, i, end = -1;
      for (i = 0; i < p.length; i++) { if (p[i]) b++; else a++; if (end < 0 && Math.max(a, b) >= TS.t && Math.abs(a - b) >= 2) end = i; }
      return { a: a, b: b, done: end >= 0 };
    };
    var setAttr = function (el, o) { for (var k in o) el.setAttribute(k, o[k]); };
    var tbRender = function () {
      var c = tcount(TS.p), n = TS.p.length;
      $("#tb-a").textContent = c.a; $("#tb-b").textContent = c.b;
      $$("#tb-type button").forEach(function (b) { b.setAttribute("aria-pressed", String(+b.dataset.v === TS.t)); });
      for (var i = 0; i < 4; i++) { var inp = $("#tb-n" + i); if (document.activeElement !== inp) inp.value = TS.n[i] || ""; }
      $("#tb-wa").textContent = "Team A wins the point"; $("#tb-wb").textContent = "Team B wins the point";
      var aLeft = Math.floor(n / 6) % 2 === 0;
      $("#tb-lname").textContent = aLeft ? "Team A" : "Team B"; $("#tb-rname").textContent = aLeft ? "Team B" : "Team A";
      var alert = $("#tb-alert");
      if (c.done) {
        var w = c.a > c.b ? 0 : 1, hi = Math.max(c.a, c.b), lo = Math.min(c.a, c.b);
        $("#tb-who").textContent = "Tie-break over"; $("#tb-side").textContent = tname(w) + " wins " + hi + "-" + lo;
        alert.textContent = TS.t === 7 ? tname(w) + " wins the set 7-6. Next set: team B (" + nm(1) + " & " + nm(3) + ") serves first, as they did not serve first in the tie-break." : tname(w) + " wins the match tie-break " + hi + "-" + lo + " and the match.";
        $("#tb-srv").setAttribute("opacity", "0"); $("#tb-arrow").setAttribute("opacity", "0"); $("#tb-box").setAttribute("opacity", "0");
      } else {
        var rot = n === 0 ? 0 : Math.floor((n + 1) / 2) % 4, team = rot % 2, right = n % 2 === 0;
        $("#tb-who").textContent = nm(rot) + " (team " + (team ? "B" : "A") + ")";
        $("#tb-side").textContent = "serves point " + (n + 1) + " from the " + (right ? "right" : "left") + " side";
        var onLeft = (team === 0) === aLeft, sx, sy, bx, by;
        if (onLeft) { sx = 50; sy = right ? 170 : 70; bx = 220; by = right ? 20 : 120; }
        else { sx = 390; sy = right ? 70 : 170; bx = 81; by = right ? 120 : 20; }
        setAttr($("#tb-srv"), { cx: sx, cy: sy, opacity: 1 });
        setAttr($("#tb-box"), { x: bx, y: by, opacity: 0.28 });
        setAttr($("#tb-arrow"), { d: "M" + sx + " " + sy + " L" + (bx + 70) + " " + (by + 50), opacity: 1 });
        if (n > 0 && n % 6 === 0) alert.textContent = "Change ends now: " + n + " points played. Play on straight away (20 seconds at most).";
        else if (c.a === c.b && c.a >= TS.t - 1) alert.textContent = c.a + "-" + c.b + ": keep going, you need a 2-point lead.";
        else if (Math.max(c.a, c.b) >= TS.t - 1 && Math.abs(c.a - c.b) >= 1) alert.textContent = "Set point for team " + (c.a > c.b ? "A" : "B") + (TS.t === 10 ? " (match point)" : "") + ".";
        else alert.textContent = n === 0 ? "Point 1 is the only one served alone. After it, every player serves two points." : "";
      }
      $$(".tb-btns button", tbe).forEach(function (b) { b.disabled = c.done; });
      var a = 0, b = 0;
      $("#tb-log").innerHTML = TS.p.map(function (w, i) { if (w) b++; else a++; return '<span class="' + ((i + 1) % 6 === 0 ? "sw" : "") + '">' + (i + 1) + ". " + (w ? "B" : "A") + " " + a + "-" + b + ((i + 1) % 6 === 0 ? " · change ends" : "") + "</span>"; }).join("") || '<span>No points yet.</span>';
    };
    $$(".tb-btns button", tbe).forEach(function (b) { b.addEventListener("click", function () { if (tcount(TS.p).done) return; TS.p.push(+b.dataset.w); tbSave(); tbRender(); }); });
    $$("#tb-type button").forEach(function (b) { b.addEventListener("click", function () { var v = +b.dataset.v; if (v === TS.t) return; if (TS.p.length && !confirm("Switch tie-break type and clear the points?")) return; TS.t = v; TS.p = []; tbSave(); tbRender(); }); });
    for (var ti = 0; ti < 4; ti++) (function (i) { $("#tb-n" + i).addEventListener("input", function () { TS.n[i] = this.value; tbSave(); tbRender(); }); })(ti);
    $("#tb-undo").addEventListener("click", function () { TS.p.pop(); tbSave(); tbRender(); });
    $("#tb-reset").addEventListener("click", function () { TS.p = []; tbSave(); tbRender(); });
    $("#tb-rand").addEventListener("click", function () { TS.p = []; var g = 0; while (!tcount(TS.p).done && g++ < 80) TS.p.push(Math.random() < 0.5 ? 0 : 1); tbSave(); tbRender(); });
    $("#tb-copy").addEventListener("click", function () {
      var c = tcount(TS.p), txt = (TS.t === 7 ? "Set tie-break" : "Match tie-break") + ": " + tname(0) + " " + c.a + " - " + c.b + " " + tname(1) + (c.done ? "" : " (in progress)") + "\nPoints: " + TS.p.map(function (w) { return w ? "B" : "A"; }).join(" ") + "\nTracked with padelglassbox.com/tie-break";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Result copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    tbRender();
  }
  /* ---------- padel injuries: body area picker ---------- */
  var inj = $("#inj");
  if (inj && window.INJ) {
    var itxt = $("#inj-txt"), izb = $$("#inj-zones button"), idots = $$(".inj-dot", inj);
    var iz = store.get("pp-inj-z", null);
    var irender = function () {
      izb.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.z === iz ? "true" : "false"); });
      idots.forEach(function (d) { d.classList.toggle("on", d.dataset.z === iz); });
      var z = window.INJ[iz];
      if (!z) { itxt.innerHTML = "<h2>Pick an area</h2><p>Choose a body area to see what padel studies report and what helps.</p>"; return; }
      itxt.innerHTML = "<h2>" + z.t + "</h2><p>" + z.s + "</p><p><b>Padel moves that load it:</b> " + z.m + "</p><p><b>Habits that help:</b></p><ul class=\"b-why\">" + z.h.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul><p><b>Get it checked if:</b> " + z.r + "</p><p class=\"wr-src\">General information from a 2023 review of padel injury studies and NHS advice. Not a diagnosis: see a doctor or physiotherapist if pain lasts.</p>";
    };
    var ipick = function (z) { iz = z; store.set("pp-inj-z", iz); irender(); };
    izb.forEach(function (b) { b.addEventListener("click", function () { ipick(b.dataset.z); }); });
    idots.forEach(function (d) { d.style.cursor = "pointer"; d.addEventListener("click", function () { ipick(d.dataset.z); }); });
    irender();
  }

  /* ---------- padel injuries: prevention habits check ---------- */
  var injc = $("#injc");
  if (injc && window.INJH) {
    var hbox = $$("input", $("#injc-list")), hout = $("#injc-out");
    var hsaved = store.get("pp-injc", []);
    hbox.forEach(function (b) { b.checked = hsaved.indexOf(b.dataset.h) > -1; });
    var hrender = function () {
      var on = hbox.filter(function (b) { return b.checked; }).map(function (b) { return b.dataset.h; });
      store.set("pp-injc", on);
      var miss = hbox.filter(function (b) { return !b.checked; }).map(function (b) { return b.dataset.h; });
      var n = on.length, tot = hbox.length, h, p, cls;
      if (n === tot) { cls = " good"; h = "All " + tot + " habits: great"; p = "You do everything on the list. Keep it up, and still stop if something hurts."; }
      else if (n >= 6) { cls = " good"; h = n + " of " + tot + ": good habits"; p = "You're doing most of the right things. Add the last few:"; }
      else if (n >= 3) { cls = " mid"; h = n + " of " + tot + ": room to improve"; p = "Pick one or two of these to add first. The warm-up and shoes are the quickest wins."; }
      else { cls = " fault"; h = n + " of " + tot + ": start with the basics"; p = "Start with a proper warm-up and the right shoes, then add the rest over time:"; }
      hout.className = "result" + cls;
      hout.innerHTML = "<h2>" + h + "</h2><p>" + p + "</p>" + (miss.length ? '<ul class="b-why">' + miss.map(function (k) { var r = window.INJH[k]; return "<li>" + r[0] + (r[1] ? ' (<a href="' + r[1] + '" style="color:#e8f84a">' + r[2] + "</a>)" : "") + "</li>"; }).join("") + "</ul>" : "") + '<p class="wr-src">Based on general sports injury advice from NI Direct and the NHS. Habits lower the risk, they don\'t remove it.</p>';
    };
    hbox.forEach(function (b) { b.addEventListener("change", hrender); });
    $("#injc-reset").addEventListener("click", function () { hbox.forEach(function (b) { b.checked = false; }); hrender(); });
    hrender();
  }
  /* ---------- padel grip: shot grip finder ---------- */
  var gp = $("#gp");
  if (gp && window.GRIPS) {
    var gsh = $$("button", $("#gp-shots")), ghd = $$("button", $("#gp-hand"));
    var gst = store.get("pp-grip", { s: "vol", h: "r" });
    if (!window.GRIPS[gst.s]) gst.s = "vol";
    var GN = { c: "Continental grip", e: "Continental (eastern forehand is an option)", eb: "Continental (eastern backhand is an option)" };
    var grender = function () {
      store.set("pp-grip", gst);
      gsh.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === gst.s ? "true" : "false"); });
      ghd.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === gst.h ? "true" : "false"); });
      var r = window.GRIPS[gst.s], g = r[1];
      $("#gp-h").textContent = GN[g];
      $("#gp-p").textContent = r[0] + ": " + r[2];
      var bev = 1, alt = "";
      if (g === "e") { bev = gst.h === "r" ? 2 : 8; }
      if (g === "eb") { bev = gst.h === "r" ? 8 : 2; }
      $("#gp-mark").setAttribute("transform", "translate(110 110) rotate(" + ((bev - 1) * 45) + ") translate(0 -97)");
      if (g !== "c") alt = "The marker shows the optional grip: the V of your hand moves one bevel round, to bevel " + bev + ". For the continental grip it stays on bevel 1. ";
      else alt = "The marker shows where the V between your thumb and first finger sits: bevel 1, the top edge. ";
      $("#gp-src").textContent = alt + (gst.h === "l" ? "Left-handed: everything is mirrored." : "Right-handed view.");
    };
    gsh.forEach(function (b) { b.addEventListener("click", function () { gst.s = b.dataset.v; grender(); }); });
    ghd.forEach(function (b) { b.addEventListener("click", function () { gst.h = b.dataset.v; grender(); }); });
    grender();
  }

  /* ---------- padel grip: grip check ---------- */
  var gc = $("#gc");
  if (gc && window.GCFIX) {
    var gbox = $$("input", $("#gc-list")), gout = $("#gc-out");
    var gsv = store.get("pp-gc", []);
    gbox.forEach(function (b) { b.checked = gsv.indexOf(b.dataset.g) > -1; });
    var gcrender = function () {
      var on = gbox.filter(function (b) { return b.checked; }).map(function (b) { return b.dataset.g; });
      store.set("pp-gc", on);
      var fx = [];
      on.forEach(function (k) { var f = window.GCFIX[k]; if (f && fx.indexOf(f) < 0) fx.push(f); });
      var h, p, cls;
      if (!on.length) { cls = ""; h = "Your grip check"; p = "Tick what you notice and your fixes appear here. Nothing to tick? Your grip sounds good: keep it relaxed and continental."; }
      else if (fx.length >= 3) { cls = " mid"; h = fx.length + " things to fix"; p = "Work on one at a time, starting with the first. Small grip changes feel odd for a few sessions, then natural."; }
      else { cls = " good"; h = fx.length === 1 ? "One quick fix" : "Two quick fixes"; p = "Small changes, big difference:"; }
      var lk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
      gout.className = "result" + cls;
      gout.innerHTML = "<h2>" + h + "</h2><p>" + p + "</p>" + (fx.length ? '<ul class="b-why">' + fx.map(function (f) { return "<li>" + f + "</li>"; }).join("") + "</ul>" : "") +
        (on.length ? '<p class="wr-src">General coaching advice. Pain that doesn\'t go away? See ' + lk("padel-injuries", "padel injuries") + ". Next: practise with the " + lk("drills", "drills planner") + ".</p>" : "");
    };
    gbox.forEach(function (b) { b.addEventListener("change", gcrender); });
    $("#gc-reset").addEventListener("click", function () { gbox.forEach(function (b) { b.checked = false; }); gcrender(); });
    gcrender();
  }

  /* ---------- overheads: bandeja vs víbora vs smash chooser ---------- */
  var oh = $("#oh");
  if (oh && window.OHS) {
    var ogr = $$("[data-oh]", oh);
    var ost = store.get("pp-oh", { pos: "mid", ball: "easy", opp: "back", lvl: "new" });
    var ZONE = { smash: [280, 50, 70, 140], vibora: [362, 22, 56, 54], bandeja: [366, 40, 48, 160], glass: [370, 40, 44, 160] };
    var MEX = { near: 185, mid: 95, deep: 45 };
    var opick = function () {
      var why = [], k;
      if (ost.ball === "over") { k = "glass"; why.push("The ball will go over you, so an overhead would be hit late and off balance."); }
      else if (ost.ball === "hard") { k = "bandeja"; why.push("You are stretching or moving back, so control beats power."); if (ost.pos === "deep") why.push("If you can't get behind it at all, letting it go to the glass is fine too."); }
      else if (ost.pos === "near") { k = "smash"; why.push("High, slow ball and you are close to the net: the best chance to finish."); if (ost.lvl === "new") why.push("Still new? Go for placement over power."); }
      else if (ost.pos === "mid") {
        if (ost.lvl === "new") { k = "bandeja"; why.push("From the service line a bandeja is the safe choice while you are learning. The víbora comes later."); }
        else { k = "vibora"; why.push("Balanced around the service line with a comfortable ball: room to attack with spin."); }
      } else { k = "bandeja"; why.push("From deep, a smash usually comes back off their glass. Keep the net with a deep bandeja."); }
      if (ost.opp === "net" && k !== "smash" && k !== "glass") why.push("They are at the net, so a deep, low ball pushes them back. Don't leave it short.");
      if (ost.opp === "net" && k === "smash") why.push("They are close: aim at their feet or between them, not at their bodies.");
      return [k, why];
    };
    var orender = function () {
      store.set("pp-oh", ost);
      ogr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === ost[g.dataset.oh] ? "true" : "false"); }); });
      var r = opick(), k = r[0], s = window.OHS[k], z = ZONE[k];
      $("#oh-h").textContent = s.h;
      $("#oh-p1").textContent = s.what;
      $("#oh-how").innerHTML = s.how.map(function (x) { return "<li>" + x + "</li>"; }).join("");
      $("#oh-aim").innerHTML = "<b>Aim:</b> " + s.aim + ". <b>Then:</b> " + s.after;
      $("#oh-why").textContent = "Why: " + r[1].join(" ");
      var zr = $("#oh-zone"); zr.setAttribute("x", z[0]); zr.setAttribute("y", z[1]); zr.setAttribute("width", z[2]); zr.setAttribute("height", z[3]);
      var mx = MEX[ost.pos], my = 140, tx = z[0] + z[2] / 2, ty = z[1] + z[3] / 2;
      $("#oh-me").setAttribute("cx", mx); $("#oh-me").setAttribute("cy", my);
      $("#oh-p").setAttribute("cx", ost.pos === "deep" ? 45 : (ost.pos === "near" ? 185 : 110));
      var opx = ost.opp === "net" ? 262 : 392;
      $$(".oh-op", oh).forEach(function (c) { c.setAttribute("cx", opx); });
      var d = k === "glass" ? "M" + mx + " " + my + " L26 " + (my - 10) + " Q220 -30 " + tx + " " + ty : "M" + mx + " " + my + " Q" + ((mx + tx) / 2) + " " + (k === "smash" ? 80 : 30) + " " + tx + " " + ty;
      $("#oh-path").setAttribute("d", d);
    };
    ogr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { ost[g.dataset.oh] = b.dataset.v; orender(); }); }); });
    orender();
  }

  /* ---------- intermediate racket upgrade check ---------- */
  var irb = $("#ir");
  if (irb && window.IRGO) {
    var igr = $$("[data-ir]", irb);
    var ist = store.get("pp-ir", { shape: "round", weight: "x", face: "glass", often: "2", style: "allround", arm: "no", feel: "power" });
    var NM = { round: "Round", teardrop: "Teardrop", diamond: "Diamond", light: "under 355 g", mid: "355 to 370 g", heavy: "over 370 g", glass: "Fibreglass", carbon: "Carbon" };
    var ipick = function () {
      var a = ist, why = [], t = {};
      var sore = a.arm === "yes";
      if (a.style === "control" || sore) t.shape = (a.style === "control" || a.feel === "control") ? "round" : "teardrop";
      else if (a.style === "attack" && a.often === "4" && a.feel !== "control") t.shape = "diamond";
      else t.shape = "teardrop";
      if (a.feel === "control" && t.shape === "diamond") t.shape = "teardrop";
      t.bal = t.shape === "round" ? "Low (head-light)" : (t.shape === "diamond" ? "Medium to high" : "Medium");
      if (sore && t.shape !== "round") t.bal = "Low to medium";
      t.w = (sore || a.feel === "heavy") ? "light" : (t.shape === "diamond" ? "heavy" : "mid");
      t.wt = t.w === "light" ? "About 355 to 365 g" : (t.w === "heavy" ? "About 365 to 375 g" : "About 360 to 370 g");
      t.core = sore ? "Soft" : (t.shape === "diamond" ? "Medium to firm" : "Soft or medium");
      t.face = sore ? "glass" : (a.often === "1" ? "glass" : "either");
      t.ft = t.face === "glass" ? "Fibreglass" : (t.shape === "diamond" ? "Carbon" : "Fibreglass or carbon");
      // compare
      var rows = [], changes = 0, unknown = 0;
      var row = function (lab, tgt, cur, same) {
        var tag;
        if (cur === "x") { tag = "check yours"; unknown++; } else if (same) tag = "keep"; else { tag = "change"; changes++; }
        rows.push([lab, tgt + " (" + tag + (cur !== "x" && !same ? ", yours: " + NM[cur] : "") + ")"]);
      };
      row("Shape", NM[t.shape], a.shape, a.shape === t.shape);
      rows.push(["Balance", t.bal]);
      row("Weight", t.wt, a.weight, a.weight === t.w || (t.w === "light" && a.weight === "light"));
      rows.push(["Core", t.core]);
      row("Face", t.ft, a.face, t.face === "either" ? (t.shape === "diamond" ? a.face === "carbon" : true) : a.face === t.face);
      // reasons
      if (t.shape === "teardrop") why.push("Teardrop is the usual next step: more punch than round, with a sweet spot that still forgives.");
      if (t.shape === "round") why.push(sore ? "Round rackets have a big, central sweet spot and usually a low balance, which is easier on the arm." : "You win with control, and round gives the biggest, most forgiving sweet spot.");
      if (t.shape === "diamond") why.push("You attack and play a lot, so a diamond's extra head weight can pay off. Try one first: the sweet spot is small and high.");
      if (t.shape === "diamond" && a.shape === "round") why.push("Round straight to diamond is a big jump. Many players try a teardrop in between.");
      if (sore) why.push("Sore arm: stay light, low balance and soft, and avoid stiff, head-heavy rackets.");
      if (a.feel === "heavy") why.push("A tired arm late in matches points to a lighter racket or a lower balance.");
      if (a.feel === "control") why.push("Balls flying long: more power will not help. Keep the balance low to medium.");
      if (a.feel === "power" && t.shape !== "round") why.push("More power comes from a slightly higher balance and a firmer feel, but timing and the overhead technique matter more.");
      if (a.style === "attack" && t.shape !== "diamond" && !sore) why.push(a.often === "4" ? "Get control of long balls first. A diamond can come later." : "A diamond is usually for players who play most days. Teardrop gives you power without the risk.");
      var h, p, cls;
      if (a.feel === "worn") { cls = " mid"; h = "Check it, then replace it"; p = "A racket that feels dead or damaged is the clearest reason to buy a new one. Here is what to look for:"; }
      else if (a.often === "1" && a.feel === "fine") { cls = " good"; h = "Keep your racket"; p = "You play once a week or less and nothing bothers you. Spend on a new overgrip or a lesson instead. When you do upgrade, look for:"; }
      else if (changes === 0 && unknown === 0) { cls = " good"; h = "Your racket already fits"; p = "Your specs match what suits your game. Keep it unless it is worn. If you replace it, stay close to:"; }
      else if (changes === 0) { cls = " mid"; h = "Check your racket's label"; p = "What you know matches. Check the rest on the frame or shop page, or with the balance decoder. Look for:"; }
      else { cls = ""; h = changes === 1 ? "Change one thing" : "Time for a different racket"; p = "For your game, look for:"; }
      return { cls: cls, h: h, p: p, rows: rows, why: why, shape: t.shape };
    };
    var irender = function () {
      store.set("pp-ir", ist);
      igr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === ist[g.dataset.ir] ? "true" : "false"); }); });
      var r = ipick(), out = $("#ir-out");
      out.className = "result" + r.cls;
      $("#ir-h").textContent = r.h;
      $("#ir-p").textContent = r.p;
      $("#ir-spec").innerHTML = r.rows.map(function (x) { return "<dt>" + x[0] + "</dt><dd>" + x[1] + "</dd>"; }).join("");
      $("#ir-why").innerHTML = r.why.map(function (x) { return "<li>" + x + "</li>"; }).join("");
      var lk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
      $("#ir-shop").innerHTML = '<a href="' + window.IRGO[r.shape] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a;font-weight:700">Browse ' + r.shape + " rackets</a> (affiliate link) · Compare specs in the " + lk("racket-balance", "balance decoder") + (ist.feel === "worn" ? " · Run the " + lk("racket-care", "racket health check") : "");
    };
    igr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { ist[g.dataset.ir] = b.dataset.v; irender(); }); }); });
    irender();
  }
})();
