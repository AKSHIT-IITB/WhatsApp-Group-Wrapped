// WhatsApp Wrapped 2024 - app.js

// ---- member colors (dynamic, stays in JS) ----
var members = ["Aryan", "Akshit", "Yash", "Shreya", "Dev", "Kavya", "Joshmitha", "Tanvi"];

function getColor(name) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(`--c-${name.toLowerCase()}`)
    .trim() || "#7c83ff";
}

function getInitials(name) {
  return name.slice(0, 2).toUpperCase();
}

function formatNum(n) {
  if (n == null || isNaN(n)) return "—";
  return n.toLocaleString();
}

function ghostColor(p) {
  if (p > 40) return "#f87171";   // soft red
  if (p > 25) return "#fbbf24";   // soft amber
  return "#4ade80";               // soft green
}

function killColor(score) {
  if (score > 8) return "#ff4545";
  if (score > 4) return "#ffbe45";
  return "#34d399";
}

function getRank(obj, name) {
  var sorted = Object.entries(obj).sort(function(a, b) { return b[1] - a[1]; });
  for (var i = 0; i < sorted.length; i++) {
    if (sorted[i][0] === name) return i + 1;
  }
  return sorted.length;
}

// ---- global state ----
var data = null;
var slides = [];
var currentSlide = 0;

// ---- boot ----
async function boot() {
  try {
    var res = await fetch("data.json");
    data = await res.json();
  } catch (e) {
    data = EMBEDDED_DATA;
  }
  slides = buildAllSlides(data);
  showSlide(0);
  setupControls();
  document.getElementById("slide-total").textContent = "/ " + slides.length;
}

// ---- slide engine ----
function showSlide(index) {
  var container = document.getElementById("slides");

  var oldSlide = container.querySelector(".slide.active");
  if (oldSlide) {
    oldSlide.classList.remove("active");
    oldSlide.classList.add("exit");
    setTimeout(function() {
      if (oldSlide.parentNode) oldSlide.parentNode.removeChild(oldSlide);
    }, 480);
  }

  var newSlide = document.createElement("div");
  newSlide.className = "slide";
  newSlide.innerHTML = slides[index].getHTML();
  container.appendChild(newSlide);

  requestAnimationFrame(function() {
    requestAnimationFrame(function() {
      newSlide.classList.add("active");
      if (slides[index].onEnter) {
        slides[index].onEnter(newSlide);
      }
    });
  });

  document.getElementById("slide-counter").textContent = index + 1;
  document.getElementById("btn-prev").disabled = (index === 0);
  document.getElementById("btn-next").disabled = (index === slides.length - 1);
  currentSlide = index;
}

function goToNext() {
  if (currentSlide < slides.length - 1) showSlide(currentSlide + 1);
}

function goToPrev() {
  if (currentSlide > 0) showSlide(currentSlide - 1);
}

// ---- controls ----
function setupControls() {
  document.getElementById("btn-next").addEventListener("click", goToNext);
  document.getElementById("btn-prev").addEventListener("click", goToPrev);

  document.addEventListener("keydown", function(e) {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); goToNext(); }
    if (e.key === "ArrowLeft") { e.preventDefault(); goToPrev(); }
  });

  document.getElementById("slides").addEventListener("click", function(e) {
    if (!e.target.closest("#nav")) goToNext();
  });

  var touchStartX = null;
  document.addEventListener("touchstart", function(e) {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });
  document.addEventListener("touchend", function(e) {
    if (touchStartX === null) return;
    var diff = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(diff) > 50) diff < 0 ? goToNext() : goToPrev();
    touchStartX = null;
  }, { passive: true });
}

// ---- animation helpers ----
function animateBars(root) {
  var bars = root.querySelectorAll(".bar-fill[data-w]");
  for (var i = 0; i < bars.length; i++) {
    var bar = bars[i];
    var target = bar.getAttribute("data-w");
    setTimeout(function(b, t) { b.style.width = t + "%"; }, 80, bar, target);
  }
}

function animateGhostBars(root) {
  var bars = root.querySelectorAll(".ghost-fill[data-w]");
  for (var i = 0; i < bars.length; i++) {
    var bar = bars[i];
    var target = bar.getAttribute("data-w");
    setTimeout(function(b, t) { b.style.width = t + "%"; }, 80, bar, target);
  }
}

