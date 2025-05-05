

import subprocess, time, pathlib, json, re, threading, contextlib, textwrap, sys
import yt_dlp, pyautogui, keyboard, http.cookiejar as cj

BASE         = pathlib.Path(__file__).parent
DL_DIR       = BASE / "downloads"
LINKS_FILE   = BASE / "reels_links.txt"

ADB_BIN      = r"C:\Users\YOUR_USER\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"
DEVICE       = "emulator-5574"                  # id z `adb devices`
TARGET_MP4   = "/sdcard/Movies/upload.mp4"      # katalog skanowany
DELAY_SEC    = 20                               # przerwa między postami
RESET_EVERY  = 5                                # restart Billin co X postów

COOKIE_JSON  = BASE / "cookies.json"
COOKIE_TXT   = BASE / "cookies.txt"

TAG_BLOCK = ("#fyp #foryou #foryoupage #viral #trending #trend #explorepage #explore #tiktokpolska #polska #motywacja #życie #sukces #pasja #marzenia #praca #cel #inspiracja #polishgirl #polishboy #humor #śmieszne #śmiesznefilmy #zabawa #przyjaźń #miłość #związek #lifestyle #dziennikżycia #życiejestpiękne #motywacjadodziałania #viralvideo #popularne #moda #uroda #beauty #fashion #style #ootd #makeup #makijaż #włosy #kosmetyki #kuchnia #jedzenie #przepis #gotowanie #gotujzmną #gotujesobiebardzo #przepisy #zdrowejedzenie #podróże #wakacje #relaks #muzyka #piosenka #hit #challenge #wyzwanie #dance #taniec #moves #sports #fitness #trening #treningwdomu #ćwiczenia #zdrowie #dieta #motywacjatreningowa #trenerpersonalny #samorozwój #mindset #psychologia #medytacja #wiedza #edukacja #nauka #szkoła #studia #studialife #student #uczsię #technologia #smartfony #gadżety #gry #gaming #gamer #gra #funny #funnyvideos #goodvibes #positivevibes #happy #happylife #goodmood #happymood #smile #laugh #śmiech #śmiesznememy #śmiesznezwierzaki #zwierzaki #kot #koty #pies #psy #animalsoftiktok #animalvideos #petsoftiktok #pets #cute #cutepets #sweet #kocham #kochamżycie #kochamzwierzaki #kochamkoty #kochampsy #kochammuzykę #kochamśpiewać #motywacjanadzień #codziennamotywacja #rozwojosobisty #praca #pracanasoba #inspiracjażyciowa #cytat #cytaty #cytatynadzis #myśli #przemyślenia #motywacyjne #nowetrendy #hot #gorące #rekord #nowość #ciekawe #poznajświat #światjestpiękny #podróżemałeiduże #zwiedzanie #relakswdomu #relaks #chill #chillout #relax #selflove #selfcare #dbajosiebie #selfimprovement #pozytywnemyśli #positiveenergy #dailyquote #quoteoftheday #dziennycytat #wiara #niepoddawajsie #walkaomarzenia #spełniajmarzenia #żyjpełniążycia #żyjchwilą #żyjtakjakchcesz #żyjmarzeniami #cele #ambicja #ambitnie #hustle #grind #workhard #nevergiveup #keepgoing #believeinyourself #successmindset #mindsetmatters #growthmindset #grow #prosper #achieve #achievements #goalsetter #dreambig #smallsteps #motivationquote #motywacjadotreningu #siłownia #gymmotivation #homeworkout #training #bodygoals #healthylifestyle #fitnessgirl #fitnessboy #workoutathome #fit #zdrowystylżycia #aktywnośćfizyczna #calisthenics #stretching #zdrowytrybżycia #zdroweodżywianie #aktywnywypoczynek #pieknezycie #kochamżycie #kochamdzien #goodenergy #bądźszczęśliwy #słuchamuzyki #muzykanażywo #muzykalna #wokal #śpiewam #śpiewanie #musiclover #musicislife #singer #nowamuzyka #tiktoktrend #tiktokhits #viralhit #viraltiktok #tiktokers #tiktokpl #tiktokpoland #tiktokpopularne #polishcreator #polishinfluencer #influencerlife #influencermarketing #youtuber #instagood #followme #likeforlikes #likeforfollow #likeforlikeback #subforsub #subscribe #followforfollowback #comment4comment #sfs #c4c #boostyouraccount #boostyourself #tiktokboost #boostfollowers #getfollowers #viralcontent #viralreels #viralshorts")

