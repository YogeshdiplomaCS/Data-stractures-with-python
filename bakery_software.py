7#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║       🎂  SWEET BLISS BAKERY  🧁                            ║
║       Complete Bakery Management System                     ║
║       Powered by Python · NumPy · Pandas                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, json, csv, random, string, datetime, time, math, re
import numpy as np
import pandas as pd
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════
#  BAKERY CONFIG
# ══════════════════════════════════════════════════════════════════
BAKERY_NAME    = "Sweet Bliss Bakery"
BAKERY_TAG     = "Every Bite is a Memory ✨"
BAKERY_ADDR    = "42, Baker Street, Confection Lane, Mumbai - 400001"
BAKERY_PHONE   = "+91 98765-43210"
BAKERY_EMAIL   = "hello@sweetbliss.in"
BAKERY_GST     = "27SWEET1234B1Z5"
TAX_RATE       = 5.0          # GST %
DATA_FILE      = "bakery_data.json"
ORDERS_CSV     = "orders.csv"
SALES_CSV      = "sales_report.csv"
INVENTORY_CSV  = "inventory.csv"
VERSION        = "v3.0"

# ══════════════════════════════════════════════════════════════════
#  256-COLOUR GRADIENT PALETTE
# ══════════════════════════════════════════════════════════════════
RST = "\033[0m"
BLD = "\033[1m"
DIM = "\033[2m"
UL  = "\033[4m"

def fg(n):    return f"\033[38;5;{n}m"
def bg(n):    return f"\033[48;5;{n}m"
def bold(s):  return f"{BLD}{s}{RST}"

# Named palette
P = {
    # Warm bakery gradient: cream → gold → orange → rose → magenta
    "cream":    fg(230),
    "butter":   fg(229),
    "honey":    fg(220),
    "gold":     fg(214),
    "caramel":  fg(208),
    "tangerine":fg(202),
    "rose":     fg(211),
    "blush":    fg(217),
    "magenta":  fg(200),
    "coral":    fg(203),
    "mint":     fg(120),
    "lime":     fg(154),
    "sky":      fg(117),
    "lavender": fg(183),
    "violet":   fg(141),
    "white":    fg(255),
    "silver":   fg(250),
    "muted":    fg(244),
    "dim_grey": fg(240),
    "chocolate":fg(130),
    "brown":    fg(94),
    "berry":    fg(161),
    "red":      fg(196),
    "green":    fg(46),
    "cyan":     fg(51),
    "blue":     fg(39),
    # Backgrounds
    "bg_dark":  bg(232),
    "bg_maroon":bg(52),
    "bg_gold":  bg(220),
    "bg_black": bg(16),
}

def c(key, text):       return f"{P.get(key,'')}{text}{RST}"
def cb(key, text):      return f"{BLD}{P.get(key,'')}{text}{RST}"
def strip_a(s):         return re.sub(r'\033\[[0-9;]*m','',s)
def vis_len(s):         return len(strip_a(s))

def grad(text, colors):
    """Apply gradient colours across a string."""
    out = ""
    n   = len(colors)
    for i, ch in enumerate(text):
        out += f"{P.get(colors[i % n], '')}{ch}"
    return out + RST

def rainbow(text):
    cols = ["gold","caramel","tangerine","rose","magenta","violet","lavender","sky","mint","lime"]
    return grad(text, cols)

def bakery_grad(text):
    cols = ["honey","gold","caramel","tangerine","rose","blush","magenta"]
    return grad(text, cols)

# ══════════════════════════════════════════════════════════════════
#  MENU DATA  (Categories & Items)
# ══════════════════════════════════════════════════════════════════
MENU = {
    "🎂 Cakes": {
        "Vanilla Sponge Cake":    {"price": 450,  "unit": "piece", "stock": 20},
        "Chocolate Truffle Cake": {"price": 650,  "unit": "piece", "stock": 15},
        "Red Velvet Cake":        {"price": 700,  "unit": "piece", "stock": 12},
        "Black Forest Cake":      {"price": 750,  "unit": "piece", "stock": 10},
        "Mango Mousse Cake":      {"price": 800,  "unit": "piece", "stock": 8},
        "Butterscotch Cake":      {"price": 500,  "unit": "piece", "stock": 14},
        "Strawberry Cake":        {"price": 600,  "unit": "piece", "stock": 11},
        "Rainbow Layer Cake":     {"price": 950,  "unit": "piece", "stock": 6},
        "Tiramisu Cake":          {"price": 1100, "unit": "piece", "stock": 5},
        "Lemon Drizzle Cake":     {"price": 550,  "unit": "piece", "stock": 9},
    },
    "🧁 Cupcakes": {
        "Vanilla Cupcake":        {"price": 60,   "unit": "piece", "stock": 80},
        "Chocolate Cupcake":      {"price": 70,   "unit": "piece", "stock": 75},
        "Red Velvet Cupcake":     {"price": 80,   "unit": "piece", "stock": 60},
        "Blueberry Cupcake":      {"price": 75,   "unit": "piece", "stock": 50},
        "Salted Caramel Cupcake": {"price": 90,   "unit": "piece", "stock": 45},
        "Oreo Cupcake":           {"price": 85,   "unit": "piece", "stock": 55},
    },
    "🍫 Chocolates": {
        "Dark Chocolate Bar":     {"price": 120,  "unit": "bar",   "stock": 100},
        "Milk Chocolate Bar":     {"price": 100,  "unit": "bar",   "stock": 120},
        "White Chocolate Bar":    {"price": 110,  "unit": "bar",   "stock": 90},
        "Hazelnut Praline Box":   {"price": 350,  "unit": "box",   "stock": 40},
        "Truffle Assortment Box": {"price": 450,  "unit": "box",   "stock": 30},
        "Chocolate Bark (250g)":  {"price": 180,  "unit": "pack",  "stock": 60},
        "Bonbons (12 pcs)":       {"price": 280,  "unit": "box",   "stock": 35},
    },
    "🍩 Donuts": {
        "Glazed Donut":           {"price": 50,   "unit": "piece", "stock": 100},
        "Chocolate Donut":        {"price": 60,   "unit": "piece", "stock": 80},
        "Sprinkle Donut":         {"price": 55,   "unit": "piece", "stock": 90},
        "Boston Cream Donut":     {"price": 70,   "unit": "piece", "stock": 60},
        "Cinnamon Sugar Donut":   {"price": 55,   "unit": "piece", "stock": 75},
    },
    "🥐 Pastries & Breads": {
        "Butter Croissant":       {"price": 80,   "unit": "piece", "stock": 50},
        "Pain au Chocolat":       {"price": 90,   "unit": "piece", "stock": 40},
        "Blueberry Muffin":       {"price": 65,   "unit": "piece", "stock": 60},
        "Banana Bread (loaf)":    {"price": 280,  "unit": "loaf",  "stock": 20},
        "Sourdough Loaf":         {"price": 320,  "unit": "loaf",  "stock": 15},
        "Garlic Herb Focaccia":   {"price": 260,  "unit": "piece", "stock": 18},
        "Cinnamon Roll":          {"price": 90,   "unit": "piece", "stock": 45},
    },
    "🍪 Cookies & Biscuits": {
        "Choco Chip Cookies(6)":  {"price": 120,  "unit": "pack",  "stock": 80},
        "Oatmeal Raisin(6)":      {"price": 110,  "unit": "pack",  "stock": 70},
        "Peanut Butter Cookie(6)":{"price": 130,  "unit": "pack",  "stock": 65},
        "Shortbread Fingers(12)": {"price": 150,  "unit": "pack",  "stock": 55},
        "Macarons (6 pcs)":       {"price": 300,  "unit": "box",   "stock": 40},
        "Biscotti (250g)":        {"price": 180,  "unit": "pack",  "stock": 50},
    },
    "🥧 Pies & Tarts": {
        "Apple Pie":              {"price": 400,  "unit": "piece", "stock": 15},
        "Lemon Tart":             {"price": 350,  "unit": "piece", "stock": 18},
        "Belgian Waffle":         {"price": 150,  "unit": "piece", "stock": 30},
        "Cheesecake Slice":       {"price": 180,  "unit": "piece", "stock": 25},
        "Fruit Tart":             {"price": 280,  "unit": "piece", "stock": 20},
    },
    "☕ Beverages": {
        "Hot Chocolate":          {"price": 120,  "unit": "cup",   "stock": 200},
        "Cappuccino":             {"price": 140,  "unit": "cup",   "stock": 200},
        "Matcha Latte":           {"price": 160,  "unit": "cup",   "stock": 150},
        "Cold Coffee":            {"price": 130,  "unit": "cup",   "stock": 180},
        "Mango Smoothie":         {"price": 150,  "unit": "cup",   "stock": 160},
    },
}

