import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import difflib
from datetime import date

from environment.trading_env import TradingEnvironment
from agent.q_learning_agent import QLearningAgent

# ===============================================================
# MASTER STOCK DATABASE  (name → yfinance ticker)
# ===============================================================
STOCK_DB = {
    # ── NSE Large Cap ──────────────────────────────────────────
    "RELIANCE": "RELIANCE.NS",
    "RELIANCE INDUSTRIES": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "TATA CONSULTANCY SERVICES": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "INFY": "INFY.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "STATE BANK OF INDIA": "SBIN.NS",
    "SBI": "SBIN.NS",
    "SBIN": "SBIN.NS",
    "BAJAJ FINANCE": "BAJFINANCE.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "BHARTI AIRTEL": "BHARTIARTL.NS",
    "AIRTEL": "BHARTIARTL.NS",
    "BHARTIARTL": "BHARTIARTL.NS",
    "WIPRO": "WIPRO.NS",
    "HCL TECHNOLOGIES": "HCLTECH.NS",
    "HCL TECH": "HCLTECH.NS",
    "HCL": "HCLTECH.NS",
    "HCLTECH": "HCLTECH.NS",
    "ASIAN PAINTS": "ASIANPAINT.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "MARUTI SUZUKI": "MARUTI.NS",
    "MARUTI": "MARUTI.NS",
    "ULTRATECH CEMENT": "ULTRACEMCO.NS",
    "ULTRACEMCO": "ULTRACEMCO.NS",
    "TITAN": "TITAN.NS",
    "TITAN COMPANY": "TITAN.NS",
    "NESTLE INDIA": "NESTLEIND.NS",
    "NESTLE": "NESTLEIND.NS",
    "NESTLEIND": "NESTLEIND.NS",
    "KOTAK MAHINDRA BANK": "KOTAKBANK.NS",
    "KOTAK BANK": "KOTAKBANK.NS",
    "KOTAKBANK": "KOTAKBANK.NS",
    "AXIS BANK": "AXISBANK.NS",
    "AXISBANK": "AXISBANK.NS",
    "LARSEN AND TOUBRO": "LT.NS",
    "L&T": "LT.NS",
    "LT": "LT.NS",
    "MAHINDRA AND MAHINDRA": "M&M.NS",
    "M&M": "M&M.NS",
    "MAHINDRA": "M&M.NS",
    "SUN PHARMA": "SUNPHARMA.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    "SUN PHARMACEUTICAL": "SUNPHARMA.NS",
    "BAJAJ AUTO": "BAJAJ-AUTO.NS",
    "HERO MOTOCORP": "HEROMOTOCO.NS",
    "HERO MOTO": "HEROMOTOCO.NS",
    "HEROMOTOCO": "HEROMOTOCO.NS",
    "TATA MOTORS": "TATAMOTORS.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "TATA STEEL": "TATASTEEL.NS",
    "TATASTEEL": "TATASTEEL.NS",
    "HINDALCO": "HINDALCO.NS",
    "HINDALCO INDUSTRIES": "HINDALCO.NS",
    "POWER GRID": "POWERGRID.NS",
    "POWERGRID": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "ONGC": "ONGC.NS",
    "OIL AND NATURAL GAS": "ONGC.NS",
    "COAL INDIA": "COALINDIA.NS",
    "COALINDIA": "COALINDIA.NS",
    "JSWSTEEL": "JSWSTEEL.NS",
    "JSW STEEL": "JSWSTEEL.NS",
    "ADANI ENTERPRISES": "ADANIENT.NS",
    "ADANIENT": "ADANIENT.NS",
    "ADANI PORTS": "ADANIPORTS.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "ADANI GREEN": "ADANIGREEN.NS",
    "ADANIGREEN": "ADANIGREEN.NS",
    "ADANI POWER": "ADANIPOWER.NS",
    "ADANIPOWER": "ADANIPOWER.NS",
    "ADANI TOTAL GAS": "ATGL.NS",
    "ATGL": "ATGL.NS",
    "VEDANTA": "VEDL.NS",
    "VEDL": "VEDL.NS",
    "GRASIM": "GRASIM.NS",
    "GRASIM INDUSTRIES": "GRASIM.NS",
    "CIPLA": "CIPLA.NS",
    "DR REDDY": "DRREDDY.NS",
    "DR REDDYS": "DRREDDY.NS",
    "DRREDDY": "DRREDDY.NS",
    "DIVIS LABS": "DIVISLAB.NS",
    "DIVISLAB": "DIVISLAB.NS",
    "BRITANNIA": "BRITANNIA.NS",
    "EICHER MOTORS": "EICHERMOT.NS",
    "EICHERMOT": "EICHERMOT.NS",
    "ROYAL ENFIELD": "EICHERMOT.NS",
    "BAJAJ FINSERV": "BAJAJFINSV.NS",
    "BAJAJFINSV": "BAJAJFINSV.NS",
    "SHRIRAM FINANCE": "SHRIRAMFIN.NS",
    "SHRIRAMFIN": "SHRIRAMFIN.NS",
    "TECH MAHINDRA": "TECHM.NS",
    "TECHM": "TECHM.NS",
    "HAVELLS": "HAVELLS.NS",
    "HAVELLS INDIA": "HAVELLS.NS",
    "SIEMENS": "SIEMENS.NS",
    "ABB INDIA": "ABB.NS",
    "ABB": "ABB.NS",
    "PIDILITE": "PIDILITIND.NS",
    "PIDILITE INDUSTRIES": "PIDILITIND.NS",
    "PIDILITIND": "PIDILITIND.NS",
    "GODREJ CONSUMER": "GODREJCP.NS",
    "GODREJCP": "GODREJCP.NS",
    "HINDUSTAN UNILEVER": "HINDUNILVR.NS",
    "HUL": "HINDUNILVR.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "TATA CONSUMER": "TATACONSUM.NS",
    "TATACONSUM": "TATACONSUM.NS",
    "INDUSIND BANK": "INDUSINDBK.NS",
    "INDUSINDBK": "INDUSINDBK.NS",
    "FEDERAL BANK": "FEDERALBNK.NS",
    "FEDERALBNK": "FEDERALBNK.NS",
    "BANK OF BARODA": "BANKBARODA.NS",
    "BANKBARODA": "BANKBARODA.NS",
    "BOB": "BANKBARODA.NS",
    "CANARA BANK": "CANBK.NS",
    "CANBK": "CANBK.NS",
    "PUNJAB NATIONAL BANK": "PNB.NS",
    "PNB": "PNB.NS",
    "UNION BANK": "UNIONBANK.NS",
    "UNIONBANK": "UNIONBANK.NS",

    # ── Mid Cap ────────────────────────────────────────────────
    "IRFC": "IRFC.NS",
    "INDIAN RAILWAY FINANCE": "IRFC.NS",
    "IRCTC": "IRCTC.NS",
    "INDIAN RAILWAY CATERING": "IRCTC.NS",
    "HAL": "HAL.NS",
    "HINDUSTAN AERONAUTICS": "HAL.NS",
    "BEL": "BEL.NS",
    "BHARAT ELECTRONICS": "BEL.NS",
    "BHEL": "BHEL.NS",
    "BHARAT HEAVY ELECTRICALS": "BHEL.NS",
    "GAIL": "GAIL.NS",
    "GAIL INDIA": "GAIL.NS",
    "IOC": "IOC.NS",
    "INDIAN OIL": "IOC.NS",
    "INDIAN OIL CORPORATION": "IOC.NS",
    "BPCL": "BPCL.NS",
    "BHARAT PETROLEUM": "BPCL.NS",
    "HPCL": "HPCL.NS",
    "HINDUSTAN PETROLEUM": "HPCL.NS",
    "NMDC": "NMDC.NS",
    "SAIL": "SAIL.NS",
    "STEEL AUTHORITY": "SAIL.NS",
    "REC": "RECLTD.NS",
    "RECLTD": "RECLTD.NS",
    "PFC": "PFC.NS",
    "POWER FINANCE": "PFC.NS",
    "IREDA": "IREDA.NS",
    "RVNL": "RVNL.NS",
    "RAIL VIKAS NIGAM": "RVNL.NS",
    "CONCOR": "CONCOR.NS",
    "CONTAINER CORPORATION": "CONCOR.NS",
    "MUTHOOT FINANCE": "MUTHOOTFIN.NS",
    "MUTHOOTFIN": "MUTHOOTFIN.NS",
    "MANAPPURAM": "MANAPPURAM.NS",
    "CHOLAFIN": "CHOLAFIN.NS",
    "CHOLA FINANCE": "CHOLAFIN.NS",
    "L&T FINANCE": "LTF.NS",
    "LTF": "LTF.NS",
    "VOLTAS": "VOLTAS.NS",
    "CROMPTON": "CROMPTON.NS",
    "POLYCAB": "POLYCAB.NS",
    "DIXON TECHNOLOGIES": "DIXON.NS",
    "DIXON": "DIXON.NS",
    "TRENT": "TRENT.NS",
    "AVENUE SUPERMARTS": "DMART.NS",
    "DMART": "DMART.NS",
    "ZOMATO": "ZOMATO.NS",
    "SWIGGY": "SWIGGY.NS",
    "NYKAA": "NYKAA.NS",
    "FSN ECOMMERCE": "NYKAA.NS",
    "PAYTM": "PAYTM.NS",
    "POLICYBAZAAR": "POLICYBZR.NS",
    "POLICYBZR": "POLICYBZR.NS",
    "TATA ELXSI": "TATAELXSI.NS",
    "TATAELXSI": "TATAELXSI.NS",
    "MPHASIS": "MPHASIS.NS",
    "PERSISTENT": "PERSISTENT.NS",
    "PERSISTENT SYSTEMS": "PERSISTENT.NS",
    "COFORGE": "COFORGE.NS",
    "LTIMINDTREE": "LTIM.NS",
    "LTIM": "LTIM.NS",
    "LTI MINDTREE": "LTIM.NS",
    "CYIENT": "CYIENT.NS",
    "KPIT TECHNOLOGIES": "KPITTECH.NS",
    "KPITTECH": "KPITTECH.NS",
    "TATA POWER": "TATAPOWER.NS",
    "TATAPOWER": "TATAPOWER.NS",
    "CESC": "CESC.NS",
    "JSW ENERGY": "JSWENERGY.NS",
    "JSWENERGY": "JSWENERGY.NS",
    "TORRENT POWER": "TORNTPOWER.NS",
    "TORNTPOWER": "TORNTPOWER.NS",
    "SUZLON": "SUZLON.NS",
    "SUZLON ENERGY": "SUZLON.NS",
    "INOX WIND": "INOXWIND.NS",
    "INOXWIND": "INOXWIND.NS",
    "DLF": "DLF.NS",
    "OBEROI REALTY": "OBEROIRLTY.NS",
    "GODREJ PROPERTIES": "GODREJPROP.NS",
    "GODREJPROP": "GODREJPROP.NS",
    "PRESTIGE ESTATES": "PRESTIGE.NS",
    "BRIGADE ENTERPRISES": "BRIGADE.NS",
    "SOBHA": "SOBHA.NS",
    "SRF": "SRF.NS",
    "PI INDUSTRIES": "PIIND.NS",
    "PIIND": "PIIND.NS",
    "UPL": "UPL.NS",
    "COROMANDEL": "COROMANDEL.NS",
    "CHAMBAL FERTILISERS": "CHAMBLFERT.NS",
    "CHAMBLFERT": "CHAMBLFERT.NS",
    "DEEPAK NITRITE": "DEEPAKNTR.NS",
    "DEEPAKNTR": "DEEPAKNTR.NS",
    "NAVIN FLUORINE": "NAVINFLUOR.NS",
    "NAVINFLUOR": "NAVINFLUOR.NS",
    "ASTRAL": "ASTRAL.NS",
    "ASTRAL POLY": "ASTRAL.NS",
    "SUPREME INDUSTRIES": "SUPREMEIND.NS",
    "SUPREMEIND": "SUPREMEIND.NS",
    "KEI INDUSTRIES": "KEI.NS",
    "KEI": "KEI.NS",
    "V-GUARD": "VGUARD.NS",
    "VGUARD": "VGUARD.NS",
    "BHARAT FORGE": "BHARATFORG.NS",
    "BHARATFORG": "BHARATFORG.NS",
    "MOTHERSON": "MOTHERSON.NS",
    "MINDA INDUSTRIES": "MINDAIND.NS",
    "BALKRISHNA INDUSTRIES": "BALKRISIND.NS",
    "BALKRISIND": "BALKRISIND.NS",
    "APOLLO TYRES": "APOLLOTYRE.NS",
    "APOLLOTYRE": "APOLLOTYRE.NS",
    "MRF": "MRF.NS",
    "CEAT": "CEATLTD.NS",
    "CEATLTD": "CEATLTD.NS",
    "TVS MOTORS": "TVSMOTOR.NS",
    "TVS MOTOR": "TVSMOTOR.NS",
    "TVSMOTOR": "TVSMOTOR.NS",
    "ESCORTS": "ESCORTS.NS",
    "SONA BLW": "SONACOMS.NS",
    "SONACOMS": "SONACOMS.NS",
    "AARTI INDUSTRIES": "AARTIIND.NS",
    "AARTIIND": "AARTIIND.NS",
    "JUBILANT FOODWORKS": "JUBLFOOD.NS",
    "JUBLFOOD": "JUBLFOOD.NS",
    "DOMINOS": "JUBLFOOD.NS",
    "DEVYANI INTERNATIONAL": "DEVYANI.NS",
    "WESTLIFE FOODWORLD": "WESTLIFE.NS",
    "PAGE INDUSTRIES": "PAGEIND.NS",
    "PAGEIND": "PAGEIND.NS",
    "JOCKEY": "PAGEIND.NS",
    "VEDANT FASHIONS": "MANYAVAR.NS",
    "MANYAVAR": "MANYAVAR.NS",
    "RAYMOND": "RAYMOND.NS",
    "ADITYA BIRLA FASHION": "ABFRL.NS",
    "ABFRL": "ABFRL.NS",
    "EMAMI": "EMAMILTD.NS",
    "EMAMILTD": "EMAMILTD.NS",
    "MARICO": "MARICO.NS",
    "DABUR": "DABUR.NS",
    "COLGATE": "COLPAL.NS",
    "COLPAL": "COLPAL.NS",
    "HINDUSTAN ZINC": "HINDZINC.NS",
    "HINDZINC": "HINDZINC.NS",
    "MONOTYPE INDIA": "MONO.NS",
    "MONOTYPE": "MONO.NS",
    "MONO": "MONO.NS",

    # ── US Stocks ──────────────────────────────────────────────
    "APPLE": "AAPL",
    "AAPL": "AAPL",
    "MICROSOFT": "MSFT",
    "MSFT": "MSFT",
    "GOOGLE": "GOOGL",
    "ALPHABET": "GOOGL",
    "GOOGL": "GOOGL",
    "AMAZON": "AMZN",
    "AMZN": "AMZN",
    "META": "META",
    "FACEBOOK": "META",
    "NVIDIA": "NVDA",
    "NVDA": "NVDA",
    "TESLA": "TSLA",
    "TSLA": "TSLA",
    "NETFLIX": "NFLX",
    "NFLX": "NFLX",
    "AMD": "AMD",
    "INTEL": "INTC",
    "INTC": "INTC",
    "QUALCOMM": "QCOM",
    "QCOM": "QCOM",
    "BROADCOM": "AVGO",
    "AVGO": "AVGO",
    "SALESFORCE": "CRM",
    "CRM": "CRM",
    "ORACLE": "ORCL",
    "ORCL": "ORCL",
    "IBM": "IBM",
    "PALANTIR": "PLTR",
    "PLTR": "PLTR",
    "SNOWFLAKE": "SNOW",
    "SNOW": "SNOW",
    "COINBASE": "COIN",
    "COIN": "COIN",
    "SHOPIFY": "SHOP",
    "SHOP": "SHOP",
    "UBER": "UBER",
    "LYFT": "LYFT",
    "AIRBNB": "ABNB",
    "ABNB": "ABNB",
    "SPOTIFY": "SPOT",
    "SPOT": "SPOT",
    "JPMORGAN": "JPM",
    "JPM": "JPM",
    "GOLDMAN SACHS": "GS",
    "GS": "GS",
    "VISA": "V",
    "MASTERCARD": "MA",
    "PAYPAL": "PYPL",
    "PYPL": "PYPL",
    "JOHNSON AND JOHNSON": "JNJ",
    "J&J": "JNJ",
    "JNJ": "JNJ",
    "PFIZER": "PFE",
    "PFE": "PFE",
    "MODERNA": "MRNA",
    "MRNA": "MRNA",
    "BERKSHIRE HATHAWAY": "BRK-B",
    "BERKSHIRE": "BRK-B",
    "WALMART": "WMT",
    "WMT": "WMT",
    "COSTCO": "COST",
    "COST": "COST",
    "DISNEY": "DIS",
    "DIS": "DIS",
    "BOEING": "BA",
    "BA": "BA",
    "EXXON": "XOM",
    "XOM": "XOM",
    "CHEVRON": "CVX",
    "CVX": "CVX",
}

