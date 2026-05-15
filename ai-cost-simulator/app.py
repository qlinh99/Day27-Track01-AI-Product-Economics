import streamlit as st
import pandas as pd

# =========================================================
# AI Conversation Cost Simulator
# This app does NOT call any real LLM API.
# It simulates cost based on token estimates and model prices.
# =========================================================

MODEL_PRICING = {
    "Gemini 2.5 Flash-Lite": {"input": 0.10, "output": 0.40},
    "GPT-4o-mini": {"input": 0.15, "output": 0.60},
    "Gemini 2.5 Flash": {"input": 0.30, "output": 2.50},
    "DeepSeek V4 Pro": {"input": 1.74, "output": 3.48},
    "Claude Sonnet 4.6": {"input": 3.00, "output": 15.00},
    "GPT-5.5": {"input": 5.00, "output": 30.00},
}

CONFIGS = {
    "Budget Bot": {
        "model": "Gemini 2.5 Flash-Lite",
        "web_mode": "OFF",
        "history": "Last 3",
        "classifier": "Keyword",
        "quality": "Low-Medium",
        "best_for": "Low season, simple FAQ, cost saving",
    },
    "Smart Mix": {
        "model": "GPT-4o-mini",
        "web_mode": "Selective: Visa + Weather",
        "history": "Last 5",
        "classifier": "LLM",
        "quality": "Medium-High",
        "best_for": "Balanced cost and quality",
    },
    "Premium Concierge": {
        "model": "GPT-5.5",
        "web_mode": "Broad: Guide + Visa + Weather",
        "history": "Full",
        "classifier": "LLM",
        "quality": "High",
        "best_for": "VIP customers, high-value bookings",
    },
}

SCENARIOS = {
    "Scenario A — Low season": {
        "conversations_per_day": 300,
        "turns": 4,
        "intent_mix": {
            "Guide": 0.50,
            "Visa": 0.25,
            "Weather": 0.10,
            "Booking": 0.10,
            "Complaint": 0.05,
        },
    },
    "Scenario B — High season": {
        "conversations_per_day": 1200,
        "turns": 7,
        "intent_mix": {
            "Guide": 0.30,
            "Visa": 0.15,
            "Weather": 0.10,
            "Booking": 0.35,
            "Complaint": 0.10,
        },
    },
}

TOKEN_CONSTANTS = {
    "system_prompt": 500,
    "user_message": 80,
    "assistant_output": 180,
    "prior_turn_history": 260,
    "rag_chunks": 1250,
    "web_results": 800,
    "classifier_input": 150,
    "classifier_output": 20,
}

WEB_API_COST = 0.008
HUMAN_BASELINE_PER_CONV = 0.50


def money(value: float, decimals: int = 4) -> str:
    return f"${value:,.{decimals}f}"


def get_history_tokens(turn: int, history_strategy: str) -> int:
    if history_strategy == "Full":
        return (turn - 1) * TOKEN_CONSTANTS["prior_turn_history"]
    if history_strategy == "Last 3":
        return min(turn - 1, 3) * TOKEN_CONSTANTS["prior_turn_history"]
    if history_strategy == "Last 5":
        return min(turn - 1, 5) * TOKEN_CONSTANTS["prior_turn_history"]
    if history_strategy == "Summarize":
        return 150
    return 0


def should_use_web(intent: str, web_mode: str) -> bool:
    if web_mode == "OFF":
        return False
    if web_mode == "Selective: Visa + Weather":
        return intent in ["Visa", "Weather"]
    if web_mode == "Broad: Guide + Visa + Weather":
        return intent in ["Guide", "Visa", "Weather"]
    return False


def calculate_classifier_cost(classifier: str, input_price: float, output_price: float) -> float:
    if classifier == "Keyword":
        return 0.0

    return (
        TOKEN_CONSTANTS["classifier_input"] * input_price
        + TOKEN_CONSTANTS["classifier_output"] * output_price
    ) / 1_000_000