CAT_COLORS = {
    "🎂 Cakes":             ["rose","magenta","violet"],
    "🧁 Cupcakes":          ["blush","rose","tangerine"],
    "🍫 Chocolates":        ["chocolate","brown","caramel"],
    "🍩 Donuts":            ["gold","honey","caramel"],
    "🥐 Pastries & Breads": ["butter","cream","honey"],
    "🍪 Cookies & Biscuits":["caramel","gold","tangerine"],
    "🥧 Pies & Tarts":      ["mint","lime","sky"],
    "☕ Beverages":          ["sky","lavender","violet"],
}

# ══════════════════════════════════════════════════════════════════
#  DATA STORE
# ══════════════════════════════════════════════════════════════════
class Store:
    def __init__(self):
        self.data = {
            "orders":    {},
            "customers": {},
            "inventory": {},
            "daily_sales": {},
            "next_order_no": 1001,
        }
        # Seed inventory from menu
        for cat, items in MENU.items():
            for item, info in items.items():
                self.data["inventory"][item] = {
                    "category": cat,
                    "price": info["price"],
                    "unit": info["unit"],
                    "stock": info["stock"],
                    "sold": 0,
                    "revenue": 0.0,
                }
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f:
                    saved = json.load(f)
                    # Merge, don't overwrite inventory prices
                    for k,v in saved.items():
                        if k == "inventory":
                            for item, info in v.items():
                                if item in self.data["inventory"]:
                                    self.data["inventory"][item].update(info)
                        else:
                            self.data[k] = v
            except: pass

    def save(self):
        with open(DATA_FILE,"w") as f:
            json.dump(self.data, f, indent=2, default=str)

db = Store()

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def clear():  os.system("cls" if os.name=="nt" else "clear")
def pause():  input(c("muted","\n  [ Press Enter to continue ] "))
def now_str():return datetime.datetime.now().strftime("%d %b %Y  %I:%M %p")
def today():  return datetime.date.today().isoformat()
def gen_id(): return ''.join(random.choices(string.ascii_uppercase+string.digits, k=6))
def fmt_rs(v):
    try:    return f"Rs. {float(v):>9,.2f}"
    except: return "Rs.      0.00"

W = 72   # terminal width

def hline(ch="─", col_name="gold"):
    return c(col_name, ch * W)

def box_top(col_name="gold"):
    print(cb(col_name, "╔" + "═"*(W-2) + "╗"))

def box_mid(col_name="gold"):
    print(cb(col_name, "╠" + "═"*(W-2) + "╣"))

def box_bot(col_name="gold"):
    print(cb(col_name, "╚" + "═"*(W-2) + "╝"))

def box_row(left, right="", lc="cream", rc="honey", bc="gold"):
    content = W - 4
    l_vis   = vis_len(c(lc, left))
    r_vis   = vis_len(c(rc, right))
    gap     = max(0, content - l_vis - r_vis)
    print(cb(bc,"║") + c(lc," "+left) + " "*gap + c(rc,right+" ") + cb(bc,"║"))

def thin_top(bc="caramel"):
    print(c(bc, "┌" + "─"*(W-2) + "┐"))

def thin_bot(bc="caramel"):
    print(c(bc, "└" + "─"*(W-2) + "┘"))

def thin_row(left, right="", lc="cream", rc="honey", bc="caramel"):
    content = W - 4
    l_vis   = vis_len(c(lc, left))
    r_vis   = vis_len(c(rc, right))
    gap     = max(0, content - l_vis - r_vis)
    print(c(bc,"│") + c(lc," "+left) + " "*gap + c(rc,right+" ") + c(bc,"│"))

def section_hdr(title, icon="✦", colors=None):
    colors = colors or ["gold","honey","caramel"]
    print()
    gt = grad(f"  {icon} {title} {icon}", colors)
    print(gt)
    print(c("caramel","  " + "═"*(W-4)))

def ok_box(msg):
    lines = str(msg).split("\n")
    print()
    print(c("lime","  ╔─") + cb("mint","  ✔  SUCCESS  ") + c("lime","─"*(W-16) + "╗"))
    for l in lines:
        row = f"  ║  {l}"
        print(row + " "*max(0,W-vis_len(row)-1) + c("lime","║"))
    print(c("lime","  ╚" + "═"*(W-4) + "╝"))

def err_box(msg):
    lines = str(msg).split("\n")
    print()
    print(c("red","  ╔─") + cb("coral","  ✘  ERROR  ") + c("red","─"*(W-14) + "╗"))
    for l in lines:
        row = f"  ║  {l}"
        print(row + " "*max(0,W-vis_len(row)-1) + c("red","║"))
    print(c("red","  ╚" + "═"*(W-4) + "╝"))

def warn_box(msg):
    print(c("honey",f"\n  ⚠  {msg}"))

def info_box(msg):
    print(c("sky",f"\n  ℹ  {msg}"))

def inp(label, required=True, default=None):
    p = f"  {c('tangerine','❯❯')} {c('cream',label)}"
    if default: p += c("muted", f" [{default}]")
    p += c("gold"," : ")
    while True:
        val = input(p).strip()
        if not val and default: return default
        if val or not required: return val
        err_box("This field is required.")

def confirm(msg):
    ans = input(c("honey",f"\n  ✦  {msg} ") + c("muted","(yes/no): ")).strip().lower()
    return ans in ("yes","y")

def menu(title, opts, back="Back", colors=None):
    colors = colors or ["gold","honey","caramel","tangerine","rose"]
    section_hdr(title, "🍰", colors)
    for i,o in enumerate(opts,1):
        col_name = colors[(i-1) % len(colors)]
        print(f"  {c(col_name,f'[{i}]')}  {c('cream',o)}")
    print(f"  {c('muted','[0]')}  {c('muted',back)}")
    print()
    while True:
        ch = input(c("gold","  ❯ ")).strip()
        if ch=="0": return 0
        if ch.isdigit() and 1<=int(ch)<=len(opts): return int(ch)
        err_box("Invalid choice.")

def table(headers, rows, widths, hc="gold", rc="cream", bc="caramel"):
    """Colourful bordered table."""
    total = sum(widths) + len(widths)*3 + 1
    sep = c(bc,"+" + "+".join("─"*(w+2) for w in widths) + "+")
    print("  " + sep)
    h_row = c(bc,"|") + c(bc,"|").join(cb(hc,f" {h[:w].center(w)} ") for h,w in zip(headers,widths)) + c(bc,"|")
    print("  " + h_row)
    print("  " + sep)
    for ri, row in enumerate(rows):
        alt = "bg_dark" if ri%2==1 else ""
        r_row = c(bc,"|") + c(bc,"|").join(c(rc,f" {str(v)[:w].ljust(w)} ") for v,w in zip(row,widths)) + c(bc,"|")
        print("  " + r_row)
    print("  " + sep)

