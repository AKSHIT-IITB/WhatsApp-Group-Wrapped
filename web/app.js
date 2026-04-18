// WhatsApp Wrapped 2024 - app.js

// ---- member colors ----
var members = ["Aryan", "Akshit", "Yash", "Shreya", "Dev", "Kavya", "Joshmitha", "Tanvi"];

function getColor(name) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(`--c-${name.toLowerCase()}`)
    .trim() || "#7c83ff";
}

function formatNum(n) {
  if (n == null || isNaN(n)) return "—";
  return n.toLocaleString();
}

// ---- global state ----
var data = null;
var slides = [];
var currentSlide = 0;

// ---- boot ----
async function boot() {
  var res = await fetch("data.json");
  data = await res.json();
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

  // ---- inject ambient blobs centrally for every slide that has a color ----
  var color = slides[index].color;
  if (color) {
    newSlide.insertAdjacentHTML('afterbegin', `
      <div class="blob blob-primary" style="background:${color};"></div>
      <div class="blob blob-secondary" style="background:${color};"></div>
    `);
  }

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

// ===========================================================
// SLIDE BUILDERS
// ===========================================================

function slideIntro(d) {
  return {
    getHTML: function() {
      return `
        <div class="intro-bg"></div>
        <div class="intro-overlay"></div>
        <h1 class="intro-title">Your Group<br>Wrapped.</h1>
      `;
    }
  };
}

function slideTotalMessages(d) {
  var sorted = d.derived.sorted.total_messages;
  var pct    = d.derived.pct.total_messages;
  var max    = sorted[0][1];

  return {
    color: "#b8c0ff",
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val  = sorted[i][1];
        var p    = pct[name];
        var label = val > max * 0.3 ? formatNum(val) : "";
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${p}" style="background:${getColor(name)};">${label}</div>
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
  var sorted = d.derived.sorted.word_count;
  var pct    = d.derived.pct.word_count;
  var max    = sorted[0][1];

  return {
    color: "#cbb4fd",
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val  = sorted[i][1];
        var p    = pct[name];
        var label = val > max * 0.3 ? formatNum(val) : "";
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${p}" style="background:${getColor(name)};">${label}</div>
            </div>
            <span class="bar-val">${formatNum(val)}</span>
          </div>`;
      }
      return `
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
  var sorted = d.derived.sorted.night_owl;
  var pct    = d.derived.pct.night_owl;

  return {
    color: "#cbb4fd",
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val  = sorted[i][1];
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct[name]}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val">${val}</span>
          </div>`;
      }
      return `
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
  var sorted = d.derived.sorted.ghost_percentage;
  var pct    = d.derived.pct.ghost_percentage;

  return {
    color: "#b8c0ff",
    getHTML: function() {
      var items = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var p    = sorted[i][1];
        items += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct[name]}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val" style="color:${getColor(name)};">${p.toFixed(1)}%</span>
          </div>`;
      }
      return `
        <div class="slide-label">Stat 04 · Ghost Report</div>
        <h2 class="slide-title">The ghosting report.</h2>
        <p class="slide-sub">% of messages with no reply within 10 minutes</p>
        <div class="ghost-row">${items}</div>
      `;
    },
    onEnter: animateBars
  };
}

function slideConversationStarter(d) {
  var sorted = d.derived.sorted.conversation_starter;
  var podiumOrder  = [sorted[1], sorted[0], sorted[2]];
  var podiumHeights = [150, 195, 118];
  var medals = ["🥈", "🥇", "🥉"];

  return {
    color: "#d4b0ff",
    getHTML: function() {
      var podiumHTML = "";
      for (var i = 0; i < podiumOrder.length; i++) {
        var name = podiumOrder[i][0];
        var val  = podiumOrder[i][1];
        podiumHTML += `
          <div class="podium-item">
            <div class="avatar podium-avatar" data-name="${name.toLowerCase()}"></div>
            <span class="podium-medal">${medals[i]}</span>
            <div class="podium-bar" data-h="${podiumHeights[i]}" style="background:${getColor(name)};">${val}</div>
            <span class="podium-label">${name}</span>
          </div>`;
      }
      return `
        <div class="podium-container">
          <div class="slide-label">Stat 05 · Conversation Starter</div>
          <h2 class="slide-title">Who keeps this group alive?</h2>
          <p class="slide-sub">Times they broke a 60-minute silence</p>
          <div class="podium-wrap--spaced">${podiumHTML}</div>
        </div>
      `;
    },
    onEnter: animatePodium
  };
}

function slideOverallEmojis(d) {
  var emojis = (d.stats.overall_emojis || []).slice(0, 6);
  var max = emojis.length ? emojis[0][1] : 1;

  return {
    color: "#cbb4fd",
    getHTML: function() {
      return `
        <div class="slide-label">Stat 06 · Emojis</div>
        <h2 class="slide-title">The most iconic emojis.</h2>
        <p class="slide-sub">Most-used emojis across all messages</p>
        <div class="emoji-list">
          ${emojis.map(([e, c]) => {
            var pct = ((c / max) * 100).toFixed(1);
            return `
              <div class="emoji-row-clean">
                <span class="emoji">${e}</span>
                <div class="emoji-line">
                  <div class="emoji-fill" data-w="${pct}"></div>
                </div>
                <span class="count">${c}</span>
              </div>`;
          }).join("")}
        </div>
      `;
    },
    onEnter: function(root) {
      var fills = root.querySelectorAll(".emoji-fill[data-w]");
      for (var i = 0; i < fills.length; i++) {
        var fill = fills[i];
        var target = fill.getAttribute("data-w");
        setTimeout(function(b, t) { b.style.width = t + "%"; }, 80 + i * 40, fill, target);
      }
    }
  };
}

function slideBusiestDay(d) {
  var s = d.stats;

  return {
    color: "#f9b8ff",
    getHTML: function() {
      var date  = s.busiest_day[0];
      var count = s.busiest_day[1];
      return `
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
    color: "#cbb4fd",
    getHTML: function() {
      var sil = s.longest_silence;
      return `
        <div class="slide-label">Stat 08 · Longest Silence</div>
        <h2 class="slide-title">The great silence.</h2>
        <p class="slide-sub">Longest gap with zero messages</p>
        <div class="big-number silence-number">${sil.hours}h</div>
        <div class="stat-pair silence-stat-pair">
          <div class="stat-box">
            <div class="sb-val silence-date-val">${sil.start}</div>
            <div class="sb-lbl">last message</div>
          </div>
          <div class="stat-box">
            <div class="sb-val silence-revived-val">${sil.end}</div>
            <div class="sb-lbl">group revived</div>
          </div>
        </div>
      `;
    }
  };
}

function slideAvgResponseTime(d) {
  var respTimes  = d.stats.avg_response_time;
  var bubbleSizes = d.derived.response_bubble_size;

  return {
    color: "#a8d8ff",
    getHTML: function() {
      var bubblesHTML = "";
      for (var i = 0; i < members.length; i++) {
        var name = members[i];
        var val  = respTimes[name];
        var size = bubbleSizes[name];
        if (!val) continue;
        bubblesHTML += `
          <div class="bubble" style="width:${size}px;height:${size}px;background:${getColor(name)};">
            <span class="b-name">${name.slice(0, 5)}</span>
            <span class="b-val">${val}m</span>
          </div>`;
      }
      return `
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
  var sorted = d.derived.sorted.hype_person;
  var pct    = d.derived.pct.hype_person;

  return {
    color: "#cbb4fd",
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var val  = sorted[i][1];
        rows += `
          <div class="bar-row">
            <span class="bar-name">${name}</span>
            <div class="bar-track">
              <div class="bar-fill" data-w="${pct[name]}" style="background:${getColor(name)};"></div>
            </div>
            <span class="bar-val">${val.toFixed(1)}m</span>
          </div>`;
      }
      return `
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
  var sorted = d.derived.sorted.conversation_killer;

  return {
    color: "#b8c0ff",
    getHTML: function() {
      var rows = "";
      for (var i = 0; i < sorted.length; i++) {
        var name = sorted[i][0];
        var dk   = sorted[i][1];
        rows += `
          <tr>
            <td class="killer-name-cell">
              <div class="avatar killer-avatar" data-name="${name.toLowerCase()}"></div>
              ${name}
            </td>
            <td style="color:${getColor(name)};font-weight:700;">${dk.kills}</td>
            <td class="killer-total">${formatNum(dk.total)}</td>
            <td><span class="score-pill">${dk.score.toFixed(1)}%</span></td>
          </tr>`;
      }
      return `
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
    color: "#d4b0ff",
    getHTML: function() {
      var buttons = "";
      for (var i = 0; i < members.length; i++) {
        var name = members[i];
        buttons += `
          <button class="picker-btn" data-name="${name}" style="border-color:${getColor(name)}44;">
            <img class="picker-avatar" src="images/${name.toLowerCase()}.jpeg" alt="${name}" />
            <span class="picker-name">${name}</span>
          </button>`;
      }
      return `
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
          var idx  = members.indexOf(name);
          showSlide(13 + idx);
        });
      }
    }
  };
}

function slideProfile(name, d) {
  var s           = d.stats;
  var derived     = d.derived;
  var color       = getColor(name);
  var msgs        = s.total_messages[name];
  var words       = s.word_count[name];
  var nightMsgs   = s.night_owl[name];
  var ghostPct    = s.ghost.ghost_percentage[name] != null ? s.ghost.ghost_percentage[name] : 0;
  var starts      = s.conversation_starter[name];
  var emojis      = s.most_used_emoji[name];
  var respTime    = s.avg_response_time[name];
  var hypeTime    = s.hype_person[name];
  var killer      = s.conversation_killer[name] || { kills: 0, total: 0, score: 0 };
  var wpm         = derived.words_per_message[name];
  var personality = derived.personality[name];
  var msgRank     = derived.ranks.total_messages[name];
  var wordRank    = derived.ranks.word_count[name];
  var memberIndex = members.indexOf(name);

  var emojisHTML = emojis.map(function(item) {
    return '<div class="pe-item"><span class="pe-emoji">' + item[0] + '</span><span class="pe-count">' + item[1] + '×</span></div>';
  }).join("") || '<span class="pe-none">none recorded</span>';

  var badgesHTML = personality.map(function(p) {
    return '<div class="personality-badge" style="background:' + color + '22;border-color:' + color + '44;"><span>' + p.emoji + '</span><span>' + p.label + '</span></div>';
  }).join("");

  return {
    color: color,
    getHTML: function() {
      return `
        <div class="profile-layout">
          <div class="profile-left">
            <div class="slide-label" style="color:${color};">Profile · ${memberIndex + 1} of ${members.length}</div>
            <div class="profile-avatar avatar" data-name="${name.toLowerCase()}"></div>
            <div class="profile-name" style="color:${color};">${name}</div>
            <div style="display:flex;flex-direction:column;gap:6px;">${badgesHTML}</div>
            <div class="profile-emojis">
              <div class="pe-label">most used emojis</div>
              <div class="pe-row">${emojisHTML}</div>
            </div>
          </div>
          <div class="profile-right">
            <div class="ps-row">
              <div class="ps-card">
                <div class="ps-val" style="color:${color};">${formatNum(msgs)}</div>
                <div class="ps-lbl">messages sent</div>
                <div class="ps-rank">#${msgRank} in group</div>
              </div>
              <div class="ps-card">
                <div class="ps-val" style="color:${color};">${formatNum(words)}</div>
                <div class="ps-lbl">words typed</div>
                <div class="ps-rank">#${wordRank} in group</div>
              </div>
            </div>
            <div class="ps-row">
              <div class="ps-card">
                <div class="ps-val ps-val--sm">${respTime != null ? respTime + "m" : "—"}</div>
                <div class="ps-lbl">median reply time</div>
                <div class="ps-rank">within 60-min window</div>
              </div>
              <div class="ps-card">
                <div class="ps-val ps-val--sm">${killer.score.toFixed(1)}%</div>
                <div class="ps-lbl">convo kill rate</div>
                <div class="ps-rank">${killer.kills} kills · ${formatNum(killer.total)} msgs</div>
              </div>
            </div>
            <div class="ps-wpm">
              <span class="ps-wpm-val" style="color:${color};">${wpm}</span>
              <span class="ps-wpm-lbl">avg words per message</span>
            </div>
          </div>
        </div>
      `;
    }
  };
}

// ---- assemble all slides in order ----
function buildAllSlides(d) {
  var allSlides = [];

  allSlides.push(slideIntro(d));
  allSlides.push(slideTotalMessages(d));
  allSlides.push(slideWordCount(d));
  allSlides.push(slideNightOwl(d));
  allSlides.push(slideGhostReport(d));
  allSlides.push(slideConversationStarter(d));
  allSlides.push(slideOverallEmojis(d));
  allSlides.push(slideBusiestDay(d));
  allSlides.push(slideLongestSilence(d));
  allSlides.push(slideAvgResponseTime(d));
  allSlides.push(slideHypePerson(d));
  allSlides.push(slideConversationKiller(d));
  allSlides.push(slideProfilePicker());

  for (var i = 0; i < members.length; i++) {
    allSlides.push(slideProfile(members[i], d));
  }

  return allSlides;
}

document.addEventListener("DOMContentLoaded", boot);