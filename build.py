#!/usr/bin/env python3
"""Expand the Design-Craft (.dc.html) portfolio template into a static index.html."""
import re, html, json

SITE_URL = "https://yaswanthkosuru.github.io"

raw = open("source/Yaswanth Portfolio.dc.html").read()

# ---------------------------------------------------------------- data (from the DC Component.renderVals) ----
def ico(p):
    return ("<svg width=\"26\" height=\"26\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" "
            "stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\">"
            f"<path d=\"{p}\"/></svg>")

services = [
    {"num":"01","name":"Frontend","desc":"Product UIs that feel fast — dashboards, contest workspaces with Monaco Editor, live verdict streams over SSE.","tags":["React.js & Next.js","Redux","Tailwind CSS","TypeScript"],"icon":ico("M3 5h18v14H3zM3 9h18")},
    {"num":"02","name":"Backend & APIs","desc":"REST APIs, WebSocket systems and event-driven microservices — from Django DRF endpoints to Node.js services with queue-based fan-out.","tags":["Node.js & Express","Django & DRF","FastAPI & Prisma","PostgreSQL · Redis · Mongo"],"icon":ico("M8 9l-4 3 4 3M16 9l4 3-4 3M13 6l-2 12")},
    {"num":"03","name":"AI / LLM Systems","desc":"Production RAG pipelines with Langchain + Langgraph — auto-generating quizzes, flashcards and notes; rate-controlled LLM evaluation at scale.","tags":["Langchain & Langgraph","OpenAI API","RAG Pipelines","Python NLP"],"icon":ico("M12 2a4 4 0 0 1 4 4c2 0 4 2 4 4s-1 3-2 4c1 1 1 3 0 4s-3 2-5 1c-1 2-3 3-5 2s-3-3-2-5c-2-1-3-3-2-5s3-3 5-3a4 4 0 0 1 3-6z")},
    {"num":"04","name":"Cloud & DevOps","desc":"Kubernetes deployments with autoscaling and zero-downtime releases, serverless pipelines on Azure, observability with Prometheus and Grafana.","tags":["Azure · AWS S3","Docker & Kubernetes","Vercel","Prometheus & Grafana"],"icon":ico("M17.5 19a4.5 4.5 0 1 0-.4-9A7 7 0 1 0 4 14.9")},
]

steps = [
    {"step":"01 / 03","name":"Learnfluid","role":"Full Stack Developer","period":"APR 2025 — PRESENT","mode":"REMOTE · FULL-TIME","top":"clamp(90px,12vh,130px)","img":"https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=1200&q=80",
     "bullets":["Replaced a manual Excel-based tutoring workflow by shipping two production platforms (tutor + student) end-to-end — scheduling, content delivery, and multi-stage approval.","Engineered a Langchain + Langgraph RAG pipeline that auto-generates quizzes, flashcards and notes from uploaded course material.","Built a content authoring engine with 10+ interactive question formats, reusable across all scheduled classes."],
     "stack":["React.js","Node.js","Prisma","Langchain","Langgraph","PostgreSQL","Vercel"]},
    {"step":"02 / 03","name":"Framespik","role":"Backend Developer — Freelance","period":"DEC 2024 — FEB 2025","mode":"REMOTE · CONTRACT","top":"clamp(110px,14vh,158px)","img":"https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=1200&q=80",
     "bullets":["Delivered 15+ REST API endpoints for onboarding, multi-cloud asset uploads (AWS S3 + Azure Blob) and crew management, built from the ground up.","Implemented real-time UI customization with Django Channels and Redis Pub/Sub, synchronizing state across concurrent sessions over WebSockets."],
     "stack":["Django","DRF","Channels","Redis","AWS S3","Azure Blob"]},
    {"step":"03 / 03","name":"A.I HYR","role":"Full Stack Developer Intern","period":"MAR 2024 — JUL 2024","mode":"HYDERABAD · ONSITE","top":"clamp(130px,16vh,186px)","img":"https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200&q=80",
     "bullets":["Scaled concurrent upload capacity 50× (20 → 1,000+ sessions) by re-architecting ingestion to direct client-to-Azure-Blob multipart uploads — per-session server memory from 1–2 GB to near zero.","Eliminated cascading API failures during bulk resume processing by decoupling OpenAI calls into two Azure Queue pipelines.","Shipped candidate-facing interview-prep flows and partner dashboards — 2+ educational partners and 500+ students onboarded in the first month."],
     "stack":["Node.js","Express","React","MongoDB","Azure Functions","OpenAI API"]},
]
for s in steps:
    s["imgStyle"] = f"position:absolute;inset:0;background-image:url({s['img']});background-size:cover;background-position:center;opacity:0.85"