function animatePodium(root) {
  var bars = root.querySelectorAll(".podium-bar[data-h]");
  for (var i = 0; i < bars.length; i++) {
    var bar = bars[i];
    var height = bar.getAttribute("data-h");
    setTimeout(function(b, h) { b.style.height = h + "px"; }, 100 + i * 80, bar, height);
  }
}

function animateBubbles(root) {
  var bubbles = root.querySelectorAll(".bubble");
  for (var i = 0; i < bubbles.length; i++) {
    setTimeout(function(b) { b.classList.add("pop"); }, 60 + i * 60, bubbles[i]);
  }
}

function animateTimeline(root) {
  var fill = root.querySelector(".tl-fill");
  if (fill) setTimeout(function() { fill.style.width = "100%"; }, 200);
}

// ===========================================================
// SLIDE BUILDERS — one function per slide
// ===========================================================

function slideIntro(d) {
  return {
    getHTML: function() {
      return `
        <div class="intro-bg"></div>
        <div class="intro-overlay"></div>
        <h1 class="intro-title">Your Group<br>Wrapped.</h1>
        </div>
      `;
    }
  };
}

function slideTotalMessages(d) {
  var s = d.stats;
  var sorted = Object.entries(s.total_messages).sort(function(a, b) { return b[1] - a[1]; });
  var max = sorted[0][1];
  var top = sorted[0];

  return {
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val = sorted[i][1];
        var pct = ((val / max) * 100).toFixed(1);
        var label = val > max * 0.3 ? formatNum(val) : "";
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct}" style="background:${getColor(name)};">${label}</div>
            </div>
            <span class="bar-val">${formatNum(val)}</span>
          </div>`;
      }
      return `
        <div class="slide-label">Stat 01 · Total Messages</div>
        <h2 class="slide-title">Who never shuts up?</h2>
        <p class="slide-sub">Messages sent per person, all time</p>
        <div class="bar-chart">${rows}</div>
      `;
    },
    onEnter: animateBars
  };
}

function slideWordCount(d) {
  var s = d.stats;
  var sorted = Object.entries(s.word_count).sort(function(a, b) { return b[1] - a[1]; });
  var max = sorted[0][1];
  var top = sorted[0];
  var bottom = sorted[sorted.length - 1];

  return {
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val = sorted[i][1];
        var pct = ((val / max) * 100).toFixed(1);
        var label = val > max * 0.3 ? formatNum(val) : "";
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct}" style="background:${getColor(name)};">${label}</div>
            </div>
            <span class="bar-val">${formatNum(val)}</span>
          </div>`;
      }
      var topWPM = (top[1] / s.total_messages[top[0]]).toFixed(1);
      var bottomWPM = (bottom[1] / s.total_messages[bottom[0]]).toFixed(1);
      return `
        <div class="blob" style="width:360px;height:360px;background:${getColor("Tanvi")};bottom:-90px;right:-80px;"></div>
        <div class="slide-label">Stat 02 · Word Count</div>
        <h2 class="slide-title">Words, words, words.</h2>
        <p class="slide-sub">Total words typed — emojis counted too</p>
        <div class="bar-chart">${rows}</div>
      `;
    },
    onEnter: animateBars
  };
}

