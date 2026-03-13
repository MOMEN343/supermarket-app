# -*- coding: utf-8 -*-
import os
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
import re

from kivy.config import Config
Config.set('graphics', 'width',  '430')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.scrollview  import ScrollView
from kivy.uix.label       import Label
from kivy.uix.button      import Button
from kivy.uix.textinput   import TextInput
from kivy.uix.widget      import Widget
from kivy.uix.popup       import Popup
from kivy.graphics         import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.core.text       import LabelBase
from kivy.core.window     import Window
from kivy.metrics         import dp, sp
from kivy.animation       import Animation
from kivy.clock           import Clock

import database as db

# ─── تهيئة قاعدة البيانات ─────────────────────────────────
db.init_db()
db.seed_sample_data()

# ─── الخطوط ───────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))

# سنستخدم خط 'Amiri' لأنه يعتبر من أكثر الخطوط العربية استقراراً ودعماً لكافة الأشكال (البداية، الوسط، النهاية، والمنفصل)
# وهذا يحل مشكلة ظهور المربعات التي تظهر في بعض الخطوط الأخرى.
FONTS_DIR = os.path.join(BASE_DIR, 'fonts', 'Amiri-1.000')

F_REG  = 'Amiri-Regular.ttf'
F_BOLD = 'Amiri-Bold.ttf'

# التحقق من المسار لضمان عمله في كل البيئات
if not os.path.exists(os.path.join(FONTS_DIR, F_REG)):
    # بديل في حال لم يتوفر Amiri
    FONTS_DIR = os.path.join(BASE_DIR, 'fonts', 'extracted', 'Beiruti', 'static')
    F_REG, F_BOLD = 'Beiruti-Regular.ttf', 'Beiruti-Bold.ttf'

# تسجيل الخط ليكون هو الخط الأساسي في التطبيق
LabelBase.register(
    name='Cairo', # نبقيه بنفس الاسم لتفادي تعديل كل الودجت
    fn_regular=os.path.join(FONTS_DIR, F_REG),
    fn_bold   =os.path.join(FONTS_DIR, F_BOLD),
)

# حيلة لجعله الخط الافتراضي في Kivy لجميع المكونات
LabelBase.register(
    name='Roboto',
    fn_regular=os.path.join(FONTS_DIR, F_REG),
    fn_bold   =os.path.join(FONTS_DIR, F_BOLD),
)

Window.clearcolor = (0.06, 0.06, 0.11, 1)
Window.softinput_mode = 'below_target'

def ar(t):
    """
    دالة معالجة النصوص العربية مع تنظيف عميق للرموز التي تسبب ظهور مربعات.
    """
    if not t: return ""
    try:
        # 1. إعادة تشكيل الحروف
        reshaped = arabic_reshaper.reshape(str(t))
        # 2. ترتيب النص
        bidi_text = get_display(reshaped)
        # 3. تنظيف رموز التحكم التي قد تظهر كمربعات في بعض المحركات
        clean = re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069\u200b-\u200d]', '', bidi_text)
        return clean
    except Exception:
        return str(t)

# ─── أيقونات مرسومة يدوياً (Procedural Icons) ────────────────
class SunIcon(Widget):
    def __init__(self, **kw):
        super().__init__(size_hint=(None, None), size=(dp(24), dp(24)), **kw)
        with self.canvas:
            Color(1, 0.9, 0.2, 1)
            self.body = Ellipse(pos=(self.x+dp(4), self.y+dp(14)), size=(dp(16), dp(16))) # رفعناه أكثر للوسط
        self.bind(pos=self._u, size=self._u)
    def _u(self, *_):
        self.body.pos = (self.x+dp(4), self.y+dp(14))

class MoonIcon(Widget):
    def __init__(self, **kw):
        super().__init__(size_hint=(None, None), size=(dp(24), dp(24)), **kw)
        with self.canvas:
            Color(0.85, 0.85, 0.95, 1)
            self.body = Ellipse(pos=(self.x+dp(4), self.y+dp(14)), size=(dp(16), dp(16)))
            Color(0.14, 0.07, 0.36, 1) 
            self.mask = Ellipse(pos=(self.x+dp(8), self.y+dp(16)), size=(dp(16), dp(16)))
        self.bind(pos=self._u, size=self._u)
    def _u(self, *_):
        self.body.pos = (self.x+dp(4), self.y+dp(14))
        self.mask.pos = (self.x+dp(8), self.y+dp(16))

# ─── الألوان ───────────────────────────────────────────────
C = {
    'bg':     (0.06, 0.06, 0.11, 1),
    'card':   (0.12, 0.12, 0.20, 1),
    'hdr':    (0.14, 0.07, 0.36, 1),
    'purple': (0.48, 0.22, 0.95, 1),
    'blue':   (0.12, 0.62, 0.96, 1),
    'orange': (0.96, 0.44, 0.18, 1),
    'green':  (0.18, 0.84, 0.58, 1),
    'red':    (0.95, 0.25, 0.35, 1),
    'white':  (1, 1, 1, 1),
    'gray':   (0.58, 0.58, 0.74, 1),
    'dim':    (0.18, 0.18, 0.30, 1),
    'nav':    (0.08, 0.08, 0.16, 1),
    'input':  (0.10, 0.10, 0.18, 1),
}