dotBase = "display:flex;align-items:center;justify-content:center;width:clamp(34px,3.4vw,44px);height:clamp(34px,3.4vw,44px);border-radius:11px;font-weight:700;font-size:15px;"
pipeline = [
    {"letter":"A","name":"SCOPE","sub":"START","on":False},
    {"letter":"B","name":"ARCHITECT","sub":"PLAN","on":False},
    {"letter":"C","name":"BUILD","sub":"CODE","on":False},
    {"letter":"D","name":"DEPLOY","sub":"SHIP","on":False},
    {"letter":"Z","name":"OPERATE","sub":"LIVE","on":True},
]
for s in pipeline:
    s["dot"] = dotBase + ("background:#C4F542;color:#0A0A0B;box-shadow:0 0 30px -6px rgba(196,245,66,0.6);" if s["on"]
        else "background:rgba(255,255,255,0.05);color:#fff;border:1px solid rgba(255,255,255,0.12);")

scores = [
    {"val":"29ms","label":"P50 LATENCY"},
    {"val":"15.8","label":"REQ/S · 4 USERS"},
    {"val":"0","label":"FAILURES UNDER LOAD"},
    {"val":"6","label":"LANGUAGES SUPPORTED"},
]

journey = [
    {"year":"2019 — 2023","tag":"B.TECH · ECE","title":"Engineering degree","sub":"B.Tech in Electronics & Communication — SRKR Engineering College","desc":"Four years of core engineering (CGPA 8.00/10). Where curiosity turned into code — self-taught the web stack and started shipping real side-projects."},
    {"year":"2024","tag":"INTERNSHIP · FULL-STACK","title":"Full Stack Intern — A.I HYR","sub":"Node.js · React · Azure · OpenAI (Mar – Jul 2024)","desc":"Scaled concurrent uploads 50× with direct client-to-Azure-Blob transfers, and decoupled bulk resume evaluations into Azure Queue pipelines to kill cascading OpenAI failures."},
    {"year":"2024 — 2025","tag":"FREELANCE · BACKEND","title":"Backend Developer — Framespik","sub":"Django · DRF · Channels · Redis (Dec 2024 – Feb 2025)","desc":"Delivered 15+ REST endpoints for onboarding and multi-cloud asset uploads, plus real-time UI sync across sessions with Django Channels and Redis Pub/Sub."},
    {"year":"2025 — Now","tag":"FULL-TIME · LIVE","title":"Full Stack Developer — Learnfluid","sub":"React · Node · Prisma · Langchain / Langgraph","desc":"Shipped tutor + student platforms end-to-end and built a Langchain/Langgraph RAG pipeline that auto-generates quizzes, flashcards and notes from course material."},
]

refs = [
    {"name":"GitHub","desc":"All public repos — judge platform, chat system, and more.","href":"https://github.com/yaswanthkosuru"},
    {"name":"stdlib-js PRs","desc":"6+ merged PRs — 4 production utility modules.","href":"https://github.com/stdlib-js"},
    {"name":"Zulip","desc":"Open-source contributions to the Zulip project.","href":"https://github.com/zulip/zulip"},
    {"name":"Code Judge","desc":"Firecracker microVM judge — 29ms p50, 6 languages.","href":"https://github.com/yaswanthkosuru"},
    {"name":"Chat System","desc":"K8s + Redis Pub/Sub WebSocket chat with observability.","href":"https://github.com/yaswanthkosuru"},
    {"name":"Resume PDF","desc":"The full resume this page is built from.","href":"uploads/resume.pdf"},
]