function slideNightOwl(d) {
  var s = d.stats;
  var sorted = Object.entries(s.night_owl)
    .sort(function(a, b) { return b[1] - a[1]; })
  var max = sorted[0][1];
  var top = sorted[0];

  return {
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val = sorted[i][1];
        var pct = ((val / max) * 100).toFixed(1);
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track bar-track--short">
              <div class="bar-fill" data-w="${pct}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val">${val}</span>
          </div>`;
      }
      return `
        <div class="blob" style="width:340px;height:340px;background:#a78bfa;top:-70px;right:-70px;"></div>
        <div class="slide-label">Stat 03 · Night Owl</div>
        <h2 class="slide-title">Who's awake at 3am?</h2>
        <p class="slide-sub">Messages sent between midnight and 4am</p>
        <div class="night-owl-wrap">
          <div class="bar-chart bar-chart--narrow">${rows}</div>
        </div>
      `;
    },
    onEnter: animateBars
  };
}

function slideGhostReport(d) {
  var s = d.stats;

  var sorted = Object.entries(s.ghost.ghost_percentage)
    .sort(function(a, b) { return b[1] - a[1]; });

  var max = sorted[0][1];  // 🔥 THIS was missing

  return {
    getHTML: function() {
      var items = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var p = sorted[i][1];

        var pct = ((p / max) * 100).toFixed(1); // 🔥 correct scaling

        items += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val" style="color:${getColor(name)};">
                ${p.toFixed(1)}%
            </span>
          </div>`;
      }

      return `
        <div class="slide-label">Stat 04 · Ghost Report</div>
        <h2 class="slide-title">The ghosting report.</h2>
        <p class="slide-sub">% of messages with no reply within 10 minutes</p>
        <div class="ghost-row">
          ${items}
        </div>
      `;
    },
    onEnter: animateBars
  };
}

function slideConversationStarter(d) {
  var s = d.stats;
  var sorted = Object.entries(s.conversation_starter)
    .sort(function(a, b) { return b[1] - a[1]; });

  var podiumOrder = [sorted[1], sorted[0], sorted[2]];
  var podiumHeights = [150, 195, 118];
  var medals = ["🥈", "🥇", "🥉"];

  return {
    getHTML: function() {
      var podiumHTML = "";

      for (var i = 0; i < podiumOrder.length; i++) {
        var name = podiumOrder[i][0];
        var val = podiumOrder[i][1];

        podiumHTML += `
          <div class="podium-item">
            
            <!-- 🔴 CHANGE 1: removed initials from avatar -->
            <div class="avatar podium-avatar" style="background:${getColor(name)};"></div>

            <!-- medal stays -->
            <span class="podium-medal">${medals[i]}</span>

            <!-- bar -->
            <div class="podium-bar" data-h="${podiumHeights[i]}" style="background:${getColor(name)};">
              ${val}
            </div>

            <!-- 🔴 CHANGE 2: full name shown here (already correct, just kept) -->
            <span class="podium-label">${name}</span>

          </div>`;
      }

      return `
        <!-- 🔴 CHANGE 3: added spacing wrapper -->
        <div class="podium-container">

          <div class="slide-label">Stat 05 · Conversation Starter</div>
          <h2 class="slide-title">Who keeps this group alive?</h2>
          <p class="slide-sub">Times they broke a 60-minute silence</p>

          <!-- 🔴 CHANGE 4: added margin class -->
          <div class="podium-wrap podium-wrap--spaced">
            ${podiumHTML}
          </div>

        </div>
      `;
    },
    onEnter: animatePodium
  };
}

function slideMostUsedEmoji(d) {
  var s = d.stats;

  return {
    getHTML: function() {
      var cards = "";
      for (var i = 0; i < members.length; i++) {
        var name = members[i];
        var top = s.most_used_emoji[name] || [];
        var emojisHTML = top.map(function(item) { return "<span>" + item[0] + "</span>"; }).join("");
        var countsHTML = top.map(function(item) { return '<span class="ec-count">' + item[1] + "×</span>"; }).join("");
        cards += `
          <div class="emoji-card">
            <div class="ec-name" style="color:${getColor(name)};">${name}</div>
            <div class="ec-emojis">${emojisHTML}</div>
            <div class="ec-counts">${countsHTML}</div>
          </div>`;
      }
      return `
        <div class="blob" style="width:300px;height:300px;background:#ff7c5c;bottom:-60px;right:-60px;"></div>
        <div class="slide-label">Stat 06 · Most Used Emoji</div>
        <h2 class="slide-title">Everyone's emoji signature.</h2>
        <p class="slide-sub">Top 3 emojis per person</p>
        <div class="emoji-grid">${cards}</div>
      `;
    }
  };
}

function slideBusiestDay(d) {
  var s = d.stats;

  return {
    getHTML: function() {
      var date = s.busiest_day[0];
      var count = s.busiest_day[1];
      var pct = ((count / d.total_messages_group) * 100).toFixed(1);
      return `
        <div class="blob" style="width:400px;height:400px;background:#34d399;top:-110px;right:-80px;"></div>
        <div class="slide-label">Stat 07 · Busiest Day</div>
        <h2 class="slide-title">The most chaotic day.</h2>
        <div class="big-number">${count}</div>
        <p class="busiest-day-sub">messages in a single day</p>
        <div class="card busiest-day-card">
          <div class="busiest-day-date">${date}</div>
        </div>
      `;
    }
  };
}