def calculate_turn_cost(
    turn: int,
    intent: str,
    model_name: str,
    web_mode: str,
    history_strategy: str,
    classifier: str,
) -> dict:
    prices = MODEL_PRICING[model_name]
    input_price = prices["input"]
    output_price = prices["output"]

    classifier_cost = calculate_classifier_cost(classifier, input_price, output_price)

    # Booking and Complaint are handed off/escalated.
    # They only need intent classification, not full LLM generation.
    if intent in ["Booking", "Complaint"]:
        return {
            "Turn": 1,
            "Intent": intent,
            "History tokens": 0,
            "RAG tokens": 0,
            "Web tokens": 0,
            "Input tokens": 0,
            "Output tokens": 0,
            "Model cost": 0.0,
            "Web cost": 0.0,
            "Classifier cost": classifier_cost,
            "Total turn cost": classifier_cost,
        }

    history_tokens = get_history_tokens(turn, history_strategy)
    rag_tokens = TOKEN_CONSTANTS["rag_chunks"]
    web_enabled = should_use_web(intent, web_mode)
    web_tokens = TOKEN_CONSTANTS["web_results"] if web_enabled else 0
    web_cost = WEB_API_COST if web_enabled else 0.0

    input_tokens = (
        TOKEN_CONSTANTS["system_prompt"]
        + TOKEN_CONSTANTS["user_message"]
        + rag_tokens
        + history_tokens
        + web_tokens
    )
    output_tokens = TOKEN_CONSTANTS["assistant_output"]

    model_cost = (
        input_tokens * input_price + output_tokens * output_price
    ) / 1_000_000

    total_cost = model_cost + web_cost + classifier_cost

    return {
        "Turn": turn,
        "Intent": intent,
        "History tokens": history_tokens,
        "RAG tokens": rag_tokens,
        "Web tokens": web_tokens,
        "Input tokens": input_tokens,
        "Output tokens": output_tokens,
        "Model cost": model_cost,
        "Web cost": web_cost,
        "Classifier cost": classifier_cost,
        "Total turn cost": total_cost,
    }


def calculate_intent_conversation_cost(
    intent: str,
    turns: int,
    model_name: str,
    web_mode: str,
    history_strategy: str,
    classifier: str,
) -> tuple[float, pd.DataFrame]:
    if intent in ["Booking", "Complaint"]:
        row = calculate_turn_cost(1, intent, model_name, web_mode, history_strategy, classifier)
        return row["Total turn cost"], pd.DataFrame([row])

    rows = [
        calculate_turn_cost(t, intent, model_name, web_mode, history_strategy, classifier)
        for t in range(1, turns + 1)
    ]
    df = pd.DataFrame(rows)
    return float(df["Total turn cost"].sum()), df


def calculate_weighted_average(
    scenario: dict,
    model_name: str,
    web_mode: str,
    history_strategy: str,
    classifier: str,
) -> tuple[float, pd.DataFrame]:
    rows = []
    weighted_total = 0.0

    for intent, weight in scenario["intent_mix"].items():
        cost, _ = calculate_intent_conversation_cost(
            intent,
            scenario["turns"],
            model_name,
            web_mode,
            history_strategy,
            classifier,
        )
        weighted_cost = cost * weight
        weighted_total += weighted_cost

        rows.append(
            {
                "Intent": intent,
                "Intent mix": f"{weight:.0%}",
                "Turns counted": 1 if intent in ["Booking", "Complaint"] else scenario["turns"],
                "Web search enabled": should_use_web(intent, web_mode),
                "Cost per conversation": cost,
                "Weighted cost": weighted_cost,
            }
        )

    return weighted_total, pd.DataFrame(rows)


def calculate_monthly_summary(avg_cost: float, scenario: dict) -> dict:
    monthly_ai_cost = avg_cost * scenario["conversations_per_day"] * 30
    human_monthly = HUMAN_BASELINE_PER_CONV * scenario["conversations_per_day"] * 30
    savings_percent = (human_monthly - monthly_ai_cost) / human_monthly * 100

    if monthly_ai_cost == 0:
        cheaper_times = float("inf")
    else:
        cheaper_times = human_monthly / monthly_ai_cost

    return {
        "Avg cost per conversation": avg_cost,
        "Monthly AI cost": monthly_ai_cost,
        "Human baseline": human_monthly,
        "Savings %": savings_percent,
        "AI cheaper than human": cheaper_times,
    }


def format_cost_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    formatted = df.copy()
    for col in cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].map(lambda x: f"${x:,.6f}")
    return formatted


def run_config(config_name: str, scenario_name: str) -> dict:
    config = CONFIGS[config_name]
    scenario = SCENARIOS[scenario_name]
    avg_cost, intent_df = calculate_weighted_average(
        scenario,
        config["model"],
        config["web_mode"],
        config["history"],
        config["classifier"],
    )
    summary = calculate_monthly_summary(avg_cost, scenario)
    return {"config": config, "scenario": scenario, "summary": summary, "intent_df": intent_df}


st.set_page_config(page_title="AI Conversation Cost Simulator", layout="wide")

st.title("AI Conversation Cost Simulator")
st.caption("Tool giả lập chi phí chatbot AI cho travel agency Việt Nam. Không gọi API LLM thật.")