DATA = {"services":services,"steps":steps,"pipeline":pipeline,"scores":scores,"journey":journey,"refs":refs}

# ---------------------------------------------------------------- mini DC template engine ----
def resolve(path, ctx):
    parts = path.strip().split('.')
    val = ctx[parts[0]]
    for p in parts[1:]:
        val = val[p] if isinstance(val, dict) else getattr(val, p)
    return val

SCFOR_OPEN = re.compile(r'<sc-for\b[^>]*\blist="\{\{\s*([^}]+?)\s*\}\}"[^>]*\bas="([^"]+)"[^>]*>')

def find_matching(s, start):
    """Given index just after an <sc-for ...> open tag, return index of its matching </sc-for>."""
    depth = 1
    i = start
    open_re = re.compile(r'<sc-for\b')
    while depth > 0:
        nxt_open = open_re.search(s, i)
        nxt_close = s.find('</sc-for>', i)
        if nxt_close == -1:
            raise ValueError("unbalanced sc-for")
        if nxt_open and nxt_open.start() < nxt_close:
            depth += 1
            i = nxt_open.end()
        else:
            depth -= 1
            i = nxt_close + len('</sc-for>')
    return i  # index just after the closing </sc-for>

def render(tpl, ctx):
    # Expand sc-for loops (outermost first; recurse into body per item)
    out = []
    i = 0
    while True:
        m = SCFOR_OPEN.search(tpl, i)
        if not m:
            out.append(tpl[i:])
            break
        out.append(tpl[i:m.start()])
        list_expr, var = m.group(1), m.group(2)
        body_start = m.end()
        end = find_matching(tpl, body_start)
        body = tpl[body_start:end - len('</sc-for>')]
        items = resolve(list_expr, ctx)
        for item in items:
            child = dict(ctx)
            child[var] = item
            out.append(render(body, child))
        i = end
    joined = ''.join(out)
    # Replace {{ path }} scalars
    def repl(mm):
        return str(resolve(mm.group(1), ctx))
    return re.sub(r'\{\{\s*([^}]+?)\s*\}\}', repl, joined)

# ---------------------------------------------------------------- extract helmet + main ----
hm = re.search(r'<helmet>(.*?)</helmet>', raw, re.S).group(1)
main = re.search(r'(<main\b.*?</main>)', raw, re.S).group(1)
main_rendered = render(main, DATA)

# Add form field names so the mailto handler can read them
for a, b in [
    ('placeholder="Jane"', 'name="firstName" placeholder="Jane"'),
    ('placeholder="Doe"', 'name="lastName" placeholder="Doe"'),
    ('placeholder="you@company.com"', 'name="email" type="email" placeholder="you@company.com"'),
    ('placeholder="Studio Inc."', 'name="company" placeholder="Studio Inc."'),
    ('placeholder="Product, stack, timeline — what should I know?"', 'name="brief" placeholder="Product, stack, timeline — what should I know?"'),
]:
    assert main_rendered.count(a) == 1, (a, main_rendered.count(a))
    main_rendered = main_rendered.replace(a, b)