# ألوان الأفاتار حسب الحرف الأول
AVATAR_COLORS = [C['purple'], C['blue'], C['orange'], C['green'],
                 (0.80,0.20,0.50,1), (0.20,0.70,0.80,1), (0.90,0.60,0.10,1)]

def avatar_color(name):
    idx = ord(name[0]) % len(AVATAR_COLORS)
    return AVATAR_COLORS[idx]

# ─── مكونات UI ────────────────────────────────────────────
class Card(BoxLayout):
    def __init__(self, bg=None, radius=16, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*(bg or C['card']))
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *_):
        self._r.pos = self.pos; self._r.size = self.size

class Avatar(BoxLayout):
    def __init__(self, letter, color, size_px=46, **kw):
        super().__init__(size_hint=(None,None), size=(dp(size_px), dp(size_px)), **kw)
        with self.canvas.before:
            Color(*color)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(size_px/2)])
        self.bind(pos=self._u, size=self._u)
        self.add_widget(Label(text=letter, font_name='Cairo',
                              font_size=sp(size_px*0.44), bold=True, color=C['white']))
    def _u(self, *_):
        self._r.pos = self.pos; self._r.size = self.size

class Btn(Button):
    def __init__(self, bg=None, radius=12, **kw):
        super().__init__(**kw)
        self.background_normal = ''
        self.background_color  = (0,0,0,0)
        self.font_name = 'Cairo'
        self.color     = C['white']
        with self.canvas.before:
            Color(*(bg or C['purple']))
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=self._u, size=self._u)
    def _u(self, *_):
        self._r.pos = self.pos; self._r.size = self.size
    def on_press(self):   Animation(opacity=0.65, duration=0.07).start(self)
    def on_release(self): Animation(opacity=1.0,  duration=0.12).start(self)

# ─── حقل إدخال عربي ذكي (حل مشكلة الحروف المنفصلة) ──────────
class ArInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._raw = ""
        self.halign = 'right'
        self.base_direction = 'ltr' # نتحكم بالاتجاه يدوياً لضمان الدقة وتجنب العكس المزدوج
        self.font_name = 'Cairo'
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        # نضيف الحرف للنص الخام
        self._raw += substring
        # نعرض النص مشكلاً وموصولاً
        self.text = ar(self._raw)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        # نحذف آخر حرف من النص الخام
        self._raw = self._raw[:-1]
        self.text = ar(self._raw)

    @property
    def raw_text(self):
        return self._raw

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # وضع المؤشر دائماً في نهاية النص (يسار النص العربي المشكل)
            self.cursor = (len(self.text), 0)
        return super().on_touch_down(touch)

def make_input(hint, **kw):
    return ArInput(
        hint_text=ar(hint),
        font_size=sp(15),
        background_color=C['input'],
        foreground_color=C['white'],
        hint_text_color=list(C['gray']),
        cursor_color=C['purple'],
        padding=[dp(12), dp(10)],
        **kw
    )

def section_title(text):
    return Label(
        text=ar(text), font_name='Cairo', font_size=sp(17), bold=True,
        color=C['white'], size_hint_y=None, height=dp(32),
        halign='right', text_size=(Window.width - dp(28), None),
    )

# ═══════════════════════════════════════════════════════════
#  Popup: إضافة زبون جديد
# ═══════════════════════════════════════════════════════════
class AddCustomerPopup(Popup):
    def __init__(self, on_done, **kw):
        super().__init__(
            title='', separator_height=0,
            background='', background_color=(0,0,0,0),
            size_hint=(0.92, None), height=dp(280),
            **kw
        )
        self.on_done = on_done

        box = Card(bg=(0.12,0.10,0.24,1), radius=20,
                   orientation='vertical',
                   padding=[dp(20), dp(20)], spacing=dp(14))

        box.add_widget(Label(
            text=ar('اضافة زبون جديد'),
            font_name='Cairo', font_size=sp(20), bold=True,
            color=C['white'], size_hint_y=None, height=dp(34),
        ))

        self.name_in  = make_input('اسم الزبون *', size_hint_y=None, height=dp(46))
        self.phone_in = make_input('رقم الهاتف',   size_hint_y=None, height=dp(46))

        box.add_widget(self.name_in)
        box.add_widget(self.phone_in)

        # أزرار الحفظ والإلغاء
        btn_row = BoxLayout(orientation='horizontal',
                            size_hint_y=None, height=dp(48), spacing=dp(10))
        cancel = Btn(text=ar('الغاء'), bg=C['dim'],   radius=12, font_size=sp(15))
        cancel.bind(on_release=lambda *_: self.dismiss())
        save   = Btn(text=ar('حفظ'),   bg=C['green'], radius=12, font_size=sp(15))
        save.bind(on_release=self._save)
        btn_row.add_widget(cancel)
        btn_row.add_widget(save)
        box.add_widget(btn_row)

        self.content = box

    def _save(self, *_):
        # نأخذ الاسم "الخام" لضمان تخزينه بشكل صحيح في قاعدة البيانات
        name = self.name_in.raw_text.strip() if hasattr(self.name_in, 'raw_text') else self.name_in.text.strip()
        if not name:
            self.name_in.hint_text = ar('* الاسم مطلوب!')
            return
        # رقم الهاتف لا يحتاج تشكيل لذا نأخذ النص مباشرة
        phone = self.phone_in.text.strip()
        db.add_customer(name, phone)
        self.dismiss()
        self.on_done()

