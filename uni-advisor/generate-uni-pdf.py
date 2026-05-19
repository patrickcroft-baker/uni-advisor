#!/usr/bin/env python3
"""
University research PDF generator for uni-advisor skill.
Usage: python3 generate-uni-pdf.py <input.json> <output.pdf>

Input JSON schema:
{
  "university":         "IE Madrid",
  "course":             "Bachelor in Business Administration",
  "country":            "Spain",
  "date_researched":    "2026-05-14",
  "overview":           "Paragraph of prose about the university.",
  "quick_stats": {
    "fees":     "€18–22k / yr",
    "grades":   "BBB – AAB",
    "ranking":  "FT Top 15 EU",
    "type":     "Direct apply"
  },
  "fees": {
    "annual": "~€18,000–22,000/year",
    "notes":  "Private institution. Verify at ie.edu."
  },
  "entry_requirements": {
    "grades":  "3 A-levels, BBB–AAB equivalent. STEM accepted.",
    "english": "IELTS 6.5+ or TOEFL 90+",
    "other":   "30–45 min personal interview. No admissions test."
  },
  "course_structure": ["Year 1: ...", "Year 2: ..."],
  "rankings": [
    {"source": "FT European Business Schools 2025", "rank": "#12 in Europe"}
  ],
  "application": {
    "deadline": "Rolling — apply by January",
    "portal":   "ie.edu/admissions (NOT via UCAS)",
    "process":  "Application → interview → decision in 4–6 weeks"
  },
  "open_day": "Virtual and campus open days. See ie.edu/events.",
  "pros": ["Strength 1", "Strength 2"],
  "cons": ["Weakness 1"],
  "fit":   "Optional paragraph: how this institution fits the student — their grades, subjects, interests, constraints.",
  "notes": "Caveats and data freshness notes."
}
"""

import sys, json, os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date

# ── Font paths ────────────────────────────────────────────────────────────────
# Looks for bundled fonts in a fonts/ subdirectory next to this script first.
# Falls back to system DejaVu on Linux/WSL. See setup.sh for font download.
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

def _find_font(filename, linux_path):
    bundled = os.path.join(_SKILL_DIR, 'fonts', filename)
    if os.path.exists(bundled):
        return bundled
    if os.path.exists(linux_path):
        return linux_path
    raise FileNotFoundError(
        f"Font '{filename}' not found.\n"
        f"  Run setup.sh to download fonts, or place {filename} in:\n"
        f"  {os.path.join(_SKILL_DIR, 'fonts', filename)}"
    )