# SEO patches: name inside the h1 (visually hidden — no design change), the real
# LinkedIn URL, and lazy-loading on below-the-fold images.
# NOTE: the shipped index.html has diverged from the .dc.html source (local
# project images, new logo, hero photo card, GoatCounter, Experience rework…) —
# rebuilding will LOSE those hand-applied changes. Diff against index.html first.
for a, b in [
    ('style="animation-delay:.38s">0-to-1 platforms',
     'style="animation-delay:.38s"><span class="sr-only">Yaswanth Kosuru — Full-Stack Engineer. </span>0-to-1 platforms'),
    ('<a href="#" style="color:rgba(255,255,255,0.7);text-decoration:none">LinkedIn ↗</a>',
     '<a href="https://www.linkedin.com/in/yaswanth04/" target="_blank" rel="noopener" style="color:rgba(255,255,255,0.7);text-decoration:none">LinkedIn ↗</a>'),
    ('alt="Code Execution Judge" style="position:absolute',
     'alt="Code Execution Judge" loading="lazy" decoding="async" style="position:absolute'),
    ('alt="Distributed WebSocket Chat" style="position:absolute',
     'alt="Distributed WebSocket Chat" loading="lazy" decoding="async" style="position:absolute'),
    ('alt="Learnfluid Platforms" style="position:absolute',
     'alt="Learnfluid Platforms" loading="lazy" decoding="async" style="position:absolute'),
    ('alt="Code on screen" style="position:absolute',
     'alt="Code on screen" loading="lazy" decoding="async" style="position:absolute'),
    ('<img src="uploads/yklogo-enhanced.png" alt="YK logo" style="',
     '<img src="uploads/yklogo-enhanced.png" alt="YK logo" loading="lazy" decoding="async" style="'),
]:
    assert main_rendered.count(a) == 1, (a, main_rendered.count(a))
    main_rendered = main_rendered.replace(a, b)

