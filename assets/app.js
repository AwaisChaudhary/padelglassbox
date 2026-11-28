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
        "<p>" + why.join(" ") + "</p>" + '<p class="aff-disclosure-inline" role="note"><strong>Affiliate disclosure:</strong> the shop link below is an affiliate link. If you buy through it we may earn a small commission, at no extra cost to you. It does not change your result.</p><div class="btns"><button class="btn lime sm" type="button" id="copy-fit">Copy my racket profile</button><a class="btn sm" href="/go/padel-' + shape + '-rackets" rel="sponsored nofollow noopener" target="_blank">Shop ' + shape + ' rackets</a></div>';
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

  /* ---------- cool-down timer (copy of warm-up) ---------- */
  var cdx = $("#cd");
  if (cdx && window.CD) (function () {
    var W = { len: store.get("pp-cd-len", "q"), snd: store.get("pp-cd-snd", "on"), i: 0, left: 0, run: false }, tick = null, ac = null, lock = null;
    var steps = function () { return window.CD[W.len] || window.CD.q; };
    var fmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var beep = function (f, d) {
      if (W.snd !== "on") return;
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = f; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.18, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d); o.start(); o.stop(ac.currentTime + d); } catch (e) {}
    };
    var wake = function (on) {
      try { if (on && navigator.wakeLock && !lock) navigator.wakeLock.request("screen").then(function (l) { lock = l; l.addEventListener("release", function () { lock = null; }); }, function () {}); else if (!on && lock) { lock.release(); lock = null; } } catch (e) {}
    };
    var list = $("#cd-list");
    var buildList = function () {
      list.innerHTML = steps().map(function (s, n) { return '<li data-n="' + n + '"><b>' + (n + 1) + ". " + s.n + '</b><span class="pill">' + s.ph + '</span><span class="wu-t">' + fmt(s.t) + "</span><p>" + s.d + "</p></li>"; }).join("");
      $$("li", list).forEach(function (li) { li.addEventListener("click", function () { go(+li.dataset.n); }); });
    };
    var total = function () { return steps().reduce(function (a, s) { return a + s.t; }, 0); };
    var wrender = function () {
      var S = steps(), s = S[W.i], done = 0;
      for (var k = 0; k < W.i; k++) done += S[k].t;
      done += s.t - W.left;
      $("#cd-clock").textContent = fmt(W.left);
      $("#cd-of").textContent = "Step " + (W.i + 1) + " of " + S.length;
      $("#cd-ph").textContent = s.ph; $("#cd-name").textContent = s.n; $("#cd-how").textContent = s.d;
      $("#cd-next").textContent = W.i + 1 < S.length ? "Next: " + S[W.i + 1].n : "Last stretch. Well done!";
      $("#cd-arc").setAttribute("stroke-dashoffset", (326.7 * (1 - W.left / s.t)).toFixed(1));
      $("#cd-prog").style.width = (done / total() * 100) + "%";
      $("#cd-left").textContent = fmt(total() - done) + " left in total";
      $("#cd-go").textContent = W.run ? "Pause" : (W.left < s.t || W.i ? "Resume" : "Start");
      $$("li", list).forEach(function (li, n) { li.classList.toggle("on", n === W.i); li.classList.toggle("done", n < W.i); });
      $$("#cd-len button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === W.len ? "true" : "false"); });
      $$("#cd-snd button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === W.snd ? "true" : "false"); });
    };
    var stop = function () { W.run = false; clearInterval(tick); tick = null; wake(false); };
    var finish = function () {
      stop(); beep(880, 0.6);
      $("#cd-clock").textContent = "0:00"; $("#cd-name").textContent = "Cool-down done. Drink some water!"; $("#cd-how").textContent = "Next time: warm up first with the warm-up timer, and keep moving gently tomorrow if you feel sore.";
      $("#cd-next").textContent = ""; $("#cd-prog").style.width = "100%"; $("#cd-left").textContent = ""; $("#cd-go").textContent = "Start again";
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
    $("#cd-go").addEventListener("click", function () {
      if (W.run) { stop(); wrender(); return; }
      if (W.end) go(0);
      W.run = true; W.last = Date.now(); beep(990, 0.2); wake(true); tick = setInterval(step, 250); wrender();
    });
    $("#cd-skip").addEventListener("click", function () { if (W.i + 1 >= steps().length) finish(); else go(W.i + 1); });
    $("#cd-back").addEventListener("click", function () { go(W.left < steps()[W.i].t - 2 ? W.i : W.i - 1); });
    $$("#cd-len button").forEach(function (b) { b.addEventListener("click", function () { if (b.dataset.v === W.len) return; stop(); W.len = b.dataset.v; store.set("pp-cd-len", W.len); buildList(); go(0); }); });
    $$("#cd-snd button").forEach(function (b) { b.addEventListener("click", function () { W.snd = b.dataset.v; store.set("pp-cd-snd", W.snd); wrender(); }); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden && W.run) wake(true); });
    buildList(); go(0);
  })();

  /* ---------- padel pronunciation (glossary) ---------- */
  var prn = $("#pron");
  if (prn) {
    $$("[data-say]", prn).forEach(function (b) {
      b.addEventListener("click", function () {
        try { var u = new SpeechSynthesisUtterance(b.dataset.say); u.lang = b.dataset.lang; u.rate = 0.8; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u); }
        catch (e) { $("#pron-note").textContent = "Your browser can't play speech. Say it: " + b.textContent; }
      });
    });
  }

  /* ---------- racket weight calculator ---------- */
  var rwb = $("#rw-out");
  if (rwb) {
    var rlk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var rv = store.get("pgb-rw", { lvl: "new", str: "avg", arm: "no", sty: "all", age: "ad", freq: "1" });
    var rwrender = function () {
      var lo = { "new": 345, mid: 355, adv: 360 }[rv.lvl], hi = lo + 15;
      if (rv.str === "light") { lo -= 10; hi -= 10; } else if (rv.str === "strong") { lo += 5; hi += 5; }
      if (rv.sty === "ctrl") { lo -= 5; hi -= 5; } else if (rv.sty === "pow") { lo += 5; hi += 5; }
      if (rv.age === "55") { lo -= 5; hi -= 5; }
      if (rv.freq === "4" && rv.lvl === "new") { lo -= 0; hi -= 5; }
      if (rv.arm === "some") { hi = Math.min(hi, 365); lo = Math.min(lo, hi - 10); }
      if (rv.arm === "yes") { hi = Math.min(hi, 360); lo = Math.min(lo, 345); }
      lo = Math.max(335, lo); hi = Math.min(385, Math.max(hi, lo + 10));
      var bal = (rv.arm !== "no" || rv.lvl === "new" || rv.sty === "ctrl") ? "Low or even balance (head-light, about 255 to 265 mm)" : (rv.sty === "pow" && rv.lvl !== "new" ? "Higher balance (head-heavy, about 265 mm or more)" : "Even balance (about 260 to 270 mm)");
      var shape = (rv.lvl === "new" || rv.arm === "yes" || rv.sty === "ctrl") ? "Round" : (rv.sty === "pow" && rv.lvl === "adv" ? "Diamond or teardrop" : "Teardrop");
      var feel = (rv.arm !== "no" || rv.lvl === "new") ? "Soft core (soft EVA or foam)" : (rv.lvl === "adv" && rv.sty === "pow" ? "Medium to hard" : "Medium");
      if (rv.age === "jr") {
        $("#rw-h").textContent = "Junior racket";
        $("#rw-p").innerHTML = "Under 14s need a lighter junior racket picked by height and age, not an adult weight. Use the " + rlk("padel-racket-for-kids", "junior racket finder") + ".";
        $("#rw-spec").innerHTML = ""; $("#rw-t").innerHTML = "";
        store.set("pgb-rw", rv); return;
      }
      $("#rw-h").textContent = lo + " to " + hi + " g";
      var why = rv.arm === "yes" ? "With arm pain, stay light and head-light, and get the pain checked. " : (rv.arm === "some" ? "Because your arm sometimes hurts, we cap the range on the light side. " : "");
      why += { "new": "New players learn faster with a racket that is easy to swing.", mid: "You can handle a little more weight for depth and stability.", adv: "Experienced players can use extra weight for power, if their arm is happy." }[rv.lvl];
      if (rv.freq === "4") why += " Playing 4+ times a week adds up: lean to the lighter end if you feel tired.";
      $("#rw-p").textContent = why;
      var rows = [["Weight", lo + " to " + hi + " g on the label"], ["Balance", bal], ["Shape", shape], ["Feel", feel], ["Too heavy if", "you're late at the net or your arm is tired by set two"]];
      $("#rw-spec").innerHTML = rows.map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + r[1] + "</dd>"; }).join("");
      $("#rw-t").innerHTML = "Pick a shape: " + rlk("racket-finder", "racket finder") + " · Check balance: " + rlk("racket-balance", "balance explained") + " · Sore arm: " + rlk("padel-elbow", "padel elbow check");
      store.set("pgb-rw", rv);
    };
    $$("[data-rw]").forEach(function (g) {
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === rv[g.dataset.rw] ? "true" : "false"); });
      choose(g, function (v) { rv[g.dataset.rw] = v; rwrender(); });
    });
    $("#rw-copy").addEventListener("click", function () {
      var txt = "My padel racket weight: " + $("#rw-h").textContent + "\n" + $$("#rw-spec dt").map(function (d) { return d.textContent + ": " + d.nextSibling.textContent; }).join("\n");
      try { navigator.clipboard.writeText(txt).then(function () { toast("Result copied"); }, function () { toast("Copy failed"); }); } catch (e) { toast("Copy failed"); }
    });
    rwrender();
  }

  /* ---------- run 17: shared picker helper ---------- */
  var pgbPicker = function (px, key, def, render) {
    var st = store.get(key, def);
    $$("[data-" + px + "]").forEach(function (g) {
      var k = g.getAttribute("data-" + px);
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === st[k] ? "true" : "false"); });
      choose(g, function (v) { st[k] = v; render(st); store.set(key, st); });
    });
    var cpy = $("#" + px + "-copy");
    if (cpy) cpy.addEventListener("click", function () {
      var txt = $("#" + px + "-h").textContent + "\n" + $$("#" + px + "-spec dt").map(function (d) { return d.textContent + ": " + d.nextSibling.textContent; }).join("\n");
      try { navigator.clipboard.writeText(txt).then(function () { toast("Result copied"); }, function () { toast("Copy failed"); }); } catch (e) { toast("Copy failed"); }
    });
    render(st);
  };
  var pgbLk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
  var pgbSpec = function (id, rows) { $(id).innerHTML = rows.map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + r[1] + "</dd>"; }).join(""); };

  /* ---------- padel bag picker ---------- */
  if ($("#bg-out")) pgbPicker("bg", "pgb-bg", { rk: "1", go: "walk", kit: "shoe", lvl: "1" }, function (v) {
    var type, size, why;
    if (v.rk === "4" || v.lvl === "4") {
      type = v.go === "fly" || v.rk === "4" && v.kit === "full" ? "Large racket bag or wheeled bag" : "Large racket bag";
      size = "Up to about 6 rackets, about 45 to 55+ litres"; why = "You carry several rackets and play a lot, so you need the big racket section and room for full kit.";
    } else if (v.rk === "2" || v.kit === "full") {
      type = "Medium racket bag"; size = "2 to 3 rackets, about 35 to 45 litres";
      why = v.rk === "2" ? "Two or three rackets plus shoes is too tight for a backpack." : "A full change of clothes, shoes and a towel need more room than a backpack.";
      if (v.go === "walk" && v.rk === "1") { type = "Large padel backpack or medium racket bag"; size = "About 30 to 40 litres"; why = "One racket but full kit: a bigger backpack works if you walk or cycle; a racket bag if you drive."; }
    } else if (v.kit === "min" && v.go !== "car") {
      type = "Padel backpack (small)"; size = "1 racket, about 20 litres"; why = "One racket and a few small things: a light backpack keeps your hands free.";
    } else {
      type = "Padel backpack"; size = "1 racket (2 is tight), about 25 to 30 litres"; why = "One racket, balls and shoes fit well, and a backpack is easy to carry to the court.";
    }
    var th = v.go === "car" ? "Yes: your bag stays in the car, where heat and cold can harm the racket's core" : (v.go === "fly" ? "Recommended: car boots, hotel rooms and outdoor courts on trips swing in temperature" : (v.lvl !== "1" ? "Useful: worth it for regular players and outdoor play" : "Nice to have, not essential if you go straight to the court"));
    var shoe = v.kit === "min" ? "Not needed if you wear your court shoes there" : "Yes, a separate, ideally vented shoe pocket";
    var more = [];
    if (v.go === "walk") more.push("padded straps, bottle holder");
    if (v.go === "fly") more.push("check the airline cabin-bag size, sturdy padded racket pocket");
    if (v.go === "car") more.push("take the bag inside after you play");
    if (v.kit === "full") more.push("separate pocket for damp clothes");
    $("#bg-h").textContent = type; $("#bg-p").textContent = why;
    pgbSpec("#bg-spec", [["Size", size], ["Thermal pocket", th], ["Shoe pocket", shoe], ["Also look for", more.length ? more.join("; ") : "padded racket pocket, valuables pocket"]]);
    $("#bg-t").innerHTML = "Pack list: " + pgbLk("padel-equipment", "equipment checklist") + " · Shoes: " + pgbLk("padel-shoes", "shoe finder") + " · Racket care: " + pgbLk("racket-care", "keep it in shape");
  });

  /* ---------- control vs power test ---------- */
  if ($("#cp-out")) pgbPicker("cp", "pgb-cp", { lvl: "0", win: "1", side: "1", ovh: "0", miss: "1", arm: "2", freq: "0" }, function (v) {
    var ks = ["lvl", "win", "side", "ovh", "miss", "arm", "freq"], sc = 0, painYes = v.arm === "x";
    ks.forEach(function (k) { sc += v[k] === "x" ? 0 : +v[k]; });
    var pct = Math.round(sc / 14 * 100);
    if (v.lvl === "0") pct = Math.min(pct, 45);
    if (painYes) pct = Math.min(pct, 20);
    var t, rows, why;
    if (pct < 40) {
      t = "Control"; why = "A forgiving racket will win you more points right now.";
      rows = [["Shape", "Round"], ["Balance", "Low, head-light"], ["Weight", "About 340 to 360 g"], ["Core", "Soft EVA or foam"], ["Face", "Fibreglass or soft carbon mix"], ["Sweet spot", "Large and central"]];
    } else if (pct < 70) {
      t = "Hybrid (all-round)"; why = "You have some attack in your game but still need forgiveness: a teardrop gives a bit of both.";
      rows = [["Shape", "Teardrop or hybrid"], ["Balance", "Medium, even"], ["Weight", "About 355 to 370 g"], ["Core", "Medium"], ["Face", "Carbon or carbon mix"], ["Sweet spot", "Medium"]];
    } else {
      t = "Power"; why = "Your overheads are reliable and you finish points: a power racket rewards that.";
      rows = [["Shape", "Diamond (or a head-heavy teardrop)"], ["Balance", "High, head-heavy"], ["Weight", "About 360 to 375 g"], ["Core", "Firmer, high-density EVA"], ["Face", "Carbon, rough face for spin"], ["Sweet spot", "Smaller and higher"]];
    }
    if (painYes) why = "With arm pain, stay with a light, head-light, soft racket and get the pain checked. " + why;
    else if (v.lvl === "0" && sc >= 7) why = "You lean towards attack, but in your first year a control racket helps you build technique. Re-take the test in a few months.";
    $("#cp-h").textContent = t; $("#cp-p").textContent = why;
    $("#cp-dot").style.left = Math.max(3, Math.min(97, pct)) + "%";
    pgbSpec("#cp-spec", rows);
    $("#cp-t").innerHTML = "Weight: " + pgbLk("padel-racket-weight", "weight calculator") + " · Full match: " + pgbLk("racket-finder", "racket finder") + (painYes || v.arm === "0" ? " · Sore arm: " + pgbLk("padel-elbow", "padel elbow check") : " · Side: " + pgbLk("which-side-padel", "which side quiz"));
  });

  /* ---------- women's racket spec picker ---------- */
  if ($("#wr-out")) pgbPicker("wr", "pgb-wr", { lvl: "new", str: "avg", arm: "no", sty: "all", hand: "m" }, function (v) {
    var lo = { "new": 340, mid: 345, adv: 355 }[v.lvl], hi = lo + 15;
    if (v.str === "light") { lo -= 5; hi -= 5; } else if (v.str === "strong") { lo += 5; hi += 5; }
    if (v.sty === "pow" && v.lvl !== "new") { lo += 5; hi += 5; } else if (v.sty === "ctrl") { hi -= 5; }
    if (v.arm === "yes") { lo = Math.min(lo, 340); hi = Math.min(hi, 355); } else if (v.arm === "some") { hi = Math.min(hi, 360); }
    lo = Math.max(335, lo); hi = Math.min(370, Math.max(hi, lo + 10));
    var shape = (v.lvl === "new" || v.arm === "yes" || v.sty === "ctrl" && v.lvl !== "adv") ? "Round" : (v.lvl === "adv" && v.sty === "pow" && v.arm === "no" ? "Diamond or head-heavy teardrop" : "Teardrop or hybrid");
    var bal = (v.arm !== "no" || v.lvl === "new" || v.sty === "ctrl") ? "Low (head-light)" : (v.sty === "pow" && v.lvl === "adv" ? "Medium to high" : "Medium");
    var core = (v.arm !== "no" || v.lvl === "new") ? "Soft EVA or foam" : (v.lvl === "adv" && v.sty === "pow" ? "Medium to firm" : "Soft to medium");
    var face = (v.arm !== "no" || v.lvl === "new") ? "Fibreglass or soft mix" : "Carbon or carbon mix";
    var grip = { s: "Standard handle + 1 thin overgrip", m: "Standard handle + 1 overgrip", l: "Standard handle + 2 overgrips" }[v.hand];
    var label = (hi <= 360) ? "A women's (lighter) version often fits this range" : "Regular versions usually fit this range";
    $("#wr-h").textContent = lo + " to " + hi + " g, " + shape.split(" ")[0].toLowerCase();
    $("#wr-p").textContent = (v.arm === "yes" ? "With arm pain, stay light and soft, and get it checked by a doctor or physio. " : "") + { "new": "Easy to swing and forgiving while you learn.", mid: "A little more weight and a teardrop add depth without losing control.", adv: "You can handle more weight and balance for power, if your arm is happy." }[v.lvl];
    pgbSpec("#wr-spec", [["Weight", lo + " to " + hi + " g"], ["Balance", bal], ["Shape", shape], ["Core", core], ["Face", face], ["Grip", grip], ["Label", label]]);
    $("#wr-t").innerHTML = "Control or power: " + pgbLk("control-vs-power-padel-racket", "7-question test") + " · Exact weight: " + pgbLk("padel-racket-weight", "weight calculator") + " · Grips: " + pgbLk("padel-overgrip", "overgrip guide");
  });

  /* ---------- tennis players racket picker ---------- */
  if ($("#tp-out")) pgbPicker("tp", "pgb-tp", { tl: "rec", st: "base", arm: "no", pd: "0" }, function (v) {
    var lo = { rec: 350, comp: 355, ex: 360 }[v.tl], hi = lo + 10;
    if (v.tl === "rec") hi = 360;
    if (v.arm === "yes") { lo = 345; hi = 355; } else if (v.arm === "some") { hi = Math.min(hi, 360); lo = Math.min(lo, 350); }
    var adv = v.pd === "season" && v.tl !== "rec" && v.arm === "no";
    var shape = v.arm === "yes" || (v.tl === "rec" && v.pd === "0") ? "Round (or a soft teardrop)" : (adv ? "Teardrop, or a diamond if your bandeja lands deep" : "Teardrop");
    var bal = v.arm !== "no" ? "Low (head-light)" : (v.tl === "rec" ? "Low to medium" : (adv ? "Medium, medium-high if you attack" : "Medium"));
    var core = v.arm !== "no" ? "Soft EVA or foam" : (adv ? "Medium" : "Soft to medium");
    var face = v.arm !== "no" ? "Fibreglass (flexes more, kinder to the arm)" : (adv ? "Carbon or carbon mix" : "Fibreglass or soft carbon mix");
    var avoid = adv ? "Anything over about 375 g" : "Diamonds and anything 370 g or over, for now";
    var H = {
      base: ["Big topspin swings: shorten the backswing and hit flatter or with slice", "Staying back: follow your partner to the net", "Taking the ball early: let it come off the back glass first"],
      srv: ["The overhead serve: in padel you serve underarm, after a bounce, below the waist", "Smashing every high ball: use the bandeja to keep the net", "Going for power: placement and lobs win the point"],
      net: ["Punching volleys hard: block and place them, low at the feet", "Covering the court alone: share the middle with your partner and call it", "Poaching everything: hold your side, the walls give second chances"]
    }[v.st];
    $("#tp-h").textContent = lo + " to " + hi + " g, " + shape.split(" ")[0].toLowerCase();
    $("#tp-p").textContent = (v.arm === "yes" ? "Comfort first: light, head-light and soft. Get lasting elbow pain checked by a doctor or physio. " : "") +
      (adv ? "You have a season behind you, so you can add a little weight and attack." : "Your tennis arm is fast, but padel is short and close: a forgiving racket helps you build the padel swing.");
    pgbSpec("#tp-spec", [["Weight", lo + " to " + hi + " g"], ["Balance", bal], ["Shape", shape], ["Core", core], ["Face", face], ["Avoid", avoid], ["Grip", "Continental, with 1 overgrip"]]);
    $("#tp-hab").innerHTML = H.map(function (h) { return "<li>" + h + "</li>"; }).join("");
    $("#tp-t").innerHTML = "Exact weight: " + pgbLk("padel-racket-weight", "weight calculator") + " · Serve: " + pgbLk("serve-rules", "serve rules") + " · Walls: " + pgbLk("padel-back-glass", "back glass guide");
  });

  /* ---------- spin checker ---------- */
  if ($("#sn-out")) pgbPicker("sn", "pgb-sn", { tech: "1", face: "0", wear: "2", ball: "1", clean: "0", shape: "1" }, function (v) {
    var W = { tech: 4, face: 1.5, wear: 1, ball: 1.5, clean: 0.5, shape: 1 }, sc = 0, mx = 0;
    Object.keys(W).forEach(function (k) { sc += (+v[k]) * W[k]; mx += 2 * W[k]; });
    var pct = Math.round(sc / mx * 100);
    if (v.tech === "0") pct = Math.min(pct, 45);
    var h = pct < 40 ? "Little spin" : (pct < 70 ? "Some spin" : "Lots of spin");
    var F = [];
    if (v.tech !== "2") F.push([0, "Brush across the ball: swing high to low with an open face on bandejas and slices. This matters more than any racket."]);
    if (v.ball === "0") F.push([1, "Open a new can: old, soft balls grip the face less."]); else if (v.ball === "1") F.push([3, "Use fresher balls for matches."]);
    if (v.wear === "0") F.push([2, "Your face is worn smooth: a new textured face will feel different, but only on brushing shots."]);
    if (v.clean !== "2") F.push([4, "Wipe sand and dust off the face every few games."]);
    if (v.face === "0" && v.tech !== "0") F.push([5, "Next racket: a sand or 3D textured face will help your slices a little."]);
    if (v.face === "1" && v.wear !== "2") F.push([5, "Painted grit wears quickly: a sand or moulded 3D finish lasts longer."]);
    if (v.shape === "0" && v.tech === "2") F.push([6, "Head speed: a teardrop moves faster than a round racket, without the diamond's small sweet spot."]);
    F.sort(function (a, b) { return a[0] - b[0]; });
    if (!F.length) F.push([0, "You have it covered. Keep the face clean and the balls fresh."]);
    var buy = v.tech === "0" ? "Not yet: technique first" : (v.face === "0" || v.wear === "0" ? "Maybe, when you next change racket" : "No need: your racket is not the limit");
    $("#sn-h").textContent = h;
    $("#sn-dot").style.left = Math.max(3, Math.min(97, pct)) + "%";
    $("#sn-p").textContent = v.tech === "0" ? "With a flat swing, no face texture adds much spin. Start with the swing." : (pct >= 70 ? "Your swing, face and balls are all working for you." : "Your swing is there; small kit changes will add a bit more bite.");
    $("#sn-fix").innerHTML = F.slice(0, 3).map(function (f) { return "<li>" + f[1] + "</li>"; }).join("");
    pgbSpec("#sn-spec", [["Spin racket worth it?", buy], ["Best face for spin", "Sand or 3D texture on carbon"], ["Shape", "Teardrop for most; diamond for strong attackers"]]);
    $("#sn-t").innerHTML = "Shots: " + pgbLk("bandeja-vs-vibora", "bandeja vs víbora") + " · Balls: " + pgbLk("padel-balls", "dead ball checker") + " · Type: " + pgbLk("control-vs-power-padel-racket", "control vs power test");
  });

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

  /* ---------- padel gift finder + voucher ---------- */
  var gfb = $("#gf");
  if (gfb && window.GFGO) {
    var ggr = $$("[data-gf]", gfb);
    var gst = store.get("pp-gf", { who: "reg", budget: "m", racket: "yes", specs: "no", shoes: "no", bag: "no" });
    var gl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var ga = function (k, t) { return '<a href="' + window.GFGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var BO = { s: 0, m: 1, l: 2, xl: 3 };
    var gpick = function () {
      var a = gst, b = BO[a.budget], L = [], warn = "";
      var add = function (min, max, score, h, t) { if (b >= min && b <= max) L.push({ s: score, h: h, t: t }); };
      add(0, 3, a.who === "new" ? 3 : 6, "Padel balls", "Everyone runs out. A can holds 3 balls; bigger budgets can buy a multi-pack. " + ga("padel-balls", "Shop balls"));
      add(0, 1, a.racket === "yes" ? 6 : 2, "A pack of overgrips", "Cheap and always needed when the handle gets slippery. " + ga("padel-overgrips", "Shop overgrips") + " · " + gl("padel-grip", "How to fit one"));
      add(0, 1, a.racket === "yes" ? 4 : 0, "Frame protector tape", "Guards the top of the frame against chips off the glass. " + gl("racket-care", "Racket care tips"));
      add(0, 0, 3, "Sweatbands and padel socks", "Small, useful and hard to get wrong.");
      add(1, 1, a.bag === "no" && a.racket === "yes" ? 5 : 2, "A racket cover or small backpack", "Keeps sand, heat and knocks off the racket. " + ga("padel-bags", "Shop bags"));
      add(1, 2, a.who === "keen" ? 4 : 5, "A court booking", "Book a court for four and play together. Ask the club about gift vouchers or court credit, or print the voucher below.");
      add(2, 3, a.bag === "no" ? 7 : 1, "A padel bag", "Holds rackets, shoes and balls in one. " + ga("padel-bags", "Shop bags"));
      add(2, 3, a.shoes === "no" ? 7 : 2, "Padel shoes", "Check their size and get a herringbone sole for most courts. Keep the gift receipt. " + ga("padel-shoes", "Shop shoes") + " · " + gl("padel-shoes", "Which sole?"));
      add(2, 3, a.who === "new" ? 8 : (a.who === "reg" ? 5 : 3), b === 3 ? "A block of lessons" : "A lesson with a coach", "Lessons change a game more than gear does, at any level. Ask the club or a local coach for a voucher.");
      if (a.racket === "no") add(2, 3, 9, "Their first racket", "Pick round, light, soft and head-light. " + ga("padel-round-rackets", "Shop round rackets") + " · " + gl("cheap-padel-rackets", "What to look for"));
      if (a.racket === "yes" && a.specs === "yes") add(3, 3, a.who === "keen" ? 8 : 4, "A racket they have tried", "Only the model they already like, or one with the same shape, weight and balance. " + gl("intermediate-padel-racket", "Upgrade check"));
      if (a.racket === "yes" && a.specs === "no") add(3, 3, a.who === "keen" ? 6 : 3, "A racket voucher", "Give the money for their next racket and let them demo and choose. " + gl("racket-finder", "Racket finder"));
      add(3, 3, a.who === "keen" ? 5 : 2, "A padel weekend or camp", "For keen players: coaching and games over a few days. Check what is included before you book.");
      add(0, 3, 1, "An Americano night", "Free to organise: book courts, invite friends and use our " + gl("americano", "Americano draw maker") + ".");
      L.sort(function (x, y) { return y.s - x.s; });
      L = L.slice(0, 5);
      if (a.racket === "yes" && a.specs === "no") warn = "Skip a surprise racket: regular players are picky, and the wrong weight or balance can hurt their arm.";
      else if (a.racket === "no") warn = "A first racket is a safe gift. Avoid stiff, heavy or diamond rackets for a new player.";
      else warn = "Keep the gift receipt for anything with a size or a feel, like shoes and rackets.";
      var who = { "new": "a new player", reg: "a weekly player", keen: "a keen player" }[a.who];
      return { h: "Top gifts for " + who, p: "Best first, for your budget:", L: L, warn: warn };
    };
    var grender = function () {
      store.set("pp-gf", gst);
      ggr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === gst[g.dataset.gf] ? "true" : "false"); }); });
      var r = gpick();
      $("#gf-h").textContent = r.h;
      $("#gf-p").textContent = r.p;
      $("#gf-list").innerHTML = r.L.map(function (x) { return "<li><b>" + x.h + "</b><span>" + x.t + "</span></li>"; }).join("");
      $("#gf-warn").textContent = r.warn;
    };
    ggr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { gst[g.dataset.gf] = b.dataset.v; grender(); }); }); });
    grender();
  }
  var gvb = $("#gv");
  if (gvb) {
    var GV = { lesson: "A padel lesson", court: "A court booking for four", americano: "An Americano night with friends", racket: "A new racket of your choice", shoes: "New padel shoes, we'll choose together" };
    var vst = store.get("pp-gv", { gift: "lesson", own: "", to: "", from: "", msg: "", date: "" });
    var vin = { own: $("#gv-own"), to: $("#gv-to"), from: $("#gv-from"), msg: $("#gv-msg"), date: $("#gv-date") };
    Object.keys(vin).forEach(function (k) { vin[k].value = vst[k] || ""; vin[k].addEventListener("input", function () { vst[k] = vin[k].value; vrender(); }); });
    var vbtn = $$("[data-gv] button", gvb);
    var vrender = function () {
      store.set("pp-gv", vst);
      vbtn.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === vst.gift ? "true" : "false"); });
      vin.own.parentNode.style.display = vst.gift === "own" ? "" : "none";
      $("#gv-gift").textContent = vst.gift === "own" ? (vst.own || "Your gift here") : GV[vst.gift];
      $("#gv-to-o").textContent = vst.to || "you";
      $("#gv-from-o").textContent = vst.from || "me";
      $("#gv-msg-o").textContent = vst.msg;
      $("#gv-date-o").textContent = vst.date ? " · Use by " + vst.date : "";
    };
    vbtn.forEach(function (b) { b.addEventListener("click", function () { vst.gift = b.dataset.v; vrender(); }); });
    $("#gv-print").addEventListener("click", function () {
      var root = document.createElement("div"); root.id = "gv-print-root"; root.appendChild($("#gv-card").cloneNode(true)); root.firstChild.removeAttribute("id");
      document.body.appendChild(root); document.body.classList.add("print-gv"); window.print();
      setTimeout(function () { document.body.classList.remove("print-gv"); if (root.parentNode) root.parentNode.removeChild(root); }, 500);
    });
    vrender();
  }

  /* ---------- padel equipment: kit planner / packing list ---------- */
  var kpb = $("#kp");
  if (kpb && window.KPGO) {
    var kgr = $$("[data-kp]", kpb);
    var kst = store.get("pp-kp", { often: "first", where: "in", wx: "mild", racket: "no", shoes: "run" });
    var ktick = store.get("pp-kp-tick", {});
    var kl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var ka = function (k, t) { return '<a href="' + window.KPGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var kbuild = function () {
      var a = kst, M = [], G = [], S = [];
      var reg = a.often === "week", first = a.often === "first";
      if (a.racket === "no") M.push(["racket", "A padel racket", first ? "Rent one at the club or borrow one. Ask when you book." : "Rent for now, or buy a round, light, forgiving racket. " + kl("racket-finder", "Racket finder") + " · " + ka("padel-round-rackets", "Round rackets")]);
      else M.push(["racket", "Your racket", "Check the frame for cracks and the grip for wear. " + kl("racket-care", "Racket health check")]);
      M.push(["balls", "A can of padel balls (3 balls)", "Fresh balls bounce properly. Padel balls, not tennis balls. " + ka("padel-balls", "Shop balls")]);
      if (a.shoes === "padel") M.push(["shoes", "Your padel shoes", "Check the sole is not worn smooth. " + kl("padel-shoes", "When to replace")]);
      else if (a.shoes === "tennis") M.push(["shoes", "Your tennis or clay court shoes", reg ? "Fine to start, but padel shoes with a herringbone sole grip sand turf better if you play every week. " + ka("padel-shoes", "Shop padel shoes") : "Fine for now. " + kl("padel-shoes", "Shoe finder")]);
      else M.push(["shoes", "Court shoes, not running shoes", (first ? "Borrow tennis, clay court or padel shoes if you can. Running shoes slip on sand turf and give little side support. " : "Running shoes slip on sand turf and give little side support. Get padel shoes with a herringbone sole. " + ka("padel-shoes", "Shop padel shoes") + " · ") + kl("padel-shoes", "Which sole?")]);
      M.push(["top", a.wx === "cold" ? "A light technical top plus a base layer" : "A light technical top", "Polyester or similar that dries fast, not heavy cotton."]);
      M.push(["bottom", a.wx === "cold" && a.where === "out" ? "Leggings or joggers (or shorts with a layer)" : "Shorts, sports skirt or leggings with a pocket", "Stretchy, with a deep pocket for the second ball."]);
      M.push(["socks", "Padded sports socks", "Thin socks give blisters when you slide."]);
      M.push(["water", "A water bottle", a.wx === "warm" ? "Bring extra in the heat." : "Sip between games."]);
      if (a.wx === "cold") G.push(["jacket", "A windproof jacket or warm layer", "For the warm-up and between games. Take it off once you are warm."]);
      else G.push(["layer", "A light layer for the warm-up", "Keeps you warm while you get loose. " + kl("warm-up", "Warm-up timer")]);
      if (a.where === "out" && a.wx !== "cold") G.push(["sun", "Cap or visor, sports sunglasses and sun cream", "Glare off the glass and turf is strong on sunny days."]);
      if (a.where === "out" && a.wx === "cold") G.push(["hat", "A hat and gloves for before and after", "Hands go cold fast between games outdoors."]);
      G.push(["towel", "A small towel and a wristband", "Stops sweat running down to your hand and grip."]);
      if (a.racket === "yes" || !first) G.push(["grip", "A spare overgrip", "Swap it when the handle feels slippery. " + kl("padel-grip", "How to fit one") + " · " + ka("padel-overgrips", "Shop overgrips")]);
      if (reg) G.push(["bag", "A padel bag or sports bag", "One bag for racket, shoes and balls. A thermal pocket helps in heat and cold. " + ka("padel-bags", "Shop bags")]);
      G.push(["booking", "Your court booking and three other players", first ? "Check the booking time and arrive 10 minutes early. " + kl("beginners", "First match checklist") : "Need a format for 8 or more? " + kl("americano", "Americano draw maker")]);
      if (!reg) S.push(["sbag", "A dedicated padel bag", "Any sports bag works until you play every week."]);
      if (first && a.racket === "no") S.push(["sgrip", "Overgrips and frame protector", "Not needed on a rented racket."]);
      if (a.racket === "yes" && !reg) S.push(["sprot", "Frame protector tape", "Optional. It guards against chips but adds a few grams at the top."]);
      S.push(["sclothes", "Branded padel clothes", "Any tennis or gym kit works the same."]);
      if (first) S.push(["sracket", "Buying an expensive racket", "Play a few games first, then choose with the " + kl("racket-finder", "racket finder") + "."]);
      return { M: M, G: G, S: S };
    };
    var kgrp = function (title, L, skip) {
      if (!L.length) return "";
      return '<h3 class="kp-g">' + title + '</h3><ul class="kp-l">' + L.map(function (x) {
        if (skip) return '<li class="kp-skip"><span><b>' + x[1] + "</b><small>" + x[2] + "</small></span></li>";
        return '<li><label><input type="checkbox" data-k="' + x[0] + '"' + (ktick[x[0]] ? " checked" : "") + "><span><b>" + x[1] + "</b><small>" + x[2] + "</small></span></label></li>";
      }).join("") + "</ul>";
    };
    var klast;
    var krender = function () {
      store.set("pp-kp", kst);
      kgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === kst[g.dataset.kp] ? "true" : "false"); }); });
      var r = kbuild(); klast = r;
      var n = r.M.length + r.G.length, done = r.M.concat(r.G).filter(function (x) { return ktick[x[0]]; }).length;
      $("#kp-h").textContent = { first: "Your first game kit", some: "Your padel bag", week: "Your weekly padel kit" }[kst.often];
      $("#kp-p").textContent = done + " of " + n + " packed. Must bring: " + r.M.length + " items.";
      $("#kp-list").innerHTML = kgrp("Must bring", r.M) + kgrp("Good to have", r.G) + kgrp("Skip for now", r.S, true);
      $$("#kp-list input").forEach(function (c) { c.addEventListener("change", function () { if (c.checked) ktick[c.dataset.k] = 1; else delete ktick[c.dataset.k]; store.set("pp-kp-tick", ktick); var d2 = klast.M.concat(klast.G).filter(function (x) { return ktick[x[0]]; }).length; $("#kp-p").textContent = d2 + " of " + n + " packed. Must bring: " + klast.M.length + " items."; }); });
      $("#kp-next").innerHTML = "Next: " + kl("beginners", "first match rules") + " · " + kl("padel-shoes", "shoe finder") + " · " + kl("racket-finder", "racket finder");
    };
    kgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { kst[g.dataset.kp] = b.dataset.v; krender(); }); }); });
    $("#kp-clear").addEventListener("click", function () { ktick = {}; store.set("pp-kp-tick", ktick); krender(); });
    $("#kp-copy").addEventListener("click", function () {
      var strip = function (h) { var d = document.createElement("div"); d.innerHTML = h; return d.textContent; };
      var line = function (x) { return (ktick[x[0]] ? "[x] " : "[ ] ") + x[1]; };
      var txt = "My padel kit list\n\nMust bring\n" + klast.M.map(line).join("\n") + "\n\nGood to have\n" + klast.G.map(line).join("\n") + "\n\nSkip for now\n" + klast.S.map(function (x) { return "- " + x[1] + ": " + strip(x[2]); }).join("\n") + "\n\nhttps://padelglassbox.com/padel-equipment";
      var ok = function () { toast("List copied"); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () { toast("Copy failed"); }); else toast("Copy not supported");
    });
    krender();
  }

  /* ---------- padel racket for kids: junior size finder ---------- */
  var jrb = $("#jr");
  if (jrb && window.JRGO) {
    var jgr = $$("[data-jr]", jrb);
    var jst = store.get("pp-jr", { age: "1", h: "x", build: "a", play: "try", sore: "no" });
    var jl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var jg = function (k, t) { return '<a href="' + window.JRGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var JB = [
      { w: [210, 260], t: "Mini or foam racket", s: "Round", c: "Soft foam", f: "Fibreglass or foam", g: "Smallest junior handle" },
      { w: [260, 300], t: "Light junior racket", s: "Round", c: "Soft EVA or foam", f: "Fibreglass", g: "Thin junior handle" },
      { w: [300, 330], t: "Junior racket", s: "Round", c: "Soft EVA", f: "Fibreglass", g: "Junior handle, add an overgrip as hands grow" },
      { w: [330, 355], t: "Older junior or light adult racket", s: "Round, or teardrop for a strong, keen player", c: "Soft or medium EVA", f: "Fibreglass", g: "Junior or adult handle with a thin overgrip" },
      { w: [350, 360], t: "Light adult racket", s: "Round to start", c: "Soft EVA", f: "Fibreglass, carbon later", g: "Adult handle" }
    ];
    var jrender = function () {
      store.set("pp-jr", jst);
      jgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === jst[g.dataset.jr] ? "true" : "false"); }); });
      var a = +jst.age, i = a, note = [];
      if (jst.h !== "x") { var h = +jst.h, ha = Math.min(a, 3); if (h > ha && a < 4) { i++; note.push("tall for their age, so one band up"); } else if (h < ha) { i--; note.push("small for their age, so one band down"); } }
      if (jst.build === "s" && i === a) { i--; note.push("not so strong yet, so one band lighter"); }
      if (jst.build === "b" && i === a && jst.sore === "no" && jst.play !== "try") { i++; note.push("strong and playing often, so one band up"); }
      if (jst.sore === "yes") { i--; note.push("sore arm, so one band lighter"); }
      i = Math.max(0, Math.min(4, i));
      if (a < 4 && i === 4 && a < 3) i = 3;
      var B = JB[i];
      $("#jr-h").textContent = B.w[0] + " to " + B.w[1] + " g";
      $("#jr-p").textContent = "Look for a " + B.t.toLowerCase() + " in this weight band." + (note.length ? " Adjusted: " + note.join("; ") + "." : "");
      var x = function (gr) { return 10 + (gr - 200) * 1.5; };
      var band = $("#jr-band"); band.setAttribute("x", x(B.w[0]).toFixed(1)); band.setAttribute("width", ((B.w[1] - B.w[0]) * 1.5).toFixed(1));
      $("#jr-spec").innerHTML = "<dt>Type</dt><dd>" + B.t + "</dd><dt>Shape</dt><dd>" + B.s + "</dd><dt>Core</dt><dd>" + B.c + "</dd><dt>Face</dt><dd>" + B.f + "</dd><dt>Handle</dt><dd>" + B.g + "</dd><dt>Always</dt><dd>Wrist cord on</dd>";
      var mv;
      if (a <= 1) mv = "Adult racket: not yet. Most children move up at about 12 to 14.";
      else if (a === 2) mv = "Adult racket: probably not yet. Re-check when they grow or play more.";
      else if (jst.sore === "yes") mv = "Adult racket: wait. Fix the sore arm with a lighter, softer racket first.";
      else if (a === 3) mv = (jst.build === "b" || jst.h === "3") && jst.play !== "try" ? "Adult racket: they may be ready for a light, round one (about 350 to 360 g). Let them try one first." : "Adult racket: soon. A light adult racket is the next step when they are stronger.";
      else mv = "Adult racket: yes, a light round one to start. Then use the " + jl("racket-finder", "racket finder") + ".";
      $("#jr-move").innerHTML = mv;
      $("#jr-warn").innerHTML = jst.sore === "yes" ? "If pain lasts more than a few days, see a doctor or physio. " + jl("padel-injuries", "Padel injuries guide") : "Check the real weight in grams: some rackets sold as junior weigh 330 to 350 g.";
      $("#jr-next").innerHTML = "Shop: " + jg(i >= 3 && jst.build === "b" && jst.play === "lots" ? "padel-teardrop-rackets" : "padel-round-rackets", i >= 3 && jst.build === "b" && jst.play === "lots" ? "Teardrop rackets" : "Round rackets") + " · Next: " + jl("beginners", "beginner rules") + " · " + jl("drills", "fun drills");
    };
    jgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { jst[g.dataset.jr] = b.dataset.v; jrender(); }); }); });
    jrender();
  }

  /* ---------- padel lesson cost checker ---------- */
  var lsb = $("#ls");
  if (lsb && window.LSGO) {
    var lgr = $$("[data-ls]", lsb);
    var lst = store.get("pp-ls", { reg: "uk", type: "p1", per: "all", len: "60", blk: "1", price: 60, court: 0, n: 1, disc: "0" });
    var LCUR = { uk: "£", us: "$", eu: "€", ae: "AED " };
    var LRNG = { uk: { p1: [40, 80], p2: [25, 50], p4: [12, 30], cl: [10, 30] }, us: { p1: [50, 160], p2: [25, 80, 1], p4: [20, 60], cl: [20, 60] } };
    var LN = { p1: 1, p2: 2, p4: 4, cl: 6 };
    var LNAME = { p1: "private lesson", p2: "shared private lesson", p4: "small group lesson", cl: "group clinic" };
    var ll = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var lg = function (k, t) { return '<a href="' + window.LSGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var lin = { price: $("#ls-price"), court: $("#ls-court"), n: $("#ls-n"), disc: $("#ls-disc") };
    lin.price.value = lst.price; lin.court.value = lst.court; lin.n.value = lst.n; lin.disc.value = lst.disc;
    var money = function (c, v) { return c + (Math.round(v * 100) / 100).toFixed(v >= 100 ? 0 : 2).replace(/\.00$/, ""); };
    var lrender = function () {
      lst.price = Math.max(0, +lin.price.value || 0); lst.court = Math.max(0, +lin.court.value || 0);
      lst.n = Math.max(1, Math.min(8, Math.round(+lin.n.value || 1))); lst.disc = lin.disc.value;
      store.set("pp-ls", lst);
      lgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === lst[g.dataset.ls] ? "true" : "false"); }); });
      var c = LCUR[lst.reg], n = lst.n, len = +lst.len, blk = +lst.blk, d = +lst.disc / 100;
      var total = (lst.per === "all" ? lst.price : lst.price * n) + lst.court;
      var each = total / n, hr = each * 60 / len, block = each * blk * (1 - d);
      $("#ls-h").textContent = money(c, each) + " each";
      $("#ls-p").textContent = "For one " + len + "-minute " + LNAME[lst.type] + (n > 1 ? ", split " + n + " ways" : ", just you paying") + (lst.court ? ", court hire included." : ".");
      $("#ls-spec").innerHTML = "<dt>Whole lesson</dt><dd>" + money(c, total) + "</dd><dt>You, per hour</dt><dd>" + money(c, hr) + "</dd>" + (blk > 1 ? "<dt>" + blk + " lessons</dt><dd>" + money(c, block) + " each" + (d ? " after " + lst.disc + "% off" : "") + "</dd>" : "");
      var R = LRNG[lst.reg] && LRNG[lst.reg][lst.type], v;
      if (!lst.price) v = "Enter the price you were quoted.";
      else if (!R) v = "We found no reliable published price range for " + (lst.reg === "ae" ? "the UAE" : "Europe") + ", so compare this with two or three other local clubs or coaches.";
      else {
        var lab = c + R[0] + " to " + c + R[1] + " per person per hour" + (R[2] ? " (our estimate: the US private range split two ways)" : "");
        if (hr < R[0]) v = "Below the typical range of " + lab + ". Good value: check the group size and what is included.";
        else if (hr > R[1]) v = "Above the typical range of " + lab + ". It may be a senior coach or a premium club. Ask what is included, or try a shared lesson.";
        else v = "Within the typical range of " + lab + ".";
      }
      $("#ls-v").textContent = v;
      var tip;
      if (lst.type === "p1") tip = "Tip: share it with a friend. If the coach keeps the same total, you would pay " + money(c, total / 2) + " each (many add a small fee per extra player).";
      else if (lst.type === "cl") tip = "Tip: in a big group you get less feedback. Ask how many players there will be and whether they are your level.";
      else tip = "Tip: book with the same partner each time, so you learn to move as a pair.";
      if (lst.len === "30") tip += " A 30-minute lesson is short: it suits one focused skill.";
      $("#ls-tip").textContent = tip;
      $("#ls-next").innerHTML = "Next: " + ll("beginners", "beginner rules") + " · " + ll("level-calculator", "your level") + " · " + ll("drills", "practise between lessons") + " · Shop: " + lg("padel-round-rackets", "round rackets");
    };
    lgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () {
      lst[g.dataset.ls] = b.dataset.v;
      if (g.dataset.ls === "type") { lin.n.value = LN[b.dataset.v]; if (b.dataset.v !== "p1") { lst.per = b.dataset.v === "p2" ? "all" : "pp"; } else lst.per = "all"; }
      lrender(); }); }); });
    ["price", "court", "n", "disc"].forEach(function (k) { lin[k].addEventListener("input", lrender); lin[k].addEventListener("change", lrender); });
    lrender();
  }

  /* ---------- padel rankings points calculator ---------- */
  var rkb = $("#rk");
  if (rkb && window.RK) {
    var rgr = $$("[data-rk]", rkb);
    var rst = store.get("pp-rk", { yr: "2026", cat: "p1", rd: "qf", list: [] });
    if (!Array.isArray(rst.list)) rst.list = [];
    var RCAT = { major: "Major", p1: "P1", p2: "P2" };
    var RRD = { w: "won", f: "runner-up", sf: "semi-final", qf: "quarter-final", r16: "last 16", r32: "last 32", r64: "last 64" };
    var rl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var fmt = function (n) { return n.toLocaleString("en-GB"); };
    var ptsOf = function (r) { var t = window.RK.pts[rst.yr][r.cat]; return t && t[r.rd] ? t[r.rd] : 0; };
    var place = function (tot, rows) {
      for (var i = 0; i < rows.length; i++) { if (tot >= rows[i][2]) return i; }
      return -1;
    };
    var rrender = function () {
      store.set("pp-rk", rst);
      rgr.forEach(function (g) { $$("button", g).forEach(function (b) {
        b.setAttribute("aria-pressed", b.dataset.v === rst[g.dataset.rk] ? "true" : "false");
        if (g.dataset.rk === "rd") b.disabled = b.dataset.v === "r64" && rst.cat === "p2";
      }); });
      var max = rst.yr === "2027" ? 21 : 22;
      var scored = rst.list.map(function (r, i) { return { i: i, p: ptsOf(r) }; }).sort(function (a, b) { return b.p - a.p; });
      var keep = {}; scored.slice(0, max).forEach(function (x) { keep[x.i] = 1; });
      var tot = scored.slice(0, max).reduce(function (a, x) { return a + x.p; }, 0);
      var ul = $("#rk-list"); ul.innerHTML = "";
      rst.list.forEach(function (r, i) {
        var li = document.createElement("li"); if (!keep[i]) li.className = "off";
        li.innerHTML = "<span>" + (i + 1) + ". " + RCAT[r.cat] + ", " + RRD[r.rd] + (keep[i] ? "" : " (not counted)") + "</span><b>" + fmt(ptsOf(r)) + "</b>";
        var x = document.createElement("button"); x.type = "button"; x.textContent = "Remove"; x.setAttribute("aria-label", "Remove result " + (i + 1));
        x.addEventListener("click", function () { rst.list.splice(i, 1); rrender(); });
        li.appendChild(x); ul.appendChild(li);
      });
      $("#rk-h").textContent = fmt(tot) + " points";
      var n = rst.list.length;
      $("#rk-p").textContent = n ? "From " + Math.min(n, max) + " counted result" + (Math.min(n, max) === 1 ? "" : "s") + " using the " + rst.yr + " table (best " + max + " count)." : "Add a result to start, or try the example season.";
      var m = window.RK.men, w = window.RK.women, pm = place(tot, m), pw = place(tot, w);
      $("#rk-spec").innerHTML = "<dt>Men's no. 1</dt><dd>" + fmt(m[0][2]) + "</dd><dt>Men's no. 10</dt><dd>" + fmt(m[9][2]) + "</dd><dt>Women's no. 1</dt><dd>" + fmt(w[0][2]) + "</dd><dt>Women's no. 10</dt><dd>" + fmt(w[9][2]) + "</dd>";
      var say = function (p, rows, lab) {
        if (p === 0) return "level with or above the " + lab + " number 1s";
        if (p > 0) return "around number " + rows[p][0] + " in the " + lab + " top 10 (ahead of " + rows[p][1] + ")";
        return fmt(rows[9][2] - tot) + " short of the " + lab + " top 10";
      };
      $("#rk-v").textContent = n ? "Against the FIP ranking of " + window.RK.date + ", that total would be " + say(pm, m, "men's") + ", and " + say(pw, w, "women's") + ". Real totals also include Finals and FIP Tour points." : "";
      $("#rk-next").innerHTML = "Next: " + rl("level-calculator", "your own club level") + " · " + rl("ladder", "run a club ladder") + " · " + rl("bandeja-vs-vibora", "pro overheads");
    };
    rgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () {
      rst[g.dataset.rk] = b.dataset.v;
      if (rst.cat === "p2" && rst.rd === "r64") rst.rd = "r32";
      rrender(); }); }); });
    $("#rk-add").addEventListener("click", function () { if (rst.list.length < 40) rst.list.push({ cat: rst.cat, rd: rst.rd }); rrender(); });
    $("#rk-clear").addEventListener("click", function () { rst.list = []; rrender(); });
    $("#rk-demo").addEventListener("click", function () {
      rst.list = [{ cat: "major", rd: "sf" }, { cat: "major", rd: "qf" }, { cat: "p1", rd: "w" }, { cat: "p1", rd: "f" }, { cat: "p1", rd: "qf" }, { cat: "p1", rd: "qf" }, { cat: "p1", rd: "r16" }, { cat: "p2", rd: "w" }, { cat: "p2", rd: "sf" }, { cat: "p2", rd: "qf" }];
      rrender(); });
    rrender();
  }

  /* ---------- racket materials label decoder ---------- */
  var mtb = $("#mt");
  if (mtb && window.MTGO) {
    var mgr = $$("[data-mt]", mtb);
    var RK_KEYS = ["face", "k", "core", "surf"];
    var mdef = { which: "a", lvl: "new", arm: "no", a: { face: "glass", k: "none", core: "soft", surf: "smooth" }, b: { face: "carbon", k: "12", core: "hard", surf: "3d" } };
    var mst = store.get("pp-mt", mdef);
    if (!mst.a || !mst.b) mst = mdef;
    var FACE = { glass: [20, 20, 5, -15], hybrid: [8, 8, 2, -5], carbon: [-12, -10, -5, 15], x: [0, 0, 0, 0] };
    // [comfort, forgiveness, easy power at slow speed, power on fast swings]
    var CORE = { foam: [30, 22, 30, -25], soft: [22, 15, 22, -12], med: [5, 5, 5, 5], hard: [-20, -15, -20, 25], multi: [10, 6, 10, 6], x: [0, 0, 0, 0] };
    var SURF = { smooth: 20, sand: 70, "3d": 60, both: 75, x: 45 };
    var MN = { glass: "fibreglass", hybrid: "fibreglass + carbon", carbon: "carbon", foam: "foam", soft: "soft EVA", med: "medium EVA", hard: "hard EVA", multi: "mixed core" };
    var cl = function (n) { return Math.max(5, Math.min(95, n)); };
    var score = function (r) {
      var f = FACE[r.face] || FACE.x, c = CORE[r.core] || CORE.x;
      return [cl(50 + f[0] + c[0]), cl(50 + f[1] + c[1]), cl(50 + f[2] + c[2]), cl(50 + f[3] + c[3]), SURF[r.surf] || 45];
    };
    var LAB = ["Comfort", "Forgives mis-hits", "Easy power, slow swings", "Power, fast swings", "Spin help"];
    var mrender = function () {
      store.set("pp-mt", mst);
      var cur = mst[mst.which];
      mgr.forEach(function (g) {
        var k = g.dataset.mt, val = RK_KEYS.indexOf(k) > -1 ? cur[k] : mst[k];
        $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === val ? "true" : "false"); });
      });
      $$("button", $("#mt-which")).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === mst.which ? "true" : "false"); });
      var A = score(mst.a), B = score(mst.b);
      $("#mt-bars").innerHTML = '<p style="margin:4px 0 8px;font-size:.88rem"><span style="color:#e8f84a;font-weight:700">A</span> yellow · <span style="color:#fff;font-weight:700">B</span> white</p><dl class="spec" style="grid-template-columns:1fr">' + LAB.map(function (l, i) {
        return "<dt>" + l + '</dt><dd><div class="meter" aria-label="Racket A ' + A[i] + ' of 100"><i style="width:' + A[i] + '%"></i></div><div class="meter" aria-label="Racket B ' + B[i] + ' of 100"><i style="width:' + B[i] + '%;background:#fff"></i></div></dd>';
      }).join("") + "</dl>";
      var s = score(cur), why = [], L = mst.which.toUpperCase();
      var desc = [cur.face !== "x" ? MN[cur.face] + " face" : "", cur.core !== "x" ? MN[cur.core] + " core" : ""].filter(Boolean).join(", ");
      var h, p, cls = "";
      if (s[0] >= 70 && s[1] >= 65) { h = "Racket " + L + ": soft and forgiving"; p = "Comfortable and easy to play, with easy power at slow speed. Less punch when you swing hard."; cls = " good"; }
      else if (s[3] >= 70) { h = "Racket " + L + ": stiff and powerful"; p = "Lively when you swing fast and hit the middle. Less forgiving, and more vibration reaches the arm."; }
      else { h = "Racket " + L + ": a middle feel"; p = "A mix of comfort and firmness. Shape, weight and balance will decide most of how it plays."; cls = " mid"; }
      if (desc) p = desc.charAt(0).toUpperCase() + desc.slice(1) + ". " + p;
      if (mst.arm === "yes" && s[0] < 55) { why.push("Your arm gets sore: this build is on the stiff side. A soft EVA or foam core and a fibreglass face are kinder."); cls = ""; }
      if (mst.arm === "yes" && s[0] >= 55) why.push("Good for a sore arm. Keep the weight light and the balance low too.");
      if (mst.lvl === "new" && (s[1] < 45 || s[3] >= 70)) why.push("For a new player this may feel hard and unforgiving. Most guides start beginners on fibreglass with a soft core.");
      if (mst.lvl === "new" && s[1] >= 60) why.push("A forgiving build is a good match while you learn to hit cleanly.");
      if (mst.lvl === "adv" && s[0] >= 70 && s[3] < 45) why.push("You may miss some punch on smashes. A medium or mixed core gives more without going fully hard.");
      if (cur.k !== "none" && cur.k !== "x") why.push(cur.k + "K describes the carbon weave, usually of the outer layer only. It is not scored: guides disagree on what it changes.");
      if (cur.k !== "none" && cur.face === "glass") why.push("A K number with a fibreglass face usually means some carbon in the frame or the top sheet. Check the full spec.");
      if (cur.surf === "sand") why.push("A sandy finish grips well when new but can wear smoother over time.");
      if (cur.surf === "smooth") why.push("Smooth face: fine for flat, controlled shots. Spin comes mostly from technique.");
      if (cur.face === "x" || cur.core === "x") why.push("Some parts are not stated. Ask the shop or look for a review before you buy.");
      var d = 0; for (var i = 0; i < 4; i++) d += Math.abs(A[i] - B[i]);
      why.push(d < 25 ? "A and B are close in materials. Compare shape, weight and balance instead." : "Biggest gap between A and B: " + LAB[[0, 1, 2, 3].sort(function (x, y) { return Math.abs(B[y] - A[y]) - Math.abs(B[x] - A[x]); })[0]].toLowerCase() + ".");
      var out = $("#mt-out"); out.className = "result" + cls;
      $("#mt-h").textContent = h; $("#mt-p").textContent = p;
      $("#mt-why").innerHTML = why.map(function (x) { return "<li>" + x + "</li>"; }).join("");
      var lk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
      var shp = (s[0] >= 70 && s[1] >= 65) ? "round" : (s[3] >= 70 ? "diamond" : "teardrop");
      if (mst.lvl === "new" || mst.arm === "yes") shp = "round";
      $("#mt-next").innerHTML = "Next: " + lk("racket-finder", "match the shape") + " · " + lk("racket-balance", "check weight and balance") + " · " + '<a href="' + window.MTGO[shp] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a;font-weight:700">Browse ' + shp + " rackets</a> (affiliate link)";
    };
    mgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () {
      var k = g.dataset.mt;
      if (RK_KEYS.indexOf(k) > -1) mst[mst.which][k] = b.dataset.v; else mst[k] = b.dataset.v;
      mrender(); }); }); });
    $$("button", $("#mt-which")).forEach(function (b) { b.addEventListener("click", function () { mst.which = b.dataset.v; mrender(); }); });
    mrender();
  }
  /* ---------- court space planner ---------- */
  var csp = $("#csp");
  if (csp) {
    var FTm = 0.3048;
    var SP = { padel: ["Padel", 20, 10, 0.4, 1.5, 0.4, 1.5], pickleball: ["Pickleball", 60 * FTm, 30 * FTm, 0, 0, 0, 0], badminton: ["Badminton", 13.4, 6.1, 2, 2, 1.5, 1.5], tennis: ["Tennis", 120 * FTm, 60 * FTm, 0, 0, 0, 0] };
    var cs = store.get("csp", { s: "padel", u: "m", l: 36.58, w: 18.29 });
    function setP(group, v) { $$("button", group).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === v ? "true" : "false"); }); }
    function lay(sp, d1, d2) {
      var a = Math.max(0, Math.floor((d1 - 2 * sp[3] + sp[4]) / (sp[1] + sp[4]) + 1e-6)), b = Math.max(0, Math.floor((d2 - 2 * sp[5] + sp[6]) / (sp[2] + sp[6]) + 1e-6));
      return { a: a, b: b, n: a * b };
    }
    function need(sp, k, along) { return along ? k * sp[1] + (k - 1) * sp[4] + 2 * sp[3] : k * sp[2] + (k - 1) * sp[6] + 2 * sp[5]; }
    function cRender() {
      var f = cs.u === "ft" ? FTm : 1, L = (+$("#csp-l").value || 0) * f, W = (+$("#csp-w").value || 0) * f, sp = SP[cs.s];
      var x = lay(sp, L, W), y = lay(sp, W, L), best = x.n >= y.n ? { r: x, rot: false } : { r: y, rot: true };
      var r = best.r, u = function (m) { return cs.u === "ft" ? (m / FTm).toFixed(1) + " ft" : m.toFixed(2) + " m"; };
      var h = '<p class="big">' + r.n + " " + sp[0].toLowerCase() + " court" + (r.n === 1 ? "" : "s") + " fit" + (r.n === 1 ? "s" : "") + "</p>";
      if (r.n) h += "<p>Laid out as " + r.a + " × " + r.b + (best.rot ? ", courts running across the width." : ", courts running along the length.") + "</p>";
      // what it takes to fit one more
      var opts = [];
      [[false, L, W], [true, W, L]].forEach(function (o) {
        var g = lay(sp, o[1], o[2]), a1 = Math.max(g.a, 1), b1 = Math.max(g.b, 1);
        var tA = need(sp, g.a + 1, true), tB = need(sp, b1, false); if ((g.a + 1) * b1 > r.n) opts.push({ d: Math.max(0, tA - o[1]) + Math.max(0, tB - o[2]), t: [tA, tB], rot: o[0], n: (g.a + 1) * b1 });
        tA = need(sp, a1, true); tB = need(sp, g.b + 1, false); if (a1 * (g.b + 1) > r.n) opts.push({ d: Math.max(0, tA - o[1]) + Math.max(0, tB - o[2]), t: [tA, tB], rot: o[0], n: a1 * (g.b + 1) });
      });
      opts.sort(function (p, q) { return p.d - q.d; });
      if (opts.length) { var o = opts[0], len = o.rot ? o.t[1] : o.t[0], wid = o.rot ? o.t[0] : o.t[1]; h += '<p class="muted">To fit ' + o.n + ", you'd need about " + u(Math.max(len, L)) + " × " + u(Math.max(wid, W)) + ".</p>"; }
      // drawing
      if (L > 0 && W > 0) {
        var sc = 600 / Math.max(L, W), pw = L * sc, ph = W * sc, svg = '<svg viewBox="-10 -10 ' + (pw + 20).toFixed(0) + " " + (ph + 20).toFixed(0) + '" role="img" aria-label="Layout of ' + r.n + ' courts in your space"><rect x="0" y="0" width="' + pw.toFixed(1) + '" height="' + ph.toFixed(1) + '" fill="none" stroke="#e8f84a" stroke-width="2" stroke-dasharray="6 4"/>';
        var cl = best.rot ? sp[2] : sp[1], cw = best.rot ? sp[1] : sp[2], ml = best.rot ? sp[5] : sp[3], mw = best.rot ? sp[3] : sp[5], gl = best.rot ? sp[6] : sp[4], gw = best.rot ? sp[4] : sp[6];
        var nl = best.rot ? r.b : r.a, nw = best.rot ? r.a : r.b;
        for (var i = 0; i < nl; i++) for (var j = 0; j < nw; j++) svg += '<rect x="' + ((ml + i * (cl + gl)) * sc).toFixed(1) + '" y="' + ((mw + j * (cw + gw)) * sc).toFixed(1) + '" width="' + (cl * sc).toFixed(1) + '" height="' + (cw * sc).toFixed(1) + '" fill="#1f4fd1" stroke="#fff" stroke-width="2"/>';
        h += svg + "</svg>";
      }
      h += '<p style="margin-top:12px">Next: <a href="' + (location.protocol === "file:" ? "court-dimensions.html" : "/court-dimensions") + '">padel court dimensions</a> · <a href="' + (location.protocol === "file:" ? "padel-court-cost.html" : "/padel-court-cost") + '">what a padel court costs</a></p>';
      $("#csp-out").innerHTML = h;
      cs.l = +$("#csp-l").value; cs.w = +$("#csp-w").value; store.set("csp", cs);
    }
    $("#csp-l").value = cs.l; $("#csp-w").value = cs.w; setP($("#csp-s"), cs.s); setP($("#csp-u"), cs.u);
    $$("button", $("#csp-s")).forEach(function (b) { b.addEventListener("click", function () { cs.s = b.dataset.v; setP($("#csp-s"), cs.s); cRender(); }); });
    $$("button", $("#csp-u")).forEach(function (b) { b.addEventListener("click", function () {
      if (b.dataset.v === cs.u) return; var k = b.dataset.v === "ft" ? 1 / FTm : FTm;
      $("#csp-l").value = (+$("#csp-l").value * k).toFixed(1); $("#csp-w").value = (+$("#csp-w").value * k).toFixed(1); cs.u = b.dataset.v; setP($("#csp-u"), cs.u); cRender(); }); });
    $$("button", $("#csp-p")).forEach(function (b) { b.addEventListener("click", function () {
      var k = cs.u === "ft" ? 1 / FTm : 1; $("#csp-l").value = (+b.dataset.l * k).toFixed(2); $("#csp-w").value = (+b.dataset.w * k).toFixed(2); cRender(); }); });
    ["#csp-l", "#csp-w"].forEach(function (id) { $(id).addEventListener("input", cRender); });
    cRender();
  }

  /* ---------- pickleball score keeper ---------- */
  var pbs = $("#pbs");
  if (pbs) {
    var pz = store.get("pbs", null);
    function pNew(keep) { var o = keep || pz || {}; pz = { m: o.m || "d", y: o.y || "t", to: o.to || 11, sc: [0, 0], srv: o.first || 0, first: o.first || 0, n: (o.m || "d") === "d" && (o.y || "t") === "t" ? 2 : 1, win: -1, h: [], games: o.games || [] }; }
    if (!pz || !pz.sc) pNew({});
    function pSave() { store.set("pbs", pz); }
    function pWin(w) {
      if (pz.win >= 0) return;
      pz.h.push(JSON.stringify({ sc: pz.sc, srv: pz.srv, n: pz.n }));
      var s = pz.srv, msg = "";
      if (pz.y === "t") {
        if (w === s) { pz.sc[s]++; msg = "Point."; }
        else if (pz.m === "d" && pz.n === 1) { pz.n = 2; msg = "Second server."; }
        else { pz.srv = w; pz.n = 1; msg = "Side out."; }
      } else {
        if (w === s) { pz.sc[w]++; msg = "Point."; }
        else if (pz.sc[w] + 1 >= pz.to && pz.sc[w] + 1 - pz.sc[s] >= 2) { pz.srv = w; msg = "Side out. Game point must be won on serve."; }
        else { pz.sc[w]++; pz.srv = w; msg = "Point and side out."; }
      }
      [0, 1].forEach(function (i) { if (pz.sc[i] >= pz.to && pz.sc[i] - pz.sc[1 - i] >= 2) { pz.win = i; pz.games.push(pz.sc[0] + "-" + pz.sc[1]); } });
      pz.msg = msg; pRender(true, w);
    }
    function pRender(flash, w) {
      var s = pz.srv, call = pz.sc[s] + "-" + pz.sc[1 - s] + (pz.m === "d" && pz.y === "t" ? "-" + pz.n : "");
      $("#pbs-call").textContent = pz.win >= 0 ? (pz.win ? "Side B" : "Side A") + " wins " + pz.sc[pz.win] + "-" + pz.sc[1 - pz.win] : call;
      $$(".team", pbs).forEach(function (b, i) {
        $(".pts", b).textContent = pz.sc[i]; $(".srv", b).style.visibility = i === s && pz.win < 0 ? "visible" : "hidden";
        $(".gs", b).textContent = i === s && pz.win < 0 ? "Serving" + (pz.m === "d" && pz.y === "t" ? ": server " + pz.n : "") + ", from the " + (pz.sc[s] % 2 ? "left" : "right") : "Receiving";
        if (flash && i === w) { b.classList.remove("flash"); void b.offsetWidth; b.classList.add("flash"); }
      });
      $("#pbs-msg").textContent = pz.win >= 0 ? "Game over. Tap New game to play again." : (pz.msg || "Tap the side that wins each rally.");
      $("#pbs-games").innerHTML = pz.games.slice(-6).map(function (g, i) { return "<span>Game " + (pz.games.length - Math.min(6, pz.games.length) + i + 1) + ": " + g + "</span>"; }).join("");
      [["#pbs-m", pz.m], ["#pbs-y", pz.y], ["#pbs-g", String(pz.to)]].forEach(function (g) { $$("button", $(g[0])).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === g[1] ? "true" : "false"); }); });
      pSave();
    }
    $$(".team", pbs).forEach(function (b) { b.addEventListener("click", function () { pWin(+b.dataset.i); }); });
    $("#pbs-undo").addEventListener("click", function () {
      if (!pz.h.length) return; if (pz.win >= 0) { pz.games.pop(); pz.win = -1; }
      var o = JSON.parse(pz.h.pop()); pz.sc = o.sc; pz.srv = o.srv; pz.n = o.n; pz.msg = "Undone."; pRender();
    });
    $("#pbs-new").addEventListener("click", function () { pNew(pz); pz.msg = "New game."; pRender(); });
    $("#pbs-swap").addEventListener("click", function () { var o = pz; o.first = 1 - (o.first || 0); pNew(o); pz.msg = (pz.first ? "Side B" : "Side A") + " serves first."; pRender(); });
    [["#pbs-m", "m"], ["#pbs-y", "y"], ["#pbs-g", "to"]].forEach(function (g) {
      $$("button", $(g[0])).forEach(function (b) { b.addEventListener("click", function () { var o = pz; o[g[1]] = g[1] === "to" ? +b.dataset.v : b.dataset.v; o.games = []; pNew(o); pz.msg = "New game."; pRender(); }); });
    });
    pRender();
  }
  /* ---------- fix my padel: problem fixer (26 Nov 2026) ---------- */
  var fxw = $("#fx");
  if (fxw && window.FIX) {
    var FX = window.FIX, fst = store.get("fixp", { on: "glass", list: [] });
    if (!FX[fst.on]) fst.on = "glass";
    if (!Array.isArray(fst.list)) fst.list = [];
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var flk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + esc(t) + "</a>"; };
    var fxRender = function () {
      var x = FX[fst.on];
      $$("button", $("#fx-pick")).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === fst.on ? "true" : "false"); });
      $("#fx-h").textContent = x.q;
      $("#fx-c").innerHTML = "<strong>Likely cause:</strong> " + x.cause.map(esc).join(" Or: ");
      $("#fx-f").innerHTML = x.fix.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("");
      $("#fx-d").innerHTML = "<strong>Drill: " + esc(x.drill[0]) + ".</strong> " + esc(x.drill[1]) + " <strong>Reps: " + esc(x.drill[2]) + ".</strong>";
      $("#fx-l").innerHTML = "Read next: " + x.links.map(function (l) { return flk(l[0], l[1]); }).join(" · ");
      var inl = fst.list.indexOf(fst.on) > -1;
      $("#fx-add").textContent = inl ? "On your practice list" : "Add to my practice list";
      $("#fx-list").innerHTML = fst.list.filter(function (k) { return FX[k]; }).map(function (k) {
        var y = FX[k];
        return '<li><label><input type="checkbox" data-k="' + k + '"><span><strong>' + esc(y.drill[0]) + "</strong> (" + esc(y.drill[2]) + "): " + esc(y.fix[0]) + "</span></label></li>";
      }).join("");
      $("#fx-empty").style.display = fst.list.length ? "none" : "";
      $$("input", $("#fx-list")).forEach(function (c) { c.addEventListener("change", function () {
        if (c.checked) { fst.list = fst.list.filter(function (k) { return k !== c.dataset.k; }); store.set("fixp", fst); toast("Nice work. Removed from your list."); fxRender(); }
      }); });
      store.set("fixp", fst);
    };
    $$("button", $("#fx-pick")).forEach(function (b) { b.addEventListener("click", function () {
      fst.on = b.dataset.v; fxRender();
      if (window.innerWidth < 900) $("#fx-out").scrollIntoView({ behavior: "smooth", block: "start" });
    }); });
    $("#fx-add").addEventListener("click", function () { if (fst.list.indexOf(fst.on) < 0) { fst.list.push(fst.on); toast("Added to your practice list"); } fxRender(); });
    $("#fx-clear").addEventListener("click", function () { fst.list = []; fxRender(); });
    $("#fx-copy").addEventListener("click", function () {
      var txt = "My padel practice list (padelglassbox.com/fix-my-padel)\n" + fst.list.map(function (k) { var y = FX[k]; return "- " + y.q + " Fix: " + y.fix[0] + " Drill: " + y.drill[0] + " (" + y.drill[2] + ")"; }).join("\n");
      try { navigator.clipboard.writeText(txt).then(function () { toast("List copied"); }, function () { toast("Copy not allowed here"); }); } catch (e) { toast("Copy not allowed here"); }
    });
    fxRender();
  }

  /* ---------- which side quiz: left or right (26 Nov 2026) ---------- */
  var sdw = $("#sd");
  if (sdw) {
    var sdg = $$("[data-sd]", sdw), sst = store.get("side", {});
    var sdRender = function () {
      sdg.forEach(function (g) {
        var k = g.dataset.sd, on = $('button[aria-pressed="true"]', g);
        if (sst[k] && $('button[data-v="' + sst[k] + '"]', g)) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === sst[k] ? "true" : "false"); }); }
        else sst[k] = on ? on.dataset.v : $("button", g).dataset.v;
      });
      store.set("side", sst);
      var me = sst.hand, ph = sst.ph, why = [], role = 0;
      var midSide = me === "r" ? "left" : "right", otherSide = midSide === "left" ? "right" : "left";
      var pt = function (v, n, a, b) { if (v === "me") { role += n; why.push(a); } else if (v === "p") { role -= n; why.push(b); } };
      pt(sst.over, 2, "Your overhead is more reliable, and the middle-lob side needs it.", "Your partner's overhead is more reliable, so they should take the middle lobs.");
      pt(sst.move, 1, "You move faster sideways and backwards, which the finishing side needs.", "Your partner moves faster, which suits the finishing side.");
      if (sst.calm === "me") { role -= 1; why.push("You make fewer errors in long rallies: a strength for the building side."); }
      else if (sst.calm === "p") { role += 1; why.push("Your partner is steadier in rallies, so they suit the building side."); }
      if (sst.fh === "fh") { role += 1; why.push("Your forehand is your best shot, and on the " + midSide + " it covers the middle."); }
      else if (sst.fh === "bh") { role -= 1; why.push("Your backhand is strong: on the " + otherSide + " you hit more backhands down the line."); }
      if (sst.style === "f") { role += 1; why.push("You like to finish points."); } else if (sst.style === "b") { role -= 1; why.push("You like to build points patiently."); }
      var side, conf;
      if (ph !== "x" && ph !== me) {
        side = me === "l" ? "right" : "left";
        conf = "Clear: mixed-hand pair.";
        why.unshift(me === "l" ? "You are left-handed with a right-handed partner. On the right, your forehand and overhead cover the middle, and so do your partner's on the left." : "Your partner is left-handed. They usually play the right, so you take the left and both forehands cover the middle.");
        if (role <= -3) why.push("Your answers lean the other way, so try one set swapped, but most pairs keep this set-up.");
      } else if (role >= 2) { side = midSide; conf = role >= 4 ? "Clear lean." : "Leaning this way."; }
      else if (role <= -2) { side = otherSide; conf = role <= -4 ? "Clear lean." : "Leaning this way."; }
      else { side = "either"; conf = "Toss-up: your answers are balanced."; }
      if (ph === "x" && side !== "either" && ph !== me) conf += " With no fixed partner, ask your partner on the day which side they prefer.";
      if (me === "l" && ph === "l") why.unshift("Two left-handers: roles are mirrored, so the player with the forehand in the middle is on the right.");
      var sname = side === "left" ? "Left side (revés)" : side === "right" ? "Right side (drive)" : "Either side: play a set each way";
      var fin = side === midSide;
      $("#sd-h").textContent = sname;
      $("#sd-conf").innerHTML = "<strong>" + conf + "</strong>" + (sst.lvl === "new" ? " You are new to padel, so swap sides often for now and repeat this quiz in a few months." : "");
      $("#sd-why").innerHTML = (why.length ? why : ["Nothing in your answers points strongly either way."]).map(function (w) { return "<li>" + w + "</li>"; }).join("");
      $("#sd-job").innerHTML = side === "either" ? "<strong>How to decide:</strong> play one set with each set-up, count unforced errors, and keep the one with fewer." :
        (fin ? "<strong>Your job:</strong> finish the point. Take the middle balls on your forehand and the lobs down the middle with a bandeja, víbora or smash. Move a lot and stay ready." :
               "<strong>Your job:</strong> build the point. Keep the ball low, deep and in play, return low cross-court, and set up your partner to finish. Patience wins.");
      $("#sd-drill").innerHTML = side === "either" ? "" : (fin ? "<strong>Drill:</strong> partner feeds 15 lobs down the middle; play bandejas to the back corner. 3 sets, count the ones that land past the service line." :
        "<strong>Drill:</strong> cross-court rally at medium pace, keeping every ball below the top of the net on their side. 3 sets of 20 in a row.");
      var lk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
      $("#sd-next").innerHTML = "Next: " + (fin || side === "either" ? lk("bandeja-vs-vibora", "Bandeja vs víbora") + " · " : "") + lk("positioning", "Where to stand") + " · " + lk("fix-my-padel", "Fix my padel");
    };
    sdg.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { sst[g.dataset.sd] = b.dataset.v; sdRender(); }); }); });
    sdRender();
  }

  /* ---------- shared helpers for 26 Nov tools ---------- */
  var esc2 = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var lk2 = function (f, t) { var h = f.split("#"); return '<a href="' + (location.protocol === "file:" ? h[0] + ".html" : "/" + h[0]) + (h[1] ? "#" + h[1] : "") + '" style="color:#e8f84a">' + esc2(t) + "</a>"; };
  var copyTxt = function (txt, ok) { try { navigator.clipboard.writeText(txt).then(function () { toast(ok); }, function () { toast("Copy not allowed here"); }); } catch (e) { toast("Copy not allowed here"); } };

  /* ---------- padel match tracker (26 Nov 2026) ---------- */
  var mtw = $("#mt");
  if (mtw && window.MTRK) {
    var MK = window.MTRK, MDR = {}, mst = store.get("mtrk", { who: "me", log: [], hist: [] });
    (window.MTDR || []).forEach(function (d) { MDR[d.id] = d; });
    if (!Array.isArray(mst.log)) mst.log = [];
    if (!Array.isArray(mst.hist)) mst.hist = [];
    var SN = {}; MK.shots.forEach(function (s) { SN[s[0]] = s[1]; });
    var mtCount = function (log) {
      var c = { w: 0, e: 0, ow: 0, oe: 0, by: {}, me: { w: 0, e: 0 }, pa: { w: 0, e: 0 } };
      MK.shots.forEach(function (s) { c.by[s[0]] = { w: 0, e: 0 }; });
      log.forEach(function (x) {
        if (x.t === "ow" || x.t === "oe") { c[x.t]++; return; }
        if (!c.by[x.s]) return;
        c.by[x.s][x.t]++; c[x.t]++; c[x.p === "pa" ? "pa" : "me"][x.t]++;
      });
      c.won = c.w + c.oe; c.lost = c.e + c.ow;
      var worst = null;
      MK.shots.forEach(function (s) { var b = c.by[s[0]]; if (b.e > 0 && (!worst || b.e > c.by[worst].e || (b.e === c.by[worst].e && b.w < c.by[worst].w))) worst = s[0]; });
      c.worst = worst;
      var best = null;
      MK.shots.forEach(function (s) { var b = c.by[s[0]]; if (b.w > 0 && (!best || b.w - b.e > c.by[best].w - c.by[best].e)) best = s[0]; });
      c.best = best;
      return c;
    };
    var mtRender = function () {
      $$("button", $("#mt-who")).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === mst.who ? "true" : "false"); });
      var c = mtCount(mst.log), tot = c.won + c.lost;
      MK.shots.forEach(function (s) { var el = $("#mt-c-" + s[0]); if (el) el.textContent = c.by[s[0]].w + " / " + c.by[s[0]].e; });
      $("#mt-pts").innerHTML = "<strong>Points logged: " + tot + "</strong> · won " + c.won + ", lost " + c.lost;
      $("#mt-sum").innerHTML = tot ? "Our winners " + c.w + " (me " + c.me.w + ", partner " + c.pa.w + ") · our errors " + c.e + " (me " + c.me.e + ", partner " + c.pa.e + ") · their winners " + c.ow + " · their errors " + c.oe + "." : "Tap a button on the left when a point ends.";
      var mx = 1; MK.shots.forEach(function (s) { var b = c.by[s[0]]; mx = Math.max(mx, b.w, b.e); });
      $("#mt-bars").innerHTML = tot ? MK.shots.filter(function (s) { var b = c.by[s[0]]; return b.w || b.e; }).map(function (s) {
        var b = c.by[s[0]];
        return '<div class="mt-bar"><span>' + esc2(s[1]) + '</span><i class="w" style="width:' + (b.w / mx * 45) + '%"></i><i class="e" style="width:' + (b.e / mx * 45) + '%"></i><b>' + b.w + " / " + b.e + "</b></div>";
      }).join("") : "";
      if (c.worst) {
        var f = MK.fix[c.worst], d = MDR[MK.drill[c.worst]];
        $("#mt-h").textContent = "Biggest leak: " + SN[c.worst];
        $("#mt-tip").innerHTML = "<strong>" + c.by[c.worst].e + " errors on the " + esc2(SN[c.worst].toLowerCase()) + ".</strong>" + (c.e && tot ? " Your errors gave away " + Math.round(c.e / tot * 100) + "% of all points." : "") + (d ? " <strong>Drill:</strong> " + esc2(d.n) + ". " + esc2(d.d) : "") + (c.best ? " Best shot so far: " + esc2(SN[c.best].toLowerCase()) + "." : "");
        $("#mt-next").innerHTML = "Fix it: " + lk2(f[0], f[1]) + " · " + lk2("padel-training-plan", "4-week training plan") + " · " + lk2("drills", "Drills planner");
      } else {
        $("#mt-h").textContent = "This match";
        $("#mt-tip").innerHTML = c.w ? "No errors logged yet. Nice." : "";
        $("#mt-next").innerHTML = "Next: " + lk2("score", "Score keeper") + " · " + lk2("fix-my-padel", "Fix my padel");
      }
      var h = mst.hist.slice(-10).reverse();
      $("#mt-hempty").style.display = h.length ? "none" : "";
      $("#mt-hist").innerHTML = h.length ? '<div style="overflow-x:auto"><table class="mt"><thead><tr><th scope="col">Date</th><th scope="col">Points won / lost</th><th scope="col">Our winners</th><th scope="col">Our errors</th><th scope="col">Biggest leak</th></tr></thead><tbody>' + h.map(function (m) {
        return "<tr><td>" + esc2(m.d) + "</td><td>" + m.won + " / " + m.lost + "</td><td>" + m.w + "</td><td>" + m.e + "</td><td>" + esc2(m.worst ? SN[m.worst] || "-" : "-") + "</td></tr>";
      }).join("") + "</tbody></table></div>" : "";
      if (mst.hist.length >= 2) {
        var a = mst.hist[mst.hist.length - 2], z = mst.hist[mst.hist.length - 1];
        var ra = a.won + a.lost ? a.e / (a.won + a.lost) : 0, rz = z.won + z.lost ? z.e / (z.won + z.lost) : 0;
        $("#mt-trend").textContent = "Trend: your errors were " + Math.round(rz * 100) + "% of points in the last match, " + (rz < ra ? "down" : rz > ra ? "up" : "same as") + " from " + Math.round(ra * 100) + "% the match before.";
      } else $("#mt-trend").textContent = "";
      store.set("mtrk", mst);
    };
    $$("button", $("#mt-who")).forEach(function (b) { b.addEventListener("click", function () { mst.who = b.dataset.v; mtRender(); }); });
    $$("button[data-s]", $("#mt-grid")).forEach(function (b) { b.addEventListener("click", function () {
      mst.log.push({ s: b.dataset.s, t: b.dataset.t, p: mst.who }); mtRender();
      toast((b.dataset.t === "w" ? "Winner: " : "Error: ") + SN[b.dataset.s] + (mst.who === "pa" ? " (partner)" : ""));
    }); });
    $("#mt-oe").addEventListener("click", function () { mst.log.push({ t: "oe" }); mtRender(); toast("Their error: our point"); });
    $("#mt-ow").addEventListener("click", function () { mst.log.push({ t: "ow" }); mtRender(); toast("Their winner: their point"); });
    $("#mt-undo").addEventListener("click", function () { if (mst.log.length) { mst.log.pop(); toast("Last point removed"); } mtRender(); });
    $("#mt-reset").addEventListener("click", function () { if (!mst.log.length || window.confirm("Clear the points logged for this match?")) { mst.log = []; mtRender(); } });
    $("#mt-save").addEventListener("click", function () {
      if (!mst.log.length) { toast("Log some points first"); return; }
      var c = mtCount(mst.log), dt = new Date();
      mst.hist.push({ d: dt.toISOString().slice(0, 10), won: c.won, lost: c.lost, w: c.w, e: c.e, worst: c.worst });
      if (mst.hist.length > 50) mst.hist = mst.hist.slice(-50);
      mst.log = []; mtRender(); toast("Match saved");
    });
    $("#mt-copy").addEventListener("click", function () {
      var c = mtCount(mst.log);
      var lines = ["My padel match stats (padelglassbox.com/padel-match-tracker)", "Points won " + c.won + ", lost " + c.lost, "Our winners " + c.w + ", our errors " + c.e + ", their winners " + c.ow + ", their errors " + c.oe];
      MK.shots.forEach(function (s) { var b = c.by[s[0]]; if (b.w || b.e) lines.push("- " + s[1] + ": " + b.w + " winners, " + b.e + " errors"); });
      if (c.worst) lines.push("Biggest leak: " + SN[c.worst]);
      copyTxt(lines.join("\n"), "Summary copied");
    });
    mtRender();
  }

  /* ---------- padel training plan generator (26 Nov 2026) ---------- */
  var tpw = $("#tp");
  if (tpw && window.TPDR) {
    var TD = window.TPDR, tpg = $$("[data-tp]", tpw), tst = store.get("tplan", {}), tpText = "";
    var GN = { cons: "fewer errors", net: "winning at the net", wall: "playing off the glass", over: "lobs and overheads", serve: "serve and return", game: "winning more matches" };
    var SEC = { cons: "net", net: "over", wall: "cons", over: "net", serve: "cons", game: "cons" };
    var WK = [["Learn", "slow, easy feeds; get the movement right"], ["Repeat", "same drills, now count your streak or targets and write it down"], ["Pressure", "faster feeds, start each ball on the move, or points that count"], ["Test", "shorter drills, more games; log a match with the tracker"]];
    var r5 = function (x) { return Math.max(5, Math.round(x / 5) * 5); };
    var pick = function (tag, who, skip) {
      var l = TD.filter(function (d) { return d.f.indexOf(tag) > -1 && d.who.indexOf(who) > -1 && skip.indexOf(d.id) < 0; });
      if (!l.length) l = TD.filter(function (d) { return d.who.indexOf(who) > -1 && skip.indexOf(d.id) < 0; });
      return l[0];
    };
    var tpRender = function () {
      tpg.forEach(function (g) {
        var k = g.dataset.tp;
        if (!tst[k] || !$('button[data-v="' + tst[k] + '"]', g)) { var on = $('button[aria-pressed="true"]', g); tst[k] = on ? on.dataset.v : $("button", g).dataset.v; }
        $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === tst[k] ? "true" : "false"); });
      });
      store.set("tplan", tst);
      var lvl = tst.lvl, days = +tst.days, len = +tst.len, who = +tst.who, goal = tst.goal;
      var main = goal === "game" ? "cons" : goal, sec = SEC[goal];
      var d1 = pick(main, who, []), d2 = pick(main, who, [d1 && d1.id]) , d3 = pick(sec, who, [d1 && d1.id, d2 && d2.id]);
      var gameD = TD.filter(function (d) { return d.id === "cards"; })[0];
      var canGame = who > 1;
      var core = len - 15;
      var sessions = [];
      var techn = function (wk) {
        var gm = canGame ? r5(core * (wk === 3 ? 0.5 : lvl === "new" ? 0.4 : 0.3)) : 0, rest = core - gm;
        var b = [["Warm-up", 10, "Joints, short sprints, then easy rallies (warm-up timer)."], [d1.n, r5(rest * 0.55), d1.d], [d2 && d2.id !== d1.id ? d2.n : d1.n + " (again, harder)", rest - r5(rest * 0.55), d2 ? d2.d : d1.d]];
        if (gm) b.push([goal === "game" ? "Yellow card, red card games" : "Games: points from your goal count double", gm, gameD ? gameD.d : "Play normal games."]);
        b.push(["Cool-down", 5, "Walk, easy stretches, water."]);
        return { t: "Drill session: " + GN[goal], b: b };
      };
      var mixed = function (wk) {
        var gm = canGame ? r5(core * 0.45) : 0, rest = core - gm;
        var b = [["Warm-up", 10, "Joints, short sprints, then easy rallies."], [d3 ? d3.n : d1.n, r5(rest * 0.5), d3 ? d3.d : d1.d], [d1.n, rest - r5(rest * 0.5), d1.d]];
        if (gm) b.push(["Games", gm, "Play games or a short set. Focus on your goal."]);
        b.push(["Cool-down", 5, "Walk, easy stretches, water."]);
        return { t: canGame ? "Mixed session" : "Second skill session", b: b };
      };
      var match = function (wk) {
        if (!canGame) return { t: "Solo session: footwork and control", b: [["Warm-up", 10, "Joints and short sprints."], ["Footwork and split step", r5(core * 0.4), (TD.filter(function (d) { return d.id === "feet"; })[0] || {}).d || ""], [d1.n, core - r5(core * 0.4), d1.d], ["Cool-down", 5, "Walk, easy stretches, water."]] };
        return { t: "Match session", b: [["Warm-up", 10, "Easy rallies, volleys, a few lobs and serves. No smashing at the other pair."], ["Match play", core, wk === 3 ? "Play a full match and log it with the match tracker. Compare your errors with week 1." : "Play sets. After each set, ask: did I use what I practised?"], ["Cool-down", 5, "Walk, easy stretches, water."]] };
      };
      var plan = [];
      for (var wk = 0; wk < 4; wk++) {
        var s = [];
        if (days === 1) s = [mixed(wk)];
        else if (days === 2) s = [techn(wk), wk === 3 ? match(wk) : (lvl === "new" ? mixed(wk) : match(wk))];
        else if (days === 3) s = [techn(wk), wk === 3 ? mixed(wk) : techn(wk), match(wk)];
        else s = [techn(wk), mixed(wk), wk === 3 ? match(wk) : techn(wk), match(wk)];
        plan.push(s);
      }
      var dayName = { 1: ["Day 1"], 2: ["Day 1", "Day 3 or 4"], 3: ["Day 1", "Day 3", "Day 5"], 4: ["Day 1", "Day 2", "Day 4", "Day 6"] }[days];
      var lvTxt = { new: "Keep feeds slow and easy, and stop a drill while it still feels good.", imp: "Count every drill so you can see progress.", club: "Feed faster from week 2 and make your partner move you.", adv: "From week 3, start every drill ball on the move and add targets." }[lvl];
      $("#tp-h").textContent = "4 weeks: " + GN[goal];
      $("#tp-sum").innerHTML = "<strong>" + days + " session" + (days > 1 ? "s" : "") + " a week, " + len + " minutes each.</strong> " + lvTxt + (days >= 3 ? " Rest at least one day between drill days." : "") + (who === 1 ? " Training alone: book a match with friends when you can, to test what you practise." : "");
      $("#tp-wk").innerHTML = WK.map(function (w, i) { return "<li><strong>Week " + (i + 1) + ", " + w[0].toLowerCase() + ":</strong> " + w[1] + ".</li>"; }).join("");
      var txt = ["My 4-week padel training plan (padelglassbox.com/padel-training-plan)", "Goal: " + GN[goal] + " · " + days + " x " + len + " min a week"];
      var html = "";
      plan.forEach(function (s, wi) {
        txt.push("", "WEEK " + (wi + 1) + " (" + WK[wi][0] + ": " + WK[wi][1] + ")");
        html += '<div class="card tp-week"><h2 style="font-size:1.25rem;margin-top:0">Week ' + (wi + 1) + ": " + WK[wi][0] + '</h2><p class="muted" style="margin-top:0">' + esc2(WK[wi][1]) + '.</p><div class="tp-days">';
        s.forEach(function (ss, di) {
          txt.push(dayName[di] + " - " + ss.t);
          html += '<div class="tp-day"><h3>' + esc2(dayName[di]) + ": " + esc2(ss.t) + '</h3><table class="tp-t"><tbody>' + ss.b.map(function (b) {
            txt.push("  " + b[1] + " min  " + b[0]);
            return '<tr><td class="num"><b>' + b[1] + " min</b></td><td><strong>" + esc2(b[0]) + "</strong><br><span class=\"muted\">" + esc2(b[2]) + "</span></td></tr>";
          }).join("") + "</tbody></table></div>";
        });
        html += "</div></div>";
      });
      html += '<p class="muted">Want a timer? Run any session block by block in the ' + lk2("drills", "drills planner").replace(' style="color:#e8f84a"', "") + ". Log your week 4 match with the " + lk2("padel-match-tracker", "match tracker").replace(' style="color:#e8f84a"', "") + ".</p>";
      $("#tp-plan").innerHTML = html;
      tpText = txt.join("\n");
    };
    tpg.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { tst[g.dataset.tp] = b.dataset.v; tpRender(); }); }); });
    $("#tp-copy").addEventListener("click", function () { copyTxt(tpText, "Plan copied"); });
    $("#tp-print").addEventListener("click", function () { document.body.classList.add("print-tp"); window.print(); setTimeout(function () { document.body.classList.remove("print-tp"); }, 500); });
    tpRender();
  }

  /* ---------- padel etiquette quiz (26 Nov 2026) ---------- */
  var etw = $("#et");
  if (etw && window.ETQ) {
    var EQ = window.ETQ, est = store.get("etq", {});
    var etRender = function () {
      var n = 0, right = 0;
      $("#et-q").innerHTML = EQ.map(function (q, i) {
        var a = est[i], done = a !== undefined && q.o[a];
        if (done) { n++; if (q.o[a][1]) right++; }
        return '<div class="q"><h3>' + (i + 1) + ". " + esc2(q.q) + '</h3><div class="opts" role="group" aria-label="Situation ' + (i + 1) + '">' + q.o.map(function (o, j) {
          return '<button type="button" class="opt" data-q="' + i + '" data-v="' + j + '" aria-pressed="' + (a === j ? "true" : "false") + '">' + esc2(o[0]) + "</button>";
        }).join("") + "</div>" + (done ? '<p class="et-fb ' + (q.o[a][1] ? "ok" : "no") + '">' + (q.o[a][1] ? "Good call. " : "Not quite. ") + esc2(q.w) + "</p>" : "") + "</div>";
      }).join("");
      $$("button[data-q]", $("#et-q")).forEach(function (b) { b.addEventListener("click", function () { est[b.dataset.q] = +b.dataset.v; etRender(); }); });
      $("#et-s").innerHTML = "<strong>" + right + " of " + EQ.length + "</strong> right" + (n < EQ.length ? " · " + (EQ.length - n) + " left to answer" : "");
      $("#et-m").textContent = n < EQ.length ? "Answer all ten to get your verdict." : right === EQ.length ? "Perfect. Everyone wants to play with you." : right >= 8 ? "Great court manners. Check the ones you missed below." : right >= 5 ? "Not bad. Read the checklist below before your next game." : "Read the checklist below before your next game. Your partners will thank you.";
      store.set("etq", est);
    };
    $("#et-reset").addEventListener("click", function () { est = {}; etRender(); });
    etRender();
  }

  /* ---------- serve practice tracker (26 Nov 2026) ---------- */
  var svw = $("#sv");
  if (svw && window.SERVE) {
    var SV = window.SERVE, svCur = store.get("svcur", []), svHist = store.get("svhist", []), svT = "wide";
    var svStats = function (arr) {
      var o = { n: arr.length, inn: 0, hit: 0, by: {}, f: {} };
      arr.forEach(function (x) {
        var c = SV.r[x.r][1];
        o.by[x.t] = o.by[x.t] || { n: 0, hit: 0, inn: 0 };
        o.by[x.t].n++;
        if (c === "in") { o.inn++; o.by[x.t].inn++; }
        if (x.r === "hit") { o.hit++; o.by[x.t].hit++; }
        if (c === "f") o.f[x.r] = (o.f[x.r] || 0) + 1;
      });
      return o;
    };
    var pct = function (a, b) { return b ? Math.round(a * 100 / b) : 0; };
    var svText = "";
    var svRender = function () {
      var st = svStats(svCur);
      $("#sv-sum").innerHTML = st.n ? "<strong>" + st.n + "</strong> serve" + (st.n === 1 ? "" : "s") + " · <strong>" + pct(st.inn, st.n) + "%</strong> in · <strong>" + pct(st.hit, st.n) + "%</strong> on target" : "No serves yet. Pick a target and tap what happened.";
      $("#sv-bars").innerHTML = Object.keys(SV.t).map(function (k) {
        var b = st.by[k] || { n: 0, hit: 0, inn: 0 };
        return '<div class="mt-bar"><span>' + esc2(SV.t[k].split(" (")[0]) + '</span><span><i class="w" style="width:' + pct(b.hit, b.n) + '%"></i></span><b>' + (b.n ? pct(b.inn, b.n) + "% in" : "-") + "</b></div>";
      }).join("") + (st.n ? '<p class="muted" style="color:#9fb0e0;font-size:.85rem;margin:6px 0 0">Bar = share on target. Right = share in the box.</p>' : "");
      var worst = null; Object.keys(st.f).forEach(function (k) { if (!worst || st.f[k] > st.f[worst]) worst = k; });
      var tip;
      if (st.n < 5) tip = "Log at least 10 serves for a useful tip.";
      else if (worst && st.f[worst] >= 2) tip = SV.tip[worst];
      else if (pct(st.inn, st.n) >= 80) tip = "8 in 10 or better: well done. Now aim for the target more often, or add slice.";
      else tip = "Slow down a little: aim to get 8 in 10 serves in before you add pace or spin.";
      $("#sv-tip").textContent = tip;
      var h = $("#sv-hist");
      h.innerHTML = svHist.length ? '<table class="tp-t"><tbody>' + svHist.slice(-10).reverse().map(function (x) { return "<tr><td>" + esc2(x.d) + "</td><td>" + x.n + " serves</td><td>" + x.i + "% in</td><td>" + x.h + "% on target</td></tr>"; }).join("") + "</tbody></table>" : "";
      $("#sv-hempty").hidden = svHist.length > 0;
      svText = "Padel serve practice: " + st.n + " serves, " + pct(st.inn, st.n) + "% in, " + pct(st.hit, st.n) + "% on target. " + tip;
      store.set("svcur", svCur); store.set("svhist", svHist);
    };
    $$("button", $("#sv-tgt")).forEach(function (b) { b.addEventListener("click", function () { svT = b.dataset.v; $$("button", $("#sv-tgt")).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); }); });
    $$("button[data-r]", $("#sv-res")).forEach(function (b) { b.addEventListener("click", function () { svCur.push({ t: svT, r: b.dataset.r }); svRender(); }); });
    $("#sv-undo").addEventListener("click", function () { svCur.pop(); svRender(); });
    $("#sv-reset").addEventListener("click", function () { svCur = []; svRender(); });
    $("#sv-save").addEventListener("click", function () {
      var st = svStats(svCur); if (!st.n) { toast("Log some serves first"); return; }
      svHist.push({ d: new Date().toLocaleDateString(), n: st.n, i: pct(st.inn, st.n), h: pct(st.hit, st.n) });
      svCur = []; svRender(); toast("Session saved");
    });
    $("#sv-copy").addEventListener("click", function () { copyTxt(svText, "Summary copied"); });
    svRender();
  }

  /* ---------- padel tactics trainer (26 Nov 2026) ---------- */
  var tcw = $("#tc");
  if (tcw && window.TACQ) {
    var TQ = window.TACQ, tst = store.get("tacq", {});
    var tcRender = function () {
      var n = 0, right = 0;
      $("#tc-q").innerHTML = TQ.map(function (q, i) {
        var a = tst[i], done = a !== undefined && q.o[a];
        if (done) { n++; if (q.o[a][1]) right++; }
        return '<div class="q tc-item"><div class="tc-row">' + q.svg + '<div><h3>' + (i + 1) + ". " + esc2(q.t) + '</h3><p class="muted" style="margin:0 0 10px">' + esc2(q.s) + '</p><div class="opts" role="group" aria-label="Scenario ' + (i + 1) + '">' + q.o.map(function (o, j) {
          return '<button type="button" class="opt" data-q="' + i + '" data-v="' + j + '" aria-pressed="' + (a === j ? "true" : "false") + '">' + esc2(o[0]) + "</button>";
        }).join("") + "</div>" + (done ? '<p class="et-fb ' + (q.o[a][1] ? "ok" : "no") + '">' + (q.o[a][1] ? "Good choice. " : "Not the best option. ") + esc2(q.w) + "</p>" : "") + "</div></div></div>";
      }).join("");
      $$("button[data-q]", $("#tc-q")).forEach(function (b) { b.addEventListener("click", function () { tst[b.dataset.q] = +b.dataset.v; tcRender(); }); });
      $("#tc-s").innerHTML = "<strong>" + right + " of " + TQ.length + "</strong> best choices" + (n < TQ.length ? " · " + (TQ.length - n) + " left" : "");
      $("#tc-m").textContent = n < TQ.length ? "Answer all ten to get your verdict." : right >= 9 ? "Excellent padel brain. Now make it happen on court." : right >= 6 ? "Good tactical sense. Read the rules below for the ones you missed." : "Read the tactics table and rules below, then try again.";
      store.set("tacq", tst);
    };
    $("#tc-reset").addEventListener("click", function () { tst = {}; tcRender(); });
    tcRender();
  }

  /* ---------- improvement guide level picker (26 Nov 2026) ---------- */
  var igp = $("#ig-pick");
  if (igp) {
    var igSet = function (v) {
      $$("button", igp).forEach(function (x) { x.setAttribute("aria-pressed", x.dataset.v === v ? "true" : "false"); });
      $$(".ig-p").forEach(function (p) { p.hidden = p.dataset.lv !== v; });
      store.set("iglv", v);
    };
    $$("button", igp).forEach(function (b) { b.addEventListener("click", function () { igSet(b.dataset.v); }); });
    var igv = store.get("iglv", ""); if (igv) igSet(igv);
  }
  /* ---------- padel cost calculator ---------- */
  var pcb = $("#pc");
  if (pcb && window.PCDEF) {
    var pgr = $$("[data-pc]", pcb);
    var PK = ["court", "n", "rent", "can", "racket", "shoes", "lesson", "mem", "disc"];
    var pin = {}; PK.forEach(function (k) { pin[k] = $("#pc-" + k); }); pin.life = $("#pc-life");
    var pst = store.get("pp-pc", null);
    var load = function (reg) { var d = window.PCDEF[reg]; var o = { reg: reg, len: "60", wk: "4", life: "12", n: 4 }; PK.forEach(function (k) { if (k !== "n") o[k] = d[k]; }); return o; };
    if (!pst || !window.PCDEF[pst.reg]) pst = load("uk");
    PK.forEach(function (k) { pin[k].value = pst[k]; }); pin.life.value = pst.life;
    var pl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var pg = function (k, t) { return '<a href="' + window.PCGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var pm = function (v) { var c = window.PCDEF[pst.reg].cur; v = Math.round(v * 100) / 100; return c + (v >= 100 ? Math.round(v).toLocaleString("en-GB") : v.toFixed(2).replace(/\.00$/, "")); };
    var prender = function () {
      PK.forEach(function (k) { pst[k] = Math.max(0, +pin[k].value || 0); });
      pst.n = Math.max(1, Math.min(8, Math.round(pst.n || 1))); pst.disc = Math.min(100, pst.disc); pst.life = pin.life.value;
      store.set("pp-pc", pst);
      pgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === pst[g.dataset.pc] ? "true" : "false"); }); });
      var per = +pst.wk, n = pst.n, life = +pst.life;
      var courtEach = pst.court / n, courtMem = courtEach * (1 - pst.disc / 100);
      var balls = pst.can / 4 / n;
      var session = (pst.mem ? courtMem : courtEach) + pst.rent + balls;
      var kitM = (pst.racket + pst.shoes) / life;
      var month = session * per + pst.lesson + pst.mem + kitM;
      var play = session * per;
      $("#pc-h").textContent = pm(session) + " a game";
      $("#pc-p").textContent = "Your share of a " + pst.len + "-minute booking split " + n + " way" + (n === 1 ? "" : "s") + ", playing " + per + " times a month.";
      $("#pc-spec").innerHTML = "<dt>Per month</dt><dd>" + pm(month) + "</dd><dt>Per year</dt><dd>" + pm(month * 12) + "</dd><dt>First kit</dt><dd>" + pm(pst.racket + pst.shoes) + " up front" + (pst.racket + pst.shoes ? ", spread over " + (life / 12 === 1 ? "1 year" : life / 12 + " years") : "") + "</dd><dt>Per hour each</dt><dd>" + pm(session * 60 / +pst.len) + "</dd>";
      var parts = [["Court", (pst.mem ? courtMem : courtEach) * per], ["Racket hire", pst.rent * per], ["Balls", balls * per], ["Kit", kitM], ["Lessons", pst.lesson], ["Membership", pst.mem]];
      var mx = Math.max.apply(null, parts.map(function (x) { return x[1]; })) || 1;
      $("#pc-bars").innerHTML = parts.filter(function (x) { return x[1] > 0; }).map(function (x) { return '<div class="pc-row"><span>' + x[0] + '</span><div class="pc-bar"><i style="width:' + Math.max(3, x[1] / mx * 100) + '%"></i></div><b>' + pm(x[1]) + "</b></div>"; }).join("") + '<p class="muted" style="color:#9fb0e0;margin:6px 0 0;font-size:.85rem">Monthly cost by item</p>';
      var mt;
      if (pst.mem && pst.disc) {
        var save = (courtEach - courtMem) * per, be = (courtEach - courtMem) > 0 ? Math.ceil(pst.mem / (courtEach - courtMem)) : 0;
        mt = "Membership check: you save " + pm(save) + " a month on courts for a " + pm(pst.mem) + " fee. It pays off at " + be + " games a month" + (per >= be ? " - you play enough." : " - you play " + per + ", so it costs you " + pm(pst.mem - save) + " more than paying per game.");
      } else if (pst.mem) mt = "Add the member discount on court hire to see if the membership pays.";
      else mt = "Thinking of a membership? Enter its monthly fee and the member discount to see how many games a month it needs.";
      $("#pc-memo").textContent = mt;
      var tip;
      if (n < 4) tip = "Tip: fill the court. With 4 players your share would be " + pm(pst.court / 4) + " instead of " + pm(courtEach) + ".";
      else if (pst.rent && per >= 4) tip = "Tip: you hire a racket " + per + " times a month (" + pm(pst.rent * per) + "). A beginner racket would pay for itself in about " + Math.max(1, Math.round((window.PCDEF[pst.reg].racket || pst.rent * 10) / (pst.rent * per))) + " months.";
      else if (pst.court / n * 60 / +pst.len > (pst.reg === "us" ? 15 : pst.reg === "uk" ? 20 : pst.reg === "qa" ? 75 : 999)) tip = "Tip: your court share is above the published typical range. Try off-peak slots or another club.";
      else tip = "Tip: off-peak slots are usually the cheapest way to play more.";
      $("#pc-tip").textContent = tip;
      $("#pc-next").innerHTML = "Next: " + pl("padel-lessons", "lesson prices") + " · " + pl("padel-beginner-plan", "30-day beginner plan") + " · Shop: " + pg("padel-round-rackets", "round rackets");
    };
    pgr.forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () {
      if (g.dataset.pc === "reg") { var keep = { len: pst.len, wk: pst.wk, life: pst.life, n: pst.n }; pst = load(b.dataset.v); pst.len = keep.len; pst.wk = keep.wk; pst.life = keep.life; pst.n = keep.n; PK.forEach(function (k) { pin[k].value = pst[k]; }); pin.life.value = pst.life; }
      else pst[g.dataset.pc] = b.dataset.v;
      prender(); }); }); });
    PK.concat(["life"]).forEach(function (k) { pin[k].addEventListener("input", prender); pin[k].addEventListener("change", prender); });
    prender();
  }

  /* ---------- 30-day beginner plan ---------- */
  var bpb = $("#bp");
  if (bpb) {
    var days = $$(".bp-day", bpb), bdone = store.get("pp-bp", {}), bfil = "all";
    var bupd = function () {
      var n = 0, next = null;
      days.forEach(function (li) {
        var d = li.dataset.day, on = !!bdone[d]; li.querySelector("input").checked = on; li.classList.toggle("done", on);
        if (on) n++; else if (!next) next = li;
        li.hidden = bfil === "all" ? false : bfil === "todo" ? on : li.dataset.kind !== bfil && !(bfil === "home" && li.dataset.kind === "rest");
        li.classList.remove("next");
      });
      if (next) next.classList.add("next");
      $("#bp-bar").style.width = (n / days.length * 100) + "%";
      $("#bp-count").textContent = n + " of " + days.length + " days done";
      $("#bp-today").textContent = next ? "Next up: " + next.querySelector("b").textContent + "." : "All 30 days done. Well played! Make a plan for month two below.";
      store.set("pp-bp", bdone);
    };
    days.forEach(function (li) { li.querySelector("input").addEventListener("change", function (ev) { bdone[li.dataset.day] = ev.target.checked; bupd(); }); });
    $("#bp-next").addEventListener("click", function () { var x = $(".bp-day.next", bpb); if (x) { if (x.hidden) { bfil = "all"; $$("#bp-filter button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === "all" ? "true" : "false"); }); bupd(); } x.scrollIntoView({ behavior: "smooth", block: "center" }); } });
    $("#bp-reset").addEventListener("click", function () { if (window.confirm("Clear all your ticks and start the plan again?")) { bdone = {}; bupd(); toast("Plan reset"); } });
    choose($("#bp-filter"), function (v) { bfil = v; bupd(); });
    bupd();
  }

  /* ---------- knockout bracket generator ---------- */
  var kob = $("#ko");
  if (kob) {
    var kst = store.get("pp-ko", null), kopt = { seed: "seed", fmt: "30" };
    var kn = $("#ko-names"), kcount = function () { var n = kn.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean).length; $("#ko-count").textContent = n ? n + " pair" + (n === 1 ? "" : "s") : ""; };
    kn.addEventListener("input", kcount);
    $$("[data-ko]", kob).forEach(function (g) { choose(g, function (v) { kopt[g.dataset.ko] = v; }); });
    var kl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var order = function (size) { var s = [1, 2]; while (s.length < size) { var m = s.length * 2 + 1, nx = []; s.forEach(function (x) { nx.push(x, m - x); }); s = nx; } return s; };
    var esc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var rname = function (r, R) { var left = R - r; return left === 0 ? "Final" : left === 1 ? "Semi-finals" : left === 2 ? "Quarter-finals" : "Round " + (r + 1); };
    // resolve: build each round's slots from round-1 + winners; auto-advance byes
    var resolve = function () {
      var R = kst.rounds.length, rows = [];
      var cur = kst.first.slice();
      for (var r = 0; r < R; r++) {
        var ms = [], nxt = [];
        for (var i = 0; i < cur.length; i += 2) {
          var a = cur[i], b = cur[i + 1], w = kst.win[r + "-" + (i / 2)];
          if (a === -1 && b === -1) w = undefined;
          else if (a === -1 && b !== null) w = 1;
          else if (b === -1 && a !== null) w = 0;
          else if (a === null || b === null) w = undefined;
          ms.push({ a: a, b: b, w: w, bye: a === -1 || b === -1 });
          nxt.push(w === 0 ? a : w === 1 ? b : (a === -1 && b === -1 ? -1 : null));
        }
        rows.push(ms); cur = nxt;
      }
      return rows;
    };
    var kslots = function (rows) { var t = 0, per = []; rows.forEach(function (ms) { var real = ms.filter(function (m) { return !m.bye; }).length; per.push(real); t += Math.ceil(real / kst.courts); }); return { slots: t, per: per }; };
    var krender = function () {
      var rows = resolve(), R = rows.length, N = kst.names.length;
      var html = rows.map(function (ms, r) {
        return '<div class="ko-col"><h3>' + rname(r, R - 1) + '</h3><div class="ko-ms">' + ms.map(function (m, i) {
          var team = function (x, side) {
            if (x === -1) return '<span class="ko-t bye">Bye</span>';
            if (x === null) return '<span class="ko-t tbd">Winner of ' + (r ? rname(r - 1, R - 1).replace(/s$/, "") + " " + (i * 2 + side + 1) : "") + "</span>";
            var on = m.w === side, can = !m.bye && m.a !== null && m.b !== null;
            return '<button type="button" class="ko-t' + (on ? " win" : m.w === 1 - side ? " out" : "") + '"' + (can ? "" : " disabled") + ' data-r="' + r + '" data-i="' + i + '" data-s="' + side + '"><i>' + (kst.seeded ? (x + 1) : "") + "</i>" + esc(kst.names[x]) + "</button>";
          };
          return '<div class="ko-m' + (m.bye ? " is-bye" : "") + '">' + team(m.a, 0) + team(m.b, 1) + "</div>";
        }).join("") + "</div></div>";
      }).join("");
      var fin = rows[R - 1][0], champ = fin.w === 0 ? fin.a : fin.w === 1 ? fin.b : null;
      var third = "";
      if (kst.third && R >= 2) {
        var sf = rows[R - 2], losers = sf.map(function (m) { return m.w === 0 ? m.b : m.w === 1 ? m.a : null; });
        var tw = kst.win["3rd"], ok = losers[0] !== null && losers[1] !== null && losers[0] !== -1 && losers[1] !== -1;
        third = '<div class="ko-col"><h3>3rd place</h3><div class="ko-ms"><div class="ko-m">' + [0, 1].map(function (s) { var x = losers[s]; if (x === null || x === -1) return '<span class="ko-t tbd">Semi-final loser</span>'; return '<button type="button" class="ko-t' + (tw === s ? " win" : tw === 1 - s ? " out" : "") + '"' + (ok ? "" : " disabled") + ' data-third="' + s + '"><i>' + (kst.seeded ? x + 1 : "") + "</i>" + esc(kst.names[x]) + "</button>"; }).join("") + "</div></div></div>";
      }
      html += third + '<div class="ko-col ko-champ"><h3>Champions</h3><div class="ko-ms"><div class="ko-m"><span class="ko-t' + (champ !== null ? " win" : " tbd") + '">' + (champ !== null ? esc(kst.names[champ]) : "To be decided") + "</span></div></div></div>";
      $("#ko-bk").innerHTML = html;
      $$(".ko-t[data-r]", kob).forEach(function (b) { b.addEventListener("click", function () {
        var r = +b.dataset.r, i = +b.dataset.i, s = +b.dataset.s, k = r + "-" + i;
        if (kst.win[k] === s) delete kst.win[k]; else kst.win[k] = s;
        // clear later results that may now be invalid
        for (var rr = r + 1; rr < R; rr++) { var ii = Math.floor(i / Math.pow(2, rr - r)); delete kst.win[rr + "-" + ii]; }
        if (r >= R - 2) delete kst.win["3rd"];
        store.set("pp-ko", kst); krender(); }); });
      $$(".ko-t[data-third]", kob).forEach(function (b) { b.addEventListener("click", function () { var s = +b.dataset.third; if (kst.win["3rd"] === s) delete kst.win["3rd"]; else kst.win["3rd"] = s; store.set("pp-ko", kst); krender(); }); });
      var sl = kslots(rows), matches = N - 1 + (kst.third && R >= 2 ? 1 : 0), byes = kst.first.length - N;
      var slots = sl.slots, mins = slots * (kst.fmt + 5);
      var done = Object.keys(kst.win).length;
      $("#ko-sum").textContent = N + " pairs · " + matches + " matches · " + R + " rounds";
      $("#ko-board").innerHTML = "<h2>" + (champ !== null ? esc(kst.names[champ]) + " win!" : "Your event") + '</h2><dl class="spec" style="display:grid;grid-template-columns:auto 1fr;gap:8px 16px"><dt>Pairs</dt><dd>' + N + "</dd><dt>Matches</dt><dd>" + matches + "</dd><dt>Rounds</dt><dd>" + R + "</dd><dt>Byes</dt><dd>" + byes + (byes ? " (to the top " + (kst.seeded ? "seeds" : "drawn teams") + ")" : "") + "</dd><dt>Courts</dt><dd>" + kst.courts + "</dd><dt>Est. time</dt><dd>About " + (mins >= 60 ? Math.floor(mins / 60) + " h " + (mins % 60 ? mins % 60 + " min" : "") : mins + " min") + "</dd></dl><p>" + sl.per.map(function (n, r) { return rname(r, R - 1) + ": " + n + " match" + (n === 1 ? "" : "es") + (n ? ", " + Math.ceil(n / kst.courts) + " slot" + (Math.ceil(n / kst.courts) === 1 ? "" : "s") : ""); }).join("<br>") + (kst.third && R >= 2 ? "<br>3rd place: 1 match, played next to the final" : "") + '</p><p style="font-size:.9rem">Time = match slots x (' + kst.fmt + " min + 5 min changeover). Results entered: " + done + ".</p><p>Next: " + kl("score", "score keeper") + " · " + kl("round-robin", "round robin groups") + " · " + kl("americano", "Americano") + "</p>";
    };
    var kstart = function (names) {
      var N = names.length, err = $("#ko-err"); err.textContent = "";
      if (N < 3 || N > 32) { err.textContent = "Add between 3 and 32 pairs, one per line."; return; }
      if (kopt.seed === "rand") { names = names.slice(); for (var i = names.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = names[i]; names[i] = names[j]; names[j] = x; } }
      var size = Math.pow(2, Math.ceil(Math.log2(N))), R = Math.log2(size);
      var first = order(size).map(function (sd) { return sd <= N ? sd - 1 : -1; });
      kst = { names: names, first: first, rounds: new Array(R), win: {}, courts: Math.max(1, Math.min(16, +$("#ko-courts").value || 1)), third: $("#ko-third").value === "1", fmt: +kopt.fmt, seeded: kopt.seed === "seed" };
      store.set("pp-ko", kst); kshow();
    };
    var kshow = function () { $("#ko-setup").hidden = true; $("#ko-live").hidden = false; kob.classList.add("live"); kst.rounds = new Array(Math.log2(kst.first.length)); krender(); };
    $("#ko-start").addEventListener("click", function () { kstart(kn.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean)); });
    $("#ko-demo").addEventListener("click", function () { kn.value = ["Sam & Priya", "Omar & Lucia", "Ben & Aisha", "Tom & Mia", "Leo & Sara", "Raj & Emma", "Dan & Noor", "Max & Ella", "Ali & Grace", "Jon & Ruth", "Kai & Zoe", "Ian & Fatima"].join("\n"); kcount(); });
    $("#ko-new").addEventListener("click", function () { if (window.confirm("Start a new draw? This clears the current results.")) { kn.value = kst.names.join("\n"); kcount(); kst = null; store.set("pp-ko", null); $("#ko-setup").hidden = false; $("#ko-live").hidden = true; kob.classList.remove("live"); $("#ko-board").innerHTML = "<h2>Your event</h2><p>Make the draw to see the number of matches, rounds and how long it will take.</p>"; } });
    $("#ko-copy").addEventListener("click", function () {
      var rows = resolve(), R = rows.length, nm = function (x) { return x === -1 ? "Bye" : x === null ? "TBD" : kst.names[x]; };
      var txt = "Padel knockout draw\n" + rows.map(function (ms, r) { return "\n" + rname(r, R - 1) + "\n" + ms.map(function (m) { return nm(m.a) + " v " + nm(m.b) + (m.w === 0 ? "  -> " + nm(m.a) : m.w === 1 ? "  -> " + nm(m.b) : ""); }).join("\n"); }).join("\n") + "\n\nMade with padelglassbox.com/padel-tournament-bracket";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Draw copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    var kimp = store.get("pp-ko-import", null);
    if (kimp && kimp.length) { store.set("pp-ko-import", null); kst = null; store.set("pp-ko", null); kn.value = kimp.join("\n"); kcount(); toast("Qualifiers added: check the order, then make the draw"); }
    if (kst && kst.names && kst.first) kshow();
  }

  /* ---------- beginner racket checker ---------- */
  var bcb = $("#bc");
  if (bcb && window.BCGO) {
    var bs = store.get("pp-bc", { shape: "round", bal: "low", core: "soft", face: "glass", arm: "n", who: "adult", w: 360 });
    var bw = $("#bc-w"); bw.value = bs.w;
    var bl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var bgo = function (k, t) { return '<a href="' + window.BCGO[k] + '" rel="sponsored nofollow noopener" target="_blank" style="color:#e8f84a">' + t + "</a> (affiliate link)"; };
    var brender = function () {
      bs.w = +bw.value || 0; store.set("pp-bc", bs);
      $$("[data-bc]", bcb).forEach(function (g) { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === bs[g.dataset.bc] ? "true" : "false"); }); });
      var out = [], score = 0, max = 0, zeros = 0, add = function (lvl, label, txt) { max += 2; score += lvl; if (!lvl) zeros++; out.push('<li class="bc-' + (lvl === 2 ? "ok" : lvl === 1 ? "mid" : "no") + '"><b>' + label + ":</b> " + txt + "</li>"); };
      var lo = bs.who === "adult" ? (bs.arm === "y" ? 340 : 350) : 330, hi = bs.who === "adult" ? (bs.arm === "y" ? 360 : 370) : 355;
      if (bs.who === "kid") { $("#bc-h").textContent = "Look at a junior racket"; $("#bc-p").textContent = "Children under about 12 usually need a shorter, lighter junior racket, not an adult one."; $("#bc-list").innerHTML = ""; $("#bc-next").innerHTML = "Next: " + bl("padel-racket-for-kids", "padel rackets for kids by age") + " · " + bl("padel-beginner-plan", "30-day beginner plan"); return; }
      add(bs.shape === "round" ? 2 : bs.shape === "tear" ? 1 : bs.shape === "x" ? 1 : 0, "Shape", bs.shape === "round" ? "Round is the best beginner shape: big, low sweet spot." : bs.shape === "tear" ? "Teardrop is OK if you already play tennis or squash, but round is more forgiving." : bs.shape === "x" ? "Check it: a round head (widest near the middle) is what you want." : "Diamond puts the sweet spot high and is hard to control. Not a beginner racket.");
      var w = bs.w;
      add(w >= lo && w <= hi ? 2 : (w >= lo - 10 && w <= hi + 10) ? 1 : 0, "Weight", w ? (w >= lo && w <= hi ? w + " g is in the sweet range (" + lo + "-" + hi + " g) for you." : w > hi ? w + " g is on the heavy side for you; aim for " + lo + "-" + hi + " g." : w + " g is light; fine for control, but it may feel unstable. " + lo + "-" + hi + " g suits most.") : "Enter the weight; aim for " + lo + "-" + hi + " g.");
      add(bs.bal === "low" ? 2 : bs.bal === "even" ? 2 : bs.bal === "x" ? 1 : 0, "Balance", bs.bal === "high" ? "Head-heavy gives power but is slow at the net and harder on the elbow." : bs.bal === "x" ? "Look for low or even balance. Round rackets are usually low." : "Low or even balance is quick and easy to handle.");
      add(bs.core === "soft" ? 2 : bs.core === "med" ? (bs.arm === "y" ? 1 : 2) : bs.core === "x" ? 1 : 0, "Core", bs.core === "hard" ? "A hard core needs a fast swing to get depth and passes more shock to the arm." : bs.core === "med" ? (bs.arm === "y" ? "Medium is OK, but with arm pain a soft core is kinder." : "Medium is a fine all-round choice.") : bs.core === "x" ? "Look for soft EVA or foam." : "Soft gives easy depth and comfort.");
      add(bs.face === "glass" || bs.face === "hyb" ? 2 : bs.face === "x" ? 1 : (bs.arm === "y" ? 0 : 1), "Face", bs.face === "carbon" ? "Carbon is stiffer and pricier. A low-K (3K) carbon face can work; high-K carbon is for fast swings." : bs.face === "x" ? "Fibreglass or a fibreglass-carbon mix is the beginner pick." : "Fibreglass-based faces are flexible and forgiving.");
      var pct = score / max; if (bs.shape === "diamond" || zeros >= 2) pct = Math.min(pct, 0.5); else if (zeros === 1) pct = Math.min(pct, 0.8);
      $("#bc-h").textContent = pct >= 0.85 ? "Great beginner racket" : pct >= 0.6 ? "OK for a beginner, with a catch" : "Not ideal for a beginner";
      $("#bc-p").textContent = "Score " + score + " of " + max + ". " + (pct >= 0.85 ? "This spec is forgiving and easy on the arm." : pct >= 0.6 ? "It will work, but see the amber points below." : "It is built for faster, more advanced players. Look for the green specs below.") + (bs.arm === "y" ? " With arm pain, also see a doctor or physio if it keeps coming back." : "");
      $("#bc-list").innerHTML = out.join("");
      $("#bc-next").innerHTML = "Next: " + bl("racket-finder", "full racket finder") + " · " + bl("cheap-padel-rackets", "cheap rackets that pass") + " · Shop: " + bgo("padel-round-rackets", "round rackets");
    };
    $$("[data-bc]", bcb).forEach(function (g) { $$("button", g).forEach(function (b) { b.addEventListener("click", function () { bs[g.dataset.bc] = b.dataset.v; brender(); }); }); });
    bw.addEventListener("input", brender);
    brender();
  }

  /* ---------- padel vs racquetball quiz ---------- */
  var vrb = $("#vr");
  if (vrb) {
    var va = { a: "p", b: "p", c: "p" };
    var vl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var VR = {
      p: ["Try padel", "Doubles, long rallies and a gentle underarm serve: most people play a proper game in their first hour.", vl("beginners", "first match checklist") + " · " + vl("padel-beginner-plan", "30-day beginner plan") + " · " + vl("padel-cost", "what it costs")],
      r: ["Try racquetball", "Fast, every surface in play and easy to book for two. If you like that intensity, padel's walls will feel familiar later.", vl("squash-court-dimensions", "squash court size") + " · " + vl("padel-vs-tennis-vs-pickleball", "padel vs tennis vs pickleball")],
      t: ["Try platform tennis", "Outdoor doubles through the winter, very close to padel. Padel is the easy switch in the warmer months.", vl("rules", "padel rules") + " · " + vl("court-sizes-compared", "court sizes compared")]
    };
    var vrender = function () { var c = { p: 0, r: 0, t: 0 }; Object.keys(va).forEach(function (k) { c[va[k]]++; }); var best = c.r > c.p && c.r >= c.t ? "r" : c.t > c.p && c.t > c.r ? "t" : "p"; $("#vr-h").textContent = VR[best][0]; $("#vr-p").textContent = VR[best][1]; $("#vr-next").innerHTML = "Next: " + VR[best][2]; };
    $$("[data-vr]", vrb).forEach(function (g) { choose(g, function (v) { va[g.dataset.vr] = v; vrender(); }); });
    vrender();
  }
  /* ---------- group stage generator (groups then knockout) ---------- */
  var gsb = $("#gs");
  if (gsb) {
    var gst = store.get("pp-grp", null), gopt = { size: "4", q: "2", fmt: "30" };
    var gn = $("#gs-names"), gesc = function (x) { return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var gl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var glist = function () { return gn.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean); };
    var gcount = function () { var n = glist().length; $("#gs-count").textContent = n ? n + " pair" + (n === 1 ? "" : "s") : ""; };
    gn.addEventListener("input", gcount);
    $$("[data-gs]", gsb).forEach(function (g) { choose(g, function (v) { gopt[g.dataset.gs] = v; }); });
    var LET = "ABCDEFGH";
    var rr = function (n) { var m = []; for (var i = 0; i < n; i++) for (var j = i + 1; j < n; j++) m.push([i, j]); return m; };
    var order4 = function (ms, n) {
      // spread matches so the same pair does not play twice in a row where possible
      if (n === 4) return [[0, 3], [1, 2], [0, 2], [1, 3], [0, 1], [2, 3]];
      if (n === 3) return [[0, 1], [1, 2], [0, 2]];
      if (n === 5) return [[0, 1], [2, 3], [0, 4], [1, 2], [3, 4], [0, 2], [1, 3], [2, 4], [0, 3], [1, 4]];
      return ms;
    };
    var table = function (g) {
      var rows = g.teams.map(function (t) { return { t: t, p: 0, w: 0, gf: 0, ga: 0 }; });
      g.m.forEach(function (m) {
        var a = m.s[0], b = m.s[1];
        if (a === "" || b === "" || a == null || b == null || a === b) return;
        a = +a; b = +b;
        var A = rows[m.p[0]], B = rows[m.p[1]];
        A.p++; B.p++; A.gf += a; A.ga += b; B.gf += b; B.ga += a;
        if (a > b) A.w++; else B.w++;
      });
      rows.sort(function (x, y) { return y.w - x.w || (y.gf - y.ga) - (x.gf - x.ga) || y.gf - x.gf || x.t - y.t; });
      return rows;
    };
    var gtime = function () { var tot = gst.groups.reduce(function (s, g) { return s + g.m.length; }, 0); return { tot: tot, mins: Math.ceil(tot / gst.courts) * (gst.fmt + 5) }; };
    var hm = function (mins) { return mins >= 60 ? Math.floor(mins / 60) + " h" + (mins % 60 ? " " + mins % 60 + " min" : "") : mins + " min"; };
    var quals = function () {
      var tabs = gst.groups.map(table), out = [];
      for (var r = 0; r < gst.q; r++) { var lvl = tabs.map(function (t, i) { return { n: gst.names[t[r].t], g: i }; }); if (r % 2) lvl.reverse(); out = out.concat(lvl); }
      return out;
    };
    var gboard = function () {
      var t = gtime(), done = 0, tabs = gst.groups.map(table);
      gst.groups.forEach(function (g) { g.m.forEach(function (m) { if (m.s[0] !== "" && m.s[1] !== "" && m.s[0] !== m.s[1]) done++; }); });
      var all = done === t.tot, q = quals(), ko = q.length;
      $("#gs-sum").textContent = gst.names.length + " pairs · " + gst.groups.length + " groups · " + t.tot + " group matches";
      $("#gs-board").innerHTML = "<h2>" + (all ? "Groups finished" : "Your event") + '</h2><dl class="spec" style="display:grid;grid-template-columns:auto 1fr;gap:8px 16px"><dt>Groups</dt><dd>' + gst.groups.map(function (g, i) { return LET[i] + " (" + g.teams.length + ")"; }).join(", ") + "</dd><dt>Group matches</dt><dd>" + t.tot + " (" + done + " played)</dd><dt>Courts</dt><dd>" + gst.courts + "</dd><dt>Group stage</dt><dd>About " + hm(t.mins) + "</dd><dt>Qualifiers</dt><dd>" + ko + " (top " + gst.q + " per group)</dd><dt>Knockout</dt><dd>" + (ko - 1) + " matches</dd></dl>" +
        "<p><b>" + (all ? "Qualified" : "Qualifying now") + ":</b><br>" + q.map(function (x, i) { return (i + 1) + ". " + gesc(x.n) + " (" + LET[x.g] + ")"; }).join("<br>") + "</p>" +
        '<button class="btn lime sm" type="button" id="gs-send"' + (all ? "" : "") + ">Send to knockout bracket</button>" +
        '<p style="font-size:.9rem;margin-top:10px">' + (all ? "Seed order: group winners first, then runners-up, so winners meet runners-up early." : "You can send the current order now, but finish the groups first for the final order.") + "</p><p>Next: " + gl("padel-tournament-bracket", "knockout bracket") + " · " + gl("score", "score keeper") + " · " + gl("americano", "Americano") + "</p>";
      $("#gs-send").addEventListener("click", function () { store.set("pp-ko-import", q.map(function (x) { return x.n; })); location.href = location.protocol === "file:" ? "padel-tournament-bracket.html" : "/padel-tournament-bracket"; });
      return tabs;
    };
    var grender = function () {
      $("#gs-groups").innerHTML = gst.groups.map(function (g, gi) {
        var nm = function (i) { return gesc(gst.names[g.teams[i]]); };
        return '<div class="card" style="margin-bottom:14px"><h3>Group ' + LET[gi] + '</h3><div style="overflow-x:auto"><table class="mt gs-tab" id="gs-t' + gi + '"></table></div><h4 style="margin:14px 0 6px">Matches</h4>' +
          g.m.map(function (m, mi) { return '<div class="gs-m"><span>' + nm(m.p[0]) + '</span><input class="search" type="number" min="0" max="99" inputmode="numeric" aria-label="Games won by ' + nm(m.p[0]) + '" data-g="' + gi + '" data-m="' + mi + '" data-s="0" value="' + gesc(m.s[0]) + '"><b>v</b><input class="search" type="number" min="0" max="99" inputmode="numeric" aria-label="Games won by ' + nm(m.p[1]) + '" data-g="' + gi + '" data-m="' + mi + '" data-s="1" value="' + gesc(m.s[1]) + '"><span>' + nm(m.p[1]) + "</span></div>"; }).join("") + "</div>";
      }).join("");
      $$(".gs-m input", gsb).forEach(function (inp) { inp.addEventListener("input", function () { gst.groups[+inp.dataset.g].m[+inp.dataset.m].s[+inp.dataset.s] = inp.value === "" ? "" : String(Math.max(0, Math.min(99, parseInt(inp.value, 10) || 0))); store.set("pp-grp", gst); gtables(); }); });
      gtables();
    };
    var gtables = function () {
      var tabs = gboard();
      tabs.forEach(function (rows, gi) {
        $("#gs-t" + gi).innerHTML = '<thead><tr><th scope="col">#</th><th scope="col">Pair</th><th scope="col">P</th><th scope="col">W</th><th scope="col">Games</th><th scope="col">+/-</th></tr></thead><tbody>' + rows.map(function (r, i) { var d = r.gf - r.ga; return "<tr" + (i < gst.q ? ' class="gs-q"' : "") + "><td>" + (i + 1) + "</td><td>" + gesc(gst.names[r.t]) + "</td><td>" + r.p + "</td><td>" + r.w + "</td><td>" + r.gf + "-" + r.ga + "</td><td>" + (d > 0 ? "+" : "") + d + "</td></tr>"; }).join("") + "</tbody>";
      });
    };
    var gshow = function () { $("#gs-setup").hidden = true; $("#gs-live").hidden = false; gsb.classList.add("live"); grender(); };
    $("#gs-start").addEventListener("click", function () {
      var names = glist(), N = names.length, err = $("#gs-err"), size = +gopt.size; err.textContent = "";
      if (N < 4) { err.textContent = "Add at least 4 pairs."; return; }
      if (N > 32) { err.textContent = "Up to 32 pairs, please."; return; }
      var G = Math.max(2, Math.round(N / size)); while (G > 2 && Math.ceil(N / G) < 3) G--; G = Math.min(G, 8);
      if (Math.floor(N / G) < 2) G = Math.floor(N / 2);
      var idx = names.map(function (_, i) { return i; });
      if ($("#gs-draw").value === "rand") for (var i = idx.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = idx[i]; idx[i] = idx[j]; idx[j] = x; }
      var groups = []; for (var g = 0; g < G; g++) groups.push({ teams: [] });
      idx.forEach(function (t, k) { var row = Math.floor(k / G), pos = k % G; groups[row % 2 ? G - 1 - pos : pos].teams.push(t); });
      groups.forEach(function (g) { g.m = order4(rr(g.teams.length), g.teams.length).map(function (p) { return { p: p, s: ["", ""] }; }); });
      var q = Math.min(+gopt.q, Math.min.apply(null, groups.map(function (g) { return g.teams.length; })) - 1);
      gst = { names: names, groups: groups, q: Math.max(1, q), fmt: +gopt.fmt, courts: Math.max(1, Math.min(16, +$("#gs-courts").value || 1)) };
      store.set("pp-grp", gst); gshow();
    });
    $("#gs-demo").addEventListener("click", function () { gn.value = ["Sam & Priya", "Omar & Lucia", "Ben & Aisha", "Tom & Mia", "Leo & Sara", "Raj & Emma", "Dan & Noor", "Max & Ella", "Ali & Grace", "Jon & Ruth", "Kai & Zoe", "Ian & Fatima"].join("\n"); gcount(); });
    $("#gs-new").addEventListener("click", function () { if (window.confirm("Start a new event? This clears the current groups and scores.")) { gn.value = gst.names.join("\n"); gcount(); gst = null; store.set("pp-grp", null); $("#gs-setup").hidden = false; $("#gs-live").hidden = true; gsb.classList.remove("live"); $("#gs-board").innerHTML = "<h2>Your event</h2><p>Make the groups to see the number of matches, how long the group stage takes, and who qualifies.</p>"; } });
    $("#gs-copy").addEventListener("click", function () {
      var txt = "Padel group stage\n" + gst.groups.map(function (g, gi) { var nm = function (i) { return gst.names[g.teams[i]]; }; return "\nGroup " + LET[gi] + "\n" + g.teams.map(function (t) { return "- " + gst.names[t]; }).join("\n") + "\nMatches:\n" + g.m.map(function (m) { return nm(m.p[0]) + " v " + nm(m.p[1]) + (m.s[0] !== "" && m.s[1] !== "" ? "  " + m.s[0] + "-" + m.s[1] : ""); }).join("\n"); }).join("\n") + "\n\nMade with padelglassbox.com/padel-group-stage-generator";
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Groups copied"); }, function () { toast("Couldn't copy"); }); else toast("Couldn't copy");
    });
    if (gst && gst.groups && gst.names) gshow();
  }

  /* ---------- DUPR match checker ---------- */
  var dpb = $("#dp");
  if (dpb) {
    var dmode = "d";
    var dv = function (id) { var x = parseFloat($("#dp-" + id).value); return isNaN(x) ? null : Math.max(2, Math.min(8, x)); };
    var dl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var drender = function () {
      $("#dp-a2w").hidden = $("#dp-b2w").hidden = dmode === "s";
      var a1 = dv("a1"), a2 = dv("a2"), b1 = dv("b1"), b2 = dv("b2");
      if (a1 === null || b1 === null || (dmode === "d" && (a2 === null || b2 === null))) { $("#dp-h").textContent = "Type the ratings"; $("#dp-p").textContent = "Use numbers from 2.000 to 8.000."; $("#dp-t").innerHTML = ""; return; }
      var A = dmode === "d" ? (a1 + a2) / 2 : a1, B = dmode === "d" ? (b1 + b2) / 2 : b1, gap = A - B, ag = Math.abs(gap);
      var h, p;
      if (ag < 0.1) { h = "Even match"; p = "The teams are almost level. Win more points than them and your rating should go up; lose clearly and it should drop."; }
      else if (gap > 0) { h = "You are the favourite by " + ag.toFixed(3); p = ag >= 0.5 ? "DUPR expects your team to win clearly. A narrow win could still lower your rating, and a loss would cost you more than usual." : "DUPR expects your team to win. Win comfortably to gain; a very tight win may barely move you."; }
      else { h = "They are the favourite by " + ag.toFixed(3); p = ag >= 0.5 ? "DUPR expects you to lose. A close loss could still raise your rating, and a win would lift it a lot." : "DUPR expects a close loss. Take as many points as you can: a tight score or a win should move you up."; }
      $("#dp-h").textContent = h;
      $("#dp-p").textContent = p;
      $("#dp-t").innerHTML = (dmode === "d" ? "Team averages: you " + A.toFixed(3) + " v them " + B.toFixed(3) + ". " : "") + "Next: " + dl("pickleball-score", "pickleball score keeper") + " · " + dl("pickleball-rules", "pickleball rules");
    };
    $$("[data-dp]", dpb).forEach(function (g) { choose(g, function (v) { dmode = v; drender(); }); });
    $$("input", dpb).forEach(function (i) { i.addEventListener("input", drender); });
    drender();
  }

  /* ---------- padel vs squash habit fixer ---------- */
  var svb = $("#sv");
  if (svb) {
    var sl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var SV = {
      back: ["Let the glass do the work", "In padel the ball must land on their side before it touches their walls, and hitting hard into the back glass only sends it back to them. Aim deep and low at their feet, or lob over them.", sl("wall-rules", "wall rules") + " · " + sl("padel-tactics", "tactics trainer")],
      wrist: ["Lock your wrist", "Padel rackets are heavier and have no strings. A squash flick sends the ball long and strains the elbow. Keep the wrist firm and swing from the shoulder.", sl("padel-grip", "grip guide") + " · " + sl("padel-injuries", "elbow care")],
      all: ["Move as a pair", "You only cover your half. Move up and back with your partner like you are tied by a rope, and leave the middle ball to the forehand on that side (agree this first).", sl("positioning", "where to stand") + " · " + sl("which-side-padel", "left or right side quiz")],
      volley: ["Wait for the rebound", "At the back of the court, let the ball bounce and come off the glass: you get more time and an easier shot. Volley mainly when you are at the net.", sl("wall-rules", "playing off the glass") + " · " + sl("drills", "drills planner")],
      drop: ["Swap boasts for lobs", "Drop shots can work, but the padel shot that wins most points is the lob that pushes the net team back. Your soft hands make a great lob.", sl("shots", "shot library") + " · " + sl("bandeja-vs-vibora", "bandeja vs víbora")],
      serve: ["Serve underarm", "Padel serves are underarm: bounce the ball behind the line and hit it at or below your waist, diagonally into the box. You get 2 tries.", sl("how-to-serve-padel", "how to serve") + " · " + sl("serve-rules", "serve rules checker")]
    };
    $$("[data-sv]", svb).forEach(function (g) { choose(g, function (v) { var r = SV[v]; $("#sv-h").textContent = r[0]; $("#sv-p").textContent = r[1]; $("#sv-next").innerHTML = "Next: " + r[2]; }); });
    var r0 = SV.back; $("#sv-h").textContent = r0[0]; $("#sv-p").textContent = r0[1]; $("#sv-next").innerHTML = "Next: " + r0[2];
  }

  /* ---------- padel booking app chooser ---------- */
  var bkb = $("#bk");
  if (bkb) {
    var bl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var bw = "uk", bn = "book";
    var BW = {
      uk: ["ClubSpark, Playtomic or MATCHi", "In the UK, many LTA registered venues take bookings through ClubSpark, and many padel-only clubs use Playtomic or MATCHi. Use the booking link on your club's website."],
      eu: ["Playtomic first", "Playtomic is the most widely used padel app in Spain and across Europe. MATCHi is common at some venues. Your club's website shows which one it uses."],
      us: ["Check your club: Playtomic, PlayByPoint, CourtReserve or OpenCourt", "In the US, Playtomic and PlayByPoint are the two most used systems at padel clubs, then CourtReserve. Clubs often show PlayByPoint, CourtReserve or OpenCourt under their own app name."],
      me: ["Start with Playtomic, then check the club", "Playtomic is used in many countries, including the Middle East, but some clubs use their own app or WhatsApp booking. Check the club's website or social pages."],
      x: ["Ask the club which system it uses", "Playtomic is the most widely used padel app worldwide, but many clubs use their own booking page. Look for the book link on the club's website."]
    };
    var BN = {
      book: ["Tip:", "Book 60 or 90 minutes for 4 players, a few days ahead for evenings. Then use the invite maker below to fill the court and split the price."],
      find: ["Tip:", "Open matches are the fastest way: Playtomic lets you join games at your level (0 to 7). Club apps like PlayByPoint and CourtReserve list clinics and socials more than partner matches, so join those and the club WhatsApp group."],
      learn: ["Tip:", "Club apps list lessons, clinics and leagues. In the UK, the LTA has coach and competition finders, and Grade 5 and 4 events suit beginners to intermediates."]
    };
    var brender = function () {
      var a = BW[bw], b = BN[bn];
      $("#bk-h").textContent = a[0];
      $("#bk-p").textContent = a[1] + " " + b[0] + " " + b[1];
      $("#bk-next").innerHTML = "Next: " + (bn === "find" ? bl("level-calculator", "check your level") + " · " + bl("americano", "Americano nights") : bn === "learn" ? bl("padel-lessons", "padel lessons") + " · " + bl("padel-beginner-plan", "30-day plan") : bl("padel-cost", "court prices") + " · " + bl("padel-etiquette", "etiquette"));
    };
    $$("[data-bk]", bkb).forEach(function (g) { choose(g, function (v) { if (g.dataset.bk === "where") bw = v; else bn = v; brender(); }); });
    brender();
  }

  /* ---------- padel game invite maker ---------- */
  var pib = $("#pinv");
  if (pib) {
    var pv = { lvl: "Improver (2-3)", need: "1", type: "Friendly, rotate partners" };
    var pmsg = "";
    var prender = function () {
      var day = $("#pi-day").value.trim() || "[day]", tm = $("#pi-time").value || "[time]", club = $("#pi-club").value.trim() || "[club]";
      var len = $("#pi-len").value, cur = $("#pi-cur").value, price = parseFloat($("#pi-price").value);
      var each = isNaN(price) || price <= 0 ? "" : cur + (Math.round(price / 4 * 100) / 100).toFixed(2).replace(/\.00$/, "");
      var n = parseInt(pv.need, 10);
      pmsg = "Padel game: " + n + " player" + (n === 1 ? "" : "s") + " needed\n" +
        "When: " + day + ", " + tm + " (" + len + " min)\n" +
        "Where: " + club + "\n" +
        "Level: " + pv.lvl + "\n" +
        "Game: " + pv.type + "\n" +
        (each ? "Cost: " + each + " each (court split 4 ways)\n" : "") +
        ($("#pi-balls").checked ? "Balls: I'm bringing new ones\n" : "Balls: please bring a can if you have one\n") +
        "Reply here to grab a spot. First come, first served.";
      $("#pi-msg").textContent = pmsg;
      $("#pi-each").textContent = each ? "Each player pays " + each + " for " + len + " minutes." : "Add the court price to split it.";
      $("#pi-wa").href = "https://wa.me/?text=" + encodeURIComponent(pmsg);
    };
    $$("[data-pi]", pib).forEach(function (g) { choose(g, function (v) { pv[g.dataset.pi] = v; prender(); }); });
    $$("input, select", pib).forEach(function (i) { i.addEventListener("input", prender); i.addEventListener("change", prender); });
    $("#pi-copy").addEventListener("click", function () {
      if (navigator.clipboard) navigator.clipboard.writeText(pmsg).then(function () { toast("Invite copied"); }, function () { toast("Select the text to copy"); });
      else toast("Select the text to copy");
    });
    prender();
  }

  /* ---------- history of padel timeline filter ---------- */
  var htb = $("#ht");
  if (htb) {
    var yrs = new Date().getFullYear() - 1969;
    $("#ht-age").textContent = "Padel is " + yrs + " years old this year. Tap a theme to filter.";
    $$("[data-ht]", htb).forEach(function (g) { choose(g, function (v) { $$(".ht-i", htb).forEach(function (li) { li.hidden = !(v === "all" || li.dataset.era === v); }); }); });
  }

  /* ---------- padel lob picker + facing a lob ---------- */
  var lbl = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
  var lpb = $("#lbp");
  if (lpb) {
    var lv = { opp: "net", bal: "set", opp2: "avg" };
    var lrender = function () {
      var h, p, t;
      if (lv.opp === "back") {
        h = "Don't lob: keep it low";
        p = "Both opponents are already back, so a lob only hands them the net. Play a low, slow ball at their feet (a chiquita) and move forward together.";
        t = "Next: " + lbl("shots", "padel shots") + " · " + lbl("padel-tactics", "tactics trainer");
      } else if (lv.bal === "rush") {
        h = "High defensive lob";
        p = "You are in trouble, so go for height and safety, not speed. Aim cross-court and deep, past the service line, and use the time to get back into position.";
        t = "Target: past the service line, before the back glass. Then recover: " + lbl("positioning", "where to stand");
      } else if (lv.opp2 === "short" || (lv.opp === "mid" && lv.bal === "set")) {
        h = "Attacking lob";
        p = "You have time and a net player you can beat over the top. Play a lower, faster lob just over their reach" + (lv.opp === "mid" ? ", over the player at the net" : "") + ", cross-court. Follow it in and take the net as they turn.";
        t = "Risk: too low and it is an easy smash. If unsure, add height.";
      } else if (lv.opp2 === "tall") {
        h = "Extra high, extra deep lob";
        p = "Tall or quick smashers kill medium lobs. Go higher than feels normal and aim deep, so it lands well past the service line and dies near the back glass.";
        t = "Mix in low balls at their feet so they cannot wait for the lob.";
      } else {
        h = "Deep cross-court lob";
        p = (lv.bal === "glass" ? "Let the ball come off the back glass, stay low and lift it. " : "") + "Play a high lob cross-court, landing between the service line and the back glass. When they turn and run back, move up to the net with your partner.";
        t = "Cross-court is the longest line: more room for error. Down the line is your surprise.";
      }
      $("#lbp-h").textContent = h; $("#lbp-p").textContent = p; $("#lbp-t").innerHTML = t;
    };
    $$("[data-lbp]", lpb).forEach(function (g) { choose(g, function (v) { lv[g.dataset.lbp] = v; lrender(); }); });
    lrender();
  }
  var ldb = $("#lbd");
  if (ldb) {
    var dv = { dep: "mid", side: "fh" };
    var LD = {
      "short-fh": ["Smash it, flat or with a víbora", "A short lob on your forehand side is your chance to attack. Hit a flat smash to win the point, or a víbora with side spin into the side glass."],
      "short-bh": ["Víbora or topspin smash", "On the backhand side you cannot swing a forehand flat smash easily. Turn sideways and play a víbora, or a topspin smash if you are confident."],
      "mid-fh": ["Bandeja or aggressive víbora", "A middle lob is not short enough to put away safely. A bandeja keeps the net; a firmer víbora puts pressure on."],
      "mid-bh": ["Bandeja, or a gancho if you have it", "Keep it simple: a controlled bandeja to the back corner so you keep the net. Advanced players use a gancho on this side."],
      "deep-fh": ["Let it go onto the back glass", "A deep lob is hard to attack. Let it pass, play it off the back glass and lob back or hit a low ball, then win the net again."],
      "deep-bh": ["Let it go, then lob back", "Turn and run back, let it come off the back glass and play a defensive lob. Trying to smash a deep lob on your backhand usually loses the net anyway."]
    };
    var drender = function () {
      var a = LD[dv.dep + "-" + dv.side];
      $("#lbd-h").textContent = a[0]; $("#lbd-p").textContent = a[1];
      $("#lbd-t").innerHTML = "Left-handed? Swap the sides. Learn the shots: " + lbl("bandeja-vs-vibora", "bandeja vs víbora vs smash") + " · " + lbl("out-of-court-play", "out-of-court play");
    };
    $$("[data-lbd]", ldb).forEach(function (g) { choose(g, function (v) { dv[g.dataset.lbd] = v; drender(); }); });
    drender();
  }

  /* ---------- overgrip change calculator + worn signs ---------- */
  var ogb = $("#ogc");
  if (ogb) {
    var ov = { sweat: "1", clim: "1", lvl: "1" };
    var orender = function () {
      var n = parseFloat($("#og-n").value), len = parseFloat($("#og-len").value), price = parseFloat($("#og-p").value), cur = $("#og-cur").value;
      if (isNaN(n) || n <= 0) { $("#og-h").textContent = "Add your sessions per week"; $("#og-p2").textContent = ""; $("#og-y").textContent = ""; return; }
      var life = 10 * parseFloat(ov.sweat) * parseFloat(ov.clim) * parseFloat(ov.lvl);
      var sess = Math.max(1, Math.round(life / len));
      var days = Math.min(60, Math.round(sess / n * 7));
      var perYear = Math.ceil(365 / Math.max(days, 1));
      var when = days >= 56 ? "about every 2 months" : days >= 12 ? "about every " + Math.round(days / 7) + " weeks" : days >= 6 ? "about once a week" : "every few days";
      $("#og-h").textContent = sess === 1 ? "Every session" : "Every " + sess + " sessions";
      $("#og-p2").textContent = (sess === 1 ? "Fit a fresh one before each game" : "That is " + when) + " (about " + (Math.round(life * 10) / 10) + " hours of play per overgrip" + (days >= 60 ? ", capped at the two-month maximum" : "") + ").";
      $("#og-y").textContent = "About " + perYear + " overgrips a year" + (!isNaN(price) && price > 0 ? ", roughly " + cur + Math.round(perYear * price) + " a year." : ".");
      $("#og-tip").textContent = ov.sweat === "0.6" || ov.clim === "0.5" ? "Sweaty hands or humid courts: try an absorbent (dry) overgrip and keep a towel or wristband handy." : perYear >= 24 ? "Using 2 or more a month? A 12-pack usually costs less per grip." : "Change it sooner if it feels slippery when dry, whatever the calculator says.";
    };
    $$("[data-og]", ogb).forEach(function (g) { choose(g, function (v) { ov[g.dataset.og] = v; orender(); }); });
    $$("input, select", ogb).forEach(function (i) { i.addEventListener("input", orender); i.addEventListener("change", orender); });
    orender();
  }
  var ogsb = $("#ogs");
  if (ogsb) {
    var osr = function () {
      var c = $$("[data-ogs]:checked", ogsb).length;
      $("#ogs-out").textContent = c === 0 ? "No signs ticked: your overgrip is fine for now." : c === 1 ? "One sign: change it before your next match." : c + " signs: change it today. Your hand is working harder than it needs to.";
    };
    $$("[data-ogs]", ogsb).forEach(function (i) { i.addEventListener("change", osr); });
    osr();
  }


  /* ---------- volley picker + volley fault finder ---------- */
  var vpb = $("#vop");
  if (vpb) {
    var vv = { spd: "med", ht: "chest", opp: "back" };
    var vrender = function () {
      var h, p, t = "";
      if (vv.ht === "high") {
        if (vv.spd === "slow") { h = "Finish it: firm volley or smash"; p = "A slow, high ball is your chance. Step in and play a firm volley " + (vv.opp === "net" ? "at the feet of the nearest opponent or through the middle." : "into the back corner, at the double glass, or a smash if it is above your head."); }
        else { h = "High block, deep"; p = "Fast and high is hard to control. Keep the racket in front of your head, block it firmly and send it deep down the middle. If it is over your head, a bandeja is safer."; t = lbl("bandeja-vs-vibora", "Bandeja vs víbora vs smash"); }
      } else if (vv.ht === "low") {
        h = "Low volley: slow and deep";
        p = "You are below the net, so you cannot attack. Bend your knees, open the face a little and play it slow" + (vv.opp === "back" ? " and deep, past the service line." : vv.opp === "mid" ? " and low at the feet of the player coming in." : ", soft, back down the middle, then get ready for the next ball.");
        t = "Keep the racket head up: bend the legs, not the wrist.";
      } else if (vv.spd === "fast") {
        h = "Block volley";
        p = "Hold the racket firm in front of you and do not swing. Let the ball's speed send it back, deep and through the middle" + (vv.opp === "net" ? ", or softly at their feet if they are both very close." : ".");
        t = "Short backswing, firm wrist, step in.";
      } else if (vv.spd === "slow") {
        h = vv.opp === "back" ? "Slice volley into the corner" : "Attacking volley at the feet";
        p = vv.opp === "back" ? "A slow ball at chest height can hurt them. Cut under it for backspin and send it deep into the corner, so it stays low after the back glass." : "Step in and play it firmly down at the feet of the player " + (vv.opp === "mid" ? "coming in." : "nearest you, or through the middle between them.");
        t = "If it is not clearly easy, play a deep push instead.";
      } else {
        h = vv.opp === "mid" ? "Volley at the feet of the player coming in" : vv.opp === "net" ? "Low, soft volley down the middle" : "Deep push volley";
        p = vv.opp === "mid" ? "One opponent is moving forward. A low volley at their feet makes them hit up to you." : vv.opp === "net" ? "All four at the net: keep it low so they must hit up. Down the middle makes them think about who takes it." : "Push it deep, past the service line and through the middle. Keep them back and wait for an easier ball. Or play a setup volley into the corner.";
      }
      $("#vop-h").textContent = h; $("#vop-p").textContent = p; $("#vop-t").innerHTML = t;
    };
    $$("[data-vop]", vpb).forEach(function (g) { choose(g, function (v) { vv[g.dataset.vop] = v; vrender(); }); });
    vrender();
  }
  var vfs = $("#vof-s");
  if (vfs) {
    var VF = {
      up: ["Racket face too open, or you were late.", "Get the racket ready earlier, meet the ball in front of you and keep the face a little more closed. Use a continental grip, not a flat one.", "Drill: partner feeds 20 balls at chest height; every volley must land past the service line."],
      net: ["Trying to attack a difficult ball.", "On low or fast balls, play a softer block and aim higher over the net. Only attack balls above the net.", "Bend your knees on low balls instead of dropping the racket head."],
      long: ["Swinging too much.", "Shorten the swing to a short punch and stop the racket after contact. Let the step give you power, not the arm.", "Aim for the ball to bounce before the back glass, past the service line."],
      late: ["Racket too low in the ready position.", "Keep the racket up and in front of your body all the time at the net, even when you run in after the serve.", "Split step every time an opponent hits."],
      lob: ["Standing too close to the net.", "Stand about two to three metres from the net and step forward into each volley. Then you have time to go back for the lob.", "See the lob guide for how to answer lobs."],
      weak: ["Arm only, no step or shoulder turn.", "Turn your shoulders and step towards the ball with the opposite foot as you hit. On easy balls you may use a slightly longer swing.", "Power comes from the legs and the step."],
      bh: ["Wrist and grip, usually.", "Keep the continental grip (do not turn to a forehand grip), turn the shoulders more and lead with the step of the right foot (right-hander). Keep the racket head above the wrist.", "Practise 10 backhand blocks against a wall, then with a partner."]
    };
    var vfr = function () { var a = VF[vfs.value]; $("#vof-c").textContent = a[0]; $("#vof-f").textContent = a[1]; $("#vof-d").innerHTML = a[2] + (vfs.value === "lob" ? " " + lbl("padel-lob", "Padel lob guide") : " More problems: " + lbl("fix-my-padel", "fix my padel")); };
    vfs.addEventListener("change", vfr);
    vfr();
  }

  /* ---------- return of serve picker ---------- */
  var rpb = $("#rtp");
  if (rpb) {
    var rv = { tgt: "glass", spin: "flat", srv: "net" };
    var rrender = function () {
      var stand = { flat: "one step behind the service line, near the side glass", side: "a little further from the side glass, so the ball can come in to you", slice: "a little closer to the glass, knees bent early, ready for a low ball", fast: "a little deeper than usual, racket back early" }[rv.spin];
      var h, p;
      if (rv.tgt === "glass") { h = "Let it off the glass, then block it back"; p = "A good serve into the side glass is hard to attack. Let it come off the glass, then play a simple, controlled return deep to the server" + (rv.srv === "net" ? ", or low at their feet as they come in." : "."); }
      else if (rv.tgt === "t") { h = "Lob, to buy time"; p = "A serve down the middle gives you little angle. A high lob over the net player is the safest return" + (rv.srv === "net" ? ". Better players can also play a soft ball at the server's feet." : ". The server stayed back, so you can also play low and deep and come in."); }
      else if (rv.tgt === "body") { h = "Step aside and block"; p = "Move your feet out of the way first, then play a short, firm block deep down the middle. Do not try a big swing at a ball into your body."; }
      else { h = "Attack it and take the net"; p = rv.srv === "net" ? "An easy serve is your chance. Step in and play low at the feet of the server coming in (a chiquita), or lob over the net player, then move up to the net with your partner." : "An easy serve and nobody at the net: play deep and come in, so your pair takes the net first."; }
      if (rv.spin === "slice") p += " With slice, keep it slow and deep, or lob: do not hit a low ball hard.";
      if (rv.spin === "fast") p += " Speed does not change direction, only time: prepare early.";
      $("#rtp-h").textContent = h; $("#rtp-p").textContent = p;
      $("#rtp-t").innerHTML = "Stand " + stand + ". Remember: the serve must bounce first. Rules: " + lbl("serve-rules", "serve rules checker");
    };
    $$("[data-rtp]", rpb).forEach(function (g) { choose(g, function (v) { rv[g.dataset.rtp] = v; rrender(); }); });
    rrender();
  }

  /* ---------- back glass rebound picker ---------- */
  var bgb = $("#bgp");
  if (bgb) {
    var bv = { spd: "med", ht: "mid", wall: "back", opp: "net" };
    var brender = function () {
      var where = { fast: "Stand well away from the glass: a fast, flat ball comes out a long way.", med: "Stand about a big step and a half from the glass and adjust with small steps.", slow: "Move in closer: a slow lob drops near the wall." }[bv.spd];
      if (bv.wall === "sb") where += " Side then back glass: it will come out towards the middle, so check who takes it with your partner.";
      if (bv.wall === "bs") where += " Back then side glass: it runs along the side wall towards the net. Follow it.";
      var h, p;
      if (bv.ht === "high" && bv.wall === "back") { h = bv.opp === "net" ? "Bajada: attack it low" : "Bajada, deep"; p = "The ball comes off high, so you can attack. Take it on the way down at about shoulder height with a compact swing and drive it " + (bv.opp === "net" ? "low, at the feet of the net player or through the middle. Then move up." : "deep through the middle, then take the net."); }
      else if (bv.ht === "low" || bv.wall !== "back") { h = "Safe lift: high lob"; p = (bv.ht === "low" ? "A low rebound is a defensive ball. Get down early and lift it " : "Double-wall balls are awkward, so keep it simple: lift it ") + (bv.opp === "net" ? "into a high, deep lob over the net pair, cross-court." : "high and deep, back into a neutral rally."); }
      else { h = bv.opp === "net" ? "Lob or low ball at the feet" : "Deep, steady drive"; p = bv.opp === "net" ? "At waist height you have a choice. The lob is the safer shot and moves them back. If they are very close to the net, a low, slow ball at their feet can work." : "They are back too, so a lob only gives them the net. Play a steady ball deep through the middle and look to come in."; }
      $("#bgp-h").textContent = h; $("#bgp-p").textContent = p; $("#bgp-t").textContent = where;
    };
    $$("[data-bgp]", bgb).forEach(function (g) { choose(g, function (v) { bv[g.dataset.bgp] = v; brender(); }); });
    brender();
  }

  /* ---------- smash or not: lob picker ---------- */
  var smb = $("#smp");
  if (smb) {
    var sv = { dep: "mid", ht: "high", bal: "fwd", out: "n" };
    var srender = function () {
      var h, p, t;
      if (sv.ht === "head" || sv.bal === "back") {
        if (sv.dep === "deep") { h = "Let it come off the glass"; p = "A deep lob you can only reach while moving back is not an overhead. Turn, run back, let it bounce and come off the back glass, then lob or play a low ball."; t = lbl("padel-back-glass", "How to play off the back glass"); }
        else { h = sv.bal === "back" ? "Bandeja" : "Víbora or bandeja"; p = sv.bal === "back" ? "Moving backwards, a smash is a gamble. Play a controlled bandeja deep into the corner and keep the net." : "At head height you cannot hit down hard. A bandeja is the safe choice; a víbora adds side spin and pace if you are comfortable."; t = lbl("bandeja-vs-vibora", "Bandeja vs víbora vs smash"); }
      } else if (sv.dep === "short") {
        if (sv.out === "y") { h = "Smash: flat at the feet or an angle"; p = "A short, high lob is the one to finish. On a court where they can run outside, an x3 or x4 can be chased, so a flat smash at a player's feet or a sharp angle is often safer."; }
        else { h = "Smash: x3 is on"; p = "Short, high and you are moving forward: the best ball for an x3. Topspin it to bounce about a metre before their service line, so it flies out over the side wall. Or play a flat smash at their feet."; }
        t = "After the smash, move straight back to the net.";
      } else if (sv.dep === "mid") {
        h = "Kick smash or bandeja"; p = "Around the service line you can smash, but an x3 is hard from here. A kick smash with heavy topspin keeps them back; a bandeja is the safer option if you are not sure."; t = lbl("bandeja-vs-vibora", "Compare overheads");
      } else {
        h = "Bandeja, deep"; p = "Too deep to smash, even above your head. A smash from here usually comes back off their glass. Play a bandeja into the corner and hold the net."; t = lbl("bandeja-vs-vibora", "Bandeja vs víbora vs smash");
      }
      $("#smp-h").textContent = h; $("#smp-p").textContent = p; $("#smp-t").innerHTML = t;
    };
    $$("[data-smp]", smb).forEach(function (g) { choose(g, function (v) { sv[g.dataset.smp] = v; srender(); }); });
    srender();
  }

  /* ---------- chiquita or lob picker ---------- */
  var cqb = $("#cqp");
  if (cqb) {
    var cv = { pos: "mid", opp: "normal", ball: "easy" };
    var crender = function () {
      var h, p, t = "Mix it with lobs so they never know which is coming.";
      if (cv.pos === "back" || cv.ball === "hard") { h = "Lob"; p = cv.pos === "back" ? "Pinned near the back glass you cannot get forward after a chiquita. Play a high, deep lob, cross-court, and wait for the next chance." : "On a fast or awkward ball a soft chiquita is hard to control. Lift it into a high, deep lob."; t = lbl("padel-lob", "How to hit a lob"); }
      else if (cv.opp === "close") { h = "Lob over them"; p = "They are very close to the net, so a chiquita gives them an easy volley down. A lob over their heads is the better ball, then come forward."; t = lbl("padel-lob", "How to hit a lob"); }
      else if (cv.pos === "glass") { h = cv.opp === "back" ? "Chiquita or bajada" : "Bajada or chiquita"; p = "A high rebound off the glass gives you time. Drive it low with a bajada, or take pace off and drop a chiquita at their feet, then move in."; t = lbl("padel-back-glass", "Playing off the back glass"); }
      else { h = "Chiquita"; p = cv.opp === "back" ? "They are stepping back for your lob. Catch them out: a soft, low ball at their feet, then move in with your partner." : "A good chance. Play it soft and low at the feet of the net player or through the middle, then move forward at once."; }
      $("#cqp-h").textContent = h; $("#cqp-p").textContent = p; $("#cqp-t").innerHTML = t;
    };
    $$("[data-cqp]", cqb).forEach(function (g) { choose(g, function (v) { cv[g.dataset.cqp] = v; crender(); }); });
    crender();
  }

  /* ---------- padel weather checker ---------- */
  var wxb = $("#wxc");
  if (wxb) {
    var wv = { court: "out", rain: "dry", temp: "mild", wind: "calm", storm: "no" };
    var wrender = function () {
      var lvl = 0, h, p, kit = [], t = "Always follow your club's decision on court closures.";
      var open = wv.court !== "in";
      var reasons = [];
      if (wv.storm === "yes" && wv.court !== "in") { lvl = 3; reasons.push("Thunder or lightning: stop now and go inside a building or a closed car. Wait 30 minutes after the last thunder. An open-sided roof is not shelter."); }
      if (wv.court === "out") {
        if (wv.rain === "snow" || wv.rain === "pool") { lvl = Math.max(lvl, 3); reasons.push(wv.rain === "snow" ? "Snow or ice: the ball won't bounce properly and the turf is dangerous." : "Standing water: slips happen and the bounce is random."); }
        else if (wv.rain === "rain") { lvl = Math.max(lvl, 2); reasons.push("Steady rain: wet glass and turf are slippery and the ball skids low. Wait, or move indoors."); }
        else if (wv.rain === "drizzle") { lvl = Math.max(lvl, 1); reasons.push("Light drizzle: often playable on a well-drained court if the venue allows it. Stop if anyone slips."); kit.push("A towel for the glass, your grip and the ball"); }
        else if (wv.rain === "after") { lvl = Math.max(lvl, 1); reasons.push("Just after rain: do the towel test near the service line. Wet towel = wait 15 to 30 minutes more."); kit.push("A towel to test the turf and wipe the glass"); }
      } else if (wv.court === "cov" && (wv.rain === "rain" || wv.rain === "pool" || wv.rain === "snow")) { lvl = Math.max(lvl, 1); reasons.push("Covered court: rain can still blow in at the sides. Check the corners and back glass are dry."); kit.push("A towel for any wet glass"); }
      if (open && wv.temp === "freeze") { lvl = Math.max(lvl, 1); reasons.push("Below 5°C: balls go dead and cold muscles strain easily. Watch for frost on the turf."); }
      if (open && (wv.temp === "freeze" || wv.temp === "cold")) { kit.push("Layers you can take off, plus a spare dry top"); kit.push("A fresh tube of balls, kept warm in your bag"); kit.push("A 15-minute warm-up, including wrist and elbow"); }
      if (open && wv.temp === "hot") { lvl = Math.max(lvl, 1); reasons.push("Above 32°C: glass courts get very hot. Book early or late, drink often and rest in the shade at change of ends."); }
      if (open && (wv.temp === "warm" || wv.temp === "hot")) { kit.push("More water than you think"); kit.push("Lower lobs: balls fly further in the heat"); }
      if (open && wv.wind === "strong") { lvl = Math.max(lvl, 1); reasons.push("Strong gusts: lobs and smashes drift above the glass. Keep the ball low and let more balls come off the glass."); }
      else if (open && wv.wind === "breeze") { kit.push("Keep lobs a little lower than usual"); }
      if (wv.rain !== "dry" && open) kit.push("Shoes with good tread; dry them at room temperature after");
      if (!kit.length) kit.push("Your usual kit: balls, water, overgrip");
      var pills = ["Play", "Play with care", "Wait", "Don't play"];
      h = ["Good to play", "Playable, with care", "Wait or move indoors", "Don't play now"][lvl];
      p = reasons.length ? reasons.join(" ") : (wv.court === "in" ? "Indoors the weather doesn't affect the court. Enjoy it." : "No weather problems. Normal game, normal bounce.");
      $("#wxc-pill").textContent = pills[lvl];
      $("#wxc-pill").className = "pill " + ["b", "i", "a", "a"][lvl];
      $("#wxc-h").textContent = h; $("#wxc-p").textContent = p;
      $("#wxc-kit").innerHTML = kit.filter(function (x, i, a) { return a.indexOf(x) === i; }).map(function (x) { return "<li>" + x + "</li>"; }).join("");
      $("#wxc-t").innerHTML = t + " Next: " + lbl("padel-balls", "when to change balls") + " · " + lbl("warm-up", "warm-up timer");
    };
    $$("[data-wxc]", wxb).forEach(function (g) { choose(g, function (v) { wv[g.dataset.wxc] = v; wrender(); }); });
    wrender();
  }

  /* ---------- padel elbow arm-load check ---------- */
  var peb = $("#pec");
  if (peb) {
    var pv = { wt: "x", bal: "x", core: "med", grip: "relax", late: "some", bh: "turn", load: "same", pain: "no" };
    var prender = function () {
      var f = [];
      if (pv.load === "more") f.push([3, "Build up more slowly: add one session a week at a time and keep rest days. A sudden jump is a classic trigger."]);
      if (pv.late === "often") f.push([3, "Meet the ball in front of you. Off the back glass, step back and let it come to you, so your legs and shoulders do the work."]);
      else if (pv.late === "some") f.push([1, "Work on meeting the ball in front of your body, especially after the back glass."]);
      if (pv.bh === "wrist") f.push([3, "Turn your shoulders on the backhand and keep the wrist firm. A wrist flick loads the outside of the elbow."]);
      if (pv.grip === "tight") f.push([2, "Relax your grip between shots (about 3 or 4 out of 10). Fit a fresh overgrip so you don't need to squeeze."]);
      if (pv.wt === "heavy") f.push([2, "Your racket is heavy. Try about 340 to 360 g, as long as you can still swing smoothly."]);
      if (pv.bal === "high") f.push([2, "A head-heavy racket loads the arm on every swing. Look for low balance, under about 260 mm, often a round shape."]);
      if (pv.core === "hard") f.push([2, "A stiff racket passes on more shock. A soft foam core absorbs more."]);
      if (pv.wt === "x" || pv.bal === "x") f.push([0, "Check your racket's weight and balance on the maker's page, or weigh it on a kitchen scale."]);
      f.sort(function (a, b) { return b[0] - a[0]; });
      var score = f.reduce(function (s, x) { return s + x[0]; }, 0);
      var lvl = score >= 7 ? 2 : score >= 3 ? 1 : 0;
      var h = ["Low arm load", "Some arm load", "High arm load"][lvl];
      var p = ["Your racket and habits look arm-friendly. Keep warming up the forearm and use fresh balls.", "A few habits add load to your elbow. Start with the first change below.", "Several things add up. Change the top two first; gear alone won't fix technique."][lvl];
      if (pv.pain === "yes") p = "You have pain during play or daily life: rest from what hurts. The NHS advises seeing a GP if it is no better after 2 weeks of self-care. Then work on the changes below. " + p;
      else if (pv.pain === "some") p = "Pain after playing is an early warning. Cut back for a while and make the changes below. " + p;
      $("#pec-pill").textContent = "Load score " + score;
      $("#pec-pill").className = "pill " + ["b", "i", "a"][lvl];
      $("#pec-h").textContent = h; $("#pec-p").textContent = p;
      $("#pec-list").innerHTML = (f.length ? f : [[0, "Nothing to change. Keep rest days and warm up properly."]]).map(function (x) { return "<li>" + x[1] + "</li>"; }).join("");
      $("#pec-t").innerHTML = "Next: " + lbl("racket-finder", "racket finder") + " · " + lbl("padel-injuries", "padel injuries guide") + " · " + lbl("warm-up", "warm-up timer");
    };
    $$("[data-pec]", peb).forEach(function (g) { choose(g, function (v) { pv[g.dataset.pec] = v; prender(); }); });
    prender();
  }

  /* ---------- compare two padel rackets ---------- */
  var rcb = $("#rc-out");
  if (rcb && $("#rc-rows")) {
    var rv = { lvl: "int", style: "both", arm: "ok", ashape: "round", acore: "soft", aface: "glass", bshape: "diamond", bcore: "hard", bface: "carbon" };
    var SH = { round: "Round", tear: "Teardrop", diamond: "Diamond" }, CO = { soft: "Soft", med: "Medium", hard: "Hard" }, FA = { glass: "Fibreglass", mix: "Carbon + glass", carbon: "Carbon" };
    var num = function (id) { var v = parseFloat(($("#" + id) || {}).value); return isNaN(v) ? null : v; };
    var ideal = function () {
      var L = rv.lvl, S = rv.style, sore = rv.arm === "sore";
      var shape = sore || L === "beg" ? "round" : (S === "pow" && L === "adv" ? "diamond" : (S === "ctrl" ? "round" : "tear"));
      if (L === "int" && S === "pow" && !sore) shape = "tear";
      var core = sore || L === "beg" ? "soft" : (L === "adv" && S === "pow" ? "hard" : "med");
      var face = sore || L === "beg" ? "glass" : (L === "adv" ? "carbon" : "mix");
      var w = sore ? [340, 360] : (L === "beg" ? [345, 360] : (L === "int" ? [350, 370] : [355, 375]));
      var b = sore || S === "ctrl" || L === "beg" ? [245, 260] : (S === "pow" ? [265, 280] : [255, 268]);
      return { shape: shape, core: core, face: face, w: w, b: b };
    };
    var ORD = { shape: ["round", "tear", "diamond"], core: ["soft", "med", "hard"], face: ["glass", "mix", "carbon"] };
    var dist = function (k, v, t) { return Math.abs(ORD[k].indexOf(v) - ORD[k].indexOf(t)); };
    var rdist = function (v, r) { return v === null ? null : (v < r[0] ? (r[0] - v) : (v > r[1] ? (v - r[1]) : 0)); };
    var rcrender = function () {
      var I = ideal(), sa = 0, sb = 0, rows = [], na = (($("#rc-a-name") || {}).value || "").trim() || "A", nb = (($("#rc-b-name") || {}).value || "").trim() || "B";
      var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
      na = esc(na); nb = esc(nb);
      var add = function (lab, va, vb, mean, wgt, da, db) {
        if (da !== null && db !== null) { sa += wgt * da; sb += wgt * db; }
        var fit = function (d, o) { return d === null || o === null || d === o ? "" : (d < o ? " ✓" : ""); };
        rows.push("<tr><td>" + lab + "</td><td>" + va + fit(da, db) + "</td><td>" + vb + fit(db, da) + "</td><td>" + mean + "</td></tr>");
      };
      var sA = rv.ashape, sB = rv.bshape, msh;
      if (sA === sB) msh = "Same shape: the sweet spot sits in a similar place.";
      else msh = (ORD.shape.indexOf(sB) > ORD.shape.indexOf(sA) ? nb : na) + " has the higher, smaller sweet spot: more power on overheads when you hit it right, less forgiving on mishits.";
      add("Shape", SH[sA], SH[sB], msh, 5, dist("shape", sA, I.shape), dist("shape", sB, I.shape));
      var bA = num("rc-a-b"), bB = num("rc-b-b"), mb;
      if (bA === null || bB === null) mb = "Add both balance numbers (from the same shop) to compare. Above about 265 mm is head-heavy, below about 255 mm feels quick.";
      else if (Math.abs(bA - bB) < 5) mb = "Under 5 mm apart: they will feel similar in balance.";
      else mb = (bA > bB ? na : nb) + " is " + Math.abs(bA - bB) + " mm more head-heavy: more weight behind smashes, slower at the net and more load on the arm.";
      var dbA = rdist(bA, I.b), dbB = rdist(bB, I.b);
      add("Balance", bA === null ? "–" : bA + " mm", bB === null ? "–" : bB + " mm", mb, 4, dbA === null ? null : dbA / 5, dbB === null ? null : dbB / 5);
      var cA = rv.acore, cB = rv.bcore;
      add("Core", CO[cA], CO[cB], cA === cB ? "Same core feel." : (ORD.core.indexOf(cA) < ORD.core.indexOf(cB) ? na : nb) + " is softer: easier power at slow speeds and kinder on the arm. The harder one needs fast swings to come alive.", 3, dist("core", cA, I.core), dist("core", cB, I.core));
      var fA = rv.aface, fB = rv.bface;
      add("Face", FA[fA], FA[fB], fA === fB ? "Same face material." : (ORD.face.indexOf(fA) < ORD.face.indexOf(fB) ? na : nb) + " is more forgiving and comfortable; the other is stiffer and more precise, with more vibration.", 2, dist("face", fA, I.face), dist("face", fB, I.face));
      var wA = num("rc-a-w"), wB = num("rc-b-w"), mw;
      if (wA === null || wB === null) mw = "Add both weights to compare. Under 5 g apart doesn't matter; 15 to 20 g you will feel.";
      else if (Math.abs(wA - wB) < 6) mw = "Only " + Math.abs(wA - wB) + " g apart: rackets of one model vary this much. Ignore it.";
      else mw = (wA > wB ? na : nb) + " is " + Math.abs(wA - wB) + " g heavier: more stable and solid, but slower to swing and more tiring for the arm.";
      var dwA = rdist(wA, I.w), dwB = rdist(wB, I.w);
      add("Weight", wA === null ? "–" : wA + " g", wB === null ? "–" : wB + " g", mw, 1, dwA === null ? null : dwA / 8, dwB === null ? null : dwB / 8);
      $("#rc-rows").innerHTML = rows.join("");
      $("#rc-ha").innerHTML = na; $("#rc-hb").innerHTML = nb;
      var gap = Math.abs(sa - sb), win = sa < sb ? na : nb, pill, h, p;
      var who = { beg: "a beginner", int: "an improving player", adv: "an advanced player" }[rv.lvl] + { ctrl: " who likes control", both: " with an all-round game", pow: " who likes power" }[rv.style] + (rv.arm === "sore" ? " with a sore arm" : "");
      if (gap < 1.5) { pill = "Close call"; h = "Both could suit you"; p = "For " + who + ", these two are close on paper. Try both if you can, or pick the one that feels better after a few games."; }
      else { pill = gap > 5 ? "Clear winner" : "Leans one way"; h = win + " suits you better"; p = "For " + who + ", " + win + " is closer to the shape, balance, core and face we would suggest (" + SH[I.shape].toLowerCase() + ", " + I.b[0] + " to " + I.b[1] + " mm balance, " + CO[I.core].toLowerCase() + " core, " + I.w[0] + " to " + I.w[1] + " g). A ✓ marks the better fit on each spec."; }
      $("#rc-pill").textContent = pill; $("#rc-pill").className = "pill " + (gap < 1.5 ? "i" : "b");
      $("#rc-h").innerHTML = h; $("#rc-p").innerHTML = p;
      $("#rc-t").innerHTML = "Shape and balance count most, weight least. Next: " + lbl("racket-balance", "draw both to scale") + " · " + lbl("racket-finder", "racket finder");
      store.set("pgb-rc", { v: rv, aw: wA, bw: wB, ab: bA, bb: bB });
    };
    var saved = store.get("pgb-rc", null);
    if (saved && saved.v) {
      Object.keys(saved.v).forEach(function (k) { rv[k] = saved.v[k]; });
      [["rc-a-w", saved.aw], ["rc-b-w", saved.bw], ["rc-a-b", saved.ab], ["rc-b-b", saved.bb]].forEach(function (x) { if (x[1] !== null && x[1] !== undefined && $("#" + x[0])) $("#" + x[0]).value = x[1]; });
      $$("[data-rc]").forEach(function (g) { var val = rv[g.dataset.rc]; $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === val ? "true" : "false"); }); });
    }
    $$("[data-rc]").forEach(function (g) { choose(g, function (v) { rv[g.dataset.rc] = v; rcrender(); }); });
    ["rc-a-w", "rc-b-w", "rc-a-b", "rc-b-b", "rc-a-name", "rc-b-name"].forEach(function (id) { var el = $("#" + id); if (el) el.addEventListener("input", rcrender); });
    var rcc = $("#rc-copy");
    if (rcc) rcc.addEventListener("click", function () {
      var txt = $("#rc-h").textContent + "\n" + $$("#rc-rows tr").map(function (tr) { return $$("td", tr).map(function (td) { return td.textContent; }).join(" | "); }).join("\n") + "\n" + location.href;
      try { navigator.clipboard.writeText(txt).then(function () { toast("Comparison copied"); }); } catch (e) { toast("Copy not available"); }
    });
    rcrender();
  }

  /* ---------- split-step reaction trainer ---------- */
  var fwb = $("#fwt");
  if (fwb) {
    var fv = { pace: "med", len: String(store.get("pgb-fw-len", "60")), mode: "net", beep: "on" };
    $$("[data-fwt]", fwb).forEach(function (g) { if (g.dataset.fwt === "len") $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === fv.len ? "true" : "false"); }); });
    var DIRS = { net: ["← Left volley", "Right volley →", "↑ Lob! Turn and go back"], back: ["← Left", "Right →", "↓ Short ball: move in", "Glass: step back and wait"] };
    DIRS.all = DIRS.net.concat(DIRS.back.slice(2));
    var PACE = { slow: [5000, 7000], med: [3500, 5000], fast: [2500, 3500] };
    var ftimer = null, fend = 0, freps = 0, fnext = null, actx = null;
    var fmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var beep = function () {
      if (fv.beep !== "on") return;
      try { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); var o = actx.createOscillator(), g = actx.createGain(); o.frequency.value = 880; g.gain.value = 0.15; o.connect(g); g.connect(actx.destination); o.start(); o.stop(actx.currentTime + 0.12); } catch (e) {}
    };
    var cue = $("#fwt-cue"), dir = $("#fwt-dir"), stage = $("#fwt-stage");
    var fstop = function (done) {
      clearInterval(ftimer); clearTimeout(fnext); ftimer = null;
      $("#fwt-go").disabled = false; $("#fwt-stop").disabled = true; stage.classList.remove("on", "hit");
      cue.textContent = done ? "Done" : "Stopped"; dir.textContent = freps + " split steps. " + (done ? "Rest 1 minute, then go again." : "");
    };
    var frep = function () {
      if (!ftimer) return;
      var list = DIRS[fv.mode], p = PACE[fv.pace];
      stage.classList.add("hit"); cue.textContent = "Split"; dir.textContent = ""; beep();
      setTimeout(function () { if (!ftimer) return; stage.classList.remove("hit"); cue.textContent = "Go"; dir.textContent = list[Math.floor(Math.random() * list.length)]; }, 380);
      freps++; $("#fwt-reps").textContent = freps + " reps";
      fnext = setTimeout(frep, p[0] + Math.random() * (p[1] - p[0]));
    };
    $$("[data-fwt]", fwb).forEach(function (g) { choose(g, function (v) { fv[g.dataset.fwt] = v; if (g.dataset.fwt === "len") { store.set("pgb-fw-len", v); if (!ftimer) $("#fwt-time").textContent = fmt(+v); } }); });
    $("#fwt-time").textContent = fmt(+fv.len);
    $("#fwt-go").addEventListener("click", function () {
      freps = 0; $("#fwt-reps").textContent = "0 reps"; fend = Date.now() + (+fv.len) * 1000 + 3000;
      $("#fwt-go").disabled = true; $("#fwt-stop").disabled = false; stage.classList.add("on");
      cue.textContent = "Get ready"; dir.textContent = "Ready position, racket up";
      ftimer = setInterval(function () { var left = (fend - Date.now()) / 1000; $("#fwt-time").textContent = fmt(Math.min(left, +fv.len)); if (left <= 0) fstop(true); }, 250);
      fnext = setTimeout(frep, 3000);
    });
    $("#fwt-stop").addEventListener("click", function () { fstop(false); });
  }

  /* ---------- middle ball decider ---------- */
  var pcb = $("#pcd");
  if (pcb) {
    var cv2 = { hands: "rr", ball: "low", pos: "net" };
    var pcrender = function () {
      var H = cv2.hands, B = cv2.ball, P = cv2.pos, who, why, call = "Mine", pill = "Rule of thumb";
      var fhMid = { rr: "left", ll: "right", lr: "both", ll2: "none" }[H];
      if (P === "split" && B !== "glass") {
        if (B === "lob") { who = "The player at the back"; why = "The net player can't reach it, so the back player takes it and the net player moves back too, or across if needed."; call = "Switch / yours"; }
        else { who = "The net player, if they can reach it"; why = "Anything the net player can volley comfortably is theirs. Whatever passes them belongs to the player at the back. Then get level again: both up or both back."; }
      } else if (B === "serve") {
        who = "The net player, if it is within reach"; why = "On a return down the middle, the server's partner at the net is closer and should volley it. The server is still moving in and takes what passes."; call = "Mine (net player)";
      } else if (fhMid === "left" || fhMid === "right") {
        var side = fhMid === "left" ? "left-side" : "right-side";
        who = "The " + side + " player";
        why = "The middle is their forehand side" + (B === "lob" ? ", so they can take a middle lob with a bandeja or smash. Exception: if their partner is clearly better placed, the partner calls it early." : (B === "glass" ? ". Off the back glass the forehand has more room to turn and hit." : ". Forehand volleys are usually stronger and easier to aim down the middle."));
      } else if (fhMid === "both") {
        pill = "Agree first"; who = B === "lob" ? "The player with the better overhead" : "The player further forward, or whoever calls first";
        why = "With a lefty on the right, both forehands meet in the middle. That is a strength, but both of you will want it. Agree before the match who takes it, call very early, and the other player covers behind.";
      } else {
        pill = "Agree first"; who = B === "lob" ? "The player with the better backhand overhead" : "The player who is closer, or whoever calls first";
        why = "With a lefty on the left, both backhands meet in the middle, which is the weak spot opponents aim for. Agree a rule before the match and call every middle ball early. Many pairs like this switch sides so both forehands face the middle.";
      }
      $("#pcd-pill").textContent = pill; $("#pcd-pill").className = "pill " + (pill === "Agree first" ? "i" : "b");
      $("#pcd-h").textContent = who; $("#pcd-p").textContent = why + " Call: \"" + call + "\", before the ball crosses the net.";
      $("#pcd-t").innerHTML = "Your pair's own agreed rule always wins. Next: " + lbl("which-side-padel", "left or right side quiz") + " · " + lbl("positioning", "where to stand");
    };
    $$("[data-pcd]", pcb).forEach(function (g) { choose(g, function (v) { cv2[g.dataset.pcd] = v; pcrender(); }); });
    pcrender();
  }

  /* ---------- padel rules quiz ---------- */
  var rqb = $("#rq");
  if (rqb) {
    var rlk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var qs = $$(".rq-q", rqb), cur = 0, right = 0, done = 0, wrong = [];
    var rqshow = function () {
      $("#rq-h").textContent = right + " / " + done;
      $("#rq-bar").style.width = Math.round(done / qs.length * 100) + "%";
    };
    qs.forEach(function (q, i) {
      $$("button", q).forEach(function (b) {
        b.addEventListener("click", function () {
          if (q.dataset.done) return;
          q.dataset.done = "1"; done++;
          var c = q.dataset.c, ok = b.dataset.v === c;
          $$("button", q).forEach(function (x) {
            x.disabled = true;
            x.style.opacity = "1"; x.style.cursor = "default"; if (x.dataset.v === c) { x.style.background = "#eef9b8"; x.style.borderColor = "#9fb400"; x.style.color = "#0b1530"; x.textContent = "✓ " + x.textContent; }
            else if (x === b) { x.textContent = "✗ " + x.textContent; x.style.borderColor = "#ff9b78"; }
          });
          if (ok) right++; else wrong.push(q.dataset.l);
          var why = $(".rq-why", q); why.hidden = false;
          why.innerHTML = "<strong>" + (ok ? "Right." : "Not quite.") + "</strong> " + why.textContent;
          $("#rq-p").textContent = ok ? "Correct. Read why, then go on." : "That one catches a lot of players. Read why, then go on.";
          $("#rq-t").innerHTML = "Full rule: " + rlk(q.dataset.l, q.dataset.l.replace(/-/g, " "));
          rqshow();
          if (i < qs.length - 1) { $("#rq-next").hidden = false; $("#rq-next").focus(); }
          else {
            var pct = right / qs.length, msg;
            if (pct === 1) msg = "Perfect. You could referee your club's next tournament.";
            else if (pct >= 0.8) msg = "Very good. You know the rules better than most club players.";
            else if (pct >= 0.5) msg = "Not bad. A few rules still trip you up: worth a quick read before your next match.";
            else msg = "Plenty to learn, and that is normal for new players. Start with the rules page below.";
            $("#rq-pill").textContent = "Final score";
            $("#rq-p").textContent = msg;
            var seen = {}, rev = wrong.filter(function (x) { if (seen[x]) return false; seen[x] = 1; return true; });
            $("#rq-t").innerHTML = rev.length ? "Read again: " + rev.map(function (x) { return rlk(x, x.replace(/-/g, " ")); }).join(" · ") : "Next: " + rlk("rules", "all padel rules") + " · " + rlk("golden-point-star-point", "golden point and Star Point");
            $("#rq-copy").hidden = false; $("#rq-again").hidden = false;
          }
        });
      });
    });
    $("#rq-next").addEventListener("click", function () {
      qs[cur].hidden = true; cur++; qs[cur].hidden = false; $("#rq-next").hidden = true;
      var f = $("button", qs[cur]); if (f) f.focus();
    });
    $("#rq-again").addEventListener("click", function () { location.reload(); });
    $("#rq-copy").addEventListener("click", function () {
      var txt = "I scored " + right + "/" + qs.length + " on the padel rules quiz. Can you beat it? " + location.href.split("#")[0];
      try { navigator.clipboard.writeText(txt).then(function () { toast("Score copied"); }, function () { toast(txt); }); } catch (e) { toast(txt); }
    });
    rqshow();
  }

  /* ---------- junior padel planner ---------- */
  var jpb = $("#jp-out");
  if (jpb) {
    var jlk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var jv = store.get("pgb-jp", { age: "u12", exp: "new", goal: "fun", where: "uk" });
    var jprender = function () {
      var A = jv.age, X = jv.exp, G = jv.goal, W = jv.where;
      var rk = { u8: "Lightest junior racket, well under 300 g", u12: "About 260 to 330 g, round, soft core", u14: "About 300 to 355 g, round or teardrop", u18: "Light adult racket, about 340 to 360 g" }[A];
      var ball = (A === "u8" || (A === "u12" && X === "new")) ? "Foam or low-compression balls" : (A === "u12" ? "Low-compression, moving to normal balls" : "Normal padel balls");
      var sess = A === "u8" ? "30 to 45 minutes" : (A === "u18" && X === "reg" && G !== "fun" ? "60 to 90 minutes" : "About 60 minutes");
      var score = X === "new" ? "Rally scoring, double bounce allowed at first" : (X === "some" ? "Short games to 7 or 11, then normal scoring" : "Normal padel scoring with golden point");
      var freq = G === "fun" ? "Once a week, with friends" : (G === "better" ? "One group lesson plus one play session a week" : "Two or more sessions a week, plus matches");
      var comp;
      if (W === "uk") comp = (X === "new" || G === "fun") ? "LTA Team Challenge at your local venue: fun team matches" : (A === "u8" ? "Club games first; UK junior nationals start at 12U" : "LTA Youth Tour (half-day events, LTA ranking points), then the Junior National Championships (12U to 18U)");
      else if (W === "us") comp = (X === "new" || G === "fun") ? "A club junior programme or clinic" : "USPA junior tournaments once they are match-play ready";
      else comp = (X === "new" || G === "fun") ? "A club junior group" : "Your national federation's junior events; FIP runs international junior tournaments";
      var head = { u8: "Play first, rules later", u12: "Build the rallies", u14: "Learn the walls and the net", u18: "Ready for the full game" }[A];
      var intro = { u8: "At 5 to 7, short, game-based sessions with soft balls matter more than technique.", u12: "At 8 to 11, small groups and mini-rallies build skills fast.", u14: "At 12 to 13, most children can play the full court and start learning the walls.", u18: "At 14 to 17, teenagers can play with adults and enter age-group events." }[A];
      if (G === "comp" && X === "new") intro += " Give them a few months of regular play before the first tournament.";
      $("#jp-h").textContent = head; $("#jp-p").textContent = intro;
      var rows = [["Racket", rk], ["Ball", ball], ["Session", sess], ["Group", "4 to 8 children per coach"], ["Scoring", score], ["How often", freq], ["Next step", comp]];
      $("#jp-spec").innerHTML = rows.map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + r[1] + "</dd>"; }).join("");
      $("#jp-t").innerHTML = "Exact racket weight: " + jlk("padel-racket-for-kids", "junior racket finder") + " · Learn the rules: " + jlk("padel-rules-quiz", "rules quiz");
      store.set("pgb-jp", jv);
    };
    $$("[data-jp]").forEach(function (g) {
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === jv[g.dataset.jp] ? "true" : "false"); });
      choose(g, function (v) { jv[g.dataset.jp] = v; jprender(); });
    });
    $("#jp-copy").addEventListener("click", function () {
      var txt = $("#jp-h").textContent + "\n" + $$("#jp-spec dt").map(function (d) { return d.textContent + ": " + d.nextSibling.textContent; }).join("\n");
      try { navigator.clipboard.writeText(txt).then(function () { toast("Plan copied"); }, function () { toast("Copy failed"); }); } catch (e) { toast("Copy failed"); }
    });
    jprender();
  }

  /* ---------- bandeja fault fixer ---------- */
  var bjb = $("#bjf");
  if (bjb) {
    var BJ = {
      net: ["Ball into the net", "You let it drop too low, or swung straight down like a smash.", "Hit it higher, about eye height, in front of you. Swing forward and across your body, not down."],
      long: ["Ball flies long into their back glass hard", "Too much pace, or the racket face is open and flat.", "Slow the swing, slice under the ball and aim just past their service line. The bandeja is not meant to win the point."],
      short: ["Ball sits up short in the middle", "Hit too softly, or contact too far behind your head.", "Turn sideways earlier so the ball stays in front, and push through towards the target. Aim deep, past the service line."],
      late: ["Always late, ball behind my head", "You face the net and step back too late.", "Turn your body side-on the moment you see the lob, racket up like holding a tray, and move back with side steps."],
      stuck: ["I stay back after the shot", "You watch the ball instead of moving.", "Let the swing carry your weight forward and walk back up to the net, level with your partner."],
      arm: ["It hurts my shoulder or elbow", "You are muscling it with the arm only.", "Use the body turn and keep the swing smooth and slow. If pain lasts, rest and see a physio; check the arm-load tips on padel elbow."]
    };
    var bjrender = function (k) {
      var r = BJ[k];
      $("#bjf-h").textContent = r[0]; $("#bjf-p").innerHTML = "<strong>Why:</strong> " + r[1] + "<br><strong>Fix:</strong> " + r[2];
    };
    choose($("[data-bjf]"), bjrender);
    bjrender("net");
  }

  /* ---------- court surface checker ---------- */
  var csb = $("#cs-out");
  if (csb) {
    var clk = function (f, t) { return '<a href="' + (location.protocol === "file:" ? f + ".html" : "/" + f) + '" style="color:#e8f84a">' + t + "</a>"; };
    var cv = store.get("pgb-cs", { where: "out", sand: "some", fib: "dk", cond: "dry" });
    var csrender = function () {
      var name, speed, bounce, sole, tip, why;
      if (cv.fib === "flat") {
        name = "Porous concrete or cement"; speed = "Fast"; bounce = "High and true";
        sole = "Hard-court or hybrid sole, well cushioned"; tip = "The ball comes through quickly off the floor and glass: shorter backswings, and attack high balls.";
        why = "A hard floor with no fibres. Allowed by the rules, now mostly found on older courts.";
      } else {
        var mono = cv.fib === "mono", fibr = cv.fib === "fibr";
        var sc = (cv.sand === "lots" ? 2 : cv.sand === "some" ? 1 : 0) + (mono ? 1 : fibr ? -1 : 0) + (cv.cond === "damp" ? 1 : 0) + (cv.cond === "worn" ? 1 : 0) + (cv.where === "in" ? -0.5 : 0);
        name = (mono ? "Monofilament" : fibr ? "Fibrillated" : "Sand-filled") + " artificial grass" + (cv.sand === "none" ? ", low sand" : cv.sand === "lots" ? ", heavy sand" : "");
        if (sc >= 2.5) { speed = "Slow"; bounce = "Low, can skid"; tip = "Be patient: lob more, play deep and low, and finish at the net. Hard flat hits sit up less here."; }
        else if (sc >= 1) { speed = "Medium"; bounce = "Medium, even"; tip = "A normal club court: mix lobs and low balls to the feet, and use the back glass."; }
        else { speed = "Fast"; bounce = "Higher and livelier"; tip = "Shorter swings and earlier preparation. Smashes and fast balls off the glass come back quicker."; }
        sole = cv.sand === "none" ? "Omni (small studs) or hybrid" : (cv.sand === "lots" ? "Herringbone (zig-zag)" : "Herringbone or hybrid");
        why = mono ? "Straight, separate fibres usually mean a newer monofilament turf: even bounce and good grip." : fibr ? "Flat, split fibres are fibrillated turf: a bit faster and livelier, and it wears sooner." : "Most club courts are sand-filled grass. Look closer at the fibres to narrow it down.";
        if (cv.sand === "lots") why += " Lots of loose sand slows the ball and your feet slide more until it settles.";
        if (cv.sand === "none") why += " Very little sand can mean texturised low-sand turf, or a court that needs topping up.";
      }
      if (cv.cond === "damp") { why += " A damp or just-dried court plays heavy and slow; balls get heavy too."; }
      if (cv.cond === "worn") { why += " Worn, flat fibres make the ball skid or die and bald spots are slippery. Tell the club."; }
      if (cv.where === "out") why += " Outdoors, check rain, cold and wind before you play.";
      $("#cs-h").textContent = name;
      $("#cs-p").textContent = why;
      var rows = [["Speed", speed], ["Bounce", bounce], ["Shoes", sole], ["Tactic", tip]];
      $("#cs-spec").innerHTML = rows.map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + r[1] + "</dd>"; }).join("");
      $("#cs-t").innerHTML = "Shoes: " + clk("padel-shoes", "shoe finder") + " · " + (cv.where === "out" ? "Weather: " + clk("padel-weather", "weather checker") : "Balls: " + clk("padel-balls", "dead ball checker")) + " · Slow court: " + clk("padel-lob", "the lob");
      store.set("pgb-cs", cv);
    };
    $$("[data-cs]").forEach(function (g) {
      $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === cv[g.dataset.cs] ? "true" : "false"); });
      choose(g, function (v) { cv[g.dataset.cs] = v; csrender(); });
    });
    $("#cs-copy").addEventListener("click", function () {
      var txt = "My padel court: " + $("#cs-h").textContent + "\n" + $$("#cs-spec dt").map(function (d) { return d.textContent + ": " + d.nextSibling.textContent; }).join("\n");
      try { navigator.clipboard.writeText(txt).then(function () { toast("Result copied"); }, function () { toast("Copy failed"); }); } catch (e) { toast("Copy failed"); }
    });
    csrender();
  }

  /* ---------- rest timer (rules page) ---------- */
  var rtb = $("#rt");
  if (rtb) {
    var rtT = null, rtLeft = 0, rac = null, seg = $(".opts", rtb);
    var rbeep = function (f, d) { try { rac = rac || new (window.AudioContext || window.webkitAudioContext)(); var o = rac.createOscillator(), g = rac.createGain(); o.frequency.value = f; o.connect(g); g.connect(rac.destination); g.gain.setValueAtTime(0.2, rac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, rac.currentTime + d); o.start(); o.stop(rac.currentTime + d); } catch (e) {} };
    var fmt = function (n) { return Math.floor(n / 60) + ":" + ("0" + (n % 60)).slice(-2); };
    var rstop = function (msg) { clearInterval(rtT); rtT = null; $("#rt-msg").textContent = msg; };
    choose(seg, function (v) {
      clearInterval(rtT); rtLeft = +v; $("#rt-clock").textContent = fmt(rtLeft); $("#rt-msg").textContent = "Running...";
      rbeep(660, 0.1);
      rtT = setInterval(function () {
        rtLeft--; $("#rt-clock").textContent = fmt(Math.max(0, rtLeft));
        if (rtLeft === 5) rbeep(660, 0.12);
        if (rtLeft <= 0) { rbeep(990, 0.5); rstop("Time! Play the next point."); }
      }, 1000);
    });
    $("#rt-stop").addEventListener("click", function () { $$("button", seg).forEach(function (x) { x.setAttribute("aria-pressed", "false"); }); rstop("Stopped. Pick a break to start."); });
  }

  /* ---------- generic step timer (solo practice, workout) ---------- */
  function pgbStepTimer(px, getSteps, doneName, doneHow) {
    var W = { snd: store.get("pgb-" + px + "-snd", "on"), i: 0, left: 0, run: false }, tick = null, ac = null, lock = null, S = getSteps();
    var fmt = function (s) { s = Math.max(0, Math.ceil(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); };
    var beep = function (f, d) {
      if (W.snd !== "on") return;
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = f; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.18, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d); o.start(); o.stop(ac.currentTime + d); } catch (e) {}
    };
    var wake = function (on) {
      try { if (on && navigator.wakeLock && !lock) navigator.wakeLock.request("screen").then(function (l) { lock = l; l.addEventListener("release", function () { lock = null; }); }, function () {}); else if (!on && lock) { lock.release(); lock = null; } } catch (e) {}
    };
    var list = $("#" + px + "-list"), el = function (k) { return $("#" + px + "-" + k); };
    var total = function () { return S.reduce(function (a, s) { return a + s.t; }, 0); };
    var buildList = function () {
      list.innerHTML = S.map(function (s, n) { return '<li data-n="' + n + '"><b>' + (n + 1) + ". " + s.n + '</b><span class="pill">' + s.ph + '</span><span class="wu-t">' + fmt(s.t) + "</span><p>" + s.d + "</p></li>"; }).join("");
      $$("li", list).forEach(function (li) { li.addEventListener("click", function () { go(+li.dataset.n); }); });
      el("sum").textContent = S.length + " steps · " + Math.round(total() / 60) + " min";
    };
    var render = function () {
      var s = S[W.i], done = 0;
      for (var k = 0; k < W.i; k++) done += S[k].t;
      done += s.t - W.left;
      el("clock").textContent = fmt(W.left);
      el("of").textContent = "Step " + (W.i + 1) + " of " + S.length;
      el("ph").textContent = s.ph; el("name").textContent = s.n; el("how").textContent = s.d;
      el("next").textContent = W.i + 1 < S.length ? "Next: " + S[W.i + 1].n : "Last step. Nearly done!";
      el("arc").setAttribute("stroke-dashoffset", (326.7 * (1 - W.left / s.t)).toFixed(1));
      el("prog").style.width = (done / total() * 100) + "%";
      el("left").textContent = fmt(total() - done) + " left in total";
      el("go").textContent = W.run ? "Pause" : (W.left < s.t || W.i ? "Resume" : "Start");
      $$("li", list).forEach(function (li, n) { li.classList.toggle("on", n === W.i); li.classList.toggle("done", n < W.i); });
      $$("#" + px + "-snd button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === W.snd ? "true" : "false"); });
    };
    var stop = function () { W.run = false; clearInterval(tick); tick = null; wake(false); };
    var finish = function () {
      stop(); beep(880, 0.6);
      el("clock").textContent = "0:00"; el("name").textContent = doneName; el("how").textContent = doneHow;
      el("next").textContent = ""; el("prog").style.width = "100%"; el("left").textContent = ""; el("go").textContent = "Start again";
      $$("li", list).forEach(function (li) { li.classList.remove("on"); li.classList.add("done"); });
      W.i = 0; W.left = S[0].t; W.end = true;
    };
    var go = function (n) { W.end = false; W.i = Math.max(0, Math.min(S.length - 1, n)); W.left = S[W.i].t; W.last = Date.now(); render(); };
    var step = function () {
      var now = Date.now(); W.left -= (now - W.last) / 1000; W.last = now;
      var c = Math.ceil(W.left);
      if (c !== W.shown && c <= 3 && c > 0) beep(660, 0.12);
      W.shown = c;
      if (W.left <= 0) { if (W.i + 1 >= S.length) return finish(); beep(990, 0.35); go(W.i + 1); return; }
      render();
    };
    el("go").addEventListener("click", function () {
      if (W.run) { stop(); render(); return; }
      if (W.end) go(0);
      W.run = true; W.last = Date.now(); beep(990, 0.2); wake(true); tick = setInterval(step, 250); render();
    });
    el("skip").addEventListener("click", function () { if (W.i + 1 >= S.length) finish(); else go(W.i + 1); });
    el("back").addEventListener("click", function () { go(W.left < S[W.i].t - 2 ? W.i : W.i - 1); });
    $$("#" + px + "-snd button").forEach(function (b) { b.addEventListener("click", function () { W.snd = b.dataset.v; store.set("pgb-" + px + "-snd", W.snd); render(); }); });
    document.addEventListener("visibilitychange", function () { if (!document.hidden && W.run) wake(true); });
    buildList(); go(0);
    return { reload: function () { stop(); S = getSteps(); buildList(); go(0); } };
  }
  function pgbSegSet(px, keys, st, onChange) {
    keys.forEach(function (k) {
      var g = $("#" + px + "-" + k); if (!g) return;
      var mark = function () { $$("button", g).forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.v === st[k] ? "true" : "false"); }); };
      $$("button", g).forEach(function (b) { b.addEventListener("click", function () { if (st[k] === b.dataset.v) return; st[k] = b.dataset.v; mark(); onChange(); }); });
      mark();
    });
  }
  function pgbRR(items, tagOf) {
    var groups = {}, order = [], out = [];
    items.forEach(function (x) { var t = tagOf(x); if (!groups[t]) { groups[t] = []; order.push(t); } groups[t].push(x); });
    var more = true;
    while (more) { more = false; order.forEach(function (t) { if (groups[t].length) { out.push(groups[t].shift()); more = true; } }); }
    return out;
  }

  /* ---------- solo practice planner ---------- */
  if ($("#sp") && window.SP) (function () {
    var st = store.get("pgb-sp", { where: "c", focus: "all", len: "20" });
    var build = function () {
      var L = +st.len * 60, warm = Object.assign({}, window.SP.warm, { t: st.len === "10" ? 120 : 180 }), cool = Object.assign({}, window.SP.cool, { t: st.len === "10" ? 60 : 120 });
      var budget = L - warm.t - cool.t;
      var cand = window.SP.pool.filter(function (d) { return d.w.indexOf(st.where) >= 0; });
      var has = function (d, t) { return (" " + d.f + " ").indexOf(" " + t + " ") >= 0; };
      var ordered;
      if (st.focus === "all") ordered = pgbRR(cand, function (d) { return d.ph; });
      else ordered = cand.filter(function (d) { return has(d, st.focus); }).concat(pgbRR(cand.filter(function (d) { return !has(d, st.focus); }), function (d) { return d.ph; }));
      var pick = [], used = 0, pass = 0;
      while (used < budget - 45 && pass < 3) {
        ordered.forEach(function (d) {
          if (used + d.t <= budget) { pick.push(pass ? Object.assign({}, d, { n: d.n + " (again)" }) : d); used += d.t; }
        });
        pass++;
      }
      if (pick.length && budget - used > 0) pick[pick.length - 1] = Object.assign({}, pick[pick.length - 1], { t: pick[pick.length - 1].t + (budget - used) });
      if (st.focus !== "all") {
        var foc = pick.filter(function (d) { return has(d, st.focus); });
        if (!foc.length) pick.unshift({ n: "Tip: this focus needs a court or wall", ph: "Note", t: 15, d: "There are no drills for this focus in a home space, so the session mixes ball control, shadow swings and footwork instead.", w: "cwh", f: "" });
      }
      store.set("pgb-sp", st);
      return [warm].concat(pick, [cool]);
    };
    var T = pgbStepTimer("sp", build, "Session done. Nice work!", "Write down your best wall rally or serve score, and try to beat it next time.");
    pgbSegSet("sp", ["where", "focus", "len"], st, function () { T.reload(); });
  })();

  /* ---------- padel workout builder ---------- */
  if ($("#wo") && window.WO) (function () {
    var st = store.get("pgb-wo", { kit: "h", focus: "all", len: "25", lvl: "new" });
    var build = function () {
      var work = st.lvl === "reg" ? 45 : 40, rest = 60 - work;
      var plan = { "15": [5, 2], "25": [6, 3], "35": [7, 4] }[st.len] || [6, 3], N = plan[0], R = plan[1];
      var cand = window.WO.pool.filter(function (x) { return x.k.indexOf(st.kit) >= 0; });
      var has = function (x, t) { return (" " + x.f + " ").indexOf(" " + t + " ") >= 0; };
      var ordered = st.focus === "all" ? pgbRR(cand, function (x) { return x.f.split(" ")[0]; }) :
        cand.filter(function (x) { return has(x, st.focus); }).concat(pgbRR(cand.filter(function (x) { return !has(x, st.focus); }), function (x) { return x.f.split(" ")[0]; }));
      if (st.focus !== "all") { var f = ordered.filter(function (x) { return has(x, st.focus); }).slice(0, N - 1), o = ordered.filter(function (x) { return !has(x, st.focus); }); ordered = f.concat(o); }
      var ex = ordered.slice(0, N);
      var S = [{ n: "Warm up: march, arm circles, easy squats", ph: "Warm up", t: 180, d: "March or jog on the spot, big arm circles both ways, trunk turns, then 10 slow half squats and 5 lunges each leg." }];
      for (var r = 0; r < R; r++) {
        ex.forEach(function (x, i) {
          S.push({ n: x.n + (R > 1 ? " · round " + (r + 1) + " of " + R : ""), ph: x.ph, t: work, d: x.d });
          var last = i === ex.length - 1;
          if (!last) S.push({ n: "Rest", ph: "Rest", t: rest, d: "Breathe. Next: " + ex[i + 1].n + "." });
          else if (r < R - 1) S.push({ n: "Round rest", ph: "Rest", t: 60, d: "Drink some water. Next round starts with " + ex[0].n + "." });
        });
      }
      S.push({ n: "Stretch: calves, thighs, hips, forearm", ph: "Cool down", t: 120, d: "Slow, held stretches of 20 to 30 seconds. The full routine is on the cool-down timer page." });
      store.set("pgb-wo", st);
      return S;
    };
    var T = pgbStepTimer("wo", build, "Workout done. Great job!", "Two sessions a week is the target. Next time add a few reps, or a little weight when 12 clean reps feel easy.");
    pgbSegSet("wo", ["kit", "focus", "len", "lvl"], st, function () { T.reload(); });
  })();

})();