# ═══════════════════════════════════════════════════════════
#  Popup: تسجيل معاملة (دفع / دين / مشترى)
# ═══════════════════════════════════════════════════════════
class TransactionPopup(Popup):
    def __init__(self, customer, tx_type, on_done, **kw):
        super().__init__(
            title='', separator_height=0,
            background='', background_color=(0,0,0,0),
            size_hint=(0.92, None), height=dp(320),
            **kw
        )
        self.customer = customer
        self.tx_type  = tx_type
        self.on_done  = on_done

        titles = {'payment': 'تسجيل دفعة', 'debt': 'تسجيل دين', 'purchase': 'مشترى جديد'}
        colors = {'payment': C['green'],    'debt': C['red'],     'purchase': C['blue']}
        col = colors[tx_type]

        box = Card(bg=(0.12,0.10,0.24,1), radius=20,
                   orientation='vertical',
                   padding=[dp(20), dp(20)], spacing=dp(14))

        box.add_widget(Label(
            text=ar(titles[tx_type]),
            font_name='Cairo', font_size=sp(20), bold=True,
            color=col, size_hint_y=None, height=dp(34),
        ))
        box.add_widget(Label(
            text=ar(f'الزبون: {customer["name"]}'),
            font_name='Cairo', font_size=sp(14),
            color=C['gray'], size_hint_y=None, height=dp(24),
        ))

        self.desc_in   = make_input('الوصف', size_hint_y=None, height=dp(46))
        self.amount_in = make_input('المبلغ بالشيكل', size_hint_y=None, height=dp(46))
        box.add_widget(self.desc_in)
        box.add_widget(self.amount_in)

        btn_row = BoxLayout(orientation='horizontal',
                            size_hint_y=None, height=dp(48), spacing=dp(10))
        cancel = Btn(text=ar('الغاء'), bg=C['dim'], radius=12, font_size=sp(15))
        cancel.bind(on_release=lambda *_: self.dismiss())
        save   = Btn(text=ar('حفظ'), bg=col, radius=12, font_size=sp(15))
        save.bind(on_release=self._save)
        btn_row.add_widget(cancel)
        btn_row.add_widget(save)
        box.add_widget(btn_row)

        self.content = box

    def _save(self, *_):
        try:
            amount = float(self.amount_in.text.strip().replace(',', '.'))
        except ValueError:
            self.amount_in.hint_text = ar('* أدخل رقماً صحيحاً')
            return
        # نأخذ الوصف "الخام" لضمان عدم تخزينه معكوساً في القاعدة
        desc    = self.desc_in.raw_text.strip() if hasattr(self.desc_in, 'raw_text') else self.desc_in.text.strip()
        desc    = desc or self.tx_type
        is_paid = 0 if self.tx_type == 'debt' else 1
        db.add_transaction(self.customer['id'], self.tx_type, desc, amount, is_paid)
        self.dismiss()
        self.on_done()