# ---------------------------------------------------------------- interaction JS (from componentDidMount) ----
JS = r"""
(function(){
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Lenis smooth scroll — driven by gsap.ticker when GSAP is present so
  // ScrollTrigger stays in sync (official Lenis x ScrollTrigger wiring).
  function boot(t){ t=t||0;
    if(!window.Lenis){ if(t<80) setTimeout(function(){boot(t+1);},40); return; }
    var lenis = new window.Lenis({
      duration: 1.2,
      easing: function(t){ return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, // easeOutExpo
      smoothWheel: true, wheelMultiplier: 1, touchMultiplier: 1.6
    });
    if(hasGsap){
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function(time){ lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      function loop(time){ lenis.raf(time); requestAnimationFrame(loop); }
      requestAnimationFrame(loop);
    }
  }
  boot();

  // GSAP entrances + scroll reveals (falls back to the CSS animations when
  // GSAP is unavailable or the user prefers reduced motion).
  if(hasGsap && !reduceMotion){
    gsap.registerPlugin(ScrollTrigger);
    // don't re-measure triggers when the mobile address bar shows/hides —
    // that refresh restored a stale scroll position (scroll jump-back on phones)
    ScrollTrigger.config({ ignoreMobileResize: true });
    document.documentElement.classList.add('gsap-on');

    // --- hero intro timeline: expo.out = long soft tail, short travel = low peak velocity ---
    gsap.timeline({ defaults:{ ease:'expo.out', duration:1.4 } })
      .from('.nav-pill', { y:-24, autoAlpha:0, duration:1.0 }, 0.15)
      .from('.wb-bigname', { y:44, autoAlpha:0, duration:1.6 }, 0.25)
      .from('.hero-eyebrow', { y:18, autoAlpha:0 }, 0.5)
      .from('.hero-title', { y:26, autoAlpha:0 }, 0.62)
      .from('.hero-actions', { y:22, autoAlpha:0 }, 0.78)
      .from('.hero-card', { y:24, autoAlpha:0 }, 0.85)
      .from('.hero-stats', { y:16, autoAlpha:0 }, 0.9)
      .from('.hero-social a', { x:20, autoAlpha:0, stagger:0.07, duration:0.9 }, 0.95)
      .from('.hero-scroll', { autoAlpha:0, duration:1.2 }, 1.1);

    // --- giant name drifts up as the hero scrolls away (scrub lag = smoothed) ---
    gsap.to('.hero-bg', {
      y: 110, autoAlpha: 0, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom 30%', scrub: 0.8 }
    });

    // --- while-in-view reveals: one ScrollTrigger per element ---
    // section-level blocks (headers, h2s, panels)
    gsap.utils.toArray('.reveal').forEach(function(el){
      gsap.from(el, { y:24, autoAlpha:0, duration:1.2, ease:'expo.out',
        scrollTrigger:{ trigger:el, start:'top 85%', toggleActions:'play none none reverse' } });
    });
    // individual items (project tiles, stack cards, experience steps, journey entries,
    // reference cards) — own trigger each; small per-section stagger for same-row items;
    // clearProps so CSS :hover transforms take over after the entrance completes
    ['#work','#services','#experience','#about','#contact','#results','#journey','#references']
    .forEach(function(sec){
      gsap.utils.toArray(sec + ' .reveal-item').forEach(function(el, i){
        var vars = { y:32, autoAlpha:0, duration:1.3, ease:'expo.out', delay:(i % 4) * 0.06,
          scrollTrigger:{ trigger:el, start:'top 88%', toggleActions:'play none none reverse' } };
        // clearProps only where CSS :hover transforms take over afterwards —
        // clearing elsewhere would wipe the deck's scale scrub (wb-proc-inner)
        if(el.classList.contains('wb-tile') || el.classList.contains('wb-svc')) vars.clearProps = 'transform';
        gsap.from(el, vars);
      });
    });

    // --- mobile experience deck: a card pins only once it has been FULLY read
    // (CSS sticky can't express that for taller-than-viewport cards; the CSS
    // deck stays desktop-only via the max-width:899px static override) ---
    gsap.matchMedia().add('(max-width:899px)', function(){
      var steps = gsap.utils.toArray('#experience .exp-step');
      var head = document.querySelector('#experience .exp-head');
      if(head && steps.length){
        // section heading pins first (page order) and stays visible above the
        // whole deck; releases after the last card has been read
        ScrollTrigger.create({
          trigger: head, start: 'top 12px',   // near the top — the fixed nav
                                                // is only visible over the hero
          endTrigger: steps[steps.length - 1], end: 'bottom bottom',
          pin: true, pinSpacing: false, anticipatePin: 1
        });
      }
      // cards pin just below the pinned heading (function-based: re-measured on
      // every ScrollTrigger refresh)
      var cardLine = function(){ return 20 + (head ? head.offsetHeight : 0); };
      steps.forEach(function(stepEl, i){
        stepEl.style.zIndex = i + 1;                 // later cards cover earlier
        if(i === steps.length - 1) return;           // last card never pins
        ScrollTrigger.create({
          trigger: stepEl,
          start: function(){ return 'top ' + cardLine() + 'px'; },
          endTrigger: steps[i + 1],                  // release the moment the NEXT card
          end: function(){ return 'top ' + cardLine() + 'px'; }, // covers edge-to-edge
          pin: true,
          pinSpacing: false,
          anticipatePin: 1,
          // heights differ between cards, so hide the card the instant it is fully
          // covered (nothing pokes out below shorter cards); restore the moment
          // uncovering begins when scrolling back up
          onLeave: function(){ gsap.set(stepEl, { autoAlpha: 0 }); },
          onEnterBack: function(){ gsap.set(stepEl, { autoAlpha: 1 }); }
        });
        // depth: the covered card recedes slightly as the next card arrives —
        // no dimming (card must stay readable while pinned); animate the CHILD,
        // never the pinned element itself
        gsap.to(stepEl.querySelector('.wb-proc-inner'), {
          scale: 0.96, ease: 'none',
          scrollTrigger: {
            trigger: steps[i+1],
            start: 'top 75%',
            end: function(){ return 'top ' + cardLine() + 'px'; },
            scrub: true
          }
        });
      });
    });

    // --- journey timeline fill scrubs with scroll (with catch-up lag) ---
    gsap.fromTo('.wb-journey-fill', { scaleY:0 }, {
      scaleY:1, ease:'none',
      scrollTrigger: { trigger:'#journey', start:'top 70%', end:'bottom 75%', scrub:0.8 }
    });

    // recalc trigger positions once webfonts/images have settled
    window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
  }

  // close the mobile nav menu after tapping a link
  var navCb = document.getElementById('nav-toggle');
  if(navCb){
    document.querySelectorAll('.nav-menu a').forEach(function(a){
      a.addEventListener('click', function(){ navCb.checked = false; });
    });
  }

  // Neon spotlight on the giant name — lerped cursor tracking
  function neon(t){ t=t||0;
    var el = document.querySelector('.wb-bigname');
    if(!el){ if(t<60) setTimeout(function(){neon(t+1);},80); return; }
    var zone = el.closest('section') || el;
    var st = { x:0,o:0,ct:0,cb:0,tx:0,to:0,tct:0,tcb:0 };
    function move(e){
      var b = el.getBoundingClientRect();
      st.tx = e.clientX - b.left; st.to = 1;
      var onSecondLine = (e.clientY - b.top)/b.height > 0.5;
      st.tct = onSecondLine ? 50 : 0;
      st.tcb = onSecondLine ? 0 : 50;
      el.style.setProperty('--wb-band', Math.max(22, Math.min(48, b.width*0.035)).toFixed(1)+'px');
    }
    function leave(){ st.to = 0; }
    var autoMode = window.matchMedia && window.matchMedia('(hover: none)').matches;
    if(!autoMode){ zone.addEventListener('pointermove', move); zone.addEventListener('pointerleave', leave); }
    function tick(time){
      if(autoMode){
        // Organic, aperiodic shimmer: each channel sums sines whose frequencies
        // sit in irrational ratios (sqrt2, phi, sqrt3, sqrt5), so the combined
        // motion never repeats — light wandering across metal, not a mechanical
        // left-right sweep.
        var b = el.getBoundingClientRect();
        var T = time;
        // position: wanders the full width, lingers, doubles back
        var nx = Math.sin(T*0.00021) + Math.sin(T*0.00021*1.41421 + 1.7) + Math.sin(T*0.00021*2.23607 + 4.2);
        st.tx = b.width * (0.5 + nx/6.4);
        // brightness: breathes, with occasional brighter glints
        var no = Math.sin(T*0.00033 + 2.1) + Math.sin(T*0.00033*1.61803 + 0.6);
        st.to = Math.max(0.35, Math.min(1, 0.68 + 0.15*no + 0.18*Math.sin(T*0.00007*2.23607)));
        // lit line: drifts between YASWANTH and KOSURU at irregular moments
        var nl = Math.sin(T*0.000167 + 0.9) + Math.sin(T*0.000167*1.73205 + 3.3);
        var line2 = nl > 0;
        st.tct = line2 ? 50 : 0; st.tcb = line2 ? 0 : 50;
        // band width: slowly swells and narrows
        var nb = 0.030 + 0.012*Math.sin(T*0.000113 + 5.0) + 0.006*Math.sin(T*0.000113*1.41421);
        el.style.setProperty('--wb-band', Math.max(20, Math.min(56, b.width*nb)).toFixed(1)+'px');
      }
      st.x += (st.tx-st.x)*0.2; st.o += (st.to-st.o)*0.1;
      st.ct += (st.tct-st.ct)*0.18; st.cb += (st.tcb-st.cb)*0.18;
      el.style.setProperty('--wb-x', st.x.toFixed(1)+'px');
      el.style.setProperty('--wb-o', st.o.toFixed(3));
      el.style.setProperty('--wb-ct', st.ct.toFixed(2)+'%');
      el.style.setProperty('--wb-cb', st.cb.toFixed(2)+'%');
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  neon();

  // Contact "Send request" — client-side only (no backend); compose a mailto instead.
  var contact = document.getElementById('contact');
  var sendBtn = contact && contact.querySelector('button');
  if(sendBtn){
    sendBtn.addEventListener('click', function(e){
      e.preventDefault();
      function val(n){ var el = contact.querySelector('[name="'+n+'"]'); return el ? el.value : ''; }
      var body = encodeURIComponent(
        'From: ' + val('firstName') + ' ' + val('lastName') +
        '\nEmail: ' + val('email') + '\nCompany: ' + val('company') +
        '\n\n' + val('brief'));
      window.location.href = 'mailto:yaswanthkosuru999@gmail.com?subject=' +
        encodeURIComponent('Project briefing') + '&body=' + body;
    });
  }
})();
"""

