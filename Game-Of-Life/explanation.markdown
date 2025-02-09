# توضیحات کد  

این کد به بررسی کد C++ ارائه شده می‌پردازد که شامل **شبیه‌سازی تغییرات ماتریس** و **الگوریتم BFS** برای یافتن کوتاه‌ترین مسیر است.  

---

## بخش ۱: تغییرات ماتریس ( گیم آف لایف)

### ۱. **مشخصات ماتریس**
- ابعاد ماتریس: ۱۰ سطر (`ROWS = 10`) و ۱۵ ستون (`COLS = 15`).
- دو ماتریس موازی:
  - `jad[][]`: ذخیره کاراکترهای `@` (خانه زنده) و `#` (خانه مرده).
  - `val[][]`: ذخیره مقادیر عددی `0` یا `1` متناظر با `jad`.

### ۲. **مراحل اجرا**
۱. **دریافت ورودی اولیه**:  
   - کاربر ماتریس اولیه `jad` را وارد می‌کند.
   - مقادیر `val` بر اساس کاراکترها تنظیم می‌شود:
     - `@` → `1`
     - `#` → `0`.

۲. **به‌روزرسانی در ۳ مرحله**:  
   - در هر مرحله، مقدار هر خانه با توجه به **تعداد همسایه‌های زنده** محاسبه می‌شود:
     - همسایه‌ها: چهار خانه مجاور (بالا، پایین، چپ، راست).
     - شرط به‌روزرسانی:
       - اگر تعداد همسایه‌های زنده **بیشتر از ۱** باشد → سلول زنده (`1`).
       - در غیر این صورت → خانه مرده (`0`).
   - ماتریس `jad` با کاراکترهای `@` و `#` به‌روزرسانی می‌شود.

۳. **نمایش مراحل**:  
   - پس از هر مرحله، ماتریس چاپ می‌شود.
   - مکث ۲ ثانیه بین مراحل (`this_thread::sleep_for`).
   - پاک کردن صفحه کنسول (`system("cls")`) به جز در مرحله آخر.

---

## بخش ۲: الگوریتم BFS برای یافتن مسیر

### ۱. **آماده‌سازی داده‌ها**
- ماتریس `grid` از `jad` کپی می‌شود.
- دریافت مختصات شروع (`startRow`, `startCol`) و پایان (`endRow`, `endCol`).

### ۲. **اجرای BFS**
- **ساختارهای داده**:  
  - `queue[][]`: صف برای ذخیره مختصات خانه های در حال پردازش.
  - `visited[][]`: علامت‌گذاری خانه های بازدیدشده.
  - `parent[][]`: ذخیره والد هر خانه برای بازسازی مسیر.

- **مراحل**:  
  ۱. نقطه شروع به صف اضافه و `visited` علامت‌گذاری می‌شود.  
  ۲. تا زمانی که صف خالی نشده یا مقصد پیدا نشده:  
     - خانه فعلی از ابتدای صف حذف می‌شود.  
     - چهار خانه مجاور (بالا، پایین، چپ، راست) بررسی می‌شوند:  
       - اگر خانه مجاور **در محدوده ماتریس**، **بازدیدنشده**، و **قابل عبور** (`#`) باشد → به صف اضافه می‌شود.  
       - اگر خانه مجاور، نقطه پایان باشد → حلقه متوقف می‌شود.

### ۳. **بازسازی مسیر**
- اگر مسیر وجود داشته باشد:  
  - مسیر از نقطه پایان به شروع با استفاده از `parent[][]` بازسازی می‌شود.  
  - مسیر در قالب `(row, col) -> ...` چاپ می‌شود.  
  - سلول‌های مسیر در ماتریس با `*` نمایش داده می‌شوند.  
- اگر مسیر وجود نداشته باشد → پیام خطا نمایش داده می‌شود.

---

## نمونه خروجی

### شبیه‌سازی ماتریس (مرحله اول):

@ # @ # @ ...

. # @ # @ # ...


### مسیر یافت شده:

Path from start to end:  
(1,1) -> (1,2) -> (2,2)

- # * # ...
    

.   * # @ ...


---

## محدودیت‌ها
- **اندازه ثابت ماتریس**: ابعاد ماتریس قابل تغییر نیست.
- **حرکت چهارجهته**: حرکت مورب پشتیبانی نمی‌شود.
- **کاراکترهای مجاز**: فقط `@` و `#` پذیرفته می‌شوند.
- **حافظه صف**: استفاده از آرایه ایستا ممکن است برای ماتریس‌های بزرگتر مشکل ایجاد کند.

---

این کد برای شبیه‌سازی ساده **تغییرات ماتریس ** (Game Of Life)و **یافتن مسیر(BFS) در گریدهای گسسته** طراحی شده است.