# ═══════════════════════════════════════════════════════════
#  شاشة تفاصيل الزبون
# ═══════════════════════════════════════════════════════════
class DetailScreen(BoxLayout):
    def __init__(self, customer, on_back, **kw):
        super().__init__(orientation='vertical', **kw)
        self.customer = customer
        self.on_back  = on_back
        self._build()

    def _build(self):
        self.clear_widgets()
        cust    = self.customer
        col     = avatar_color(cust['name'])
        summary = db.get_customer_summary(cust['id'])
        txs     = db.get_transactions(cust['id'])

        # ── Header ──────────────────────────────────────────
        hdr = Card(bg=C['hdr'], radius=0, orientation='horizontal',
                   size_hint_y=None, height=dp(84),
                   padding=[dp(12), dp(14)], spacing=dp(10))
        back = Btn(text=ar('رجوع'), bg=C['dim'], radius=10, font_size=sp(13),
                   size_hint=(None,None), size=(dp(68), dp(40)))
        back.bind(on_release=lambda *_: self.on_back())
        hdr.add_widget(back)
        hdr.add_widget(Avatar(letter=cust['name'][0], color=col, size_px=46))
        nc = BoxLayout(orientation='vertical', spacing=dp(2))
        nc.add_widget(Label(text=ar(cust['name']), font_name='Cairo', font_size=sp(18),
                            bold=True, color=C['white'],
                            halign='right', text_size=(dp(220), None),
                            size_hint_y=None, height=dp(28)))
        nc.add_widget(Label(text=cust.get('phone',''), font_size=sp(12), color=C['gray'],
                            halign='right', text_size=(dp(220), None),
                            size_hint_y=None, height=dp(20)))
        hdr.add_widget(nc)
        self.add_widget(hdr)

        # ── محتوى قابل للتمرير ───────────────────────────────
        scroll = ScrollView(size_hint=(1,1), do_scroll_x=False)
        box = BoxLayout(orientation='vertical', size_hint_y=None,
                        spacing=dp(12), padding=[dp(14), dp(14), dp(14), dp(20)])
        box.bind(minimum_height=box.setter('height'))

        # بطاقات الملخص المالي
        srow = BoxLayout(orientation='horizontal', size_hint_y=None,
                         height=dp(94), spacing=dp(10))
        for icon_txt, title, val, col2 in [
            ('$+', ar('رصيده لنا'),  ar(f"{summary['paid']:.2f} ش"),  C['green']),
            ('!',  ar('دين عليه'),   ar(f"{summary['debt']:.2f} ش"),   C['red']),
            ('#',  ar('مجموع شراء'), ar(f"{summary['total_purchases']:.2f} ش"), C['blue']),
        ]:
            c = Card(bg=C['card'], radius=14, orientation='vertical',
                     padding=[dp(6), dp(10)], spacing=dp(2))
            c.add_widget(Label(text=icon_txt, font_size=sp(20),
                               color=col2, bold=True,
                               size_hint_y=None, height=dp(28)))
            c.add_widget(Label(text=val, font_name='Cairo', font_size=sp(14),
                               color=col2, bold=True,
                               size_hint_y=None, height=dp(24)))
            c.add_widget(Label(text=title, font_name='Cairo', font_size=sp(11),
                               color=C['gray'], size_hint_y=None, height=dp(18)))
            srow.add_widget(c)
        box.add_widget(srow)

        # أزرار الإجراءات
        box.add_widget(section_title('اجراءات سريعة'))
        act_row = BoxLayout(orientation='horizontal', size_hint_y=None,
                            height=dp(50), spacing=dp(8))
        for txt, col3, ttype in [
            (ar('دفعة'), C['green'],  'payment'),
            (ar('دين'),  C['red'],    'debt'),
            (ar('مشترى'), C['blue'], 'purchase'),
        ]:
            b = Btn(text=txt, bg=col3, radius=12, font_size=sp(14))
            b.bind(on_release=lambda inst, t=ttype: self._open_tx(t))
            act_row.add_widget(b)
        box.add_widget(act_row)

        # سجل المعاملات
        box.add_widget(section_title('سجل المعاملات'))

        if not txs:
            box.add_widget(Label(
                text=ar('لا توجد معاملات بعد'),
                font_name='Cairo', font_size=sp(14), color=C['gray'],
                size_hint_y=None, height=dp(50),
            ))
        else:
            for tx in txs:
                row = Card(bg=C['card'], radius=12, orientation='horizontal',
                           size_hint_y=None, height=dp(66),
                           padding=[dp(12), dp(8)], spacing=dp(8))

                type_colors = {'payment': C['green'], 'debt': C['red'], 'purchase': C['blue']}
                type_labels = {'payment': ar('دفعة'), 'debt': ar('دين'), 'purchase': ar('شراء')}
                tx_col = type_colors.get(tx['type'], C['gray'])
                tx_lbl = type_labels.get(tx['type'], ar(tx['type']))

                row.add_widget(Label(text=tx_lbl, font_name='Cairo', font_size=sp(11),
                                     color=tx_col, size_hint=(None,1), width=dp(50),
                                     halign='center'))
                row.add_widget(Label(text=ar(f"{tx['amount']:.2f} ش"),
                                     font_name='Cairo', font_size=sp(15), bold=True,
                                     color=C['orange'], size_hint=(None,1), width=dp(80),
                                     halign='center'))
                info = BoxLayout(orientation='vertical', spacing=dp(2))
                info.add_widget(Label(text=ar(tx['description'] or ''),
                                      font_name='Cairo', font_size=sp(13), color=C['white'],
                                      halign='right', text_size=(dp(180), None),
                                      size_hint_y=None, height=dp(22)))
                date_str = tx['date'][:10] if tx['date'] else ''
                info.add_widget(Label(text=date_str, font_size=sp(11), color=C['gray'],
                                      halign='right', text_size=(dp(180), None),
                                      size_hint_y=None, height=dp(18)))
                row.add_widget(info)
                box.add_widget(row)
                box.add_widget(Widget(size_hint_y=None, height=dp(4)))

        scroll.add_widget(box)
        self.add_widget(scroll)

    def _open_tx(self, tx_type):
        popup = TransactionPopup(
            customer=self.customer,
            tx_type=tx_type,
            on_done=self._build,
        )
        popup.open()