# ---------------------------------------------------------------- SEO: structured data + head extras ----
schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": f"{SITE_URL}/",
            "name": "Yaswanth Kosuru — Full-Stack Engineer",
            "publisher": {"@id": f"{SITE_URL}/#person"},
            "inLanguage": "en",
        },
        {
            "@type": "ProfilePage",
            "@id": f"{SITE_URL}/#profilepage",
            "url": f"{SITE_URL}/",
            "isPartOf": {"@id": f"{SITE_URL}/#website"},
            "mainEntity": {"@id": f"{SITE_URL}/#person"},
        },
        {
            "@type": "Person",
            "@id": f"{SITE_URL}/#person",
            "name": "Yaswanth Kosuru",
            "jobTitle": "Full-Stack Engineer",
            "url": f"{SITE_URL}/",
            "image": f"{SITE_URL}/assets/yaswanth.jpg",
            "email": "mailto:yaswanthkosuru999@gmail.com",
            "sameAs": [
                "https://github.com/yaswanthkosuru",
                "https://www.linkedin.com/in/yaswanth04/",
            ],
            "worksFor": {"@type": "Organization", "name": "Learnfluid"},
            "alumniOf": {"@type": "CollegeOrUniversity", "name": "SRKR Engineering College"},
            "address": {"@type": "PostalAddress", "addressCountry": "IN"},
            "knowsAbout": [
                "React", "Next.js", "Node.js", "Django", "FastAPI",
                "LangChain", "LangGraph", "PostgreSQL", "Redis",
                "Docker", "Kubernetes", "Azure", "RAG pipelines", "WebSockets",
            ],
        },
    ],
}
SCHEMA_JSON = json.dumps(schema, ensure_ascii=False, indent=1)