_ALL_NAMES = list(STOCK_DB.keys())


# ===============================================================
# SMART TICKER RESOLVER
# ===============================================================
def _fuzzy_match(query: str, cutoff: float = 0.55):
    matches = difflib.get_close_matches(query, _ALL_NAMES, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def _validate_ticker(ticker: str) -> bool:
    try:
        info = yf.Ticker(ticker).fast_info
        return hasattr(info, "last_price") and info.last_price is not None
    except Exception:
        return False


def resolve_ticker(raw_input: str):
    """
    Returns (ticker, method) using 5-step cascade:
      1. Exact DB match  (case-insensitive)
      2. Fuzzy DB match  (typo tolerance)
      3. Raw input validated directly via yfinance
      4. Auto-append .NS  (NSE)
      5. Auto-append .BO  (BSE)
    """
    query = raw_input.upper().strip()

    if query in STOCK_DB:
        return STOCK_DB[query], "exact"

    best = _fuzzy_match(query)
    if best:
        return STOCK_DB[best], f"fuzzy → {best.title()}"

    if _validate_ticker(query):
        return query, "direct"

    nse = query + ".NS"
    if _validate_ticker(nse):
        return nse, "auto-NSE"

    bse = query + ".BO"
    if _validate_ticker(bse):
        return bse, "auto-BSE"

    return query, "unresolved"


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI-Based Stock Trading Decision System",
    layout="wide"
)