DV_R = _find_font('DejaVuSans.ttf',         '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
DV_B = _find_font('DejaVuSans-Bold.ttf',    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
DV_I = _find_font('DejaVuSans-Oblique.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf')

# ── Palette ───────────────────────────────────────────────────────────────────
HEADER  = (10,  22,  60)   # deep navy   — cover band
ACCENT  = (41,  98, 225)   # clear blue  — section bars
DARK    = (18,  20,  32)   # near-black  — primary text
MID     = (75,  82, 105)   # medium slate — labels, secondary text
RULE    = (200, 208, 222)  # visible grey — rules
CARD_BG = (238, 244, 255)  # soft blue-tint — alternating row fill
SEC_BG  = (244, 247, 253)  # section header background
WHITE   = (255, 255, 255)

# Stats cards — (strip_colour, card_bg)
C_FEES    = ((0,  180, 216), (224, 247, 252))  # cyan
C_GRADES  = ((245, 130,  0), (255, 247, 228))  # orange
C_RANK    = ((110,  55, 190), (238, 232, 252))  # purple
C_TYPE    = ((40,  165,  70), (228, 250, 234))  # green

# Pros / cons
PRO_BG  = (228, 252, 238)
PRO_TXT = (10, 110,  50)
CON_BG  = (255, 234, 234)
CON_TXT = (175,  25,  25)

MARGIN  = 16   # mm, left & right
PAGE_W  = 210
USABLE  = PAGE_W - 2 * MARGIN   # 178 mm


class UniPDF(FPDF):

    def __init__(self, data):
        super().__init__('P', 'mm', 'A4')
        self.data = data
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(True, margin=22)
        self.add_font('dv',  '',  DV_R)
        self.add_font('dv',  'B', DV_B)
        self.add_font('dv',  'I', DV_I)

    # ── Primitives ─────────────────────────────────────────────────────────────

    def f(self, style='', size=9.5):
        self.set_font('dv', style, size)

    def tc(self, rgb):
        self.set_text_color(*rgb)

    def fc(self, rgb):
        self.set_fill_color(*rgb)

    def dc(self, rgb):
        self.set_draw_color(*rgb)

    def rule(self, y=None, color=RULE):
        if y is None:
            y = self.get_y()
        self.dc(color)
        self.line(MARGIN, y, PAGE_W - MARGIN, y)

    # ── Section header ─────────────────────────────────────────────────────

    def section_header(self, title):
        # If less than 50 mm remains start a new page, otherwise add top gap
        if self.get_y() > self.h - self.b_margin - 50:
            self.add_page()
        else:
            self.ln(8)
        y = self.get_y()
        h = 9
        # Subtle background across full width
        self.fc(SEC_BG); self.dc(SEC_BG)
        self.rect(MARGIN, y, USABLE, h, style='F')
        # Bold left accent bar
        self.fc(ACCENT); self.dc(ACCENT)
        self.rect(MARGIN, y, 4, h, style='F')
        # Title — dark text so it reads as content, not UI chrome
        self.set_xy(MARGIN + 8, y + 1.5)
        self.f('B', 10.5)
        self.tc(DARK)
        self.cell(0, 6, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)
        self.tc(DARK)

    # ── Body text ──────────────────────────────────────────────────────────

    def body(self, text, size=9.5, colour=None):
        self.f('', size)
        self.tc(colour or DARK)
        self.multi_cell(0, 6.2, text)
        self.set_x(MARGIN)

    def bullet_line(self, text, colour=DARK):
        self.f('', 9.5)
        self.tc(colour)
        bx, tx = MARGIN + 4, MARGIN + 11
        y = self.get_y()
        self.set_xy(bx, y)
        self.cell(7, 6.2, '•')
        self.set_xy(tx, y)
        # Shift left margin so wrapped lines stay indented under the text, not the bullet
        self.set_left_margin(tx)
        self.multi_cell(USABLE - (tx - MARGIN), 6.2, text)
        self.set_left_margin(MARGIN)
        self.ln(0.5)
        self.set_x(MARGIN)

    # ── Key-value row ─────────────────────────────────────────────────────

    def kv(self, label, value, shade=False):
        # Guard: ensure at least one row fits on the current page
        if self.get_y() + 8 > self.h - self.b_margin:
            self.add_page()
        self.fc(CARD_BG if shade else WHITE)
        self.f('B', 8.5)
        self.tc(MID)
        self.cell(50, 7.5, label, fill=True)
        # Shift left margin so multi_cell wraps under the value column, not the label
        self.set_left_margin(MARGIN + 50)
        self.f('', 9.5)
        self.tc(DARK)
        self.multi_cell(USABLE - 50, 7.5, value, fill=True)
        self.set_left_margin(MARGIN)
        self.set_x(MARGIN)
        # Row divider
        self.dc(RULE)
        self.line(MARGIN, self.get_y(), MARGIN + USABLE, self.get_y())
        self.set_x(MARGIN)

    # ── Quick-stats cards ─────────────────────────────────────────────────

    def stats_cards(self, stats):
        gap    = 5
        n      = 4
        card_w = (USABLE - gap * (n - 1)) / n   # ~40.25 mm
        card_h = 28
        y      = self.get_y()
        cards  = [
            ('ANNUAL FEES',  stats.get('fees',    '—'), C_FEES),
            ('GRADE REQ.',   stats.get('grades',  '—'), C_GRADES),
            ('RANKING',      stats.get('ranking', '—'), C_RANK),
            ('APPLICATION',  stats.get('type',    '—'), C_TYPE),
        ]
        for i, (label, value, (strip, bg)) in enumerate(cards):
            x = MARGIN + i * (card_w + gap)
            # Card bg — tinted, no border
            self.fc(bg); self.dc(bg)
            self.rect(x, y, card_w, card_h, round_corners=True,
                      corner_radius=2.5, style='F')
            # Bold colour strip at top
            self.fc(strip); self.dc(strip)
            self.rect(x, y, card_w, 5, style='F')
            # Label (small caps, strip colour)
            self.set_xy(x, y + 7)
            self.f('B', 7)
            self.tc(strip)
            self.cell(card_w, 4.5, label, align='C',
                      new_x=XPos.LEFT, new_y=YPos.NEXT)
            # Value (big, dark)
            self.set_xy(x, y + 13)
            self.f('B', 11)
            self.tc(DARK)
            self.multi_cell(card_w, 5.8, value, align='C')

        self.set_xy(MARGIN, y + card_h + 6)

    # ── Pros / Cons two-column ─────────────────────────────────────────────

    def pros_cons(self, pros, cons):
        col_w = (USABLE - 5) / 2   # ~86.5 mm
        gap   = 5
        # Estimate height: header (8) + items (~7 mm each with possible wraps) + padding
        est_h = 16 + max(len(pros), len(cons)) * 8
        if self.get_y() + est_h > self.h - self.b_margin:
            self.add_page()
        start_y = self.get_y()

        def col_items(items, bg, fg, x_start):
            label = 'STRENGTHS' if bg == PRO_BG else 'WEAKNESSES'
            # Header row
            self.set_xy(x_start, start_y)
            self.fc(fg); self.dc(fg)
            self.rect(x_start, start_y, col_w, 8, style='F')
            self.set_xy(x_start + 3, start_y + 1)
            self.f('B', 9)
            self.tc(WHITE)
            self.cell(col_w - 3, 6, label,
                      new_x=XPos.LEFT, new_y=YPos.NEXT)
            # Item rows
            y = start_y + 10
            for item in items:
                self.fc(bg)
                bx = x_start + 3; tx = x_start + 9
                self.set_xy(bx, y)
                self.f('', 9)
                self.tc(fg)
                self.cell(6, 6, '•')
                self.set_xy(tx, y)
                self.multi_cell(col_w - (tx - x_start) - 2, 6, item)
                y = self.get_y() + 0.5
            return y

        y_pros = col_items(pros, PRO_BG, PRO_TXT, MARGIN)
        y_cons = col_items(cons, CON_BG, CON_TXT, MARGIN + col_w + gap)
        self.set_xy(MARGIN, max(y_pros, y_cons) + 2)

    # ── Cover page ─────────────────────────────────────────────────────────

    def cover(self):
        d = self.data
        self.add_page()

        band_h = 52
        # Dark header band
        self.fc(HEADER); self.dc(HEADER)
        self.rect(0, 0, PAGE_W, band_h, style='F')

        # University name
        self.set_xy(MARGIN, 10)
        self.f('B', 24)
        self.tc(WHITE)
        self.cell(0, 12, d['university'], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Course
        self.set_xy(MARGIN, 26)
        self.f('', 12)
        self.tc((180, 200, 240))
        self.cell(0, 7, d.get('course', ''), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Country + date
        self.set_xy(MARGIN, 38)
        self.f('I', 8.5)
        self.tc((140, 165, 210))
        country    = d.get('country', '')
        researched = d.get('date_researched', str(date.today()))
        self.cell(0, 5, f'{country}   •   Research date: {researched}',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Quick-stats cards
        self.set_xy(MARGIN, band_h + 6)
        if d.get('quick_stats'):
            self.stats_cards(d['quick_stats'])
        else:
            self.ln(band_h + 10)

        self.tc(DARK)

    # ── Render ─────────────────────────────────────────────────────────────

    def build(self):
        d = self.data
        self.cover()

        if d.get('overview'):
            self.section_header('Overview')
            self.body(d['overview'])

        if d.get('fit'):
            self.section_header('Personal Fit')
            self.body(d['fit'])

        if d.get('fees'):
            self.section_header('Fees')
            fees = d['fees']
            if fees.get('annual'):
                self.kv('Annual cost', fees['annual'])
            if fees.get('notes'):
                self.ln(1.5)
                self.f('I', 8.5); self.tc(MID)
                self.multi_cell(0, 5, fees['notes'])
                self.tc(DARK)

        if d.get('entry_requirements'):
            self.section_header('Entry Requirements')
            req, shade = d['entry_requirements'], False
            for k, label in [('grades','A-levels / grades'),
                              ('english','English language'),
                              ('other','Other')]:
                if req.get(k):
                    self.kv(label, req[k], shade); shade = not shade

        if d.get('course_structure'):
            self.section_header('Course Structure')
            for item in d['course_structure']:
                self.bullet_line(item)

        if d.get('rankings'):
            self.section_header('Rankings')
            shade = False
            for r in d['rankings']:
                self.kv(r.get('source',''), r.get('rank',''), shade)
                shade = not shade

        if d.get('application'):
            self.section_header('Application')
            app, shade = d['application'], False
            for k, label in [('deadline','Deadline'),
                              ('portal','Portal'),
                              ('process','Process')]:
                if app.get(k):
                    self.kv(label, app[k], shade); shade = not shade

        if d.get('open_day'):
            self.section_header('Open Day')
            self.body(d['open_day'])

        if d.get('pros') or d.get('cons'):
            self.section_header('Strengths & Weaknesses')
            self.pros_cons(d.get('pros', []), d.get('cons', []))

        if d.get('notes'):
            self.section_header('Notes & Caveats')
            self.f('I', 8.5); self.tc(MID)
            self.multi_cell(0, 5.5, d['notes'])
            self.tc(DARK)

    def footer(self):
        self.set_y(-13)
        self.dc(RULE); self.line(MARGIN, self.get_y(), PAGE_W - MARGIN, self.get_y())
        self.f('I', 7.5); self.tc(MID)
        self.cell(0, 8,
            f'uni-advisor   •   {self.data.get("university","")}   •   Page {self.page_no()}',
            align='C')


def main():
    if len(sys.argv) < 3:
        print('Usage: python3 generate-uni-pdf.py <input.json> <output.pdf>')
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
    out = sys.argv[2]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    pdf = UniPDF(data); pdf.build(); pdf.output(out)
    print(f'PDF saved: {out}')

if __name__ == '__main__':
    main()
