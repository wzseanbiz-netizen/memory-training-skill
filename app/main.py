# -*- coding: utf-8 -*-
"""记忆法训练助手 —— GTK3 桌面练习软件（记数字、记单词、记古诗词、记短文）。"""

import json
import os
import random
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

import data

PROGRESS_DIR = os.path.join(os.path.expanduser("~"), ".config", "记忆法训练助手")
PROGRESS_FILE = os.path.join(PROGRESS_DIR, "progress.json")

CSS = """
* { font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", sans-serif; }
.title { font-size: 20px; font-weight: bold; }
.section { font-size: 16px; font-weight: bold; color: #24406e; }
button { font-size: 14px; }
entry { font-size: 15px; }
"""


def load_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_progress(progress):
    try:
        os.makedirs(PROGRESS_DIR, exist_ok=True)
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def lbl(text, size=13, bold=False, color=None, wrap=False, xalign=0.0):
    if not isinstance(text, str):
        text = str(text)
    if bold:
        markup = "<b>%s</b>" % text
    elif "<b>" in text or "<span" in text:
        markup = text
    else:
        markup = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if color:
        markup = '<span foreground="%s">%s</span>' % (color, markup)
    label = Gtk.Label(markup=markup, xalign=xalign)
    label.set_line_wrap(wrap)
    if size != 13:
        label.set_markup('<span font_size="%d">%s</span>' % (size, markup))
    return label


def section(text):
    return lbl(text, size=16, bold=True, color="#24406e")


def scroll(widget, width=0):
    sw = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER,
                            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC)
    sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sw.add(widget)
    if width:
        sw.set_min_content_width(width)
    return sw


def grid(items, columns=4, gap=8):
    g = Gtk.Grid(column_spacing=gap, row_spacing=gap)
    for i, item in enumerate(items):
        g.attach(lbl(item, size=14), i % columns, i // columns, 1, 1)
    return g


def box(spacing=12):
    return Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)


def row_box(spacing=10):
    return Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)