st.title("📈 AI-Based Stock Trading Decision System")

# ===============================
# USER INPUT
# ===============================
st.subheader("🔎 Select Stock")

raw_input = st.text_input(
    "Enter Stock Name or Ticker",
    placeholder="e.g. HCL Technologies, Zomato, IRFC, Monotype India, AAPL, Tesla...",
    value=""
)

if not raw_input.strip():
    st.info("💡 Type any stock name — Indian (NSE/BSE) or Global. Typos & case don't matter!")
    st.stop()

# ── Resolve Ticker ──────────────────────────────────────────────
with st.spinner("🔍 Resolving stock ticker..."):
    ticker, method = resolve_ticker(raw_input)

col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Resolved Ticker", ticker)
with col2:
    if method == "exact":
        st.success("✅ Exact match found in database")
    elif method.startswith("fuzzy"):
        st.info(f"🔄 Auto-corrected to: **{method.split('→')[-1].strip()}**")
    elif method == "auto-NSE":
        st.success("🟢 Auto-detected as NSE stock")
    elif method == "auto-BSE":
        st.warning("🟡 Auto-detected as BSE stock")
    elif method == "direct":
        st.success("✅ Ticker validated directly")
    else:
        st.error("❌ Could not resolve this stock")

if method == "unresolved":
    st.error(
        f"❌ Could not find data for **{raw_input}**.\n\n"
        "**Tips:**\n"
        "- Indian stocks: `Zomato`, `IRFC`, `Tata Steel`, `Monotype India`\n"
        "- US stocks: `Apple`, `Tesla`, `NVIDIA`\n"
        "- Or paste the ticker directly: `MONO.NS`, `AAPL`, `RELIANCE.NS`"
    )
    st.stop()