def progress(label, val, maxi, w=25, col_fill="mint", col_empty="dim_grey"):
    pct   = min(100, int(val/max(maxi,1)*100))
    filled= int(w*pct//100)
    bar   = cb(col_fill,"█"*filled) + c(col_empty,"░"*(w-filled))
    print(f"  {c('muted',label):<22} {bar} {cb('honey',f'{pct}%')}")

# ══════════════════════════════════════════════════════════════════
#  SPLASH & BANNER
# ══════════════════════════════════════════════════════════════════
LOGO = [
    r"   ____                     _     ____  _ _         ",
    r"  / ___|_      _____  ___  | |_  | __ )| (_)___ ___ ",
    r"  \___ \ \ /\ / / _ \/ _ \ | __| |  _ \| | / __/ __|",
    r"   ___) \ V  V /  __/  __/ | |_  | |_) | | \__ \__ \\",
    r"  |____/ \_/\_/ \___|\___| \__| |____/|_|_|___/___/",
]

CAKE_ART = [
    r"        .-----.",
    r"       /        \\",
    r"      |  🎂🍫🍓  |",
    r"      |  ~~~~~~~~ |",
    r"       \________/",
    r"     ~~~~~~~~~~~~~~~",
]

def splash():
    clear()
    print()
    for i, line in enumerate(LOGO):
        grad_cols = ["rose","magenta","violet","lavender","blush","rose"]
        print(grad(line, grad_cols))
    print()
    cake_grad = ["tangerine","rose","magenta","violet","lavender"]
    for line in CAKE_ART:
        print(grad(line, cake_grad))
    print()
    tag_line = f"  ✨  {BAKERY_TAG}  ✨"
    print(bakery_grad(tag_line.center(W)))
    print()
    print(c("muted","  " + "─"*W))
    print(cb("honey", f"  {BAKERY_NAME}  |  {BAKERY_ADDR}"))
    print(c("muted", f"  {BAKERY_PHONE}  ·  {BAKERY_EMAIL}  ·  GST: {BAKERY_GST}"))
    print(c("muted","  " + "─"*W))
    print()

def print_banner():
    clear()
    box_top("rose")
    # Logo mini
    logo_short = [
        "  🎂  SWEET BLISS BAKERY  🧁",
        f"  {BAKERY_TAG}",
    ]
    for l in logo_short:
        box_row(bakery_grad(l),"","","","rose")
    box_mid("rose")
    box_row(f"  {BAKERY_ADDR}", now_str(), "silver","muted","rose")
    box_row(f"  📞 {BAKERY_PHONE}  |  📧 {BAKERY_EMAIL}", VERSION,"muted","dim_grey","rose")
    box_bot("rose")
    print()

# ══════════════════════════════════════════════════════════════════
#  MENU DISPLAY
# ══════════════════════════════════════════════════════════════════
def display_menu_catalog():
    clear()
    print()
    print(rainbow(f"  {'═'*W}"))
    print(rainbow(f"  {'BAKERY MENU CATALOG':^{W}}"))
    print(rainbow(f"  {'═'*W}"))
    print()
    for cat, items in MENU.items():
        grad_cols = CAT_COLORS.get(cat, ["gold","honey","caramel"])
        section_hdr(cat, "✦", grad_cols)
        rows = []
        for i, (name, info) in enumerate(items.items(), 1):
            inv = db.data["inventory"].get(name, {})
            stk = inv.get("stock", info["stock"])
            stk_col = "mint" if stk>20 else ("honey" if stk>5 else "red")
            rows.append((
                str(i),
                name,
                info["unit"],
                fmt_rs(info["price"]),
                c(stk_col, str(stk)),
            ))
        table(
            ["#","Item","Unit","Price","In Stock"],
            rows,
            [3,32,8,14,10],
            hc="honey", rc="cream", bc=grad_cols[0]
        )
        print()
    pause()

# ══════════════════════════════════════════════════════════════════
#  ORDER MODULE
# ══════════════════════════════════════════════════════════════════
class Order:
    def __init__(self, cust_name, cust_phone, order_type="Walk-in"):
        self.order_id   = f"ORD-{db.data['next_order_no']:04d}"
        self.cust_name  = cust_name
        self.cust_phone = cust_phone
        self.order_type = order_type   # Walk-in / Takeaway / Delivery / Pre-order
        self.items      = []           # list of {item, category, qty, price, subtotal}
        self.timestamp  = str(datetime.datetime.now())
        self.status     = "PENDING"
        self.special_note = ""

    def add_item(self, item_name, qty):
        inv = db.data["inventory"].get(item_name)
        if not inv:
            return False, "Item not found."
        if inv["stock"] < qty:
            return False, f"Only {inv['stock']} in stock."
        price = inv["price"]
        subtotal = price * qty
        # Check if item already in order
        for entry in self.items:
            if entry["item"] == item_name:
                entry["qty"]      += qty
                entry["subtotal"] += subtotal
                return True, "Qty updated."
        self.items.append({
            "item":     item_name,
            "category": inv["category"],
            "qty":      qty,
            "price":    price,
            "subtotal": subtotal,
        })
        return True, "Added."

    def remove_item(self, idx):
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            return True
        return False

    def totals(self):
        arr      = np.array([e["subtotal"] for e in self.items]) if self.items else np.array([0.0])
        subtotal = float(np.sum(arr))
        tax      = round(subtotal * TAX_RATE / 100, 2)
        total    = round(subtotal + tax, 2)
        return subtotal, tax, total

    def to_dict(self):
        subtotal, tax, total = self.totals()
        return {
            "order_id":    self.order_id,
            "customer":    self.cust_name,
            "phone":       self.cust_phone,
            "order_type":  self.order_type,
            "items":       self.items,
            "subtotal":    subtotal,
            "tax":         tax,
            "total":       total,
            "status":      self.status,
            "timestamp":   self.timestamp,
            "special_note":self.special_note,
        }

def create_order():
    clear()
    print_banner()
    section_hdr("New Order", "🛒", ["rose","magenta","violet"])

    cust_name  = inp("Customer Name")
    cust_phone = inp("Customer Phone")
    order_type = menu("Order Type",["Walk-in","Takeaway","Delivery","Pre-order"],
                      colors=["mint","sky","lavender","blush"])
    if order_type==0: return
    otypes = {1:"Walk-in",2:"Takeaway",3:"Delivery",4:"Pre-order"}
    order = Order(cust_name, cust_phone, otypes[order_type])

    while True:
        # Build flat item list
        all_items = []
        for cat, items in MENU.items():
            for name in items:
                all_items.append((name, cat))

        clear()
        print_banner()
        section_hdr(f"Order: {order.order_id}  |  Customer: {cust_name}", "🍰",
                    ["rose","magenta","violet"])

        # Show current basket
        if order.items:
            section_hdr("Current Basket", "🧺", ["mint","lime","sky"])
            table(
                ["#","Item","Qty","Unit Price","Subtotal"],
                [(str(i+1), e["item"][:28], str(e["qty"]),
                  fmt_rs(e["price"]), cb("mint",fmt_rs(e["subtotal"])))
                 for i,e in enumerate(order.items)],
                [3,30,5,14,14],
                hc="mint", rc="cream", bc="lime"
            )
            sub,tax,tot = order.totals()
            print(f"\n  {c('muted','Subtotal:')} {cb('honey',fmt_rs(sub))}"
                  f"   {c('muted',f'GST {TAX_RATE}%:')} {c('blush',fmt_rs(tax))}"
                  f"   {cb('gold','TOTAL:')} {cb('rose',fmt_rs(tot))}")
            print()

        act = menu("Add Items / Manage Order",[
            "Browse by Category",
            "Search Item by Name",
            "Remove an Item",
            "Add Special Note",
            "Confirm & Generate Bill",
        ], back="Cancel Order", colors=["gold","caramel","tangerine","rose","magenta"])

        if act==0:
            if confirm("Cancel this order?"): return
            continue

        elif act==1:
            # Browse by category
            cats = list(MENU.keys())
            ch = menu("Select Category", [c(CAT_COLORS.get(ct,["gold"])[0], ct) for ct in cats],
                      colors=["gold","honey","caramel","tangerine","rose","blush","mint","sky"])
            if ch==0: continue
            cat = cats[ch-1]
            items_in_cat = list(MENU[cat].keys())
            grad_cols = CAT_COLORS.get(cat, ["gold","honey"])
            section_hdr(cat, "✦", grad_cols)
            table(
                ["#","Item","Unit","Price","Stock"],
                [(str(i+1), name, MENU[cat][name]["unit"],
                  fmt_rs(MENU[cat][name]["price"]),
                  str(db.data["inventory"].get(name,{}).get("stock","?")))
                 for i,name in enumerate(items_in_cat)],
                [3,34,8,14,8], hc=grad_cols[0], rc="cream", bc=grad_cols[-1]
            )
            item_ch = inp("Enter item number (or 0 to go back)", default="0")
            if item_ch=="0": continue
            try:
                idx = int(item_ch)-1
                if not (0<=idx<len(items_in_cat)): raise ValueError
                chosen = items_in_cat[idx]
            except: err_box("Invalid item number."); time.sleep(1); continue
            qty_s = inp(f"Quantity for '{chosen}'")
            try: qty=int(qty_s); assert qty>0
            except: err_box("Invalid quantity."); time.sleep(1); continue
            ok, msg = order.add_item(chosen, qty)
            if ok: ok_box(f"✔ {msg}  '{chosen}' x{qty}")
            else:  err_box(msg)
            time.sleep(0.8)

        elif act==2:
            # Search
            kw = inp("Search keyword").lower()
            results = [(name, cat) for cat,items in MENU.items()
                       for name in items if kw in name.lower()]
            if not results: warn_box("No items found."); time.sleep(1); continue
            section_hdr("Search Results", "🔍", ["sky","lavender","violet"])
            table(
                ["#","Item","Category","Price"],
                [(str(i+1), name, cat, fmt_rs(MENU[cat][name]["price"]))
                 for i,(name,cat) in enumerate(results)],
                [3,30,22,14], hc="sky", rc="cream", bc="lavender"
            )
            ch2=inp("Enter number to add (0 to cancel)", default="0")
            if ch2=="0": continue
            try:
                idx=int(ch2)-1
                chosen, _ = results[idx]
            except: err_box("Invalid."); time.sleep(1); continue
            qty_s=inp(f"Quantity for '{chosen}'")
            try: qty=int(qty_s); assert qty>0
            except: err_box("Invalid."); time.sleep(1); continue
            ok,msg=order.add_item(chosen,qty)
            if ok: ok_box(f"✔ Added '{chosen}' x{qty}")
            else:  err_box(msg)
            time.sleep(0.8)

        elif act==3:
            if not order.items: warn_box("Basket is empty."); time.sleep(1); continue
            rm_s=inp("Enter item number to remove")
            try: rm=int(rm_s)-1
            except: err_box("Invalid."); time.sleep(1); continue
            if order.remove_item(rm): ok_box("Item removed.")
            else: err_box("Invalid item number.")
            time.sleep(0.8)

        elif act==4:
            order.special_note = inp("Special note / instructions", required=False)
            ok_box("Note saved.")
            time.sleep(0.8)

        elif act==5:
            if not order.items: err_box("No items in order!"); time.sleep(1); continue
            order.status = "CONFIRMED"
            # Deduct stock
            for entry in order.items:
                inv = db.data["inventory"][entry["item"]]
                inv["stock"] -= entry["qty"]
                inv["sold"]  += entry["qty"]
                inv["revenue"]= float(inv.get("revenue",0)) + entry["subtotal"]
            # Save order
            db.data["orders"][order.order_id] = order.to_dict()
            db.data["next_order_no"] += 1
            # Update daily sales
            ds = db.data["daily_sales"]
            td = today()
            if td not in ds:
                ds[td] = {"orders": 0, "revenue": 0.0, "items_sold": 0}
            _,_,tot = order.totals()
            ds[td]["orders"]     += 1
            ds[td]["revenue"]    += tot
            ds[td]["items_sold"] += sum(e["qty"] for e in order.items)
            db.save()
            # Append to CSV
            _append_order_csv(order.to_dict())
            # Print bill
            generate_bill(order.to_dict())
            return

def _append_order_csv(od):
    """Append order rows to CSV using pandas."""
    rows = []
    for e in od["items"]:
        rows.append({
            "Order ID":    od["order_id"],
            "Date":        od["timestamp"][:10],
            "Time":        od["timestamp"][11:19],
            "Customer":    od["customer"],
            "Phone":       od["phone"],
            "Order Type":  od["order_type"],
            "Category":    e["category"],
            "Item":        e["item"],
            "Quantity":    e["qty"],
            "Unit Price":  e["price"],
            "Subtotal":    e["subtotal"],
            "GST (5%)":    round(e["subtotal"]*TAX_RATE/100,2),
            "Total (incl. GST)": round(e["subtotal"]*(1+TAX_RATE/100),2),
            "Status":      od["status"],
            "Special Note":od.get("special_note",""),
        })
    df_new = pd.DataFrame(rows)
    if os.path.exists(ORDERS_CSV):
        df_old = pd.read_csv(ORDERS_CSV)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_csv(ORDERS_CSV, index=False)

# ══════════════════════════════════════════════════════════════════
#  BILL GENERATOR  (Full colourful terminal bill)
# ══════════════════════════════════════════════════════════════════
def generate_bill(od):
    clear()
    BW = W  # bill width
    sub, tax, total = od["subtotal"], od["tax"], od["total"]

    # ── Border top ──────────────────────────────────────
    print()
    print(cb("rose",    "╔" + "═"*(BW-2) + "╗"))
    print(cb("rose",    "║") + bakery_grad(f"  🎂  {BAKERY_NAME}  🧁".center(BW-4)) + cb("rose","║"))
    print(cb("rose",    "║") + c("muted", f"  {BAKERY_TAG}".center(BW-4))            + cb("rose","║"))
    print(cb("rose",    "╠") + c("rose","═"*(BW-2))                                   + cb("rose","╣"))

    def brow(l, r="", lc="cream", rc="honey"):
        content = BW-4
        lv = vis_len(c(lc,l)); rv = vis_len(c(rc,r))
        gap= max(0, content-lv-rv)
        print(cb("rose","║") + c(lc," "+l) + " "*gap + c(rc,r+" ") + cb("rose","║"))

    brow(f"📍 {BAKERY_ADDR}", "", "silver","")
    brow(f"📞 {BAKERY_PHONE}   ✉  {BAKERY_EMAIL}", "","muted","")
    brow(f"GST No: {BAKERY_GST}", "", "dim_grey","")

    print(cb("rose","╠") + c("rose","═"*(BW-2)) + cb("rose","╣"))

    # ── Order Info ─────────────────────────────────────
    brow(cb("gold",f"ORDER: {od['order_id']}"), c("muted",od["timestamp"][:16]))
    brow(f"👤 {od['customer']}", f"📱 {od['phone']}", "cream","silver")
    brow(f"🏷  Order Type: {od['order_type']}", f"Status: {od['status']}","honey","mint")
    if od.get("special_note"):
        brow(f"📝 Note: {od['special_note']}", "", "blush","")

    print(cb("rose","╠") + c("rose","─"*(BW-2)) + cb("rose","╣"))

    # ── Items table header ─────────────────────────────
    brow(cb("honey","  ITEM" + " "*21 + "QTY    PRICE     SUBTOTAL"),"","","")
    print(cb("rose","║") + c("caramel","  " + "─"*(BW-6)) + cb("rose","  ║"))

    # ── Items ──────────────────────────────────────────
    arr_subtotals = []
    for i, e in enumerate(od["items"]):
        grad_cols = CAT_COLORS.get(e.get("category",""), ["cream","honey"])
        name = e["item"][:28].ljust(28)
        qty  = str(e["qty"]).rjust(4)
        pr   = fmt_rs(e["price"]).rjust(12)
        sub_e= cb("mint",fmt_rs(e["subtotal"]).rjust(12))
        arr_subtotals.append(e["subtotal"])
        line = f"  {grad(name, grad_cols)} {c('silver',qty)} {c('cream',pr)} {sub_e}"
        line_vis = vis_len(line)+2
        pad = max(0, BW-4-line_vis)
        print(cb("rose","║") + line + " "*pad + cb("rose","║"))

    # NumPy stats on the bill
    arr  = np.array(arr_subtotals)
    max_item = od["items"][int(np.argmax(arr))]["item"] if arr.size else "-"
    min_item = od["items"][int(np.argmin(arr))]["item"] if arr.size else "-"

    print(cb("rose","║") + c("caramel","  " + "─"*(BW-6)) + cb("rose","  ║"))

    # ── Totals ─────────────────────────────────────────
    brow("Subtotal",           cb("honey",fmt_rs(sub).rjust(14)), "muted","honey")
    brow(f"GST @ {TAX_RATE}%", c("blush",fmt_rs(tax).rjust(14)), "muted","blush")
    print(cb("rose","╠") + c("rose","═"*(BW-2)) + cb("rose","╣"))
    brow(cb("gold","  GRAND TOTAL"),
         cb("rose",fmt_rs(total).rjust(14)), "","")
    print(cb("rose","╠") + c("rose","─"*(BW-2)) + cb("rose","╣"))

    # ── NumPy analytics on bill ────────────────────────
    brow(cb("sky","  🔢 Order Analytics (powered by NumPy)"),"","","")
    brow(f"  Avg item value: {fmt_rs(float(np.mean(arr)))}", "", "muted","")
    brow(f"  Highest value item: {max_item[:30]}", "", "muted","")
    brow(f"  Std deviation: {fmt_rs(float(np.std(arr)))}", "", "muted","")

    print(cb("rose","╠") + c("rose","─"*(BW-2)) + cb("rose","╣"))

    # ── Payment / Thank you ────────────────────────────
    brow(cb("mint","  ✔  Thank you for visiting Sweet Bliss Bakery!"),"","","")
    brow(c("silver","  Have a sweet day! Come back soon 🍰"),"","","")
    brow(c("muted",f"  Bill generated: {now_str()}"),"","","")
    print(cb("rose","╚") + c("rose","═"*(BW-2)) + cb("rose","╝"))

    print()
    ok_box(f"Bill generated for Order {od['order_id']}\n"
           f"  Total payable: {cb('rose', fmt_rs(total))}\n"
           f"  Saved to: {ORDERS_CSV}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  ORDER MANAGEMENT
# ══════════════════════════════════════════════════════════════════
def view_all_orders():
    clear()
    print_banner()
    section_hdr("All Orders", "📋", ["sky","lavender","violet"])
    orders = list(db.data["orders"].values())
    if not orders:
        warn_box("No orders yet."); pause(); return

    status_c = {"CONFIRMED":"mint","PENDING":"honey","CANCELLED":"red","READY":"lime","DELIVERED":"lavender"}
    rows = [(
        o["order_id"],
        o["customer"][:18],
        o["order_type"][:10],
        fmt_rs(o["total"]),
        c(status_c.get(o["status"],"cream"), o["status"]),
        o["timestamp"][:16],
    ) for o in reversed(orders[-50:])]
    table(
        ["Order ID","Customer","Type","Total","Status","Date & Time"],
        rows,
        [10,20,11,14,12,18],
        hc="sky", rc="cream", bc="lavender"
    )
    print(f"\n  {c('muted','Total orders:')} {cb('honey',str(len(orders)))}")
    pause()

def view_order_detail():
    clear()
    print_banner()
    section_hdr("Order Details", "🔍", ["sky","lavender","violet"])
    oid = inp("Enter Order ID (e.g. ORD-1001)")
    od  = db.data["orders"].get(oid)
    if not od: err_box("Order not found."); pause(); return
    generate_bill(od)

def update_order_status():
    clear()
    print_banner()
    section_hdr("Update Order Status", "✏", ["amber","honey","gold"])
    oid = inp("Enter Order ID")
    od  = db.data["orders"].get(oid)
    if not od: err_box("Order not found."); pause(); return
    statuses = ["CONFIRMED","PREPARING","READY","DELIVERED","CANCELLED"]
    ch = menu("New Status", statuses, colors=["mint","honey","lime","lavender","red"])
    if ch==0: return
    od["status"] = statuses[ch-1]
    db.save()
    ok_box(f"Order {oid} status → {statuses[ch-1]}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  INVENTORY MODULE
# ══════════════════════════════════════════════════════════════════
def view_inventory():
    clear()
    print_banner()
    section_hdr("Live Inventory", "📦", ["chocolate","caramel","honey"])

    inv = db.data["inventory"]
    rows = []
    low_stock = []
    for name, info in inv.items():
        stk = info["stock"]
        sc  = "mint" if stk>20 else ("honey" if stk>5 else "red")
        rows.append((
            info["category"][:14],
            name[:30],
            info["unit"],
            fmt_rs(info["price"]),
            c(sc,str(stk)),
            str(info.get("sold",0)),
            fmt_rs(info.get("revenue",0)),
        ))
        if stk <= 5: low_stock.append(name)

    table(
        ["Category","Item","Unit","Price","Stock","Sold","Revenue"],
        rows,
        [14,30,7,14,7,7,14],
        hc="chocolate", rc="cream", bc="caramel"
    )
    if low_stock:
        print()
        warn_box(f"Low stock items ({len(low_stock)}):")
        for item in low_stock:
            print(c("red",f"    ⚠ {item}  (Stock: {inv[item]['stock']})"))
    pause()

def restock_item():
    clear()
    print_banner()
    section_hdr("Restock Inventory", "📥", ["mint","lime","sky"])
    kw  = inp("Search item name")
    matches = [(name, info) for name, info in db.data["inventory"].items()
               if kw.lower() in name.lower()]
    if not matches: err_box("No items found."); pause(); return
    table(
        ["#","Item","Current Stock"],
        [(str(i+1), name, str(info["stock"])) for i,(name,info) in enumerate(matches)],
        [3,42,15], hc="mint", rc="cream", bc="lime"
    )
    ch=inp("Select item number", default="0")
    if ch=="0": return
    try:
        idx=int(ch)-1
        name,_ = matches[idx]
    except: err_box("Invalid."); pause(); return
    qty=inp(f"Add stock quantity for '{name}'")
    try: qty=int(qty); assert qty>0
    except: err_box("Invalid quantity."); pause(); return
    db.data["inventory"][name]["stock"] += qty
    db.save()
    ok_box(f"Restocked '{name}' by {qty} units.\n"
           f"  New stock: {db.data['inventory'][name]['stock']}")
    # Update inventory CSV
    export_inventory_csv()
    pause()

def update_price():
    clear()
    print_banner()
    section_hdr("Update Item Price", "💰", ["gold","honey","caramel"])
    kw = inp("Search item name")
    matches = [(name,info) for name,info in db.data["inventory"].items()
               if kw.lower() in name.lower()]
    if not matches: err_box("No items found."); pause(); return
    table(["#","Item","Current Price"],
          [(str(i+1),name,fmt_rs(info["price"])) for i,(name,info) in enumerate(matches)],
          [3,40,15], hc="gold", rc="cream", bc="caramel")
    ch=inp("Select item number", default="0")
    if ch=="0": return
    try: idx=int(ch)-1; name,_=matches[idx]
    except: err_box("Invalid."); pause(); return
    new_price=inp(f"New price for '{name}' (Rs.)")
    try: new_price=float(new_price); assert new_price>0
    except: err_box("Invalid price."); pause(); return
    db.data["inventory"][name]["price"] = new_price
    db.save()
    ok_box(f"Price updated: '{name}' → {fmt_rs(new_price)}")
    pause()

# ══════════════════════════════════════════════════════════════════
#  REPORTS MODULE  (NumPy + Pandas)
# ══════════════════════════════════════════════════════════════════
def sales_report():
    clear()
    print_banner()
    section_hdr("Sales Report  (NumPy + Pandas Analytics)", "📊",
                ["mint","lime","sky","lavender","violet"])

    orders = list(db.data["orders"].values())
    if not orders:
        warn_box("No orders to report."); pause(); return

    # Build DataFrame
    rows = []
    for od in orders:
        for e in od["items"]:
            rows.append({
                "order_id":   od["order_id"],
                "date":       od["timestamp"][:10],
                "customer":   od["customer"],
                "order_type": od["order_type"],
                "category":   e["category"],
                "item":       e["item"],
                "qty":        e["qty"],
                "unit_price": e["price"],
                "subtotal":   e["subtotal"],
                "status":     od["status"],
            })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])

    # ── Overall stats (NumPy) ──────────────────────────
    revenues     = np.array([od["total"] for od in orders])
    totals_arr   = df["subtotal"].values

    thin_top("violet")
    thin_row("  📈 OVERALL STATISTICS", "", "violet","")
    thin_row(f"  Total Orders",         cb("honey",str(len(orders))),        "muted","honey")
    thin_row(f"  Total Revenue (incl. GST)", cb("mint",fmt_rs(float(revenues.sum()))), "muted","mint")
    thin_row(f"  Average Order Value",  cb("sky",fmt_rs(float(revenues.mean()))),   "muted","sky")
    thin_row(f"  Highest Order",        cb("gold",fmt_rs(float(revenues.max()))),   "muted","gold")
    thin_row(f"  Lowest Order",         cb("blush",fmt_rs(float(revenues.min()))),  "muted","blush")
    thin_row(f"  Std Deviation",        cb("lavender",fmt_rs(float(revenues.std()))),"muted","lavender")
    thin_row(f"  Median Order Value",   cb("caramel",fmt_rs(float(np.median(revenues)))),"muted","caramel")
    thin_row(f"  Total Items Sold",     cb("lime",str(int(df["qty"].sum()))),       "muted","lime")
    thin_bot("violet")

    # ── Sales by Category ─────────────────────────────
    section_hdr("Revenue by Category", "🎂", ["rose","magenta","blush"])
    cat_df = df.groupby("category").agg(
        Items_Sold=("qty","sum"),
        Revenue=("subtotal","sum"),
        Orders=("order_id","nunique")
    ).reset_index().sort_values("Revenue", ascending=False)

    table(
        ["Category","Items Sold","Revenue","Orders"],
        [(row["category"][:22], str(int(row["Items_Sold"])),
          fmt_rs(row["Revenue"]), str(int(row["Orders"])))
         for _,row in cat_df.iterrows()],
        [24,12,16,10], hc="rose", rc="cream", bc="magenta"
    )

    # Category bar chart in terminal
    print()
    max_rev = float(cat_df["Revenue"].max()) if not cat_df.empty else 1
    for _,row in cat_df.iterrows():
        pct = int(row["Revenue"]/max_rev*100)
        filled = int(28*pct//100)
        gcols = CAT_COLORS.get(row["category"], ["gold","honey"])
        bar   = grad("█"*filled, gcols) + c("dim_grey","░"*(28-filled))
        print(f"  {c('muted',row['category'][:16]):<18} [{bar}] {cb('honey',fmt_rs(row['Revenue']))}")

    # ── Top 10 Items ───────────────────────────────────
    section_hdr("Top 10 Best-Selling Items", "🏆", ["gold","honey","caramel"])
    top_items = df.groupby("item").agg(
        Qty=("qty","sum"), Revenue=("subtotal","sum")
    ).sort_values("Revenue", ascending=False).head(10).reset_index()

    table(
        ["#","Item","Qty Sold","Revenue"],
        [(str(i+1), row["item"][:30], str(int(row["Qty"])), fmt_rs(row["Revenue"]))
         for i,(_,row) in enumerate(top_items.iterrows())],
        [3,32,10,16], hc="gold", rc="cream", bc="caramel"
    )

    # ── Daily Sales Trend ─────────────────────────────
    section_hdr("Daily Sales Trend", "📅", ["sky","lavender","violet"])
    daily = df.groupby("date")["subtotal"].sum().reset_index().sort_values("date")
    daily.columns = ["Date","Revenue"]
    if len(daily) > 0:
        daily_rev = daily["Revenue"].values
        table(
            ["Date","Revenue","vs Average"],
            [(str(row["Date"])[:10],
              fmt_rs(row["Revenue"]),
              c("mint","▲ Above") if row["Revenue"] >= float(np.mean(daily_rev)) else c("rose","▼ Below"))
             for _,row in daily.iterrows()],
            [14,18,14], hc="sky", rc="cream", bc="lavender"
        )

    # ── Order Type Breakdown ───────────────────────────
    section_hdr("Order Type Breakdown", "📊", ["mint","lime","sky"])
    type_df = df.groupby("order_type").agg(
        Count=("order_id","nunique"), Revenue=("subtotal","sum")
    ).reset_index()
    table(
        ["Order Type","Count","Revenue"],
        [(row["order_type"], str(int(row["Count"])), fmt_rs(row["Revenue"]))
         for _,row in type_df.iterrows()],
        [16,10,18], hc="mint", rc="cream", bc="lime"
    )

    # Save report CSV
    df.to_csv(SALES_CSV, index=False)
    print()
    ok_box(f"Full report saved to '{SALES_CSV}'")
    pause()

def daily_summary():
    clear()
    print_banner()
    section_hdr("Today's Summary", "🌟", ["gold","honey","caramel"])
    td  = today()
    ds  = db.data["daily_sales"].get(td, {"orders":0,"revenue":0.0,"items_sold":0})
    orders_today = [o for o in db.data["orders"].values() if o["timestamp"][:10]==td]

    thin_top("gold")
    thin_row("  📅 DATE", cb("amber",td), "muted","amber")
    thin_row("  🛒 Orders Placed",    cb("honey",str(ds.get("orders",0))),      "muted","honey")
    thin_row("  💰 Revenue (incl. GST)", cb("mint",fmt_rs(ds.get("revenue",0))), "muted","mint")
    thin_row("  🍰 Items Sold",       cb("lavender",str(ds.get("items_sold",0))),"muted","lavender")
    if orders_today:
        totals_arr = np.array([o["total"] for o in orders_today])
        thin_row("  📊 Avg Order Value",  cb("sky",fmt_rs(float(np.mean(totals_arr)))),"muted","sky")
        thin_row("  🏆 Highest Order",    cb("gold",fmt_rs(float(np.max(totals_arr)))),"muted","gold")
    thin_bot("gold")

    if orders_today:
        section_hdr("Today's Orders", "📋", ["sky","lavender","violet"])
        table(
            ["Order ID","Customer","Type","Total","Status"],
            [(o["order_id"],o["customer"][:18],o["order_type"][:10],
              fmt_rs(o["total"]),o["status"]) for o in orders_today],
            [10,20,11,14,12], hc="sky", rc="cream", bc="lavender"
        )
    pause()

def export_inventory_csv():
    """Export full inventory to CSV using Pandas."""
    inv = db.data["inventory"]
    rows = []
    for name, info in inv.items():
        rows.append({
            "Item":      name,
            "Category":  info["category"],
            "Unit":      info["unit"],
            "Price (Rs.)": info["price"],
            "Stock":     info["stock"],
            "Sold":      info.get("sold",0),
            "Revenue (Rs.)": info.get("revenue",0.0),
        })
    df = pd.DataFrame(rows)
    # NumPy stats
    prices   = df["Price (Rs.)"].values
    stocks   = df["Stock"].values
    revenues = df["Revenue (Rs.)"].values
    df["Price Percentile"] = [int(np.searchsorted(np.sort(prices), p) / len(prices) * 100) for p in prices]
    df.to_csv(INVENTORY_CSV, index=False)
    return df, prices, stocks, revenues

def inventory_analytics():
    clear()
    print_banner()
    section_hdr("Inventory Analytics  (NumPy + Pandas)", "📦",
                ["chocolate","caramel","honey"])

    df, prices, stocks, revenues = export_inventory_csv()

    thin_top("chocolate")
    thin_row("  💲 PRICE ANALYTICS (NumPy)", "", "chocolate","")
    thin_row(f"  Min Price",  cb("mint",  fmt_rs(float(np.min(prices)))),    "muted","mint")
    thin_row(f"  Max Price",  cb("rose",  fmt_rs(float(np.max(prices)))),    "muted","rose")
    thin_row(f"  Mean Price", cb("honey", fmt_rs(float(np.mean(prices)))),   "muted","honey")
    thin_row(f"  Median",     cb("sky",   fmt_rs(float(np.median(prices)))), "muted","sky")
    thin_row(f"  Std Dev",    cb("lavender",fmt_rs(float(np.std(prices)))),  "muted","lavender")
    thin_bot("chocolate")

    print()
    thin_top("caramel")
    thin_row("  📦 STOCK ANALYTICS", "", "caramel","")
    thin_row(f"  Total SKUs",       cb("honey",str(len(df))),                    "muted","honey")
    thin_row(f"  Total Units",      cb("mint",str(int(np.sum(stocks)))),          "muted","mint")
    thin_row(f"  Low Stock (<= 5)", cb("red",str(int(np.sum(stocks<=5)))),        "muted","red")
    thin_row(f"  Out of Stock",     cb("rose",str(int(np.sum(stocks==0)))),       "muted","rose")
    thin_row(f"  Avg Stock/Item",   cb("sky",f"{float(np.mean(stocks)):.1f}"),    "muted","sky")
    thin_row(f"  Total Revenue",    cb("gold",fmt_rs(float(np.sum(revenues)))),   "muted","gold")
    thin_bot("caramel")

    # Top revenue items
    section_hdr("Top Revenue Generating Items", "🏆", ["gold","honey","caramel"])
    top_df = df.sort_values("Revenue (Rs.)", ascending=False).head(10)
    table(
        ["Item","Category","Sold","Revenue"],
        [(row["Item"][:28], row["Category"][:14], str(int(row["Sold"])),
          fmt_rs(row["Revenue (Rs.)"])) for _,row in top_df.iterrows()],
        [30,16,8,16], hc="gold", rc="cream", bc="caramel"
    )

    # Stock level progress bars
    section_hdr("Stock Levels (Visual)", "📊", ["sky","lavender","violet"])
    low_items = df.sort_values("Stock").head(15)
    max_stk   = max(int(df["Stock"].max()), 1)
    for _,row in low_items.iterrows():
        stk  = int(row["Stock"])
        fc   = "mint" if stk>20 else ("honey" if stk>5 else "red")
        filled=int(25*stk//max_stk)
        bar  = cb(fc,"█"*filled) + c("dim_grey","░"*(25-filled))
        print(f"  {c('muted',row['Item'][:24]):<26} [{bar}] {cb(fc,str(stk))}")

    print()
    ok_box(f"Inventory exported to '{INVENTORY_CSV}'")
    pause()

# ══════════════════════════════════════════════════════════════════
#  CUSTOMER MODULE
# ══════════════════════════════════════════════════════════════════
def customer_lookup():
    clear()
    print_banner()
    section_hdr("Customer Order History", "👤", ["sky","lavender","violet"])
    phone = inp("Enter Customer Phone Number")
    orders= [o for o in db.data["orders"].values() if o.get("phone")==phone]
    if not orders:
        warn_box(f"No orders found for phone: {phone}"); pause(); return
    cname = orders[0]["customer"]
    totals= np.array([o["total"] for o in orders])

    thin_top("sky")
    thin_row("  👤 Customer", cb("gold",cname),             "muted","gold")
    thin_row("  📱 Phone",    cb("cream",phone),             "muted","cream")
    thin_row("  🛒 Orders",   cb("honey",str(len(orders))), "muted","honey")
    thin_row("  💰 Total Spent",cb("mint",fmt_rs(float(totals.sum()))),"muted","mint")
    thin_row("  📊 Avg Order", cb("sky",fmt_rs(float(totals.mean()))),"muted","sky")
    thin_bot("sky")

    table(
        ["Order ID","Date","Type","Total","Status"],
        [(o["order_id"],o["timestamp"][:10],o["order_type"],
          fmt_rs(o["total"]),o["status"]) for o in orders],
        [10,12,12,14,12], hc="sky", rc="cream", bc="lavender"
    )
    pause()

def export_customer_csv():
    """Export customer summary using Pandas."""
    orders = list(db.data["orders"].values())
    if not orders:
        warn_box("No orders to export."); pause(); return

    rows = []
    cust_map = defaultdict(list)
    for o in orders:
        cust_map[o["phone"]].append(o)

    for phone, ords in cust_map.items():
        totals = [o["total"] for o in ords]
        rows.append({
            "Customer Name":  ords[0]["customer"],
            "Phone":          phone,
            "Total Orders":   len(ords),
            "Total Spent":    round(sum(totals),2),
            "Avg Order":      round(float(np.mean(totals)),2),
            "Last Order":     max(o["timestamp"][:10] for o in ords),
            "Favourite Type": max(set(o["order_type"] for o in ords),
                                  key=lambda x: sum(1 for o in ords if o["order_type"]==x)),
        })

    df = pd.DataFrame(rows).sort_values("Total Spent", ascending=False)
    df.to_csv("customers.csv", index=False)
    return df

def vip_customers():
    clear()
    print_banner()
    section_hdr("VIP Customer Report", "👑", ["gold","honey","caramel"])
    df = export_customer_csv()
    if df is None: pause(); return

    top10 = df.head(10)
    table(
        ["Customer","Phone","Orders","Total Spent","Avg Order","Last Visit"],
        [(row["Customer Name"][:18],row["Phone"],str(int(row["Total Orders"])),
          fmt_rs(row["Total Spent"]),fmt_rs(row["Avg Order"]),row["Last Order"])
         for _,row in top10.iterrows()],
        [20,12,8,16,14,12], hc="gold", rc="cream", bc="caramel"
    )
    ok_box("Customer report saved to 'customers.csv'")
    pause()

# ══════════════════════════════════════════════════════════════════
#  DISCOUNT & OFFERS
# ══════════════════════════════════════════════════════════════════
OFFERS = {
    "SWEET10": 10,
    "BLISS20": 20,
    "CAKE15":  15,
    "BDAY25":  25,
}

def apply_discount(total):
    code = inp("Enter Coupon Code (or press Enter to skip)", required=False)
    if not code: return total, 0
    pct = OFFERS.get(code.upper())
    if not pct:
        warn_box("Invalid coupon code."); return total, 0
    disc = round(total * pct / 100, 2)
    new_total = round(total - disc, 2)
    ok_box(f"Coupon '{code.upper()}' applied!\n"
           f"  Discount: {pct}% = {fmt_rs(disc)}\n"
           f"  New Total: {fmt_rs(new_total)}")
    return new_total, disc

def view_offers():
    clear()
    print_banner()
    section_hdr("Current Offers & Coupons", "🎁", ["rose","magenta","violet"])
    table(
        ["Coupon Code","Discount","Description"],
        [("SWEET10","10%","General sweet discount"),
         ("BLISS20","20%","First order special"),
         ("CAKE15","15%","Cake lovers offer"),
         ("BDAY25","25%","Birthday celebration")],
        [14,10,30], hc="rose", rc="cream", bc="magenta"
    )
    pause()

# ══════════════════════════════════════════════════════════════════
#  EXPORT ALL DATA
# ══════════════════════════════════════════════════════════════════
def export_all():
    clear()
    print_banner()
    section_hdr("Export All Data to CSV", "📤", ["mint","lime","sky"])

    # Orders CSV
    orders = list(db.data["orders"].values())
    if orders:
        rows=[]
        for od in orders:
            for e in od["items"]:
                rows.append({
                    "Order ID":od["order_id"],"Date":od["timestamp"][:10],
                    "Customer":od["customer"],"Phone":od["phone"],
                    "Order Type":od["order_type"],"Category":e["category"],
                    "Item":e["item"],"Qty":e["qty"],"Unit Price":e["price"],
                    "Subtotal":e["subtotal"],"Total":od["total"],
                    "Status":od["status"],"Note":od.get("special_note",""),
                })
        pd.DataFrame(rows).to_csv(ORDERS_CSV,index=False)

    # Inventory
    export_inventory_csv()

    # Customer
    export_customer_csv()

    # Daily Sales using Pandas + NumPy
    ds = db.data.get("daily_sales",{})
    if ds:
        df_ds = pd.DataFrame([
            {"Date":d,"Orders":v["orders"],"Revenue":v["revenue"],"Items Sold":v["items_sold"]}
            for d,v in ds.items()
        ]).sort_values("Date")
        if len(df_ds)>0:
            revs=df_ds["Revenue"].values
            df_ds["7-day Rolling Avg"] = np.convolve(revs, np.ones(min(7,len(revs)))/min(7,len(revs)), mode="same")
        df_ds.to_csv("daily_sales.csv",index=False)

    files = [ORDERS_CSV, INVENTORY_CSV, "customers.csv", "daily_sales.csv"]
    ok_box("All data exported successfully!\n" +
           "\n".join(f"  📄 {f}" for f in files))
    pause()

# ══════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════
def settings_panel():
    while True:
        clear()
        print_banner()
        ch=menu("Settings & Configuration",[
            "View Current Offers / Coupons",
            "Update Item Price",
            "Restock Inventory",
            "Export All Data to CSV",
            "View System Info",
        ],back="Back to Main Menu", colors=["sky","lavender","violet","mint","honey"])
        if ch==0: return
        elif ch==1: view_offers()
        elif ch==2: update_price()
        elif ch==3: restock_item()
        elif ch==4: export_all()
        elif ch==5:
            clear()
            print_banner()
            section_hdr("System Information","⚙",["sky","lavender","violet"])
            import numpy as np
            import pandas as pd
            thin_top("sky")
            thin_row("  🏪 Bakery",     cb("gold",BAKERY_NAME),       "muted","gold")
            thin_row("  📍 Address",    cb("cream",BAKERY_ADDR),       "muted","cream")
            thin_row("  📋 Version",    cb("honey",VERSION),           "muted","honey")
            thin_row("  🐍 Python",     cb("mint",sys.version[:20]),   "muted","mint")
            thin_row("  🔢 NumPy",      cb("sky",np.__version__),      "muted","sky")
            thin_row("  🐼 Pandas",     cb("lavender",pd.__version__), "muted","lavender")
            thin_row("  📦 Total SKUs", cb("caramel",str(len(db.data["inventory"]))), "muted","caramel")
            thin_row("  🛒 Total Orders",cb("rose",str(len(db.data["orders"]))),      "muted","rose")
            thin_row("  💾 Data File",  cb("muted",DATA_FILE),         "muted","muted")
            thin_bot("sky")
            pause()

# ══════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════
def dashboard():
    while True:
        print_banner()
        # Live stats strip
        total_orders  = len(db.data["orders"])
        td            = today()
        ds_today      = db.data["daily_sales"].get(td,{})
        today_rev     = ds_today.get("revenue",0)
        today_orders  = ds_today.get("orders",0)
        low_stk_count = sum(1 for i in db.data["inventory"].values() if i["stock"]<=5)

        thin_top("rose")
        thin_row(
            bakery_grad(f"  🛒 Today: {today_orders} orders  |  "
                        f"💰 Revenue: {fmt_rs(today_rev)}"),
            c("red",f"⚠ Low Stock: {low_stk_count}"),
            "","red","rose"
        )
        thin_bot("rose")
        print()

        ch = menu("Main Menu", [
            "🛒  New Order",
            "📋  View All Orders",
            "🔍  View / Print Order Bill",
            "✏   Update Order Status",
            "📦  Inventory Management",
            "📊  Sales & Analytics Reports",
            "📅  Today's Summary",
            "🎂  Browse Full Menu Catalog",
            "👤  Customer Lookup",
            "👑  VIP Customer Report",
            "🎁  Offers & Coupons",
            "⚙   Settings & Configuration",
        ], back="🚪 Exit",
           colors=["rose","magenta","violet","lavender","sky","mint","lime",
                   "gold","caramel","honey","blush","silver"])

        if ch==0:
            print()
            print(bakery_grad(f"  {'Thank you for visiting ' + BAKERY_NAME + '!':^{W}}"))
            print(bakery_grad(f"  {'Have a Sweet Day! 🍰':^{W}}"))
            print()
            sys.exit(0)
        elif ch==1:  create_order()
        elif ch==2:  view_all_orders()
        elif ch==3:  view_order_detail()
        elif ch==4:  update_order_status()
        elif ch==5:
            while True:
                c2=menu("Inventory Management",[
                    "View Live Inventory","Restock Item","Update Price","Inventory Analytics"],
                    colors=["chocolate","caramel","honey","gold"])
                if c2==0: break
                elif c2==1: view_inventory()
                elif c2==2: restock_item()
                elif c2==3: update_price()
                elif c2==4: inventory_analytics()
        elif ch==6:  sales_report()
        elif ch==7:  daily_summary()
        elif ch==8:  display_menu_catalog()
        elif ch==9:  customer_lookup()
        elif ch==10: vip_customers()
        elif ch==11: view_offers()
        elif ch==12: settings_panel()

# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════
def main():
    splash()
    time.sleep(0.5)
    dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(bakery_grad(f"\n  Goodbye! Visit Sweet Bliss Bakery again soon! 🎂\n"))
        sys.exit(0)