# ═══════════════════════════════════════════════════════════
#  الشاشة الرئيسية
# ═══════════════════════════════════════════════════════════
class HomeScreen(BoxLayout):
    def __init__(self, on_select, **kw):
        super().__init__(orientation='vertical', **kw)
        self.on_select = on_select
        self.filtered  = []

        # ── Header: ساعة وتاريخ ──────────────────────────────
        hdr = Card(bg=C['hdr'], radius=0, orientation='vertical',
                   size_hint_y=None, height=dp(230),  # زيادة الارتفاع لمنع القص
                   padding=[dp(18), dp(14)], spacing=dp(8))

        # ─── شريط العنوان والترحيب ──────────────────────────
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), 
                            padding=[dp(15), 0], spacing=dp(10))
        
        # الترحيب (يسار)
        greet_box = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(140))
        self.icon_area = BoxLayout(size_hint=(None, None), size=(dp(24), dp(24)), pos_hint={'center_y': 0.5})
        self.greet_lbl = Label(
            text='', font_name='Cairo', font_size=sp(16),
            color=C['orange'], bold=True,
            halign='left', valign='middle'
        )
        self.greet_lbl.bind(size=self.greet_lbl.setter('text_size'))
        greet_box.add_widget(self.icon_area)
        greet_box.add_widget(self.greet_lbl)
        
        # العنوان (يمين) - تصميم بسيط وراقي
        title_box = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint=(1, 1))
        title_lbl = Label(
            text=ar('سوبرماركت زعرب'),
            font_name='Cairo', font_size=sp(22),
            color=C['white'], bold=True,
            halign='right', valign='middle'
        )
        title_lbl.bind(size=title_lbl.setter('text_size'))
        
        title_box.add_widget(title_lbl)

        top_bar.add_widget(greet_box)
        top_bar.add_widget(title_box)
        hdr.add_widget(top_bar)

        # ─── تصميم الساعة العصري ────────────────────────────
        clock_card = Card(bg=(0.20, 0.15, 0.40, 0.6), radius=20,
                          orientation='horizontal',
                          size_hint=(0.9, None), height=dp(100),
                          pos_hint={'center_x': 0.5},
                          padding=[dp(10), dp(10)])
        
        inner_clock = BoxLayout(orientation='horizontal', size_hint_x=None, spacing=dp(2))
        inner_clock.bind(minimum_width=inner_clock.setter('width'))

        # صباحاً / مساءً (يسار)
        self.time_ampm = Label(
            text='', font_name='Cairo', font_size=sp(18),
            color=C['gray'], bold=True,
            size_hint=(None, 1), width=dp(70),
            halign='center', valign='middle'
        )
        
        # الوقت الرئيسي (الساعة:الدقائق)
        self.time_main = Label(
            text='00:00', font_name='Cairo', font_size=sp(66),
            bold=True, color=C['white'],
            size_hint=(None, 1), width=dp(150),
            halign='center', valign='middle'
        )
        
        # الثواني (يمين)
        self.time_sec = Label(
            text=':00', font_name='Cairo', font_size=sp(26),
            bold=True, color=C['purple'],
            size_hint=(None, 1), width=dp(45),
            halign='center', valign='bottom'
        )
        
        inner_clock.add_widget(self.time_ampm)
        inner_clock.add_widget(self.time_main)
        inner_clock.add_widget(self.time_sec)
        
        # التوسيط داخل الكارد
        centered_box = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        centered_box.add_widget(Widget()) # spacer
        centered_box.add_widget(inner_clock)
        centered_box.add_widget(Widget()) # spacer
        
        clock_card.add_widget(centered_box)
        hdr.add_widget(clock_card)

        # التاريخ واليوم
        date_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(50), spacing=dp(2))
        self.date_lbl = Label(
            text='', font_name='Cairo', font_size=sp(16),
            color=(0.90, 0.90, 1.0, 1), bold=True,
            size_hint_y=None, height=dp(24), halign='center'
        )
        self.day_lbl = Label(
            text='', font_name='Cairo', font_size=sp(13),
            color=C['gray'],
            size_hint_y=None, height=dp(20), halign='center'
        )
        date_box.add_widget(self.date_lbl)
        date_box.add_widget(self.day_lbl)
        hdr.add_widget(date_box)

        self.add_widget(hdr)

        # ── شريط البحث + زر إضافة ────────────────────────────
        sb = Card(bg=C['input'], radius=0,
                  orientation='horizontal',
                  size_hint_y=None, height=dp(60),
                  padding=[dp(12), dp(10)], spacing=dp(8))

        self.search = ArInput(
            hint_text=ar('ابحث عن زبون بالاسم او الرقم...'),
            font_size=sp(15),
            background_color=(0,0,0,0),
            foreground_color=C['white'],
            hint_text_color=list(C['gray']),
            cursor_color=C['purple'],
            padding=[dp(8), dp(10)],
        )
        self.search.bind(text=self._search)
        sb.add_widget(self.search)

        add_btn = Btn(text=ar('+ زبون'), bg=C['purple'], radius=10,
                      font_size=sp(13),
                      size_hint=(None,None), size=(dp(80), dp(40)))
        add_btn.bind(on_release=self._add_customer)
        sb.add_widget(add_btn)
        self.add_widget(sb)

        # فاصل
        div = Widget(size_hint_y=None, height=dp(1))
        with div.canvas:
            Color(*C['dim'])
            self._div = Rectangle(pos=div.pos, size=div.size)
        div.bind(pos=lambda w,p: setattr(self._div,'pos',p),
                 size=lambda w,s: setattr(self._div,'size',s))
        self.add_widget(div)

        # ── قائمة الزبائن ─────────────────────────────────────
        self.scroll = ScrollView(size_hint=(1,1), do_scroll_x=False)
        self.list_box = BoxLayout(orientation='vertical', size_hint_y=None,
                                  spacing=dp(8),
                                  padding=[dp(12), dp(12), dp(12), dp(16)])
        self.list_box.bind(minimum_height=self.list_box.setter('height'))
        self.scroll.add_widget(self.list_box)
        self.add_widget(self.scroll)

        self._load()
        Clock.schedule_interval(self._tick, 1)
        self._tick(0)

    def _tick(self, dt):
        now = datetime.now()
        
        # حساب الساعة 12
        h = now.hour % 12
        if h == 0: h = 12
        
        # الوقت
        self.time_main.text = f"{h:02}:{now.minute:02}"
        self.time_sec.text  = f":{now.second:02}"
        
        # صباحاً / مساءً
        is_pm = now.hour >= 12
        self.time_ampm.text = ar('مساءً') if is_pm else ar('صباحاً')

        # الترحيب الديناميكي
        if 5 <= now.hour < 12:
            greet, icon = 'صباح الخير', SunIcon()
        elif 12 <= now.hour < 17:
            greet, icon = 'طاب يومك', SunIcon() # Could be a different sun
        elif 17 <= now.hour < 21:
            greet, icon = 'مساء الخير', MoonIcon()
        else:
            greet, icon = 'ليلة سعيدة', MoonIcon()
        
        if hasattr(self, 'greet_lbl'):
            self.greet_lbl.text = ar(greet)
            if hasattr(self, 'icon_area'):
                self.icon_area.clear_widgets()
                self.icon_area.add_widget(icon)

        days   = ['الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','الأحد']
        months = ['', 'كانون الثاني', 'شباط', 'آذار', 'نيسان', 'أيار', 'حزيران',
                  'تموز', 'آب', 'أيلول', 'تشرين الأول', 'تشرين الثاني', 'كانون الأول']
        self.date_lbl.text = ar(f'{now.day} {months[now.month]} {now.year}')
        self.day_lbl.text  = ar(days[now.weekday()])

    def _load(self):
        q = self.search.text.strip() if hasattr(self, 'search') else ''
        self.filtered = db.search_customers(q) if q else db.get_all_customers()
        self._render()

    def _search(self, inst, val):
        # نستخدم النص الخام (Raw Text) للبحث في قاعدة البيانات لضمان دقة النتائج
        q = inst.raw_text.strip() if hasattr(inst, 'raw_text') else val.strip()
        self.filtered = db.search_customers(q) if q else db.get_all_customers()
        self._render()

    def _render(self):
        self.list_box.clear_widgets()
        if not self.filtered:
            self.list_box.add_widget(Label(
                text=ar('لا يوجد زبون بهذا الاسم'),
                font_name='Cairo', font_size=sp(16), color=C['gray'],
                size_hint_y=None, height=dp(60),
            ))
            return
        for cust in self.filtered:
            self.list_box.add_widget(self._make_row(cust))

    def _make_row(self, cust):
        col     = avatar_color(cust['name'])
        summary = db.get_customer_summary(cust['id'])

        row = Card(bg=C['card'], radius=14, orientation='horizontal',
                   size_hint_y=None, height=dp(76),
                   padding=[dp(10), dp(10)], spacing=dp(10))

        row.add_widget(Avatar(letter=cust['name'][0], color=col, size_px=46))

        info = BoxLayout(orientation='vertical', spacing=dp(2))
        info.add_widget(Label(
            text=ar(cust['name']), font_name='Cairo', font_size=sp(15),
            color=C['white'], bold=True,
            halign='right', text_size=(dp(170), None),
            size_hint_y=None, height=dp(24),
        ))
        info.add_widget(Label(
            text=cust.get('phone',''), font_size=sp(12), color=C['gray'],
            halign='right', text_size=(dp(170), None),
            size_hint_y=None, height=dp(18),
        ))
        debt = summary['debt']
        paid = summary['paid']
        if debt > 0:
            st_col = C['red']
            st_txt = ar(f"دين: {debt:.2f} ش")
        elif paid > 0:
            st_col = C['green']
            st_txt = ar(f"دفع: {paid:.2f} ش")
        else:
            st_col = C['gray']
            st_txt = ar('زبون جديد')
        info.add_widget(Label(
            text=st_txt, font_name='Cairo', font_size=sp(11),
            color=st_col,
            halign='right', text_size=(dp(170), None),
            size_hint_y=None, height=dp(16),
        ))
        row.add_widget(info)

        btn = Btn(text=ar('عرض'), bg=col, radius=10,
                  font_size=sp(13),
                  size_hint=(None,None), size=(dp(64), dp(38)))
        btn.bind(on_release=lambda *_, c=cust: self.on_select(c))
        row.add_widget(btn)
        return row

    def _add_customer(self, *_):
        popup = AddCustomerPopup(on_done=self._load)
        popup.open()