# visually-hidden text (name inside the h1 for SEO without changing the design)
SR_CSS = ".sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}"

# ---------------------------------------------------------------- compose final document ----
doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yaswanth Kosuru — Full-Stack Engineer</title>
<meta name="description" content="Yaswanth Kosuru — Full-Stack Engineer. 0-to-1 platforms, event-driven services and production LLM pipelines.">
<meta name="author" content="Yaswanth Kosuru">
<link rel="canonical" href="{SITE_URL}/">
<meta name="theme-color" content="#0A0A0B">
<link rel="icon" type="image/png" href="uploads/favicon.png">
<link rel="apple-touch-icon" href="uploads/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:site_name" content="Yaswanth Kosuru">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="Yaswanth Kosuru — Full-Stack Engineer">
<meta property="og:description" content="0-to-1 platforms, event-driven services and production LLM pipelines. React · Node · Django · Langchain · Kubernetes.">
<meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Yaswanth Kosuru — Full-Stack Engineer">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Yaswanth Kosuru — Full-Stack Engineer">
<meta name="twitter:description" content="0-to-1 platforms, event-driven services and production LLM pipelines.">
<meta name="twitter:image" content="{SITE_URL}/assets/og-image.jpg">
<meta name="twitter:image:alt" content="Yaswanth Kosuru — Full-Stack Engineer">
<script type="application/ld+json">{SCHEMA_JSON}</script>
<style>{SR_CSS}</style>
{hm.strip()}
</head>
<body>
{main_rendered}
<script>{JS}</script>
</body>
</html>
"""

open("index.html", "w").write(doc)
print("wrote index.html", len(doc), "chars")
# sanity: no unexpanded template syntax should remain
leftovers = re.findall(r'\{\{[^}]+\}\}', doc) + re.findall(r'<sc-for', doc)
print("leftover template tokens:", len(leftovers))
if leftovers:
    print(leftovers[:10])