function slideLongestSilence(d) {
  var s = d.stats;

  return {
    getHTML: function() {
      var sil = s.longest_silence;
      return `
        <div class="blob silence-blob"></div>
        <div class="slide-label">Stat 08 · Longest Silence</div>
        <h2 class="slide-title">The great silence.</h2>
        <p class="slide-sub">Longest gap with zero messages</p>
        <div class="big-number silence-number">${sil.hours}h</div>
        <div class="silence-desc">
          nearly <strong>${sil.days} days</strong> of complete radio silence 😶
        </div>
        <div class="silence-timeline">
          <div class="tl-labels">
            <span>${sil.start}</span>
            <span>${sil.end}</span>
          </div>
          <div class="tl-track">
            <div class="tl-fill"></div>
          </div>
          <div class="tl-hours">${sil.hours} hours</div>
        </div>
        <div class="stat-pair silence-stat-pair">
          <div class="stat-box">
            <div class="sb-val silence-date-val">Nov 16</div>
            <div class="sb-lbl">last message</div>
          </div>
          <div class="stat-box">
            <div class="sb-val silence-revived-val">Nov 18</div>
            <div class="sb-lbl">group revived</div>
          </div>
        </div>
      `;
    },
    onEnter: animateTimeline
  };
}

function slideAvgResponseTime(d) {
  var s = d.stats;
  var respTimes = s.avg_response_time;
  var respVals = Object.values(respTimes).filter(function(v) { return v != null; });
  var respMin = Math.min.apply(null, respVals);
  var respMax = Math.max.apply(null, respVals);

  return {
    getHTML: function() {
      var bubblesHTML = "";
      for (var i = 0; i < members.length; i++) {
        var name = members[i];
        var val = respTimes[name];
        if (!val) continue;
        var norm = (val - respMin) / (respMax - respMin + 0.01);
        var size = Math.round(68 + norm * 44);
        bubblesHTML += `
          <div class="bubble" style="width:${size}px;height:${size}px;background:${getColor(name)};">
            <span class="b-name">${name.slice(0, 5)}</span>
            <span class="b-val">${val}m</span>
          </div>`;
      }
      return `
        <div class="blob" style="width:320px;height:320px;background:#43d8c9;top:-60px;right:-60px;"></div>
        <div class="slide-label">Stat 09 · Avg Response Time</div>
        <h2 class="slide-title">Reply speed report.</h2>
        <p class="slide-sub">Median minutes before replying · within a 60-min window</p>
        <div class="bubble-wrap">${bubblesHTML}</div>
      `;
    },
    onEnter: animateBubbles
  };
}