# ─── شاشة التقارير والتصدير ──────────────────────────────────────────
def export_excel_file(filename):
    """دالة مركزية لتصدير إكسل لمنع تكرار الكود واستخدامها للتقرير التلقائي واليدوي"""
    customers = db.get_all_customers()
    html_content = f"""
    <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
            body {{ direction: rtl; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th {{ background-color: #4CAF50; color: white; border: 1px solid #ddd; padding: 12px; }}
            td {{ border: 1px solid #ddd; padding: 10px; text-align: right; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2 style="text-align: center;">تقرير مبيعات سوبرماركت زعرب - {datetime.now().strftime('%Y/%m/%d %H:%M')}</h2>
        <table>
            <thead>
                <tr>
                    <th>الاسم</th>
                    <th>رقم الهاتف</th>
                    <th>إجمالي المشتريات</th>
                    <th>الدين المتبقي</th>
                    <th>الرصيد الحالي</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for cust in customers:
        summary = db.get_customer_summary(cust['id'])
        html_content += f"""
                <tr>
                    <td>{cust['name']}</td>
                    <td>{cust.get('phone', '')}</td>
                    <td>{summary['total_purchases']:.2f}</td>
                    <td>{summary['debt']:.2f}</td>
                    <td>{summary['paid']:.2f}</td>
                </tr>
        """
        
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

class ReportsScreen(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', padding=[dp(20), dp(20)], spacing=dp(10), **kw)
        
        self.add_widget(Label(
            text=ar('قسم التقارير الشهرية'),
            font_name='Cairo', font_size=sp(22), bold=True,
            color=C['white'], size_hint_y=None, height=dp(50)
        ))
        
        info_card = Card(bg=C['card'], radius=15, orientation='vertical', padding=[dp(15), dp(15)], spacing=dp(10), size_hint_y=None, height=dp(70))
        info_card.add_widget(Label(
            text=ar('استخراج كشف حساب جديد وتصفح التقارير السابقة بسهولة.'),
            font_name='Cairo', font_size=sp(14), color=C['gray'],
            halign='center', text_size=(Window.width - dp(60), None)
        ))
        self.add_widget(info_card)
        
        self.status_lbl = Label(text="", font_name='Cairo', font_size=sp(13), color=C['green'], size_hint_y=None, height=dp(20))
        self.add_widget(self.status_lbl)
        
        self.export_btn = Btn(text=ar('استخراج تقرير الآن (Excel)'), bg=C['green'], radius=12, size_hint_y=None, height=dp(56))
        self.export_btn.bind(on_release=self._export)
        self.add_widget(self.export_btn)
        
        self.add_widget(Label(
            text=ar('قائمة التقارير المسجلة:'),
            font_name='Cairo', font_size=sp(16), bold=True,
            color=C['white'], size_hint_y=None, height=dp(30),
            halign='right', text_size=(Window.width - dp(40), None)
        ))

        # حاوية التمرير لعرض التقارير السابقة والتلقائية
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.files_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=[dp(5), dp(5)])
        self.files_box.bind(minimum_height=self.files_box.setter('height'))
        self.scroll.add_widget(self.files_box)
        self.add_widget(self.scroll)

        self._load_files()

    def _load_files(self):
        self.files_box.clear_widgets()
        import glob
        import os
        
        # جلب التقارير وإعادة ترتيبها الأحدث أولاً بواجهات عربية
        files = glob.glob("تقرير_*.xls") + glob.glob("تقرير_تلقائي_*.xls")
        files = sorted(list(set(files)), key=os.path.getmtime, reverse=True)
        
        if not files:
            self.files_box.add_widget(Label(
                text=ar('لا توجد تقارير سابقة'), font_name='Cairo', font_size=sp(14),
                color=C['gray'], size_hint_y=None, height=dp(50)
            ))
        
        for f_name in files:
            # بطاقة التقرير مع زر الفتح على اليسار والاسم على اليمين
            row = Card(bg=C['input'], radius=10, orientation='horizontal', 
                       size_hint_y=None, height=dp(60), padding=[dp(10), dp(5)], spacing=dp(10))
            
            # زر الفتح (على اليسار)
            open_btn = Btn(text=ar('فتح'), bg=C['blue'], radius=8, size_hint_x=None, width=dp(70))
            open_btn.bind(on_release=lambda inst, fname=f_name: self._open_file(fname))
            row.add_widget(open_btn)

            # اسم الملف (على اليمين)
            # بما أن الملف أصلاً يحمل اسماً عربياً، نعرضه كما هو (مع التشكيل للعرض)
            display_name = f_name.replace('.xls', '')
            lbl = Label(text=ar(display_name), font_name='Cairo', font_size=sp(14), 
                        color=C['white'], halign='right', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            row.add_widget(lbl)
            
            self.files_box.add_widget(row)

    def _export(self, *_):
        try:
            # ملف باسم عربي وتاريخ ليظل محفوظاً
            filename = f"تقرير_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xls"
            export_excel_file(filename)
            self.status_lbl.text = ar(f"تم تصدير التقرير بنجاح")
            self.status_lbl.color = C['green']
            self._load_files() # تحديث القائمة
        except Exception as e:
            self.status_lbl.text = ar(f"خطأ: {str(e)}")
            self.status_lbl.color = C['red']

    def _open_file(self, filename):
        import subprocess
        import os
        if os.path.exists(filename):
            try:
                os.startfile(filename)
            except:
                subprocess.Popen(['explorer', filename], shell=True)

# ─── شريط التنقل ──────────────────────────────────────────
class BottomNav(BoxLayout):
    def __init__(self, on_change, **kw):
        super().__init__(orientation='horizontal',
                         size_hint_y=None, height=dp(66), **kw)
        self.on_change = on_change
        with self.canvas.before:
            Color(*C['nav'])
            self._bg = Rectangle(pos=self.pos, size=self.size)
            Color(*C['dim'])
            self._ln = Rectangle(pos=self.pos, size=(self.width, dp(1)))
        
        self.bind(pos=self._u, size=self._u)
        
        tabs = [
            ('home',   ar('الرئيسية')),
            ('report', ar('التقارير')),
        ]
        
        for key, lbl in tabs:
            tab_btn = Btn(text=lbl, bg=C['nav'], radius=0)
            tab_btn.bind(on_release=lambda inst, k=key: self.on_change(k))
            self.add_widget(tab_btn)

    def _u(self, *_):
        self._bg.pos=self.pos; self._bg.size=self.size
        self._ln.pos=self.pos; self._ln.size=(self.width, dp(1))

# ─── الحاوية الجذر ────────────────────────────────────────
class Root(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', **kw)
        self.area = BoxLayout(orientation='vertical', size_hint=(1,1))
        self.add_widget(self.area)
        self.add_widget(BottomNav(on_change=self._switch))
        self.current_screen = 'home'
        self._home()

    def go_back(self):
        """العودة الدائمة للصفحة الرئيسية إذا كنا في صفحة أخرى"""
        if hasattr(self, 'current_screen') and self.current_screen != 'home':
            self._switch('home')
            return True
        return False

    def _switch(self, screen):
        self.area.clear_widgets()
        self.current_screen = screen
        if screen == 'home':
            self.area.add_widget(HomeScreen(on_select=self._detail))
        elif screen == 'report':
            self.area.add_widget(ReportsScreen())

    def _home(self):
        self._switch('home')

    def _detail(self, cust):
        self.area.clear_widgets()
        self.current_screen = 'detail'
        self.area.add_widget(DetailScreen(customer=cust, on_back=self._home))

# ─── التطبيق ───────────────────────────────────────────────
class SupermarketApp(App):
    def build(self):
        self.title = 'سوبرماركت زعرب'
        
        # إنشاء التقرير التلقائي فقط في أول يوم من كل شهر (كجرد للشهر السابق)
        try:
            now = datetime.now()
            if now.day == 1:
                # إذا كان أول يوم في الشهر، نصدر تقرير بإحصائيات الشهر الذي انتهى للتو
                auto_filename = f"تقرير_تلقائي_شهر_{now.month-1 if now.month > 1 else 12}_{now.year}.xls"
                export_excel_file(auto_filename)
        except:
            pass
            
        self.root_widget = Root()
        Window.bind(on_keyboard=self.on_keyboard) # تفعيل التقاط زر العودة (المحلي للجوال)
        return self.root_widget
        
    def on_keyboard(self, window, key, *args):
        # الكود 27 يمثل زر الرجوع في الأندرويد أو الـ ESC في الويندوز
        if key == 27:
            if self.root_widget.go_back():
                return True # العودة خطوة للخلف بنجاح (عدم إغلاق التطبيق)
            return False # نحن في الواجهة الرئيسية، اغلق التطبيق

SupermarketApp().run()