with st.sidebar:
    st.header("Config Settings")

    config_choice = st.selectbox(
        "Chọn config",
        ["Budget Bot", "Smart Mix", "Premium Concierge", "Custom"],
    )

    scenario_name = st.selectbox(
        "Chọn scenario",
        list(SCENARIOS.keys()),
    )

    if config_choice == "Custom":
        model_name = st.selectbox("Model", list(MODEL_PRICING.keys()))
        web_mode = st.selectbox(
            "Web search mode",
            ["OFF", "Selective: Visa + Weather", "Broad: Guide + Visa + Weather"],
        )
        history_strategy = st.selectbox("History strategy", ["Last 3", "Last 5", "Full", "Summarize"])
        classifier = st.selectbox("Classifier", ["Keyword", "LLM"])
        quality = "Custom"
        best_for = "User-defined config"
    else:
        config = CONFIGS[config_choice]
        model_name = config["model"]
        web_mode = config["web_mode"]
        history_strategy = config["history"]
        classifier = config["classifier"]
        quality = config["quality"]
        best_for = config["best_for"]

    st.divider()
    selected_intent = st.selectbox(
        "Xem bảng cost per turn cho intent",
        ["Guide", "Visa", "Weather", "Booking", "Complaint"],
    )

scenario = SCENARIOS[scenario_name]

avg_cost, intent_df = calculate_weighted_average(
    scenario,
    model_name,
    web_mode,
    history_strategy,
    classifier,
)
summary = calculate_monthly_summary(avg_cost, scenario)

st.subheader("1. Config Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Model", model_name)
c2.metric("Web search", web_mode)
c3.metric("History", history_strategy)
c4.metric("Classifier", classifier)

st.write(f"**Quality estimate:** {quality}")
st.write(f"**Best for:** {best_for}")

st.subheader("2. Scenario Summary")
s1, s2, s3 = st.columns(3)
s1.metric("Scenario", scenario_name)
s2.metric("Conversations/day", scenario["conversations_per_day"])
s3.metric("Turns/conversation", scenario["turns"])

st.subheader("3. Cost Result")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Avg cost / conversation", money(summary["Avg cost per conversation"], 6))
m2.metric("Monthly AI cost", money(summary["Monthly AI cost"], 2))
m3.metric("Human baseline / month", money(summary["Human baseline"], 2))
m4.metric("Savings", f"{summary['Savings %']:.2f}%")

st.metric("AI cheaper than human", f"{summary['AI cheaper than human']:.2f}×")

st.subheader("4. Cost per Intent")
st.dataframe(
    format_cost_columns(intent_df, ["Cost per conversation", "Weighted cost"]),
    use_container_width=True,
)

st.subheader(f"5. Cost per Turn — {selected_intent}")
selected_cost, turn_df = calculate_intent_conversation_cost(
    selected_intent,
    scenario["turns"],
    model_name,
    web_mode,
    history_strategy,
    classifier,
)

st.dataframe(
    format_cost_columns(
        turn_df,
        ["Model cost", "Web cost", "Classifier cost", "Total turn cost"],
    ),
    use_container_width=True,
)

st.write(f"**Total cost for {selected_intent}:** {money(selected_cost, 6)}")

st.subheader("6. Comparison Table — 3 Predefined Configs")
comparison_rows = []
for cfg_name, cfg in CONFIGS.items():
    avg, _ = calculate_weighted_average(
        scenario,
        cfg["model"],
        cfg["web_mode"],
        cfg["history"],
        cfg["classifier"],
    )
    monthly = calculate_monthly_summary(avg, scenario)

    comparison_rows.append(
        {
            "Config": cfg_name,
            "Scenario": scenario_name,
            "Model": cfg["model"],
            "Web search": cfg["web_mode"],
            "History": cfg["history"],
            "Avg cost / conv": monthly["Avg cost per conversation"],
            "Monthly AI cost": monthly["Monthly AI cost"],
            "Human baseline": monthly["Human baseline"],
            "Savings %": monthly["Savings %"],
            "Cheaper than human": monthly["AI cheaper than human"],
            "Quality": cfg["quality"],
            "Best for": cfg["best_for"],
        }
    )

comparison_df = pd.DataFrame(comparison_rows)
comparison_display = comparison_df.copy()
comparison_display["Avg cost / conv"] = comparison_display["Avg cost / conv"].map(lambda x: f"${x:,.6f}")
comparison_display["Monthly AI cost"] = comparison_display["Monthly AI cost"].map(lambda x: f"${x:,.2f}")
comparison_display["Human baseline"] = comparison_display["Human baseline"].map(lambda x: f"${x:,.2f}")
comparison_display["Savings %"] = comparison_display["Savings %"].map(lambda x: f"{x:.2f}%")
comparison_display["Cheaper than human"] = comparison_display["Cheaper than human"].map(lambda x: f"{x:.2f}×")

st.dataframe(comparison_display, use_container_width=True)

st.subheader("7. Formula Notes")
st.markdown(
    """
```text
input_tokens = system_prompt + user_message + RAG + history + web_tokens

model_cost =
(input_tokens × input_price + output_tokens × output_price) / 1,000,000

total_turn_cost = model_cost + web_api_cost + classifier_cost

monthly_cost = avg_cost_per_conversation × conversations_per_day × 30
```
"""
)