function slideHypePerson(d) {
  var s = d.stats;
  var sorted = Object.entries(s.hype_person)
    .filter(function(x) { return x[1] != null; })
    .sort(function(a, b) { return a[1] - b[1]; });
  var fastest = sorted[0];
  var max = sorted[sorted.length - 1][1];

  return {
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val = sorted[i][1];
        var pct = ((val / max) * 100).toFixed(1);
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track bar-track--medium">
              <div class="bar-fill" data-w="${pct}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val">${val.toFixed(1)}m</span>
          </div>`;
      }
      return `
        <div class="blob" style="width:360px;height:360px;background:#ff6584;bottom:-80px;right:-60px;"></div>
        <div class="slide-label">Stat 10 · Hype Person</div>
        <h2 class="slide-title">The group's hype person.</h2>
        <p class="slide-sub">Average minutes to reply — lower means more hyped</p>
        <div class="bar-chart bar-chart--narrow">${rows}</div>
      `;
    },
    onEnter: animateBars
  };
}

function slideConversationKiller(d) {
  var s = d.stats;
  var sorted = Object.entries(s.conversation_killer).sort(function(a, b) { return b[1].score - a[1].score; });
  var top = sorted[0];

  return {
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var dk = sorted[i][1];
        rows += `
          <tr>
            <td class="killer-name-cell">
              <div class="avatar killer-avatar" style="background:${getColor(name)};">${getInitials(name)}</div>
              ${name}
            </td>
            <td style="color:${getColor(name)};font-weight:700;">${dk.kills}</td>
            <td class="killer-total">${formatNum(dk.total)}</td>
            <td>
              <span class="score-pill" style="background:${killColor(dk.score)}22;color:${killColor(dk.score)};">
                ${dk.score.toFixed(1)}%
              </span>
            </td>
          </tr>`;
      }
      return `
        <div class="blob" style="width:300px;height:300px;background:#ff4545;bottom:-60px;left:-60px;"></div>
        <div class="slide-label">Custom Stat ✦ · Conversation Killer</div>
        <h2 class="slide-title">Conversation killers.</h2>
        <p class="slide-sub">% of your messages that ended the chat cold — no reply for 60+ min</p>
        <table class="killer-table">
          <thead>
            <tr>
              <th>Person</th><th>Kill shots</th><th>Total msgs</th><th>Kill rate</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      `;
    }
  };
}

function slideProfilePicker() {
  return {
    getHTML: function() {
      var buttons = "";
      for (var i = 0; i < members.length; i++) {
        var name = members[i];
        buttons += `
          <button class="picker-btn" data-name="${name}" style="border-color:${getColor(name)}44;">
            <div class="picker-avatar" style="background:${getColor(name)};">${getInitials(name)}</div>
            <span class="picker-name">${name}</span>
          </button>`;
      }
      return `
        <div class="blob" style="width:420px;height:420px;background:#25d366;top:-120px;right:-100px;"></div>
        <div class="blob" style="width:280px;height:280px;background:#f472b6;bottom:-80px;left:-80px;"></div>
        <div class="slide-label">Per-Person Profiles</div>
        <p class="slide-sub">Select a member to see their full stats</p>
        <div class="picker-grid">${buttons}</div>
      `;
    },
    onEnter: function(root) {
      var btns = root.querySelectorAll(".picker-btn");
      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", function(e) {
          e.stopPropagation();
          var name = this.getAttribute("data-name");
          var idx = members.indexOf(name);
          showSlide(13 + idx);
        });
      }
    }
  };
}

function slideProfile(name, s) {
  var color = getColor(name);
  var msgs      = s.total_messages[name] || 0;
  var words     = s.word_count[name] || 0;
  var nightMsgs = s.night_owl[name] || 0;
  var ghostPct  = s.ghost.ghost_percentage[name] != null ? s.ghost.ghost_percentage[name] : 0;
  var starts    = s.conversation_starter[name] || 0;
  var emojis    = s.most_used_emoji[name] || [];
  var respTime  = s.avg_response_time[name];
  var hypeTime  = s.hype_person[name];
  var killer    = s.conversation_killer[name] || { kills: 0, total: 0, score: 0 };

  var maxMsgs  = Math.max.apply(null, Object.values(s.total_messages));
  var maxWords = Math.max.apply(null, Object.values(s.word_count));
  var msgsPct  = ((msgs / maxMsgs) * 100).toFixed(1);
  var wordsPct = ((words / maxWords) * 100).toFixed(1);
  var wpm      = msgs > 0 ? (words / msgs).toFixed(1) : "—";
  var memberIndex = members.indexOf(name);

  function getPersonality() {
    if (msgs === Math.max.apply(null, Object.values(s.total_messages)))            return { label: "The Chatterbox",           emoji: "💬" };
    if (nightMsgs === Math.max.apply(null, Object.values(s.night_owl)))            return { label: "The Night Owl",            emoji: "🦉" };
    if (words === Math.max.apply(null, Object.values(s.word_count)))               return { label: "The Essay Writer",         emoji: "📝" };
    if (starts === Math.max.apply(null, Object.values(s.conversation_starter)))    return { label: "The Conversation Starter", emoji: "🚀" };
    if (ghostPct === Math.max.apply(null, Object.values(s.ghost.ghost_percentage)))return { label: "The Ghost",                emoji: "👻" };
    if (killer.score === Math.max.apply(null, Object.values(s.conversation_killer).map(function(v) { return v.score; }))) return { label: "The Killer", emoji: "💀" };
    if (msgs === Math.min.apply(null, Object.values(s.total_messages)))            return { label: "The Lurker",               emoji: "👁️" };
    return { label: "The Regular", emoji: "😎" };
  }

  var personality = getPersonality();
  var gCol = ghostColor(ghostPct);
  var kCol = killColor(killer.score);

  var emojisHTML = emojis.map(function(item) {
    return '<div class="pe-item"><span class="pe-emoji">' + item[0] + '</span><span class="pe-count">' + item[1] + '×</span></div>';
  }).join("") || '<span class="pe-none">none recorded</span>';

  return {
    getHTML: function() {
      return `
        <div class="blob profile-blob-large" style="background:${color};"></div>
        <div class="blob profile-blob-small" style="background:${color};"></div>
        <div class="profile-layout">
          <div class="profile-left">
            <div class="slide-label" style="color:${color};">Profile · ${memberIndex + 1} of ${members.length}</div>
            <div class="profile-avatar" style="background:${color};">${getInitials(name)}</div>
            <div class="profile-name" style="color:${color};">${name}</div>
            <div class="personality-badge" style="background:${color}22;border-color:${color}44;">
              <span>${personality.emoji}</span>
              <span>${personality.label}</span>
            </div>
            <div class="profile-emojis">
              <div class="pe-label">signature emojis</div>
              <div class="pe-row">${emojisHTML}</div>
            </div>
          </div>
          <div class="profile-right">
            <div class="ps-row">
              <div class="ps-card">
                <div class="ps-val" style="color:${color};">${formatNum(msgs)}</div>
                <div class="ps-lbl">messages sent</div>
                <div class="ps-rank">#${getRank(s.total_messages, name)} in group</div>
                <div class="ps-bar-track">
                  <div class="ps-bar-fill" data-w="${msgsPct}" style="background:${color};"></div>
                </div>
              </div>
              <div class="ps-card">
                <div class="ps-val" style="color:${color};">${formatNum(words)}</div>
                <div class="ps-lbl">words typed</div>
                <div class="ps-rank">#${getRank(s.word_count, name)} in group</div>
                <div class="ps-bar-track">
                  <div class="ps-bar-fill" data-w="${wordsPct}" style="background:${color};"></div>
                </div>
              </div>
            </div>
            <div class="ps-row">
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm">${nightMsgs}</div>
                <div class="ps-lbl">late-night msgs</div>
                <div class="ps-rank">midnight–4am</div>
              </div>
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm">${starts}</div>
                <div class="ps-lbl">convos started</div>
                <div class="ps-rank">after 60min silence</div>
              </div>
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm" style="color:${gCol};">${ghostPct.toFixed(0)}%</div>
                <div class="ps-lbl">ghost rate</div>
                <div class="ps-rank">msgs ignored</div>
              </div>
            </div>
            <div class="ps-row">
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm">${respTime != null ? respTime + "m" : "—"}</div>
                <div class="ps-lbl">median reply time</div>
                <div class="ps-rank">when replying</div>
              </div>
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm">${hypeTime != null ? hypeTime.toFixed(1) + "m" : "—"}</div>
                <div class="ps-lbl">avg reply to others</div>
                <div class="ps-rank">hype score</div>
              </div>
              <div class="ps-card ps-card--half">
                <div class="ps-val ps-val--sm" style="color:${kCol};">${killer.score.toFixed(1)}%</div>
                <div class="ps-lbl">kill rate</div>
                <div class="ps-rank">${killer.kills} convos ended</div>
              </div>
            </div>
            <div class="ps-wpm">
              <span class="ps-wpm-val" style="color:${color};">${wpm}</span>
              <span class="ps-wpm-lbl">avg words per message</span>
            </div>
          </div>
        </div>
      `;
    },
    onEnter: function(root) {
      var bars = root.querySelectorAll(".ps-bar-fill[data-w]");
      for (var i = 0; i < bars.length; i++) {
        var bar = bars[i];
        var w = bar.getAttribute("data-w");
        setTimeout(function(b, target) { b.style.width = target + "%"; }, 120, bar, w);
      }
    }
  };
}

// ---- assemble all slides in order ----
function buildAllSlides(d) {
  var s = d.stats;
  var allSlides = [];

  allSlides.push(slideIntro(d));
  allSlides.push(slideTotalMessages(d));
  allSlides.push(slideWordCount(d));
  allSlides.push(slideNightOwl(d));
  allSlides.push(slideGhostReport(d));
  allSlides.push(slideConversationStarter(d));
  allSlides.push(slideMostUsedEmoji(d));
  allSlides.push(slideBusiestDay(d));
  allSlides.push(slideLongestSilence(d));
  allSlides.push(slideAvgResponseTime(d));
  allSlides.push(slideHypePerson(d));
  allSlides.push(slideConversationKiller(d));
  allSlides.push(slideProfilePicker());

  for (var i = 0; i < members.length; i++) {
    allSlides.push(slideProfile(members[i], s));
  }

  return allSlides;
}

// ---- fallback data ----
var EMBEDDED_DATA = {
  "total_messages_group": 3759,
  "stats": {
    "total_messages": {"Aryan":1657,"Akshit":524,"Yash":247,"Shreya":66,"Dev":262,"Kavya":8,"Joshmitha":337,"Tanvi":658},
    "word_count": {"Aryan":6550,"Akshit":3563,"Yash":290,"Shreya":2885,"Dev":1984,"Kavya":24,"Joshmitha":3922,"Tanvi":7663},
    "night_owl": {"Aryan":216,"Akshit":254,"Yash":0,"Shreya":0,"Dev":0,"Kavya":0,"Joshmitha":12,"Tanvi":68},
    "ghost": {
      "ghosted_counts": {"Aryan":218,"Akshit":126,"Yash":86,"Shreya":22,"Dev":30,"Kavya":4,"Joshmitha":108,"Tanvi":170},
      "msg_counts": {"Aryan":1657,"Akshit":524,"Yash":247,"Shreya":66,"Dev":262,"Kavya":8,"Joshmitha":337,"Tanvi":658},
      "ghost_percentage": {"Aryan":13.16,"Akshit":24.05,"Yash":34.82,"Shreya":33.33,"Dev":11.45,"Kavya":50.0,"Joshmitha":32.05,"Tanvi":25.84}
    },
    "conversation_starter": {"Aryan":18,"Akshit":6,"Yash":2,"Shreya":1,"Dev":5,"Kavya":1,"Joshmitha":7,"Tanvi":21},
    "most_used_emoji": {
      "Aryan":[["😀",42],["🧠",40],["😢",37]],
      "Akshit":[["🥺",26],["😂",22],["👍",22]],
      "Yash":[["😎",3],["😭",3],["😍",3]],
      "Shreya":[["😍",5],["😀",4],["🌍",4]],
      "Dev":[["🚀",6],["👍",4],["😍",2]],
      "Kavya":[["🧠",1],["😍",1],["🥀",1]],
      "Joshmitha":[["🥀",14],["🤔",14],["😍",14]],
      "Tanvi":[["😂",79],["🥀",77],["👍",73]]
    },
    "busiest_day": ["02/11/24", 191],
    "longest_silence": {"hours":47.87,"days":1.99,"start":"16/11/24 03:51","end":"18/11/24 03:43"},
    "avg_response_time": {"Aryan":11.0,"Akshit":11.0,"Yash":10.0,"Shreya":9.0,"Dev":11.0,"Kavya":10.0,"Joshmitha":11.0,"Tanvi":11.0},
    "hype_person": {"Aryan":15.38,"Akshit":15.31,"Yash":16.52,"Shreya":15.43,"Dev":14.78,"Kavya":19.71,"Joshmitha":15.8,"Tanvi":15.13},
    "conversation_killer": {
      "Aryan":{"kills":23,"total":1657,"score":1.39},
      "Akshit":{"kills":24,"total":524,"score":4.58},
      "Yash":{"kills":14,"total":247,"score":5.67},
      "Shreya":{"kills":3,"total":66,"score":4.55},
      "Dev":{"kills":4,"total":262,"score":1.53},
      "Kavya":{"kills":1,"total":8,"score":12.5},
      "Joshmitha":{"kills":20,"total":337,"score":5.93},
      "Tanvi":{"kills":18,"total":658,"score":2.74}
    }
  }
};

document.addEventListener("DOMContentLoaded", boot);