class MemoryApp:
    PAGES = [
        ("首页", "page_home"),
        ("记数字", "page_digit"),
        ("记单词", "page_word"),
        ("记古诗词", "page_poem"),
        ("记短文", "page_text"),
        ("记忆方法", "page_method"),
        ("专注力", "page_focus"),
        ("学习统计", "page_stats"),
    ]

    def __init__(self):
        self.progress = load_progress()

        self.window = Gtk.Window(title="记忆法训练助手", default_size=(1180, 800))
        self.window.set_border_width(14)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode("utf-8"))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        for name, method in self.PAGES:
            page = getattr(self, method)()
            self.notebook.add_page(page, self.notebook.append_tab(name))

        self.window.add(self.notebook)
        self.window.connect("destroy", self.on_destroy)
        self.window.show_all()

    def on_destroy(self, _w):
        save_progress(self.progress)
        Gtk.main_quit()

    def record(self, module, ok=True):
        s = self.progress.setdefault(module, {"n": 0, "ok": 0})
        s["n"] += 1
        if ok:
            s["ok"] += 1

    def jump(self, page_index):
        self.notebook.set_current_page(page_index)

    # ================= 首页 =================

    def page_home(self):
        page = box(14)
        page.pack_start(lbl("记忆法训练助手", size=24, bold=True, color="#24406e"), False, False, 0)
        page.pack_start(lbl("基于快速记忆法的练习软件：记数字、记单词、记古诗词、记短文",
                            size=14, color="#555555"), False, False, 0)

        page.pack_start(section("四大练习（点击进入）"), False, False, 0)
        entries = [
            (1, "记数字", "数字编码 1-100、数字串记忆、读数练习、圆周率 50 位"),
            (2, "记单词", "小学/初中/高中 576 词，看词忆义、看义忆词，每词带记忆提示"),
            (3, "记古诗词", "50 首经典古诗，画图记忆法 + 逐句背诵自测"),
            (4, "记短文", "12 篇经典短文，关键词提取 + 分段记忆练习"),
        ]
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        for idx, name, desc in entries:
            row = Gtk.ListBoxRow(margin_top=6, margin_bottom=6)
            b = box(4)
            b.pack_start(lbl("<b>%s</b>" % name, size=17, color="#24406e"), False, False, 0)
            b.pack_start(lbl(desc, size=13, color="#555555", wrap=True), False, False, 0)
            row.add(b)
            row.connect("activate", lambda _r, i=idx: self.jump(i))
            listbox.add(row)
        page.pack_start(listbox, False, False, 0)

        page.pack_start(section("记忆原理（高效记忆两大步骤）"), False, False, 0)
        page.pack_start(lbl("  →  ".join(data.TWO_STEPS), size=16, bold=True, color="#1a6b3c"), False, False, 0)
        page.pack_start(lbl("先把要记的内容转成具体图像，再让图像像锁链一样两两相连、顺序不乱。"
                            "右脑图像记忆的短时容量是声音记忆的 10 倍以上。", size=13, color="#555555", wrap=True),
                        False, False, 0)

        page.pack_start(section("记忆方法总览（详见“记忆方法”页）"), False, False, 0)
        page.pack_start(lbl("、".join(m.split("（")[0] for m, _ in data.METHODS_OVERVIEW), size=13, wrap=True),
                        False, False, 0)
        return page

    # ================= 记数字 =================

    def page_digit(self):
        page = box(14)
        page.pack_start(section("一、数字编码表（1-100）"), False, False, 0)
        page.pack_start(lbl("记数字第一步：把数字转成固定图像，再串联记忆。", size=13, color="#555555"),
                        False, False, 0)
        table = grid(["%d·%s" % (k, v) for k, v in data.DIGIT_CODES.items()], columns=10, gap=6)
        page.pack_start(scroll(table), True, True, 0)

        page.pack_start(section("二、数字串记忆练习"), False, False, 0)
        train = box(12)
        top = row_box(14)
        self.digit_len = Gtk.ComboBoxText()
        self.digit_len.append("5 位数字")
        self.digit_len.append("8 位数字")
        self.digit_len.append("10 位数字")
        self.digit_len.append("12 位数字")
        self.digit_len.set_active(1)
        top.pack_start(lbl("位数：", size=14, bold=True), False, False, 0)
        top.pack_start(self.digit_len, False, False, 0)
        train.pack_start(top, False, False, 0)

        self.digit_question = lbl("点击“生成数字串”开始", size=18, bold=True, color="#24406e", wrap=True)
        train.pack_start(self.digit_question, False, False, 8)
        self.digit_answer = Gtk.Entry(width_chars=30, visibility=True)
        self.digit_answer.set_placeholder_text("先按编码转图像串联，再输入回忆的数字串")
        train.pack_start(self.digit_answer, False, False, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="生成数字串")
        b1.connect("clicked", self.digit_new)
        b2 = Gtk.Button(label="显示编码提示")
        b2.connect("clicked", self.digit_hint)
        b3 = Gtk.Button(label="隐藏，开始回忆")
        b3.connect("clicked", self.digit_hide)
        b4 = Gtk.Button(label="核对答案")
        b4.connect("clicked", self.digit_check)
        self.digit_answer.connect("activate", lambda _e: self.digit_check())
        for b in (b1, b2, b3, b4):
            btns.pack_start(b, False, False, 0)
        train.pack_start(btns, False, False, 0)
        self.digit_tip = lbl("", size=13, color="#1a6b3c")
        train.pack_start(self.digit_tip, False, False, 0)
        page.pack_start(train, False, False, 0)

        page.pack_start(section("三、读数练习（用编码读出数字串）"), False, False, 0)
        read_box = box(10)
        self.read_combo = Gtk.ComboBoxText()
        for i, s in enumerate(data.READ_PRACTICE):
            self.read_combo.append("第 %d 组" % (i + 1))
        self.read_combo.set_active(0)
        read_box.pack_start(lbl("选择一组数字，先记住再读出来：", size=13), False, False, 0)
        read_box.pack_start(self.read_combo, False, False, 0)
        self.read_show = lbl("", size=15, bold=True, wrap=True)
        read_box.pack_start(self.read_show, False, False, 0)
        rb = row_box(10)
        b1 = Gtk.Button(label="显示数字串")
        b1.connect("clicked", self.read_show_nums)
        b2 = Gtk.Button(label="隐藏，开始自测")
        b2.connect("clicked", self.read_hide)
        rb.pack_start(b1, False, False, 0)
        rb.pack_start(b2, False, False, 0)
        read_box.pack_start(rb, False, False, 0)
        page.pack_start(read_box, False, False, 0)

        page.pack_start(section("四、圆周率 50 位"), False, False, 0)
        page.pack_start(lbl("用数字编码把圆周率转成图像，一串一串地记：", size=13, color="#555555"),
                        False, False, 0)
        page.pack_start(lbl(data.PI_50, size=16, bold=True, color="#24406e", wrap=True), False, False, 0)
        return page

    def digit_new(self, _b):
        length = [5, 8, 10, 12][self.digit_len.get_active()]
        self.digit_cur = "".join(random.choice("0123456789") for _ in range(length))
        self.digit_question.set_text("数字串：%s\n（把每个数字转成编码图像，像锁链一样串起来）" % self.digit_cur)
        self.digit_answer.set_text("")
        self.digit_tip.set_text("")

    def digit_hint(self):
        if not self.digit_cur:
            return
        enc = "　".join("%s→%s" % (c, data.DIGIT_CODES[int(c)]) for c in self.digit_cur)
        self.digit_tip.set_markup('<span foreground="#8a4b00">编码提示：%s</span>' % enc)

    def digit_hide(self, _b):
        if self.digit_cur:
            self.digit_question.set_text("（已隐藏，按串联画面回忆数字串）")

    def digit_check(self):
        if not self.digit_cur:
            return
        ans = self.digit_answer.get_text().strip().replace(" ", "")
        ok = ans == self.digit_cur
        self.record("记数字", ok)
        self.digit_tip.set_markup(
            '<span foreground="%s">%s　（正确答案：%s）</span>' %
            ("#1a6b3c" if ok else "#b00000", "回忆正确！" if ok else "再练一次", self.digit_cur))

    def read_show_nums(self, _b):
        self.read_show.set_text(data.READ_PRACTICE[self.read_combo.get_active()])

    def read_hide(self, _b):
        self.read_show.set_text("（已隐藏，凭记忆按数字编码读出来）")

    # ================= 记单词 =================

    def page_word(self):
        page = box(14)
        page.pack_start(section("一、单词记忆练习（看词忆义 / 看义忆词）"), False, False, 0)
        top = row_box(14)
        self.word_levels = list(data.WORD_BANK.keys())
        self.word_level = Gtk.ComboBoxText()
        for lv in self.word_levels:
            self.word_level.append(lv)
        self.word_level.set_active(0)
        top.pack_start(lbl("学段：", size=14, bold=True), False, False, 0)
        top.pack_start(self.word_level, False, False, 0)
        self.word_mode = Gtk.ComboBoxText()
        self.word_mode.append("看词忆义（显示单词，回忆释义）")
        self.word_mode.append("看义忆词（显示释义，回忆单词）")
        self.word_mode.set_active(0)
        top.pack_start(lbl("模式：", size=14, bold=True), False, False, 0)
        top.pack_start(self.word_mode, False, False, 0)
        self.word_level.connect("changed", lambda _c: self.word_refresh())
        page.pack_start(top, False, False, 0)

        train = box(12)
        self.word_question = lbl("点击“出题”开始", size=18, bold=True, color="#24406e", xalign=0.5, wrap=True)
        train.pack_start(self.word_question, False, False, 10)
        self.word_answer = Gtk.Entry(width_chars=30, visibility=True)
        self.word_answer.set_placeholder_text("看义忆词模式：输入回忆的单词")
        train.pack_start(self.word_answer, False, False, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="出题")
        b1.connect("clicked", self.word_new)
        b2 = Gtk.Button(label="显示释义")
        b2.connect("clicked", self.word_show_meaning)
        b3 = Gtk.Button(label="提交单词")
        b3.connect("clicked", self.word_submit)
        b4 = Gtk.Button(label="看记忆提示")
        b4.connect("clicked", self.word_show_tip)
        self.word_answer.connect("activate", lambda _e: self.word_submit())
        for b in (b1, b2, b3, b4):
            btns.pack_start(b, False, False, 0)
        train.pack_start(btns, False, False, 0)
        btns2 = row_box(10)
        b5 = Gtk.Button(label="记得")
        b5.connect("clicked", lambda _b: self.word_grade(True))
        b6 = Gtk.Button(label="再记")
        b6.connect("clicked", lambda _b: self.word_grade(False))
        btns2.pack_start(lbl("自评：", size=14, bold=True), False, False, 0)
        btns2.pack_start(b5, False, False, 0)
        btns2.pack_start(b6, False, False, 0)
        train.pack_start(btns2, False, False, 0)
        self.word_tip_label = lbl("", size=13, color="#1a6b3c", wrap=True)
        train.pack_start(self.word_tip_label, False, False, 0)
        page.pack_start(train, False, False, 0)

        page.pack_start(section("二、单词库浏览（点击单词看记忆提示）"), False, False, 0)
        self.word_listbox = Gtk.ListBox()
        self.word_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.word_listbox.connect("row-activated", self.word_list_show)
        page.pack_start(scroll(self.word_listbox), True, True, 0)
        self.word_refresh()
        return page

    def word_refresh(self):
        while True:
            row = self.word_listbox.get_row_at_index(0)
            if row is None:
                break
            self.word_listbox.remove(row)
        level = data.WORD_BANK[self.word_levels[self.word_level.get_active()]]
        for word, phonetic, pos, meaning, tip in level:
            r = Gtk.ListBoxRow(margin_top=3, margin_bottom=3)
            r.add(lbl("<b>%s</b>　%s　%s　%s" % (word, phonetic, pos, meaning), size=13))
            r._tip = tip
            self.word_listbox.add(r)

    def word_list_show(self, _lb, row):
        self.word_tip_label.set_markup('<span foreground="#1a6b3c">记忆提示：%s</span>' % row._tip)

    def word_new(self, _b):
        self.word_cur = random.choice(data.WORD_BANK[self.word_levels[self.word_level.get_active()]])
        word, phonetic, pos, meaning, tip = self.word_cur
        if self.word_mode.get_active() == 0:
            self.word_question.set_markup('<span font_size="18"><b>%s　%s　%s</b></span>' % (word, phonetic, pos))
        else:
            self.word_question.set_markup('<span font_size="18"><b>%s　%s</b></span>' % (pos, meaning))
        self.word_answer.set_text("")
        self.word_tip_label.set_text("")

    def word_show_meaning(self):
        if not self.word_cur:
            return
        word, phonetic, pos, meaning, tip = self.word_cur
        self.word_tip_label.set_markup(
            '<span foreground="#1a6b3c">释义：%s　%s　【记忆提示：%s】</span>' % (pos, meaning, tip))

    def word_show_tip(self):
        if not self.word_cur:
            return
        self.word_tip_label.set_markup('<span foreground="#8a4b00">记忆提示：%s</span>' % self.word_cur[4])

    def word_submit(self):
        if not self.word_cur:
            return
        ans = self.word_answer.get_text().strip()
        word = self.word_cur[0]
        ok = ans.lower() == word.lower()
        self.word_tip_label.set_markup(
            '<span foreground="%s">%s　（正确单词：%s）</span>' %
            ("#1a6b3c" if ok else "#b00000", "答对了！" if ok else "再记一次", word))

    def word_grade(self, ok):
        if not self.word_cur:
            return
        self.record("记单词", ok)
        self.word_tip_label.set_markup(
            '<span foreground="%s">%s　（单词：%s）</span>' %
            ("#1a6b3c" if ok else "#b00000", "已记为：记得" if ok else "已记为：再记", self.word_cur[0]))

    # ================= 记古诗词 =================

    def page_poem(self):
        page = box(14)
        page.pack_start(section("一、画图记忆法"), False, False, 0)
        page.pack_start(lbl("古诗词学习四步：" + " → ".join(data.POEM_STEPS), size=15, bold=True, color="#1a6b3c"),
                        False, False, 0)
        page.pack_start(lbl("读通理解后，把每句诗提取成图像画在脑中，再闭目按图回忆，顺序自然不乱。",
                            size=13, color="#555555", wrap=True), False, False, 0)

        page.pack_start(section("二、古诗库（%d 首，选一首查看与背诵）" % len(data.POEMS)), False, False, 0)
        self.poem_combo = Gtk.ComboBoxText()
        for p in data.POEMS:
            self.poem_combo.append("%s（%s）" % (p["title"], p["author"]))
        self.poem_combo.set_active(0)
        self.poem_combo.connect("changed", self.poem_show)
        page.pack_start(self.poem_combo, False, False, 0)

        self.poem_stack = Gtk.Stack()
        view_labels = [lbl("", size=16, bold=True) for _ in range(4)]
        test_labels = [lbl("", size=16, bold=True) for _ in range(4)]
        view_box = box(12)
        test_box = box(12)
        for lb in view_labels:
            view_box.pack_start(lb, False, False, 0)
        for lb in test_labels:
            test_box.pack_start(lb, False, False, 0)
        self.poem_view_labels = view_labels
        self.poem_test_labels = test_labels
        self.poem_stack.add_titled(view_box, "view", "原文 / 译文 / 图解")
        self.poem_stack.add_titled(test_box, "test", "背诵自测")
        switcher = Gtk.StackSwitcher()
        switcher.set_stack(self.poem_stack)
        page.pack_start(switcher, False, False, 4)
        page.pack_start(self.poem_stack, True, True, 0)

        self.poem_grade_box = box(10)
        btns = row_box(10)
        b1 = Gtk.Button(label="显示原文核对")
        b1.connect("clicked", self.poem_check)
        b2 = Gtk.Button(label="记得")
        b2.connect("clicked", lambda _b: self.poem_grade(True))
        b3 = Gtk.Button(label="再记")
        b3.connect("clicked", lambda _b: self.poem_grade(False))
        btns.pack_start(b1, False, False, 0)
        btns.pack_start(b2, False, False, 0)
        btns.pack_start(b3, False, False, 0)
        self.poem_grade_box.pack_start(btns, False, False, 0)
        page.pack_start(self.poem_grade_box, False, False, 0)
        self.poem_show()
        return page

    def poem_show(self, _c=None):
        idx = self.poem_combo.get_active()
        if idx is None or idx < 0 or idx >= len(data.POEMS):
            return
        p = data.POEMS[idx]
        v = self.poem_view_labels
        v[0].set_markup("<b>%s</b>　%s" % (p["title"], p["author"]))
        v[1].set_markup('<span font_size="16">%s</span>' % p["lines"].replace("\n", "\n"))
        txt = p.get("translation", "")
        v[2].set_text("【译文】" + txt if txt else "【译文】")
        v[3].set_text("【图解提示】" + p.get("image_hint", "尝试自己把每句诗画成图"))
        t = self.poem_test_labels
        t[0].set_markup("<b>%s</b>　自测（先想图，再回忆每句）" % p["title"])
        hints = []
        for line in p["lines"].split("\n"):
            hints.append((line[:2] + "……") if len(line) > 2 else line)
        t[1].set_markup('<span font_size="16">%s</span>' % "\n".join(hints))
        t[2].set_text("先通读理解，再在脑海中把每句画成图，最后闭目回忆。")
        t[3].set_text("回忆不起来时，点“显示原文核对”对照。")

    def poem_check(self):
        idx = self.poem_combo.get_active()
        p = data.POEMS[idx]
        self.poem_test_labels[1].set_markup('<span font_size="16">%s</span>' % p["lines"].replace("\n", "\n"))

    def poem_grade(self, ok):
        idx = self.poem_combo.get_active()
        p = data.POEMS[idx]
        self.record("记古诗", ok)
        self.poem_test_labels[3].set_markup(
            '<span foreground="%s">%s　《%s》</span>' %
            ("#1a6b3c" if ok else "#b00000", "已记为：记得" if ok else "已记为：再记", p["title"]))

    # ================= 记短文 =================

    def page_text(self):
        page = box(14)
        page.pack_start(section("一、记忆短文（%d 篇）" % len(data.SHORT_TEXTS)), False, False, 0)
        self.text_combo = Gtk.ComboBoxText()
        for t in data.SHORT_TEXTS:
            self.text_combo.append("%s（%s）" % (t["title"], t["author"]))
        self.text_combo.set_active(0)
        self.text_combo.connect("changed", self.text_show_all)
        page.pack_start(self.text_combo, False, False, 0)

        page.pack_start(section("二、记忆方法"), False, False, 0)
        self.text_tip = lbl("", size=13, color="#8a4b00", wrap=True)
        page.pack_start(self.text_tip, False, False, 0)

        page.pack_start(section("三、关键词（分段提取，用于串联）"), False, False, 0)
        self.text_keys = lbl("", size=15, bold=True, color="#1a6b3c", wrap=True)
        page.pack_start(self.text_keys, False, False, 0)

        page.pack_start(section("四、正文与分段练习"), False, False, 0)
        self.text_body = lbl("", size=15, wrap=True)
        page.pack_start(scroll(self.text_body), True, True, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="显示全文")
        b1.connect("clicked", self.text_show_all)
        b2 = Gtk.Button(label="开始自测（只看关键词）")
        b2.connect("clicked", self.text_quiz)
        b3 = Gtk.Button(label="逐段核对")
        b3.connect("clicked", self.text_para)
        b4 = Gtk.Button(label="记得")
        b4.connect("clicked", lambda _b: self.text_grade(True))
        b5 = Gtk.Button(label="再记")
        b5.connect("clicked", lambda _b: self.text_grade(False))
        for b in (b1, b2, b3, b4, b5):
            btns.pack_start(b, False, False, 0)
        page.pack_start(btns, False, False, 0)
        self.text_tip_label = lbl("", size=13, color="#1a6b3c", wrap=True)
        page.pack_start(self.text_tip_label, False, False, 0)
        self.text_para_idx = 0
        self.text_show_all()
        return page

    def text_cur(self):
        return data.SHORT_TEXTS[self.text_combo.get_active()]

    def text_show_all(self, _c=None):
        t = self.text_cur()
        self.text_tip.set_text("【记忆提示】" + t["tip"])
        self.text_keys.set_markup("<b>关键词：%s</b>" % "　→　".join(t["keywords"]))
        self.text_body.set_markup(
            '<span font_size="15">%s</span>' % "\n\n".join("%d、%s" % (i + 1, p) for i, p in enumerate(t["paragraphs"])))
        self.text_para_idx = 0
        self.text_tip_label.set_text("")

    def text_quiz(self, _b):
        t = self.text_cur()
        self.text_body.set_markup(
            '<span font_size="15" foreground="#8a4b00">（已隐藏正文，先看关键词，在脑中逐段回忆，再点“逐段核对”）</span>')
        self.text_para_idx = 0
        self.text_tip_label.set_text("先在脑中把关键词串成画面，回忆每段内容。")

    def text_para(self, _b):
        t = self.text_cur()
        if self.text_para_idx >= len(t["paragraphs"]):
            self.text_tip_label.set_markup('<span foreground="#1a6b3c">已全部核对。点“显示全文”可再次通读。</span>')
            return
        para = t["paragraphs"][self.text_para_idx]
        self.text_body.set_markup(
            '<span font_size="15">第 %d 段：%s</span>' % (self.text_para_idx + 1, para))
        self.text_para_idx += 1
        self.record("记短文")
        self.text_tip_label.set_markup(
            '<span foreground="#1a6b3c">已核对第 %d 段，继续回忆下一段。</span>' % self.text_para_idx)

    def text_grade(self, ok):
        t = self.text_cur()
        self.record("记短文", ok)
        self.text_tip_label.set_markup(
            '<span foreground="%s">%s　《%s》</span>' %
            ("#1a6b3c" if ok else "#b00000", "已记为：记得" if ok else "已记为：再记", t["title"]))

    # ================= 记忆方法 =================

    def page_method(self):
        page = box(14)
        page.pack_start(section("一、记忆方法总览"), False, False, 0)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        for name, desc in data.METHODS_OVERVIEW:
            row = Gtk.ListBoxRow(margin_top=4, margin_bottom=4)
            b = box(4)
            b.pack_start(lbl("<b>%s</b>" % name, size=14), False, False, 0)
            b.pack_start(lbl(desc, size=13, color="#555555", wrap=True), False, False, 0)
            row.add(b)
            listbox.add(row)
        page.pack_start(listbox, False, False, 0)

        page.pack_start(section("二、锁链奇像法（串联联想）"), False, False, 0)
        page.pack_start(lbl("将资料转化成图像，像锁链一样一个接一个地连接起来，顺序不乱地记录下来。",
                            size=14, wrap=True), False, False, 0)
        page.pack_start(lbl("规则：" + "；".join(data.CHAIN_RULES), size=14, wrap=True), False, False, 0)
        page.pack_start(lbl("注意要点：", size=14, bold=True), False, False, 0)
        for note in data.CHAIN_NOTES:
            page.pack_start(lbl(note, size=13, wrap=True), False, False, 0)

        page.pack_start(section("三、对应联想五法"), False, False, 0)
        rows = [("方法", "示例", "要领")] + data.ASSOCIATION_METHODS
        tbl = Gtk.Grid(column_spacing=12, row_spacing=6)
        for i, (a, b, c) in enumerate(rows):
            bold = i == 0
            tbl.attach(lbl(a, size=13, bold=bold), 0, i, 1, 1)
            tbl.attach(lbl(b, size=13, bold=bold), 1, i, 1, 1)
            tbl.attach(lbl(c, size=13, bold=bold), 2, i, 1, 1)
        page.pack_start(tbl, False, False, 0)

        page.pack_start(section("四、抽象转具象（口诀：提鞋赠刀王）"), False, False, 0)
        rows = [("方法", "抽象词", "具象图像", "说明")] + data.ABSTRACT_METHODS
        tbl = Gtk.Grid(column_spacing=10, row_spacing=6)
        for i, (a, b, c, d) in enumerate(rows):
            bold = i == 0
            tbl.attach(lbl(a, size=13, bold=bold), 0, i, 1, 1)
            tbl.attach(lbl(b, size=13, bold=bold), 1, i, 1, 1)
            tbl.attach(lbl(c, size=13, bold=bold), 2, i, 1, 1)
            tbl.attach(lbl(d, size=13, bold=bold), 3, i, 1, 1)
        page.pack_start(scroll(tbl, 900), True, True, 0)

        page.pack_start(section("五、记忆宫殿（地点桩）"), False, False, 0)
        page.pack_start(lbl(data.PALACE_DEF, size=14, wrap=True), False, False, 0)
        page.pack_start(lbl("选取规则：" + "；".join(data.PALACE_RULES), size=14, wrap=True), False, False, 0)
        for place, spots in data.PALACE_PRESET.items():
            page.pack_start(lbl("<b>%s（10 桩）</b>：%s" % (place, "、".join(spots)), size=14, wrap=True),
                            False, False, 0)

        page.pack_start(section("六、三十六计（1-36，用数字编码串联）"), False, False, 0)
        page.pack_start(scroll(grid(["%d·%s" % (i + 1, s) for i, s in enumerate(data.STRATEGIES_36)],
                                    columns=6, gap=8)), True, True, 0)
        page.pack_start(section("前 12 计数字编码联想"), False, False, 0)
        rows = [("数字", "编码", "计名", "联想")] + data.STRATEGY_LINK
        tbl = Gtk.Grid(column_spacing=12, row_spacing=6)
        for i, (a, b, c, d) in enumerate(rows):
            bold = i == 0
            tbl.attach(lbl(a, size=13, bold=bold), 0, i, 1, 1)
            tbl.attach(lbl(b, size=13, bold=bold), 1, i, 1, 1)
            tbl.attach(lbl(c, size=13, bold=bold), 2, i, 1, 1)
            tbl.attach(lbl(d, size=13, bold=bold, wrap=True), 3, i, 1, 1)
        page.pack_start(scroll(tbl, 900), True, True, 0)
        return page

    # ================= 专注力 =================

    def page_focus(self):
        page = box(14)
        page.pack_start(section("专注力训练说明"), False, False, 0)
        for name, desc in data.FOCUS_NOTES:
            page.pack_start(lbl("<b>%s</b>：%s" % (name, desc), size=13, wrap=True), False, False, 0)

        page.pack_start(section("舒尔特方格（5×5）"), False, False, 0)
        shulte_box = box(10)
        self.shulte_grid = Gtk.Grid(column_spacing=4, row_spacing=4)
        self.shulte_cells = []
        self.shulte_seq = list(range(1, 26))
        self.shulte_expected = 1
        self.shulte_start = 0.0
        for r in range(5):
            for c in range(5):
                b = Gtk.Button(label="", width_chars=3, height_chars=1)
                b.set_relief(Gtk.ReliefStyle.NONE)
                b.connect("clicked", self.shulte_click)
                self.shulte_grid.attach(b, c, r, 1, 1)
                self.shulte_cells.append(b)
        shulte_box.pack_start(self.shulte_grid, False, False, 0)
        self.shulte_tip = lbl("", size=13, color="#1a6b3c")
        shulte_box.pack_start(self.shulte_tip, False, False, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="开始")
        b1.connect("clicked", self.shulte_start)
        b2 = Gtk.Button(label="重置")
        b2.connect("clicked", self.shulte_reset)
        btns.pack_start(b1, False, False, 0)
        btns.pack_start(b2, False, False, 0)
        shulte_box.pack_start(btns, False, False, 0)
        page.pack_start(shulte_box, False, False, 0)

        page.pack_start(section("数数拍手（听到指定数字就拍手）"), False, False, 0)
        cl = box(10)
        self.clap_target = Gtk.ComboBoxText()
        self.clap_target.append("2、4、7")
        self.clap_target.append("3、6、9")
        self.clap_target.append("1、4、7")
        self.clap_target.append("5、7、9")
        self.clap_target.set_active(0)
        cl.pack_start(lbl("目标数字：", size=14, bold=True), False, False, 0)
        cl.pack_start(self.clap_target, False, False, 0)
        self.clap_num = lbl("点击“开始”训练", size=20, bold=True, color="#24406e", xalign=0.5)
        cl.pack_start(self.clap_num, False, False, 8)
        btns = row_box(10)
        b1 = Gtk.Button(label="拍手")
        b1.connect("clicked", self.clap_do)
        b2 = Gtk.Button(label="开始")
        b2.connect("clicked", self.clap_start)
        b3 = Gtk.Button(label="重置")
        b3.connect("clicked", self.clap_reset)
        btns.pack_start(b1, False, False, 0)
        btns.pack_start(b2, False, False, 0)
        btns.pack_start(b3, False, False, 0)
        cl.pack_start(btns, False, False, 0)
        self.clap_tip = lbl("", size=13, color="#1a6b3c")
        cl.pack_start(self.clap_tip, False, False, 0)
        page.pack_start(cl, False, False, 0)

        page.pack_start(section("16 词记忆测试（按顺序点击）"), False, False, 0)
        mt = box(10)
        self.mem_grid = Gtk.Grid(column_spacing=6, row_spacing=6)
        self.mem_cells = []
        self.mem_seq = list(data.MEMORY_TEST_WORDS)
        self.mem_pos = 0
        self.mem_start = 0.0
        for r in range(4):
            for c in range(4):
                b = Gtk.Button(label="", width_chars=6, height_chars=1)
                b.set_relief(Gtk.ReliefStyle.NONE)
                b.connect("clicked", self.mem_click)
                self.mem_grid.attach(b, c, r, 1, 1)
                self.mem_cells.append(b)
        mt.pack_start(self.mem_grid, False, False, 0)
        self.mem_tip = lbl("", size=13, color="#1a6b3c")
        mt.pack_start(self.mem_tip, False, False, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="开始回忆")
        b1.connect("clicked", self.mem_start)
        b2 = Gtk.Button(label="重置")
        b2.connect("clicked", self.mem_reset)
        btns.pack_start(b1, False, False, 0)
        btns.pack_start(b2, False, False, 0)
        mt.pack_start(btns, False, False, 0)
        page.pack_start(mt, False, False, 0)

        page.pack_start(section("听字训练（数一数指定字出现几次）"), False, False, 0)
        lt = box(10)
        self.listen_text = Gtk.Label(label=data.LISTEN_TEXT_1, xalign=0.0, wrap=True, line_width=18)
        lt.pack_start(self.listen_text, False, False, 0)
        btns = row_box(10)
        b1 = Gtk.Button(label="第 1 段（数“红”）")
        b1.connect("clicked", lambda _b: self.listen_text.set_label(data.LISTEN_TEXT_1))
        b2 = Gtk.Button(label="第 2 段（数“红”）")
        b2.connect("clicked", lambda _b: self.listen_text.set_label(data.LISTEN_TEXT_2))
        btns.pack_start(b1, False, False, 0)
        btns.pack_start(b2, False, False, 0)
        lt.pack_start(btns, False, False, 0)
        page.pack_start(lt, False, False, 0)
        return page

    def shulte_reset(self):
        for b in self.shulte_cells:
            b.set_label("")
            b.set_sensitive(True)
        self.shulte_expected = 1
        self.shulte_tip.set_text("")

    def shulte_start(self, _b):
        self.shulte_reset()
        random.shuffle(self.shulte_seq)
        for i, b in enumerate(self.shulte_cells):
            b.set_label(str(self.shulte_seq[i]))
        self.shulte_start = time.time()
        self.shulte_tip.set_text("按 1→25 的顺序依次点击。")

    def shulte_click(self, btn):
        if self.shulte_expected > 25:
            return
        label = btn.get_label()
        if label and label.isdigit() and int(label) == self.shulte_expected:
            self.shulte_expected += 1
            btn.set_label("✓")
            btn.set_sensitive(False)
            if self.shulte_expected == 26:
                elapsed = time.time() - self.shulte_start
                self.record("舒尔特", True)
                self.shulte_tip.set_markup(
                    '<span foreground="#1a6b3c">完成！用时 %.1f 秒（越短越专注，可反复挑战）</span>' % elapsed)
        else:
            self.shulte_tip.set_markup('<span foreground="#b00000">点错了，从 1 开始按顺序点。</span>')

    def clap_reset(self):
        if getattr(self, "clap_timer", None):
            GLib.source_remove(self.clap_timer)
            self.clap_timer = None
        self.clap_idx = 0
        self.clap_right = 0
        self.clap_miss = 0
        self.clap_wrong = 0
        self.clap_cur_is_target = False
        self.clap_prev_is_target = False
        self.clap_num.set_markup('<span font_size="20"><b>点击“开始”训练</b></span>')
        self.clap_tip.set_text("")

    def clap_start(self, _b):
        self.clap_reset()
        self.clap_seq = list(range(1, 31))
        self.clap_timer = GLib.timeout_add(1000, self.clap_next)

    def clap_next(self):
        if self.clap_idx >= len(self.clap_seq):
            self.clap_timer = None
            self.record("拍手训练", self.clap_right >= 8)
            self.clap_num.set_markup('<span font_size="20"><b>完成！</b></span>')
            self.clap_tip.set_markup(
                '<span foreground="#1a6b3c">正确拍手 %d 次，漏拍 %d 次，误拍 %d 次。</span>'
                % (self.clap_right, self.clap_miss, self.clap_wrong))
            return False
        num = self.clap_seq[self.clap_idx]
        target_map = {0: [2, 4, 7], 1: [3, 6, 9], 2: [1, 4, 7], 3: [5, 7, 9]}
        tset = set(target_map[self.clap_target.get_active()])
        if self.clap_prev_is_target:
            self.clap_miss += 1
        self.clap_num.set_markup('<span font_size="20"><b>数字：%d</b></span>' % num)
        self.clap_cur_is_target = num in tset
        self.clap_prev_is_target = self.clap_cur_is_target
        self.clap_idx += 1
        return True

    def clap_do(self, _b):
        if self.clap_timer is None:
            self.clap_tip.set_text("先点击“开始”。")
            return
        if self.clap_cur_is_target:
            self.clap_right += 1
            self.clap_prev_is_target = False
            self.clap_tip.set_markup('<span foreground="#1a6b3c">拍得对！</span>')
        else:
            self.clap_wrong += 1
            self.clap_tip.set_markup('<span foreground="#b00000">这个数字不用拍手。</span>')

    def mem_reset(self):
        for i, b in enumerate(self.mem_cells):
            b.set_label(data.MEMORY_TEST_WORDS[i])
            b.set_sensitive(True)
        self.mem_pos = 0
        self.mem_tip.set_text("")

    def mem_start(self, _b):
        self.mem_reset()
        for b in self.mem_cells:
            b.set_label("")
        self.mem_start = time.time()
        self.mem_tip.set_text("按记忆顺序点击格子（点对位置会显示词语）。")

    def mem_click(self, btn):
        if self.mem_pos >= 16:
            return
        if btn.get_label():
            return
        idx = self.mem_cells.index(btn)
        if idx == self.mem_pos:
            btn.set_label(self.mem_seq[self.mem_pos])
            btn.set_sensitive(False)
            self.mem_pos += 1
            if self.mem_pos == 16:
                elapsed = time.time() - self.mem_start
                self.record("记忆测试", True)
                self.mem_tip.set_markup(
                    '<span foreground="#1a6b3c">全部按顺序点完！用时 %.1f 秒，训练了顺序记忆。</span>' % elapsed)
        else:
            self.mem_tip.set_markup('<span foreground="#b00000">顺序不对，回忆原序列再试。</span>')

    # ================= 学习统计 =================

    def page_stats(self):
        page = box(14)
        page.pack_start(section("训练记录（保存在 ~/.config/记忆法训练助手）"), False, False, 0)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        if not self.progress:
            page.pack_start(lbl("还没有训练记录，去四大练习模块练一练吧。", size=14, color="#555555"),
                            False, False, 0)
            return page
        order = ["记数字", "记单词", "记古诗", "记短文", "舒尔特", "拍手训练", "记忆测试"]
        for name in order:
            s = self.progress.get(name)
            if not s:
                continue
            rate = (s["ok"] * 100.0 / s["n"]) if s["n"] else 0.0
            row = Gtk.ListBoxRow(margin_top=6, margin_bottom=6)
            row.add(lbl("<b>%s</b>：训练 %d 次，正确/记得 %d 次，正确率 %.0f%%"
                        % (name, s["n"], s["ok"], rate), size=14))
            listbox.add(row)
        page.pack_start(listbox, True, True, 0)
        return page


def main():
    MemoryApp()
    Gtk.main()


if __name__ == "__main__":
    main()