# ===============================
# DATE RANGE FILTER
# ===============================
st.subheader("📅 Select Time Range")

col_s, col_e = st.columns(2)
with col_s:
    start_date = st.date_input("Start Date", value=date(2020, 1, 1))
with col_e:
    end_date = st.date_input("End Date", value=date(2024, 1, 1))

if start_date >= end_date:
    st.error("⚠️ Start date must be before end date.")
    st.stop()

# ===============================
# DATA LOADING
# ===============================
@st.cache_data(show_spinner=False)
def load_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if df is None or df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    if "Close" not in df.columns:
        return None

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Close"]).reset_index(drop=True)
    return df


with st.spinner(f"📡 Fetching data for **{ticker}**..."):
    data = load_stock_data(ticker, start_date, end_date)

if data is None or data.empty:
    st.error(
        f"❌ No historical data found for **{ticker}** in the selected range.\n\n"
        "Try a wider date range or verify the ticker symbol."
    )
    st.stop()

os.makedirs("data", exist_ok=True)
data.to_csv("data/temp_stock.csv", index=False)

# ===============================
# STOCK SUMMARY METRICS
# ===============================
latest_close = data["Close"].iloc[-1]
first_close  = data["Close"].iloc[0]
pct_change   = ((latest_close - first_close) / first_close) * 100
high         = data["High"].max() if "High" in data.columns else data["Close"].max()
currency     = "₹" if (".NS" in ticker or ".BO" in ticker) else "$"