# --------------- WPISZ SWOJE KOORDYNATY ----------------------
XY = {
    "add"    : (1259, 1347),
    "post"   : (1255, 1248),
    "caption": (1163,  471),
    "video"  : (1336,  333),
    "thumb"  : (1163,  315),
    "back"   : (1174, 1292),
    "publish": (1418,   89),
}


ADB = [ADB_BIN, "-s", DEVICE]
def adb(*args, quiet=True):
    kw = {"stdout": subprocess.DEVNULL,
          "stderr": subprocess.STDOUT} if quiet else {}
    subprocess.check_call(ADB + list(args), **kw)

with contextlib.suppress(subprocess.CalledProcessError):
    subprocess.check_call([ADB_BIN, "connect", DEVICE],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

pyautogui.FAILSAFE = False
def tap(name, pause=0.8):
    x, y = XY[name]
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click(); time.sleep(pause)

def type_text(txt):
    for chunk in textwrap.wrap(txt, 900, break_long_words=False):
        pyautogui.write(chunk, interval=0.003); time.sleep(0.25)

# PU YOUR COOKIES IN cookies.txt file taken via EditThisCookie V3 Chrome Extension (OPTIONAL)
import time as tm
def json2netscape(src, dst):
    data = json.loads(src.read_text())
    jar  = cj.MozillaCookieJar(str(dst))
    for c in data:
        jar.set_cookie(cj.Cookie(
            0, c["name"], c["value"], None, False,
            c["domain"].lstrip("."), c["domain"].startswith("."),
            c["domain"].startswith("."), c["path"], False,
            c.get("secure", False),
            int(c.get("expirationDate", tm.time()+31536000)),
            int(c.get("expirationDate", tm.time()+31536000)),
            None, None, {}))
    jar.save()

def yt_cookies():
    if COOKIE_TXT.exists(): return {"cookiefile": str(COOKIE_TXT)}
    if COOKIE_JSON.exists():
        json2netscape(COOKIE_JSON, COOKIE_TXT)
        return {"cookiefile": str(COOKIE_TXT)}
    return {"cookiesfrombrowser": ("chrome",)}

LINK_RE = re.compile(r"https?://\S+")
def pop_link() -> str | None:
    if not LINKS_FILE.exists(): return None
    lines = [ln for ln in LINKS_FILE.read_text().splitlines() if ln.strip()]
    if not lines: return None
    url = lines[0].strip()
    LINKS_FILE.write_text("\n".join(lines[1:]))
    return url if LINK_RE.match(url) else None

def download(url: str) -> pathlib.Path:
    opts = {
        "outtmpl": str(DL_DIR / "temp.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "retries": 3,
        **yt_cookies(),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return next(DL_DIR.glob("temp*.mp4"))

#loop
def main():
    DL_DIR.mkdir(exist_ok=True)
    posted = 0
    while True:
        url = pop_link()
        if not url:
            time.sleep(4); continue
        try:
            print("[DL]", url)
            mp4 = download(url)
        except Exception as e:
            print("[DL‑ERR]", e); time.sleep(5); continue

# push + MediaScanner
        try:
            adb("push", str(mp4), TARGET_MP4, quiet=False)
            adb("shell", "am", "broadcast", "-a",
                "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d", f"file://{TARGET_MP4}")
            print("[PUSH]", mp4.name, "-> upload.mp4")
        except subprocess.CalledProcessError as e:
            print("[ADB‑ERR]", e); mp4.unlink(missing_ok=True); continue

# GUI
        try:
            adb("shell", "am", "start", "-n", "com.billin/.MainActivity"); time.sleep(1.5)
            tap("add"); tap("post")
            tap("caption",0.5); type_text(TAG_BLOCK)
            tap("video"); tap("thumb"); tap("back")
            tap("publish", 5)
            posted += 1
        except Exception as e:
            print("[POST‑ERR]", e)

        mp4.unlink(missing_ok=True)

# restart Billin every X Posts
        if posted and posted % RESET_EVERY == 0:
            print(f"[RESET] Restartuję Billin (po {posted} postach)")
            adb("shell", "am", "force-stop", "com.billin")
            adb("shell", "am", "start", "-n", "com.billin/.MainActivity")
            time.sleep(3)

        # przerwa
        for _ in range(DELAY_SEC):
            time.sleep(1)

# launch
if __name__ == "__main__":
    try:
        subprocess.check_call([ADB_BIN, "--version"], stdout=subprocess.DEVNULL)
    except Exception:
        print("❌ Nie znaleziono adb.exe – sprawdź ADB_BIN."); sys.exit(1)

    print("BOT 1×1 działa – F1 = stop.")
    t = threading.Thread(target=main, daemon=True); t.start()
    keyboard.wait("f1"); print("Kończę…")
