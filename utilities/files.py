import os
from utilities.cmd_colors import *
import re

def make_safe_folder_name(text):
    return re.sub(r'[<>:"/\\|?*]', ' -', text).strip()

def create_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except Exception as e:
        pass

import os

def createIndexSeries(folder_path):
    # logic for the series/tv show view
    
    # check dir
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            return

    file_path = os.path.join(folder_path, "index.html")

    # html structure
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Series - IscrapeMDB</title>
    
    <!-- offline favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 5 L85 20 V50 C85 75 50 95 50 95 C50 95 15 75 15 50 V20 Z' fill='%23111827' stroke='%23d4af37' stroke-width='5'/><text x='50' y='65' font-family='serif' font-weight='bold' font-size='50' text-anchor='middle' fill='%23d4af37'>I</text></svg>">

    <script src="data/main.js"></script>
    <script src="data/review.js"></script>
    
    <style>
        /* vars & reset */
        :root {
            --bg-dark: #0f1115;
            --bg-sidebar: #111827; 
            --bg-panel: #1f2937;
            --bg-hover: rgba(212, 175, 55, 0.1);
            
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-gold: #d4af37;
            --border-color: #374151;
            
            --sidebar-width: 280px;
            --font-main: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            --font-header: 'Georgia', 'Times New Roman', serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: var(--font-main);
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            display: flex;
        }

        /* typography */
        h1, h2, h3, .serif-font { font-family: var(--font-header); }
        a { text-decoration: none; color: inherit; }

        /* layout */
        aside {
            width: var(--sidebar-width);
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            transition: transform 0.3s ease;
            z-index: 50;
        }

        .sidebar-header {
            padding: 1.5rem 1rem;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
        }

        /* logo */
        .logo-container {
            font-family: var(--font-main);
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
        }
        
        .logo-box {
            background-color: var(--accent-gold);
            color: #000;
            padding: 2px 6px;
            border-radius: 4px;
            display: inline-block;
            line-height: 1;
        }
        
        .logo-scrape { 
            color: #6b7280; 
            font-weight: 700;
        }

        .app-title {
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: normal;
            margin-top: 0.5rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* controls */
        .controls-container {
            padding: 0 0 0.5rem 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        /* season btns */
        .season-wrap {
            display: flex;
            gap: 0.3rem;
            flex-wrap: wrap; 
            justify-content: center;
            margin-bottom: 0.5rem;
        }
        
        .control-btn {
            background: var(--bg-panel);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            width: 38px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            flex: 0 0 auto;
        }
        
        .control-btn:hover {
            border-color: var(--accent-gold);
            color: var(--text-main);
        }
        
        .control-btn.active {
            background: var(--accent-gold);
            color: #000;
            border-color: var(--accent-gold);
        }

        /* sorting */
        .sort-row {
            display: flex;
            gap: 0.5rem;
        }
        
        .sort-btn {
            flex: 1;
            background: rgba(31, 41, 55, 0.5);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }

        .sort-btn:hover {
            background: var(--bg-hover);
            color: var(--accent-gold);
        }

        .sort-btn.active {
            border-color: var(--accent-gold);
            color: var(--accent-gold);
            background: rgba(212, 175, 55, 0.05);
        }


        .nav-container {
            flex: 1;
            overflow-y: auto;
            padding: 0;
        }

        /* nav items */
        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1.5rem;
            color: var(--text-muted);
            border-left: 3px solid transparent;
            transition: all 0.2s;
            cursor: pointer;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }

        .nav-item:hover {
            background-color: var(--bg-hover);
            color: var(--accent-gold);
        }

        .nav-item.active {
            background-color: rgba(212, 175, 55, 0.15);
            border-left: 3px solid var(--accent-gold);
            color: var(--accent-gold);
        }

        .nav-item .ep-code {
            font-family: monospace;
            font-size: 0.75rem;
            opacity: 0.6;
            width: 50px;
            flex-shrink: 0;
        }
        
        .nav-item .ep-title {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 0.9rem;
        }

        .nav-section-label {
            padding: 1rem 1.5rem 0.5rem;
            font-size: 0.75rem;
            font-weight: bold;
            color: #4b5563;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            background: var(--bg-sidebar);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        /* main content */
        main {
            flex: 1;
            position: relative;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background-color: var(--bg-dark);
        }

        .content-scrollable {
            overflow-y: auto;
            height: 100%;
            width: 100%;
        }

        /* specific views */
        
        /* hero */
        .hero {
            position: relative;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #000;
            overflow: hidden;
        }
        
        .hero-bg {
            position: absolute;
            inset: 0;
            background-size: cover;
            background-position: center;
            opacity: 0.4;
        }
        
        .hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(to top, var(--bg-dark), rgba(15, 17, 21, 0.5), transparent);
        }
        
        .hero-content {
            position: relative;
            z-index: 10;
            text-align: center;
            padding: 1rem;
        }

        .hero-title {
            font-size: clamp(2rem, 5vw, 5rem);
            font-weight: 900;
            margin-bottom: 0.25rem;
            text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        }

        .hero-director {
            color: #d1d5db; 
            font-size: 1rem; 
            margin-bottom: 1rem; 
            font-style: italic;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }

        /* ep header */
        .ep-header {
            background: linear-gradient(to right, #1e293b, #0f172a);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 1.5rem;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .ep-badge {
            background: var(--bg-panel);
            color: var(--accent-gold);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-family: monospace;
            border: 1px solid var(--border-color);
            font-size: 0.85rem;
        }

        /* content body */
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }

        .description-box {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #d1d5db;
            padding: 1.5rem;
            background: rgba(31, 41, 55, 0.4);
            border-left: 4px solid var(--accent-gold);
            border-radius: 4px;
            margin-bottom: 2rem;
        }

        /* reviews masonry */
        .reviews-masonry {
            column-count: 1;
            column-gap: 1rem;
            margin-top: 1rem;
        }
        
        @media (min-width: 600px) {
            .reviews-masonry { column-count: 2; }
        }
        @media (min-width: 900px) {
            .reviews-masonry { column-count: 3; }
        }

        .review-card {
            background: rgba(31, 41, 55, 0.4);
            border: 1px solid var(--border-color);
            padding: 1.25rem;
            border-radius: 8px;
            break-inside: avoid;
            margin-bottom: 1rem;
            display: inline-block;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .review-card:hover {
            background: rgba(31, 41, 55, 0.7);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-color: var(--accent-gold);
        }

        .review-title {
            color: var(--accent-gold);
            font-weight: bold;
            font-family: var(--font-header);
            margin-bottom: 0.5rem;
            display: block;
        }

        /* badges */
        .badges-wrapper {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(31, 41, 55, 0.5);
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        .badge {
            font-size: 0.75rem;
            font-weight: bold;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            border: 1px solid currentColor;
            background-color: rgba(255,255,255,0.05);
        }
        .b-Severe { color: #ef4444; }
        .b-Moderate { color: #f97316; }
        .b-Mild { color: #eab308; }
        .b-None { color: #22c55e; }

        /* credits */
        .credits-section {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-color);
        }
        
        .credits-header {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #6b7280;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }

        .director-box {
            margin-bottom: 1.5rem;
            color: var(--text-muted);
        }

        .cast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 0.75rem;
        }

        .cast-card {
            background-color: rgba(31, 41, 55, 0.3);
            border: 1px solid rgba(55, 65, 81, 0.5);
            padding: 0.75rem;
            border-radius: 6px;
            transition: background 0.2s;
        }
        
        .cast-card:hover {
            background-color: rgba(31, 41, 55, 0.6);
            border-color: var(--accent-gold);
        }

        .cast-name {
            color: #e2e8f0;
            font-weight: 500;
            font-size: 0.95rem;
        }

        .cast-role {
            color: #9ca3af;
            font-size: 0.85rem;
            margin-top: 0.25rem;
            font-style: italic;
        }


        /* utils */
        .icon { width: 1em; height: 1em; display: inline-block; vertical-align: middle; fill: currentColor; }
        .flex-center { display: flex; align-items: center; }
        .gap-2 { gap: 0.5rem; }
        .text-gold { color: var(--accent-gold); }
        .loader {
            border: 4px solid #333;
            border-top: 4px solid var(--accent-gold);
            border-radius: 50%;
            width: 40px; height: 40px;
            animation: spin 1s linear infinite;
            margin: 2rem auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .fade-in { animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }


        /* mobile */
        .mobile-toggle { display: none; }

        @media (max-width: 768px) {
            body {
                flex-direction: column;
            }

            aside {
                position: absolute;
                top: 60px;
                left: 0;
                width: 100%;
                height: calc(100% - 60px);
                transform: translateX(-100%);
                background-color: rgba(17, 24, 39, 0.98);
            }
            
            aside.open {
                transform: translateX(0);
            }

            .mobile-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 1rem;
                height: 60px;
                background-color: var(--bg-sidebar);
                border-bottom: 1px solid var(--border-color);
                flex-shrink: 0;
                z-index: 60;
            }

            .mobile-toggle {
                display: block;
                background: none;
                border: none;
                color: var(--accent-gold);
                font-size: 1.5rem;
                cursor: pointer;
            }

            .sidebar-header { display: none; }
            
            .hero-title { font-size: 2.5rem; }
        }

        @media (min-width: 769px) {
            .mobile-header { display: none; }
        }

        /* scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }

    </style>
</head>
<body>

    <div class="mobile-header">
        <h1 class="app-title" style="font-size: 1.2rem;" id="mobile-app-title">IScrapeMDB</h1>
        <button class="mobile-toggle" onclick="toggleSidebar()">
            <svg class="icon" viewBox="0 0 24 24"><path d="M3 6h18v2H3V6m0 5h18v2H3v-2m0 5h18v2H3v-2z"/></svg>
        </button>
    </div>

    <aside id="sidebar">
        <div class="sidebar-header">
            <div class="logo-container">
                <span class="logo-box">I</span>
                <span class="logo-scrape">Scrape</span>
                <span class="logo-box">MDB</span>
            </div>
            
            <div class="controls-container">
                <!-- season buttons injected via js -->
                <div class="season-wrap" id="season-buttons"></div>
                
                <!-- sort -->
                <div class="sort-row">
                    <button class="sort-btn" id="sort-high" onclick="setSort('rate_desc')">Top Rated</button>
                    <button class="sort-btn" id="sort-low" onclick="setSort('rate_asc')">Lowest Rated</button>
                </div>
            </div>
        </div>
        
        <nav class="nav-container" id="episode-list">
            <div class="loader"></div>
        </nav>
        
        <div style="padding: 1rem; text-align: center; color: #6b7280; font-size: 0.75rem; border-top: 1px solid var(--border-color);">
            IscrapeMDB Local
        </div>
    </aside>

    <main id="main-container">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted);">
            <div class="loader"></div>
            <p>Waiting for data...</p>
        </div>
    </main>

    <script>
        // svg icons
        const ICONS = {
            shield: '<svg class="icon" viewBox="0 0 512 512"><path d="M256 0C256 0 256 0 256 0C148.8 6.5 54.5 59.8 19.4 140.6C8.8 165.1 2.2 191.8 0.4 219.4C0.1 223.5 0 227.7 0 231.9C0 231.9 0 231.9 0 231.9C0 395.7 186.2 501.9 251.5 511.2C253 511.4 254.5 511.5 256 511.5C257.5 511.5 259 511.4 260.5 511.2C325.8 501.9 512 395.7 512 231.9C512 231.9 512 231.9 512 231.9C512 227.7 511.9 223.5 511.6 219.4C509.8 191.8 503.2 165.1 492.6 140.6C457.5 59.8 363.2 6.5 256 0H256zM256 64V448C197.8 438.9 64 347.1 64 231.9C64.1 229.3 64.2 226.7 64.3 224.2C79.4 146.9 159.3 103.4 256 94.6V64z"/></svg>',
            star: '<svg class="icon" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>',
            calendar: '<svg class="icon" viewBox="0 0 448 512"><path d="M152 24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H64C28.7 64 0 92.7 0 128v16 48V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V192 144 128c0-35.3-28.7-64-64-64H344V24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H152V24zM48 192H400V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192z"/></svg>',
            clock: '<svg class="icon" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm61.8-104.4l-84.9-61.7c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v141.7l66.8 48.6c5.4 3.9 6.5 11.4 2.6 16.8L334.6 349c-3.9 5.3-11.4 6.5-16.8 2.6z"/></svg>'
        };

        // globals
        let mainData = {};
        let reviewData = {};
        let currentKey = 'main';
        let activeSeason = null;
        let currentSort = 'default';

        // init
        function init() {
            if (typeof MAIN_DATA === 'undefined' || typeof REVIEW_DATA === 'undefined') {
                showError("Data Variables Not Found. <br>Did you rename .json to .js and add 'const MAIN_DATA ='?");
                return;
            }

            mainData = MAIN_DATA;
            reviewData = REVIEW_DATA;

            updateAppTitle();
            initSeasons();
            renderSidebar();
            loadContent('main');
        }

        function toggleSidebar() {
            const sb = document.getElementById('sidebar');
            sb.classList.toggle('open');
        }

        function closeSidebarMobile() {
            document.getElementById('sidebar').classList.remove('open');
        }

        function showError(msg) {
            document.getElementById('main-container').innerHTML = `
                <div style="padding: 2rem; text-align: center;">
                    <h2 style="color: #ef4444; font-size: 1.5rem; margin-bottom: 0.5rem;">Error Loading Data</h2>
                    <p style="color: #9ca3af; margin-bottom: 1rem;">${msg}</p>
                </div>
            `;
            document.getElementById('episode-list').innerHTML = `<div style="color:red; text-align:center; padding:10px;">Load Failed</div>`;
        }

        // data cleanup
        function normalizeItem(key, rawData) {
            // robustness check
            const data = rawData || {};
            const isMain = key === 'main';
            
            const title = data.Title || data.seriesTitle || data.epTitle || "Unknown Title";
            const rate = data.Rate || data.seriesRate || data.epRate || "N/A";
            const date = data.Date || data.seriesDate || data.epDate || "Unknown Date";
            const desc = data.Description || data.seriesDescription || data.epDescription || "No description available.";
            const img = data.seriesImage || data.epImage || data.img || data.image || null;
            
            const runtime = data.Runtime || "";
            const directors = Array.isArray(data.Directors) ? data.Directors : [];
            const cast = Array.isArray(data.Cast) ? data.Cast : [];

            // parents guide
            let pg = {};
            if (Array.isArray(data.ParentsGuide)) {
                data.ParentsGuide.forEach(p => {
                    if (!p || !p.type) return;
                    const t = p.type.toLowerCase();
                    const r = p.rate;
                    if (t.includes('nudity')) pg.Nudity = r;
                    else if (t.includes('violence')) pg.Violence = r;
                    else if (t.includes('profanity')) pg.Profanity = r;
                    else if (t.includes('alcohol') || t.includes('drugs')) pg.Substances = r;
                    else if (t.includes('frightening') || t.includes('intense')) pg.Disturbing = r;
                });
            } else if (data.ParentsGuide) {
                // legacy format
                pg.Nudity = data.Nudity;
                pg.Violence = data.Violence;
                pg.Profanity = data.Profanity;
                pg.Substances = data.Substances;
                pg.Disturbing = data.Disturbing;
            }

            return {
                title, rate, date, description: desc, img,
                runtime, directors, cast,
                ...pg 
            };
        }

        // helpers
        function getSeverityValue(val) {
            if (!val || val === 'None') return 0;
            if (val === 'Mild') return 1;
            if (val === 'Moderate') return 2;
            if (val === 'Severe') return 3;
            return 0;
        }

        function getRuntimeMinutes(rt) {
            if (!rt) return 0;
            let m = 0;
            const hMatch = rt.match(/(\d+)h/);
            const mMatch = rt.match(/(\d+)m/);
            if (hMatch) m += parseInt(hMatch[1]) * 60;
            if (mMatch) m += parseInt(mMatch[1]);
            return m;
        }

        function initSeasons() {
            const keys = Object.keys(mainData).filter(k => k !== 'main');
            const seasons = new Set();
            keys.forEach(k => {
                const match = k.match(/S(\d+)/);
                if (match) seasons.add(`S${match[1]}`);
            });
            
            const sortedSeasons = Array.from(seasons).sort((a,b) => {
                return parseInt(a.substring(1)) - parseInt(b.substring(1));
            });

            if (sortedSeasons.length > 0) {
                const container = document.getElementById('season-buttons');
                let html = '';
                sortedSeasons.forEach(s => {
                    html += `<button class="control-btn season-btn" onclick="toggleSeason('${s}')" id="btn-${s}">${s}</button>`;
                });
                container.innerHTML = html;
            } else {
                document.getElementById('season-buttons').style.display = 'none';
            }
        }

        function toggleSeason(s) {
            if (activeSeason === s) {
                activeSeason = null;
            } else {
                activeSeason = s;
            }
            renderSidebar();
        }

        function setSort(val) {
            if (currentSort === val) {
                currentSort = 'default';
            } else {
                currentSort = val;
            }
            renderSidebar();
        }

        function updateAppTitle() {
            const title = (mainData.main && (mainData.main.Title || mainData.main.seriesTitle)) ? (mainData.main.Title || mainData.main.seriesTitle) : "VikingLogs";
            document.title = `${title} - IscrapeMDB`;
        }

        function getParentsGuide(data) {
            const types = ['Nudity', 'Violence', 'Profanity', 'Substances', 'Disturbing'];
            let badgesHtml = '';
            let hasData = false;
            
            if (!data) return '';

            types.forEach(type => {
                if (data[type]) {
                    badgesHtml += `<span class="badge b-${data[type]}">${type}: ${data[type]}</span>`;
                    hasData = true;
                }
            });

            return hasData ? `
                <div class="badges-wrapper">
                    <div style="width:100%; color:#9ca3af; font-size:0.8rem; font-weight:bold; margin-bottom:0.5rem; text-transform:uppercase;">Parents Guide</div>
                    ${badgesHtml}
                </div>
            ` : '';
        }

        function getCreditsHtml(data) {
            let html = '';
            
            if (data && data.cast && data.cast.length > 0) {
                html += `
                    <div class="credits-section">
                    <div class="credits-header">Cast</div>
                    <div class="cast-grid">
                `;
                
                data.cast.forEach(actor => {
                    if (!actor) return;
                    html += `
                        <div class="cast-card">
                            <div class="cast-name">${actor.name || 'Unknown'}</div>
                            <div class="cast-role">${actor.role || ''}</div>
                        </div>
                    `;
                });
                
                html += `</div></div>`; 
            }
            return html;
        }

        function getReviewsHtml(key) {
            const reviews = reviewData ? reviewData[key] : null;
            let arr = [];
            
            if(reviews && reviews.Reviews && Array.isArray(reviews.Reviews)) {
                // filter nulls
                arr = reviews.Reviews.filter(r => r && typeof r === 'object');
            } else if(reviews && typeof reviews === 'object') {
                arr = Object.entries(reviews).map(([k,v]) => ({ title: k, content: v }));
            }

            if(!arr || arr.length === 0) return '';

            let html = `
            <h3 class="serif-font" style="font-size: 1.5rem; margin-top: 3rem; margin-bottom: 1rem; border-left: 4px solid var(--accent-gold); padding-left: 1rem;">
                Reviews
            </h3>
            <div class="reviews-masonry">`;
            
            arr.forEach(r => {
                if (!r) return;
                html += `
                    <div class="review-card">
                        <span class="review-title">"${r.title || 'Review'}"</span>
                        <p style="font-size: 0.9rem; line-height: 1.5; color: #d1d5db;">"${r.content || r.body || ''}"</p>
                    </div>
                `;
            });
            html += `</div>`;
            return html;
        }

        // renderers
        function renderSidebar() {
            const nav = document.getElementById('episode-list');
            
            // update season btns
            document.querySelectorAll('.season-btn').forEach(btn => {
                if (btn.id === `btn-${activeSeason}`) btn.classList.add('active');
                else btn.classList.remove('active');
            });

            // update sort btns
            const sortHigh = document.getElementById('sort-high');
            const sortLow = document.getElementById('sort-low');
            if(sortHigh) {
                sortHigh.classList.toggle('active', currentSort === 'rate_desc');
                sortHigh.innerText = currentSort === 'rate_desc' ? "Rated High (ON)" : "Top Rated";
            }
            if(sortLow) {
                sortLow.classList.toggle('active', currentSort === 'rate_asc');
                sortLow.innerText = currentSort === 'rate_asc' ? "Rated Low (ON)" : "Lowest Rated";
            }

            let html = `
                <div onclick="loadContent('main')" id="nav-main" class="nav-item">
                    ${ICONS.shield} <span style="margin-left: 0.5rem; font-weight: 500;">Series Overview</span>
                </div>
                <div class="nav-section-label">Episodes ${activeSeason ? `(${activeSeason})` : ''}</div>
            `;

            let keys = Object.keys(mainData).filter(k => k !== 'main');
            
            if (activeSeason) {
                keys = keys.filter(k => k.includes(activeSeason));
            }

            keys.sort((a, b) => {
                const itemA = normalizeItem(a, mainData[a]);
                const itemB = normalizeItem(b, mainData[b]);
                
                switch(currentSort) {
                    case 'rate_desc': return parseFloat(itemB.rate || 0) - parseFloat(itemA.rate || 0);
                    case 'rate_asc': return parseFloat(itemA.rate || 0) - parseFloat(itemB.rate || 0);
                    default:
                        // standard SXXEXX sort
                        const seasonA = parseInt(a.match(/S(\d+)/)?.[1] || 0);
                        const seasonB = parseInt(b.match(/S(\d+)/)?.[1] || 0);
                        if (seasonA !== seasonB) return seasonA - seasonB;
                        const epA = parseInt(a.match(/E(\d+)/)?.[1] || 0);
                        const epB = parseInt(b.match(/E(\d+)/)?.[1] || 0);
                        return epA - epB;
                }
            });

            keys.forEach(key => {
                const item = normalizeItem(key, mainData[key]);
                const safeKey = key.replace(/'/g, "\\'");
                html += `
                    <div onclick="loadContent('${safeKey}')" id="nav-${key}" class="nav-item" title="${item.title}">
                        <span class="ep-code">${key}</span>
                        <span class="ep-title">${item.title}</span>
                    </div>
                `;
            });
            nav.innerHTML = html;
            
            const activeNav = document.getElementById(`nav-${currentKey}`);
            if(activeNav) activeNav.classList.add('active');
        }

        function renderMainView(item) {
            // fallback image
            const searchQuery = encodeURIComponent(item.title + " tv series wallpaper 1920x1080");
            const searchBg = `https://tse2.mm.bing.net/th?q=${searchQuery}&w=1920&h=1080&c=7&rs=1&p=0`;
            const bgUrl = item.img || searchBg;
            
            const runtimeHtml = item.runtime ? `<span style="margin: 0 0.5rem; opacity: 0.5;">|</span> ${ICONS.clock} <span>${item.runtime}</span>` : '';
            const directorHtml = item.directors.length ? `<div class="hero-director">Directed by: ${item.directors.join(', ')}</div>` : '';

            return `
                <div class="content-scrollable fade-in">
                    <div class="hero">
                        <div class="hero-bg" style="background-image: url('${bgUrl}');"></div>
                        <div class="hero-overlay"></div>
                        <div class="hero-content">
                            <h1 class="hero-title serif-font">${item.title}</h1>
                            ${directorHtml}
                            <div class="flex-center gap-2 text-gold" style="justify-content: center; font-size: 1.25rem; font-weight: bold;">
                                ${ICONS.star} <span>${item.rate}</span> ${runtimeHtml}
                            </div>
                        </div>
                    </div>
                    <div class="container">
                        <div class="description-box">
                            ${item.description}
                        </div>
                        ${getParentsGuide(item)}
                        
                        ${getCreditsHtml(item)}
                        
                        ${getReviewsHtml('main')}
                    </div>
                </div>
            `;
        }

        function renderEpisodeView(key, item) {
            const runtimeHtml = item.runtime ? `<span style="margin: 0 0.5rem;">|</span> <span class="flex-center gap-2">${ICONS.clock} ${item.runtime}</span>` : '';
            const directorHtml = item.directors.length ? `<div style="color: #9ca3af; font-size: 0.9rem; margin-top: 0.2rem; font-style: italic;">Directed by: ${item.directors.join(', ')}</div>` : '';
            
            return `
                <div class="content-scrollable fade-in">
                    <div class="ep-header">
                        <div style="min-width: 0;"> <div class="flex-center gap-2">
                                <span class="ep-badge">${key}</span>
                            </div>
                            <h2 class="serif-font" style="font-size: 1.5rem; margin-top: 0.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                ${item.title}
                            </h2>
                            ${directorHtml}
                        </div>
                        <div class="flex-center gap-2" style="font-size: 0.9rem; color: #9ca3af;">
                            <span class="text-gold flex-center gap-2">${ICONS.star} ${item.rate}</span>
                            <span style="margin: 0 0.5rem;">|</span>
                            <span class="flex-center gap-2">${ICONS.calendar} ${item.date}</span>
                            ${runtimeHtml}
                        </div>
                    </div>
                    
                    <div class="container">
                        <div style="background: rgba(31,41,55,0.3); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 2rem;">
                            <p style="font-size: 1.1rem; line-height: 1.6; color: #e2e8f0;">${item.description}</p>
                        </div>

                        ${getParentsGuide(item)}
                        
                        ${getCreditsHtml(item)}

                        <h3 style="margin-top: 3rem; margin-bottom: 1rem; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 0.1em; color: #9ca3af; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
                            Episode Reviews
                        </h3>
                        ${getReviewsHtml(key)}
                    </div>
                </div>
            `;
        }

        function loadContent(key) {
            currentKey = key;
            const container = document.getElementById('main-container');
            const item = normalizeItem(key, mainData[key]);
            
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            const activeNav = document.getElementById(`nav-${key}`);
            if(activeNav) activeNav.classList.add('active');

            // auto-scroll logic
            if(activeNav) {
                activeNav.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }

            if (key === 'main') {
                container.innerHTML = renderMainView(item);
            } else {
                container.innerHTML = renderEpisodeView(key, item);
            }

            closeSidebarMobile();
        }

        window.onload = init;
    </script>
</body>
</html>"""
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        filesCreation("HTML SERIES", file_path)
    except Exception as e:
        return e

def createIndexLists(folder_path):
    # makes the list view index.html.
    
    # checks if dir exists
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Created directory: {folder_path}")
        except OSError as e:
            print(f"Error creating directory {folder_path}: {e}")
            return

    file_path = os.path.join(folder_path, "index.html")

    # main html content
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie List - IscrapeMDB</title>
    
    <!-- offline favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 5 L85 20 V50 C85 75 50 95 50 95 C50 95 15 75 15 50 V20 Z' fill='%23111827' stroke='%23d4af37' stroke-width='5'/><text x='50' y='65' font-family='serif' font-weight='bold' font-size='50' text-anchor='middle' fill='%23d4af37'>I</text></svg>">

    <script src="data/main.js"></script>
    <script src="data/review.js"></script>
    
    <style>
        /* vars */
        :root {
            --bg-dark: #0f1115;
            --bg-sidebar: #111827;
            --bg-panel: #1f2937;
            --bg-hover: rgba(212, 175, 55, 0.1);
            
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-gold: #d4af37;
            --border-color: #374151;
            
            --sidebar-width: 280px;
            --font-main: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            --font-header: 'Georgia', 'Times New Roman', serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: var(--font-main);
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            display: flex;
        }

        /* typography */
        h1, h2, h3, .serif-font { font-family: var(--font-header); }
        a { text-decoration: none; color: inherit; }

        /* layout */
        aside {
            width: var(--sidebar-width);
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            transition: transform 0.3s ease;
            z-index: 50;
        }

        .sidebar-header {
            padding: 1.5rem 1rem;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
        }

        .logo-container {
            font-family: var(--font-main);
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
        }
        
        .logo-box { background-color: var(--accent-gold); color: #000; padding: 2px 6px; border-radius: 4px; display: inline-block; line-height: 1; }
        .logo-scrape { color: #6b7280; font-weight: 700; }

        .list-meta {
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }

        /* controls */
        .controls-container {
            padding: 0 0 0.5rem 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .sort-row { display: flex; gap: 0.5rem; }
        
        .sort-btn {
            flex: 1;
            background: rgba(31, 41, 55, 0.5);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }

        .sort-btn:hover { background: var(--bg-hover); color: var(--accent-gold); }
        .sort-btn.active { border-color: var(--accent-gold); color: var(--accent-gold); background: rgba(212, 175, 55, 0.05); }

        .nav-container { flex: 1; overflow-y: auto; padding: 0; }

        /* nav items */
        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1.5rem;
            color: var(--text-muted);
            border-left: 3px solid transparent;
            transition: all 0.2s;
            cursor: pointer;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }

        .nav-item:hover { background-color: var(--bg-hover); color: var(--accent-gold); }
        .nav-item.active { background-color: rgba(212, 175, 55, 0.15); border-left: 3px solid var(--accent-gold); color: var(--accent-gold); }
        
        .nav-item .ep-title {
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.9rem;
        }

        /* hide items that don't match search */
        .nav-item.hidden-search { display: none !important; }

        .nav-section-label {
            padding: 1rem 1.5rem 0.5rem;
            font-size: 0.75rem;
            font-weight: bold;
            color: #4b5563;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            background: var(--bg-sidebar);
            position: sticky; top: 0; z-index: 10;
        }

        /* main content */
        main {
            flex: 1; position: relative; display: flex; flex-direction: column; overflow: hidden; background-color: var(--bg-dark);
        }

        .content-scrollable { overflow-y: auto; height: 100%; width: 100%; }

        /* hero section */
        .hero {
            position: relative; height: 300px;
            display: flex; align-items: center;
            justify-content: center;
            background-color: #000; overflow: hidden;
            border-bottom: 1px solid var(--border-color);
        }
        
        .hero-bg {
            position: absolute; inset: 0; background-size: cover; background-position: center; opacity: 0.3; filter: blur(10px);
        }
        
        .hero-overlay {
            position: absolute; inset: 0; background: linear-gradient(to top, var(--bg-dark), rgba(15, 17, 21, 0.5), transparent);
        }
        
        .hero-content {
            position: relative; z-index: 10; 
            text-align: center;
            padding: 2rem; 
            max-width: 800px;
            width: 100%;
        }

        .hero-title {
            font-size: clamp(2rem, 5vw, 4rem); font-weight: 900; margin-bottom: 0.5rem; text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        }

        /* search input */
        .hero-search-wrapper {
            margin: 1.5rem auto 0;
            max-width: 300px;
        }

        .hero-search-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.9rem;
            backdrop-filter: blur(5px);
            transition: all 0.2s;
        }

        .hero-search-input:focus {
            background: rgba(0, 0, 0, 0.8);
            border-color: var(--accent-gold);
            outline: none;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        }

        /* grid */
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
        }

        .movie-card-main {
            background: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
            display: flex; flex-direction: column;
            min-height: 100px;
        }

        .movie-card-main.hidden-search { display: none; }

        .movie-card-main:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            border-color: var(--accent-gold);
        }

        .mc-info { padding: 1rem; flex: 1; display: flex; flex-direction: column; justify-content: center; }
        .mc-title { font-weight: bold; margin-bottom: 0.5rem; color: #e2e8f0; font-family: var(--font-header); font-size: 1.1rem; }
        .mc-meta { margin-top: auto; display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-muted); }

        /* details */
        .ep-header {
            background: linear-gradient(to right, #1e293b, #0f172a);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 1.5rem;
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .back-btn {
            background: transparent; border: 1px solid var(--border-color); color: var(--text-muted);
            padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem;
            transition: all 0.2s;
            width: fit-content;
        }
        .back-btn:hover { background: var(--bg-hover); color: var(--accent-gold); border-color: var(--accent-gold); }

        .delete-btn {
            background: transparent; border: none; color: #4b5563;
            padding: 0.5rem; cursor: pointer; font-size: 1rem; display: flex; align-items: center;
            transition: color 0.2s; margin-left: auto;
        }
        .delete-btn:hover { color: #ef4444; }

        .container { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }

        .description-box {
            font-size: 1.1rem; line-height: 1.6; color: #d1d5db; padding: 1.5rem;
            background: rgba(31, 41, 55, 0.4); border-left: 4px solid var(--accent-gold); border-radius: 4px; margin-bottom: 2rem;
        }

        /* review & cast cards */
        .reviews-masonry { column-count: 1; column-gap: 1rem; margin-top: 1rem; }
        @media (min-width: 600px) { .reviews-masonry { column-count: 2; } }

        .review-card {
            background: rgba(31, 41, 55, 0.4); border: 1px solid var(--border-color); padding: 1.25rem; border-radius: 8px;
            break-inside: avoid; margin-bottom: 1rem; display: inline-block; width: 100%;
        }
        .review-title { color: var(--accent-gold); font-weight: bold; font-family: var(--font-header); margin-bottom: 0.5rem; display: block; }

        .badges-wrapper {
            display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; padding: 1rem;
            background: rgba(31, 41, 55, 0.5); border-radius: 6px; border: 1px solid var(--border-color);
        }
        .badge {
            font-size: 0.75rem; font-weight: bold; padding: 0.25rem 0.5rem; border-radius: 4px; text-transform: uppercase;
            border: 1px solid currentColor; background-color: rgba(255,255,255,0.05);
        }
        .b-Severe { color: #ef4444; } .b-Moderate { color: #f97316; } .b-Mild { color: #eab308; } .b-None { color: #22c55e; }

        /* utils */
        .icon { width: 1em; height: 1em; display: inline-block; vertical-align: middle; fill: currentColor; }
        .flex-center { display: flex; align-items: center; }
        .gap-2 { gap: 0.5rem; }
        .text-gold { color: var(--accent-gold); }
        .loader {
            border: 4px solid #333; border-top: 4px solid var(--accent-gold); border-radius: 50%;
            width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 2rem auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .fade-in { animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* mobile */
        .mobile-header { display: none; }
        @media (max-width: 768px) {
            body { flex-direction: column; }
            aside { position: absolute; top: 60px; left: 0; width: 100%; height: calc(100% - 60px); transform: translateX(-100%); background-color: rgba(17, 24, 39, 0.98); }
            aside.open { transform: translateX(0); }
            .mobile-header { display: flex; align-items: center; justify-content: space-between; padding: 0 1rem; height: 60px; background: var(--bg-sidebar); border-bottom: 1px solid var(--border-color); flex-shrink: 0; z-index: 60; }
            .mobile-toggle { display: block; background: none; border: none; color: var(--accent-gold); font-size: 1.5rem; cursor: pointer; }
            .sidebar-header { display: none; }
            .hero-title { font-size: 2.5rem; }
            
            .hero-content { text-align: center; padding: 1.5rem; }
            .hero { justify-content: center; }
            .hero-search-wrapper { margin: 1.5rem auto 0; }
        }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
    </style>
</head>
<body>

    <div class="mobile-header">
        <h1 class="app-title" style="font-size: 1.2rem;">IScrapeMDB</h1>
        <button class="mobile-toggle" onclick="toggleSidebar()">
            <svg class="icon" viewBox="0 0 24 24"><path d="M3 6h18v2H3V6m0 5h18v2H3v-2m0 5h18v2H3v-2z"/></svg>
        </button>
    </div>

    <aside id="sidebar">
        <div class="sidebar-header">
            <div class="logo-container">
                <span class="logo-box">I</span>
                <span class="logo-scrape">Scrape</span>
                <span class="logo-box">MDB</span>
            </div>
            
            <div class="controls-container">
                <div class="sort-row">
                    <button class="sort-btn" id="sort-high" onclick="setSort('rate_desc')">Top Rated</button>
                    <button class="sort-btn" id="sort-low" onclick="setSort('rate_asc')">Lowest Rated</button>
                </div>
            </div>
        </div>
        
        <nav class="nav-container" id="movie-list">
            <div class="loader"></div>
        </nav>
        
        <div style="padding: 1rem; text-align: center; color: #6b7280; font-size: 0.75rem; border-top: 1px solid var(--border-color);">
            IscrapeMDB Local
        </div>
    </aside>

    <main id="main-container">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted);">
            <div class="loader"></div>
            <p>Loading List...</p>
        </div>
    </main>

    <script>
        const ICONS = {
            star: '<svg class="icon" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>',
            calendar: '<svg class="icon" viewBox="0 0 448 512"><path d="M152 24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H64C28.7 64 0 92.7 0 128v16 48V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V192 144 128c0-35.3-28.7-64-64-64H344V24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H152V24zM48 192H400V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192z"/></svg>',
            clock: '<svg class="icon" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm61.8-104.4l-84.9-61.7c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v141.7l66.8 48.6c5.4 3.9 6.5 11.4 2.6 16.8L334.6 349c-3.9 5.3-11.4 6.5-16.8 2.6z"/></svg>',
            back: '<svg class="icon" viewBox="0 0 448 512"><path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/></svg>',
            trash: '<svg class="icon" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>'
        };

        // state vars
        let mainData = {};
        let listInfo = {};
        let reviewData = {};
        let currentSort = 'default';
        let isMainView = true;
        let shuffledKeys = [];

        function init() {
            if (typeof MAIN_DATA === 'undefined' || typeof REVIEW_DATA === 'undefined') {
                document.getElementById('main-container').innerHTML = `<h2 style="color:red; text-align:center;">Data Not Found. Check main.js/review.js</h2>`;
                return;
            }

            // separate list info from movies if it exists
            if(MAIN_DATA.list_info) {
                listInfo = MAIN_DATA.list_info;
                // prevent list_info from showing up as a movie
                delete MAIN_DATA.list_info; 
            } else {
                listInfo = { ListName: "My Movie List", DateCreated: "Unknown" };
            }
            
            document.title = `${listInfo.ListName || 'My List'} - IscrapeMDB`;

            mainData = MAIN_DATA;
            reviewData = REVIEW_DATA;
            
            // random sort + filter bad keys
            shuffledKeys = Object.keys(mainData)
                .filter(k => k !== "ERR")
                .sort(() => 0.5 - Math.random());

            renderSidebar();
            loadMainList(); 
        }

        function toggleSidebar() { document.getElementById('sidebar').classList.toggle('open'); }
        function closeSidebarMobile() { document.getElementById('sidebar').classList.remove('open'); }

        // data cleanup
        function normalizeItem(key, rawData) {
            // data null check to prevent crashes
            const data = rawData || {};

            return {
                title: data.Title || key || "Unknown Title",
                rate: data.Rate || "N/A",
                date: data.Date || "N/A",
                description: data.Description || "No description available.",
                img: data.seriesImage || data.img || data.image || null,
                runtime: data.Runtime || "",
                directors: Array.isArray(data.Directors) ? data.Directors : [],
                cast: Array.isArray(data.Cast) ? data.Cast : [],
                // parents guide checks
                Nudity: getPGValue(data.ParentsGuide, 'nudity'),
                Violence: getPGValue(data.ParentsGuide, 'violence'),
                Profanity: getPGValue(data.ParentsGuide, 'profanity'),
                Substances: getPGValue(data.ParentsGuide, 'alcohol') || getPGValue(data.ParentsGuide, 'drugs'),
                Disturbing: getPGValue(data.ParentsGuide, 'frightening') || getPGValue(data.ParentsGuide, 'intense')
            };
        }

        function getPGValue(pgArray, keyword) {
            if(!Array.isArray(pgArray)) return null;
            const item = pgArray.find(p => p.type && p.type.toLowerCase().includes(keyword));
            return item ? item.rate : null;
        }

        function formatDate(dateStr) {
            if (!dateStr) return "";
            try {
                // simple date formatting, fail gracefully
                const parts = dateStr.split(' ')[0].split('-');
                if(parts.length === 3) {
                    return `${parts[0].slice(2)}/${parts[1]}/${parts[2]}`;
                }
                return dateStr;
            } catch(e) { return dateStr; }
        }

        function setSort(val) {
            currentSort = (currentSort === val) ? 'default' : val;
            renderSidebar();
            if(isMainView) loadMainList();
        }

        // search logic
        function filterMovies(query) {
            const lowerQuery = (query || '').toLowerCase();
            
            // filter sidebar
            const navItems = document.querySelectorAll('#movie-list .nav-item[title]');
            navItems.forEach(item => {
                const title = (item.getAttribute('title') || '').toLowerCase();
                if(title.includes(lowerQuery)) {
                    item.classList.remove('hidden-search');
                } else {
                    item.classList.add('hidden-search');
                }
            });

            // filter main grid
            const gridItems = document.querySelectorAll('.movie-card-main');
            if(gridItems.length > 0) {
                gridItems.forEach(card => {
                    const titleEl = card.querySelector('.mc-title');
                    const title = titleEl ? titleEl.innerText.toLowerCase() : '';
                    
                    if(title.includes(lowerQuery)) {
                        card.classList.remove('hidden-search');
                    } else {
                        card.classList.add('hidden-search');
                    }
                });
            }
        }

        function deleteMovie(key) {
            if(confirm(`Remove "${key}" from this view?`)) {
                // remove from local state
                delete mainData[key];
                if(reviewData[key]) delete reviewData[key];
                
                // update keys list
                shuffledKeys = shuffledKeys.filter(k => k !== key);
                
                // refresh
                renderSidebar();
                loadMainList();
            }
        }

        // renderers
        function getSortedKeys() {
            let keys = (currentSort === 'default') ? [...shuffledKeys] : Object.keys(mainData).filter(k => k !== "ERR");
            
            // double check existence
            keys = keys.filter(k => mainData[k]);

            if (currentSort === 'rate_desc' || currentSort === 'rate_asc') {
                return keys.sort((a, b) => {
                    const itemA = normalizeItem(a, mainData[a]);
                    const itemB = normalizeItem(b, mainData[b]);
                    
                    const rateA = parseFloat(itemA.rate) || 0;
                    const rateB = parseFloat(itemB.rate) || 0;
                    
                    if (currentSort === 'rate_desc') return rateB - rateA;
                    if (currentSort === 'rate_asc') return rateA - rateB;
                    return 0;
                });
            }
            return keys;
        }

        function renderSidebar() {
            const nav = document.getElementById('movie-list');
            const sortHigh = document.getElementById('sort-high');
            const sortLow = document.getElementById('sort-low');
            
            if(sortHigh) sortHigh.classList.toggle('active', currentSort === 'rate_desc');
            if(sortLow) sortLow.classList.toggle('active', currentSort === 'rate_asc');

            let html = '';
            
            if (!isMainView) {
                html += `
                    <div onclick="loadMainList()" class="nav-item">
                        ${ICONS.back} <span style="margin-left: 0.5rem; font-weight: 500;">Main List</span>
                    </div>`;
            }
            
            html += `<div class="nav-section-label">Movies</div>`;

            const keys = getSortedKeys();
            keys.forEach(key => {
                const item = normalizeItem(key, mainData[key]);
                const safeKey = key.replace(/'/g, "\\'");
                html += `
                    <div onclick="loadMovie('${safeKey}')" class="nav-item" title="${item.title}">
                        <span class="ep-title">${item.title}</span>
                    </div>
                `;
            });
            nav.innerHTML = html;
        }

        // 1. main list view
        function loadMainList() {
            isMainView = true;
            renderSidebar(); 

            const container = document.getElementById('main-container');
            const keys = getSortedKeys();
            const fmtDate = formatDate(listInfo.DateCreated);

            // random bg from list logic
            let heroBgStyle = "";
            if(keys.length > 0) {
                const randomKey = keys[Math.floor(Math.random() * keys.length)];
                const randomMovie = normalizeItem(randomKey, mainData[randomKey]);
                
                if(randomMovie.img) {
                    heroBgStyle = `background-image: url('${randomMovie.img}');`;
                } else {
                    const searchQuery = encodeURIComponent(randomMovie.title + " movie wallpaper 1920x1080");
                    const bgUrl = `https://tse2.mm.bing.net/th?q=${searchQuery}&w=1920&h=1080&c=7&rs=1&p=0`;
                    heroBgStyle = `background-image: url('${bgUrl}');`;
                }
            }

            let gridHtml = `<div class="movie-grid">`;
            keys.forEach(key => {
                const item = normalizeItem(key, mainData[key]);
                const safeKey = key.replace(/'/g, "\\'");
                
                gridHtml += `
                    <div class="movie-card-main" onclick="loadMovie('${safeKey}')">
                        <div class="mc-info">
                            <div class="mc-title">${item.title}</div>
                            <div class="mc-meta">
                                <span class="text-gold flex-center" style="gap:4px">${ICONS.star} ${item.rate}</span>
                                <span>${item.date}</span>
                            </div>
                        </div>
                    </div>
                `;
            });
            gridHtml += `</div>`;

            container.innerHTML = `
                <div class="content-scrollable fade-in">
                    <div class="hero">
                        <div class="hero-bg" style="${heroBgStyle}"></div>
                        <div class="hero-overlay"></div>
                        <div class="hero-content">
                            <h1 class="hero-title serif-font">${listInfo.ListName || 'Movies'}</h1>
                            <div class="list-meta">
                                Created: <span class="text-gold">${fmtDate}</span> • ${keys.length} Movies
                            </div>
                            
                            <!-- main search bar -->
                            <div class="hero-search-wrapper">
                                <input type="text" id="movie-search" class="hero-search-input" placeholder="Search..." oninput="filterMovies(this.value)">
                            </div>
                        </div>
                    </div>
                    ${gridHtml}
                </div>
            `;
            
            closeSidebarMobile();
        }

        // 2. single movie view
        function loadMovie(key) {
            isMainView = false;
            renderSidebar();

            const container = document.getElementById('main-container');
            const item = normalizeItem(key, mainData[key]);
            
            // bg fallback
            const searchQuery = encodeURIComponent(item.title + " movie wallpaper 1920x1080");
            const bgUrl = item.img || `https://tse2.mm.bing.net/th?q=${searchQuery}&w=1920&h=1080&c=7&rs=1&p=0`;

            const directorStr = (item.directors && item.directors.length) 
                ? `Directed by: <span style="color: #e2e8f0;">${item.directors.join(', ')}</span>` 
                : '';

            const parentsGuideHTML = getParentsGuideHtml(item);
            const castHTML = getCastHtml(item.cast);
            const reviewsHTML = getReviewsHtml(key);
            const safeKey = key.replace(/'/g, "\\'");

            container.innerHTML = `
                <div class="content-scrollable fade-in">
                    <div class="ep-header">
                        <button class="back-btn" onclick="loadMainList()">
                            ${ICONS.back} Back to List
                        </button>
                        <div style="flex:1; text-align:center; display:flex; justify-content:center; align-items:center;">
                            <span class="text-gold" style="font-weight:bold; font-size:1.1rem;">${item.title}</span>
                        </div>
                        <button class="delete-btn" onclick="deleteMovie('${safeKey}')" title="Remove Movie">
                            ${ICONS.trash}
                        </button>
                    </div>
                    
                    <div class="hero" style="height: 350px;">
                        <div class="hero-bg" style="background-image: url('${bgUrl}'); opacity: 0.4;"></div>
                        <div class="hero-overlay"></div>
                        <div class="hero-content">
                            <h1 class="hero-title serif-font">${item.title}</h1>
                            <div class="flex-center gap-2" style="justify-content: center; color: #9ca3af; font-size: 1rem; margin-top:0.5rem;">
                                <span class="text-gold flex-center gap-2">${ICONS.star} ${item.rate}</span>
                                <span>|</span>
                                <span>${item.date}</span>
                                ${item.runtime ? `<span>|</span> <span>${item.runtime}</span>` : ''}
                            </div>
                        </div>
                    </div>

                    <div class="container">
                        ${directorStr ? `<div style="margin-bottom:1rem; color:#9ca3af; font-size:0.9rem;">${directorStr}</div>` : ''}
                        
                        <div style="background: rgba(31,41,55,0.3); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 2rem;">
                            <p style="font-size: 1.1rem; line-height: 1.6; color: #e2e8f0;">${item.description}</p>
                        </div>

                        ${parentsGuideHTML}
                        ${castHTML}

                        ${reviewsHTML}
                    </div>
                </div>
            `;
            closeSidebarMobile();
        }

        // html generators
        function getParentsGuideHtml(item) {
            const types = ['Nudity', 'Violence', 'Profanity', 'Substances', 'Disturbing'];
            let html = '';
            let hasData = false;
            if (!item) return '';

            types.forEach(t => {
                if(item[t] && item[t] !== 'None' && item[t] !== '') {
                    html += `<span class="badge b-${item[t]}">${t}: ${item[t]}</span>`;
                    hasData = true;
                }
            });
            return hasData ? `<div class="badges-wrapper"><div style="width:100%; color:#9ca3af; font-size:0.8rem; font-weight:bold; margin-bottom:0.5rem; text-transform:uppercase;">Parents Guide</div>${html}</div>` : '';
        }

        function getCastHtml(cast) {
            if (!cast || !Array.isArray(cast) || cast.length === 0) return '';
            
            let html = `<h3 class="serif-font" style="font-size: 1.2rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Cast</h3>`;
            html += `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem;">`;
            
            cast.forEach(c => {
                if (c && c.name) {
                    html += `
                        <div style="background: rgba(31, 41, 55, 0.4); padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border-color); text-align: center;">
                            <div style="font-weight: bold; color: #e2e8f0; font-size: 0.9rem;">${c.name}</div>
                            <div style="color: var(--accent-gold); font-size: 0.8rem; margin-top: 0.25rem;">${c.role || ''}</div>
                        </div>
                    `;
                }
            });
            html += `</div>`;
            return html;
        }

        function getReviewsHtml(key) {
            const reviews = reviewData ? reviewData[key] : null;
            let arr = [];
            
            if(reviews && reviews.Reviews && Array.isArray(reviews.Reviews)) {
                arr = reviews.Reviews;
            } else if(reviews && typeof reviews === 'object') {
                arr = Object.entries(reviews).map(([k,v]) => ({ title: k, content: v }));
            }

            if(!arr || arr.length === 0) return '';

            let html = `
            <h3 class="serif-font" style="font-size: 1.5rem; margin-top: 3rem; margin-bottom: 1rem; border-left: 4px solid var(--accent-gold); padding-left: 1rem;">
                Reviews
            </h3>
            <div class="reviews-masonry">`;
            
            arr.forEach(r => {
                if (r && (r.title || r.content || r.body)) {
                    html += `
                        <div class="review-card">
                            <span class="review-title">"${r.title || 'Review'}"</span>
                            <p style="font-size: 0.9rem; line-height: 1.5; color: #d1d5db;">"${r.content || r.body || '...'}"</p>
                        </div>
                    `;
                }
            });
            html += `</div>`;
            return html;
        }

        window.onload = init;
    </script>
</body>
</html>"""
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        filesCreation("HTML LIST", file_path)
    except Exception as e:
        return e
    
def createIndexMovie(folder_path):
    # generates the single movie page. keeps it simple.
    
    # check if dir exists, if not make it
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Created directory: {folder_path}")
        except OSError as e:
            print(f"Error creating directory {folder_path}: {e}")
            return

    file_path = os.path.join(folder_path, "index.html")

    # main html string
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie - IscrapeMDB</title>
    
    <!-- offline favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 5 L85 20 V50 C85 75 50 95 50 95 C50 95 15 75 15 50 V20 Z' fill='%23111827' stroke='%23d4af37' stroke-width='5'/><text x='50' y='65' font-family='serif' font-weight='bold' font-size='50' text-anchor='middle' fill='%23d4af37'>I</text></svg>">

    <script src="data/main.js"></script>
    <script src="data/review.js"></script>
    
    <style>
        /* vars & setup */
        :root {
            --bg-dark: #0f1115;
            --bg-sidebar: #111827;
            --bg-panel: #1f2937;
            --bg-hover: rgba(212, 175, 55, 0.1);
            
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --accent-gold: #d4af37;
            --border-color: #374151;
            
            --font-main: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            --font-header: 'Georgia', 'Times New Roman', serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: var(--font-main);
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* typography */
        h1, h2, h3, .serif-font { font-family: var(--font-header); }
        a { text-decoration: none; color: inherit; }

        /* layout stuff */
        
        /* header */
        header.app-header {
            padding: 1rem 2rem;
            background-color: var(--bg-sidebar);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 50;
        }

        .logo-container {
            font-family: var(--font-main);
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 3px;
        }
        
        .logo-box { background-color: var(--accent-gold); color: #000; padding: 2px 6px; border-radius: 4px; display: inline-block; line-height: 1; }
        .logo-scrape { color: #6b7280; font-weight: 700; }

        /* main content area */
        main {
            flex: 1; position: relative; display: flex; flex-direction: column; overflow: hidden; background-color: var(--bg-dark);
        }

        .content-scrollable { overflow-y: auto; height: 100%; width: 100%; }

        /* hero banner */
        .hero {
            position: relative; height: 400px;
            display: flex; align-items: center; justify-content: center;
            background-color: #000; overflow: hidden;
            border-bottom: 1px solid var(--border-color);
        }
        
        .hero-bg {
            position: absolute; inset: 0; background-size: cover; background-position: center; opacity: 0.4;
        }
        
        .hero-overlay {
            position: absolute; inset: 0; background: linear-gradient(to top, var(--bg-dark), rgba(15, 17, 21, 0.5), transparent);
        }
        
        .hero-content {
            position: relative; z-index: 10; text-align: center; padding: 1rem; max-width: 900px;
        }

        .hero-title {
            font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 900; margin-bottom: 0.5rem; text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        }

        .container { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }

        .description-box {
            font-size: 1.2rem; line-height: 1.7; color: #d1d5db; padding: 1.5rem;
            background: rgba(31, 41, 55, 0.4); border-left: 4px solid var(--accent-gold); border-radius: 4px; margin-bottom: 2rem;
        }

        /* cards */
        .reviews-masonry { column-count: 1; column-gap: 1rem; margin-top: 1rem; }
        @media (min-width: 600px) { .reviews-masonry { column-count: 2; } }

        .review-card {
            background: rgba(31, 41, 55, 0.4); border: 1px solid var(--border-color); padding: 1.25rem; border-radius: 8px;
            break-inside: avoid; margin-bottom: 1rem; display: inline-block; width: 100%;
        }
        .review-title { color: var(--accent-gold); font-weight: bold; font-family: var(--font-header); margin-bottom: 0.5rem; display: block; }

        .badges-wrapper {
            display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; padding: 1rem;
            background: rgba(31, 41, 55, 0.5); border-radius: 6px; border: 1px solid var(--border-color);
        }
        .badge {
            font-size: 0.75rem; font-weight: bold; padding: 0.25rem 0.5rem; border-radius: 4px; text-transform: uppercase;
            border: 1px solid currentColor; background-color: rgba(255,255,255,0.05);
        }
        .b-Severe { color: #ef4444; } .b-Moderate { color: #f97316; } .b-Mild { color: #eab308; } .b-None { color: #22c55e; }

        /* helpers */
        .icon { width: 1em; height: 1em; display: inline-block; vertical-align: middle; fill: currentColor; }
        .flex-center { display: flex; align-items: center; }
        .gap-2 { gap: 0.5rem; }
        .text-gold { color: var(--accent-gold); }
        .loader {
            border: 4px solid #333; border-top: 4px solid var(--accent-gold); border-radius: 50%;
            width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 2rem auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .fade-in { animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
    </style>
</head>
<body>

    <header class="app-header">
        <div class="logo-container">
            <span class="logo-box">I</span>
            <span class="logo-scrape">Scrape</span>
            <span class="logo-box">MDB</span>
        </div>
    </header>

    <main id="main-container">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted);">
            <div class="loader"></div>
            <p>Loading Movie...</p>
        </div>
    </main>

    <script>
        const ICONS = {
            star: '<svg class="icon" viewBox="0 0 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>',
            calendar: '<svg class="icon" viewBox="0 0 448 512"><path d="M152 24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H64C28.7 64 0 92.7 0 128v16 48V448c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V192 144 128c0-35.3-28.7-64-64-64H344V24c0-13.3-10.7-24-24-24s-24 10.7-24 24V64H152V24zM48 192H400V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192z"/></svg>',
            clock: '<svg class="icon" viewBox="0 0 512 512"><path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm61.8-104.4l-84.9-61.7c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v141.7l66.8 48.6c5.4 3.9 6.5 11.4 2.6 16.8L334.6 349c-3.9 5.3-11.4 6.5-16.8 2.6z"/></svg>'
        };

        // globals
        let mainData = {};
        let reviewData = {};

        function init() {
            if (typeof MAIN_DATA === 'undefined' || typeof REVIEW_DATA === 'undefined') {
                document.getElementById('main-container').innerHTML = `<h2 style="color:red; text-align:center;">Data Not Found. Check main.js/review.js</h2>`;
                return;
            }

            mainData = MAIN_DATA;
            reviewData = REVIEW_DATA;
            
            // grab the first movie only
            let keys = Object.keys(mainData).filter(k => k !== 'list_info');
            if(keys.length > 0) {
                loadMovie(keys[0]);
            } else {
                document.getElementById('main-container').innerHTML = `<div style="padding:2rem; text-align:center; color:#9ca3af;">No movie data found.</div>`;
            }
        }

        // data cleanup & null checks
        function normalizeItem(key, data) {
            // safe defaults for everything so it doesn't glitch
            if (!data) data = {};
            
            return {
                title: data.Title || key || "Unknown Title",
                rate: data.Rate || "N/A",
                date: data.Date || "N/A",
                description: data.Description || "No description available.",
                img: data.seriesImage || data.img || data.image || null,
                runtime: data.Runtime || "",
                directors: Array.isArray(data.Directors) ? data.Directors : [],
                cast: Array.isArray(data.Cast) ? data.Cast : [],
                
                // parents guide fallbacks
                Nudity: getPGValue(data.ParentsGuide, 'nudity'),
                Violence: getPGValue(data.ParentsGuide, 'violence'),
                Profanity: getPGValue(data.ParentsGuide, 'profanity'),
                Substances: getPGValue(data.ParentsGuide, 'alcohol') || getPGValue(data.ParentsGuide, 'drugs'),
                Disturbing: getPGValue(data.ParentsGuide, 'frightening') || getPGValue(data.ParentsGuide, 'intense')
            };
        }

        function getPGValue(pgArray, keyword) {
            if(!Array.isArray(pgArray)) return null;
            const item = pgArray.find(p => p.type && p.type.toLowerCase().includes(keyword));
            return item ? item.rate : null;
        }

        // render the movie
        function loadMovie(key) {
            const container = document.getElementById('main-container');
            // ensure we don't pass null data
            const item = normalizeItem(key, mainData[key]);
            
            document.title = `${item.title} - IscrapeMDB`;
            
            // fallback bg if image is toast
            const searchQuery = encodeURIComponent(item.title + " movie wallpaper 1920x1080");
            const bgUrl = item.img || `https://tse2.mm.bing.net/th?q=${searchQuery}&w=1920&h=1080&c=7&rs=1&p=0`;

            // render directors safely
            const directorStr = (item.directors && item.directors.length) 
                ? `Directed by: <span style="color: #e2e8f0;">${item.directors.join(', ')}</span>` 
                : '';

            container.innerHTML = `
                <div class="content-scrollable fade-in">
                    
                    <div class="hero">
                        <div class="hero-bg" style="background-image: url('${bgUrl}');"></div>
                        <div class="hero-overlay"></div>
                        <div class="hero-content">
                            <h1 class="hero-title serif-font">${item.title}</h1>
                            <div class="flex-center gap-2" style="justify-content: center; color: #9ca3af; font-size: 1.1rem; margin-top:0.5rem;">
                                <span class="text-gold flex-center gap-2">${ICONS.star} ${item.rate}</span>
                                <span>|</span>
                                <span>${item.date}</span>
                                ${item.runtime ? `<span>|</span> <span>${item.runtime}</span>` : ''}
                            </div>
                        </div>
                    </div>

                    <div class="container">
                        ${directorStr ? `<div style="margin-bottom:1rem; color:#9ca3af; font-size:1rem; text-align:center;">${directorStr}</div>` : ''}
                        
                        <div class="description-box">
                            ${item.description}
                        </div>

                        ${getParentsGuideHtml(item)}
                        ${getCastHtml(item.cast)}

                        <h3 class="serif-font" style="font-size: 1.5rem; margin-top: 3rem; margin-bottom: 1rem; border-left: 4px solid var(--accent-gold); padding-left: 1rem;">
                            Reviews
                        </h3>
                        ${getReviewsHtml(key)}
                    </div>
                </div>
            `;
        }

        // generators
        function getParentsGuideHtml(item) {
            const types = ['Nudity', 'Violence', 'Profanity', 'Substances', 'Disturbing'];
            let html = '';
            let hasData = false;
            
            if (!item) return '';

            types.forEach(t => {
                if(item[t]) {
                    html += `<span class="badge b-${item[t]}">${t}: ${item[t]}</span>`;
                    hasData = true;
                }
            });
            return hasData ? `<div class="badges-wrapper"><div style="width:100%; color:#9ca3af; font-size:0.8rem; font-weight:bold; margin-bottom:0.5rem; text-transform:uppercase;">Parents Guide</div>${html}</div>` : '';
        }

        function getCastHtml(cast) {
            // rigorous checks to prevent glitches
            if (!cast || !Array.isArray(cast) || cast.length === 0) return '';
            
            let html = `<h3 class="serif-font" style="font-size: 1.2rem; margin-top: 2rem; margin-bottom: 1rem; color: var(--text-muted); border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">Cast</h3>`;
            html += `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem;">`;
            
            cast.forEach(c => {
                if(c && c.name) {
                    html += `
                        <div style="background: rgba(31, 41, 55, 0.4); padding: 0.75rem; border-radius: 6px; border: 1px solid var(--border-color); text-align: center;">
                            <div style="font-weight: bold; color: #e2e8f0; font-size: 0.9rem;">${c.name}</div>
                            <div style="color: var(--accent-gold); font-size: 0.8rem; margin-top: 0.25rem;">${c.role || ''}</div>
                        </div>
                    `;
                }
            });
            html += `</div>`;
            return html;
        }

        function getReviewsHtml(key) {
            // safe access
            const reviews = reviewData ? reviewData[key] : null;
            let arr = [];

            if(reviews && reviews.Reviews && Array.isArray(reviews.Reviews)) {
                arr = reviews.Reviews;
            } else if(reviews && typeof reviews === 'object') {
                arr = Object.entries(reviews).map(([k,v]) => ({ title: k, content: v }));
            }

            if(!arr || arr.length === 0) return `<div style="padding: 2rem; text-align: center; color: #6b7280; font-style: italic;">No reviews recorded.</div>`;

            let html = `<div class="reviews-masonry">`;
            arr.forEach(r => {
                // only render if meaningful content exists
                if (r && (r.title || r.content || r.body)) {
                    html += `
                        <div class="review-card">
                            <span class="review-title">"${r.title || 'Review'}"</span>
                            <p style="font-size: 0.9rem; line-height: 1.5; color: #d1d5db;">"${r.content || r.body || '...'}"</p>
                        </div>
                    `;
                }
            });
            html += `</div>`;
            return html;
        }

        window.onload = init;
    </script>
</body>
</html>"""
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        # assuming this function exists in your env
        filesCreation("HTML MOVIE", file_path)
    except Exception as e:
        return e