st.subheader(f"📊 {raw_input.title()} — Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Latest Close",  f"{currency}{latest_close:,.2f}")
m2.metric("Period Change", f"{pct_change:+.1f}%", delta=f"{pct_change:+.1f}%")
m3.metric("Period High",   f"{currency}{high:,.2f}")
m4.metric("Data Points",   f"{len(data)} days")

# ===============================
# STOCK PRICE CHART
# ===============================
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(data["Close"], color="dodgerblue", linewidth=1.5)
ax.fill_between(data.index, data["Close"], alpha=0.08, color="dodgerblue")
ax.set_xlabel("Days")
ax.set_ylabel(f"Closing Price ({currency})")
ax.set_title(f"{raw_input.title()} ({ticker})  •  {start_date} → {end_date}")
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# ===============================
# AI TRAINING
# ===============================
st.subheader("🤖 AI Trading Simulation")

episodes = st.slider("Training Episodes", 5, 50, 10)

if st.button("▶️ Run AI Training", type="primary"):

    env     = TradingEnvironment("data/temp_stock.csv")
    agent   = QLearningAgent(actions=[0, 1, 2])   # 0=Hold  1=Buy  2=Sell
    profits = []

    progress_bar = st.progress(0, text="Training in progress…")

    for ep in range(episodes):
        state        = env.reset()
        total_reward = 0

        while True:
            action                   = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            state        = next_state
            total_reward += reward
            if done:
                profits.append(total_reward)
                break

        progress_bar.progress((ep + 1) / episodes, text=f"Episode {ep + 1}/{episodes}")

    progress_bar.empty()
    st.success("✅ AI Training Completed!")

    # ── Profit Graph ───────────────────────────────────────────
    st.subheader("📈 Profit per Episode")

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    colors = ["green" if p > 0 else "red" for p in profits]
    ax2.bar(range(1, episodes + 1), profits, color=colors, alpha=0.8)
    ax2.axhline(0, color="white", linestyle="--", linewidth=0.8)
    ax2.plot(range(1, episodes + 1), profits, marker="o", color="yellow", linewidth=1.2, markersize=4)
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Profit")
    ax2.set_title("Q-Learning Performance across Episodes")
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

    # ── Stats Table ────────────────────────────────────────────
    st.subheader("📌 Episode-wise Summary")
    profit_df = pd.DataFrame({
        "Episode": range(1, episodes + 1),
        "Profit":  [round(p, 2) for p in profits],
        "Result":  ["✅ Profit" if p > 0 else "🔴 Loss" for p in profits]
    })
    st.dataframe(profit_df, use_container_width=True, hide_index=True)

    # ── Final Decision ─────────────────────────────────────────
    last_profit = profits[-1]
    avg_profit  = sum(profits) / len(profits)
    win_rate    = sum(1 for p in profits if p > 0) / len(profits) * 100

    if avg_profit > 0 and win_rate >= 50:
        decision   = "✅ BUY / HOLD"
        confidence = "High"
    elif avg_profit > 0:
        decision   = "⚠️ HOLD"
        confidence = "Medium"
    else:
        decision   = "🔴 AVOID / SELL"
        confidence = "Low"

    st.subheader("🧠 AI Decision Summary")

    r1, r2, r3 = st.columns(3)
    r1.metric("Last Episode Profit", round(last_profit, 2))
    r2.metric("Avg Profit",          round(avg_profit, 2))
    r3.metric("Win Rate",            f"{win_rate:.0f}%")

    st.markdown(f"""
    | Field              | Value                         |
    |--------------------|-------------------------------|
    | **Stock**          | {raw_input.title()}           |
    | **Ticker**         | `{ticker}`                    |
    | **Time Range**     | {start_date} → {end_date}     |
    | **Recommendation** | {decision}                    |
    | **Confidence**     | {confidence}                  |
    """)