# 03 · Cost Calculation — Tính chi phí từng Config × 2 Scenarios

> Mục tiêu: Với mỗi config đã thiết kế ở `02-config-design.md`, tính cost/turn → cost/conversation → monthly cost cho cả 2 scenarios: low season và high season.

---

## 1. Tham số cố định dùng để tính

```text
System prompt:              500 tokens
User message:                80 tokens
Assistant response:         180 tokens output
1 prior turn history:        260 tokens
RAG top-5 chunks:          1,250 tokens
Web search results:          800 tokens nếu bật web search
Web search API call:      $0.008 / query
LLM classifier:              170 tokens = 150 input + 20 output
Keyword classifier:           $0
```

Human baseline:

```text
$0.50 / conversation
```

---

## 2. Scenarios chính thức của đề bài

### Scenario A — Low season

```text
Volume: 300 conversations / ngày
Turns per conversation: 4
Intent mix:
- Guide: 50%
- Visa: 25%
- Weather: 10%
- Booking: 10%
- Complaint: 5%
Human baseline: $0.50 × 300 × 30 = $4,500 / tháng
```

### Scenario B — High season

```text
Volume: 1,200 conversations / ngày
Turns per conversation: 7
Intent mix:
- Guide: 30%
- Visa: 15%
- Weather: 10%
- Booking: 35%
- Complaint: 10%
Human baseline: $0.50 × 1,200 × 30 = $18,000 / tháng
```

---

## 3. Công thức tính

### History tokens

```text
Full history: history = (turn - 1) × 260
Last 3:       history = min(turn - 1, 3) × 260
Last 5:       history = min(turn - 1, 5) × 260
Summarize:    history = 150 fixed
```

### Input tokens cho intent bot-handled

```text
input_tokens = system prompt + user message + RAG + history + web tokens
```

Trong đó:

```text
Guide / Visa / Weather: RAG = 1,250 tokens
Booking / Complaint: chuyển người, không tính full response generation
Web tokens = 800 nếu web search bật cho intent đó
```

### Model cost

```text
model_cost =
(input_tokens × input_price + output_tokens × output_price) / 1,000,000
```

### Total turn cost

```text
total_turn_cost = model_cost + web_api_cost + classifier_cost
```

### Weighted average cost per conversation

Scenario A:

```text
avg_cost_A =
50% × guide_cost
+ 25% × visa_cost
+ 10% × weather_cost
+ 10% × booking_cost
+  5% × complaint_cost
```

Scenario B:

```text
avg_cost_B =
30% × guide_cost
+ 15% × visa_cost
+ 10% × weather_cost
+ 35% × booking_cost
+ 10% × complaint_cost
```

### Monthly cost

```text
monthly_cost = avg_cost_per_conversation × conversations_per_day × 30
```

---

# Config 1 — Budget Bot

## Config summary

```text
Model: Gemini 2.5 Flash-Lite
Input price: $0.10 / 1M tokens
Output price: $0.40 / 1M tokens
Web search: OFF
History: Last 3
Classifier: Keyword / Regex = $0
```

## Cost per turn — Guide / Visa / Weather

Vì Budget Bot tắt web search, Guide, Visa và Weather có cùng cost theo turn.

| Turn | History tokens | Input tokens | Output tokens | Model cost | Web cost | Classifier cost | Total / turn |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1,830 | 180 | $0.000255 | $0.000000 | $0.000000 | $0.000255 |
| 2 | 260 | 2,090 | 180 | $0.000281 | $0.000000 | $0.000000 | $0.000281 |
| 3 | 520 | 2,350 | 180 | $0.000307 | $0.000000 | $0.000000 | $0.000307 |
| 4 | 780 | 2,610 | 180 | $0.000333 | $0.000000 | $0.000000 | $0.000333 |
| 5 | 780 | 2,610 | 180 | $0.000333 | $0.000000 | $0.000000 | $0.000333 |
| 6 | 780 | 2,610 | 180 | $0.000333 | $0.000000 | $0.000000 | $0.000333 |
| 7 | 780 | 2,610 | 180 | $0.000333 | $0.000000 | $0.000000 | $0.000333 |

### Cost per conversation by intent

| Intent | Scenario A — 4 turns | Scenario B — 7 turns |
|---|---:|---:|
| Guide | $0.001176 | $0.002175 |
| Visa | $0.001176 | $0.002175 |
| Weather | $0.001176 | $0.002175 |
| Booking | $0.000000 | $0.000000 |
| Complaint | $0.000000 | $0.000000 |

### Weighted result

| Item | Scenario A | Scenario B |
|---|---:|---:|
| Avg cost / conversation | $0.001000 | $0.001196 |
| Monthly AI cost | $8.9964 | $43.0650 |
| Human baseline | $4,500 | $18,000 |
| AI rẻ hơn human | 500.20× | 417.97× |
| Savings % | 99.80% | 99.76% |

### Sanity check

```text
Budget Bot cực rẻ vì dùng model cheap, không bật web search và classifier keyword = $0.
Tuy nhiên con số rẻ này đi kèm rủi ro lớn: visa/weather có thể outdated và bot có thể quên ngữ cảnh nếu conversation dài.
```

---

# Config 2 — Smart Mix

## Config summary

```text
Model: GPT-4o-mini
Input price: $0.15 / 1M tokens
Output price: $0.60 / 1M tokens
Web search: ON selective cho Visa và Weather
History: Last 5
Classifier: LLM classifier
Classifier cost per turn:
(150 × 0.15 + 20 × 0.60) / 1,000,000 = $0.0000345
```

## Cost per turn — Guide

Guide không bật web search trong Smart Mix.

| Turn | History tokens | Input tokens | Output tokens | Model cost | Web cost | Classifier cost | Total / turn |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1,830 | 180 | $0.000383 | $0.000000 | $0.000035 | $0.000417 |
| 2 | 260 | 2,090 | 180 | $0.000422 | $0.000000 | $0.000035 | $0.000456 |
| 3 | 520 | 2,350 | 180 | $0.000461 | $0.000000 | $0.000035 | $0.000495 |
| 4 | 780 | 2,610 | 180 | $0.000500 | $0.000000 | $0.000035 | $0.000534 |
| 5 | 1,040 | 2,870 | 180 | $0.000539 | $0.000000 | $0.000035 | $0.000573 |
| 6 | 1,300 | 3,130 | 180 | $0.000578 | $0.000000 | $0.000035 | $0.000612 |
| 7 | 1,300 | 3,130 | 180 | $0.000578 | $0.000000 | $0.000035 | $0.000612 |

## Cost per turn — Visa / Weather

Visa và Weather bật web search selective.

| Turn | History tokens | Input tokens | Output tokens | Model cost | Web cost | Classifier cost | Total / turn |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 2,630 | 180 | $0.000503 | $0.008000 | $0.000035 | $0.008537 |
| 2 | 260 | 2,890 | 180 | $0.000542 | $0.008000 | $0.000035 | $0.008576 |
| 3 | 520 | 3,150 | 180 | $0.000581 | $0.008000 | $0.000035 | $0.008615 |
| 4 | 780 | 3,410 | 180 | $0.000620 | $0.008000 | $0.000035 | $0.008654 |
| 5 | 1,040 | 3,670 | 180 | $0.000659 | $0.008000 | $0.000035 | $0.008693 |
| 6 | 1,300 | 3,930 | 180 | $0.000698 | $0.008000 | $0.000035 | $0.008732 |
| 7 | 1,300 | 3,930 | 180 | $0.000698 | $0.008000 | $0.000035 | $0.008732 |

### Cost per conversation by intent

| Intent | Scenario A — 4 turns | Scenario B — 7 turns |
|---|---:|---:|
| Guide | $0.001902 | $0.003699 |
| Visa | $0.034382 | $0.060539 |
| Weather | $0.034382 | $0.060539 |
| Booking | $0.000035 | $0.000035 |
| Complaint | $0.000035 | $0.000035 |

### Weighted result

| Item | Scenario A | Scenario B |
|---|---:|---:|
| Avg cost / conversation | $0.012990 | $0.016260 |
| Monthly AI cost | $116.9089 | $585.3591 |
| Human baseline | $4,500 | $18,000 |
| AI rẻ hơn human | 38.49× | 30.75× |
| Savings % | 97.40% | 96.75% |

### Sanity check

```text
Smart Mix đắt hơn Budget Bot chủ yếu vì web search selective cho Visa và Weather.
Tuy nhiên monthly cost vẫn thấp hơn human rất nhiều: khoảng $116.91/tháng ở Scenario A và $585.36/tháng ở Scenario B.
Đây là config cân bằng vì chi thêm tiền ở đúng intent có rủi ro outdated cao.
```

---

# Config 3 — Premium Concierge

## Config summary

```text
Model: GPT-5.5
Input price: $5.00 / 1M tokens
Output price: $30.00 / 1M tokens
Web search: ON broad cho Guide, Visa và Weather
History: Full history
Classifier: LLM classifier
Classifier cost per turn:
(150 × 5.00 + 20 × 30.00) / 1,000,000 = $0.00135
```

## Cost per turn — Guide / Visa / Weather

Vì Premium Concierge bật web search broad, Guide, Visa và Weather đều có web search.

| Turn | History tokens | Input tokens | Output tokens | Model cost | Web cost | Classifier cost | Total / turn |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 2,630 | 180 | $0.018550 | $0.008000 | $0.001350 | $0.027900 |
| 2 | 260 | 2,890 | 180 | $0.019850 | $0.008000 | $0.001350 | $0.029200 |
| 3 | 520 | 3,150 | 180 | $0.021150 | $0.008000 | $0.001350 | $0.030500 |
| 4 | 780 | 3,410 | 180 | $0.022450 | $0.008000 | $0.001350 | $0.031800 |
| 5 | 1,040 | 3,670 | 180 | $0.023750 | $0.008000 | $0.001350 | $0.033100 |
| 6 | 1,300 | 3,930 | 180 | $0.025050 | $0.008000 | $0.001350 | $0.034400 |
| 7 | 1,560 | 4,190 | 180 | $0.026350 | $0.008000 | $0.001350 | $0.035700 |

### Cost per conversation by intent

| Intent | Scenario A — 4 turns | Scenario B — 7 turns |
|---|---:|---:|
| Guide | $0.119400 | $0.222600 |
| Visa | $0.119400 | $0.222600 |
| Weather | $0.119400 | $0.222600 |
| Booking | $0.001350 | $0.001350 |
| Complaint | $0.001350 | $0.001350 |

### Weighted result

| Item | Scenario A | Scenario B |
|---|---:|---:|
| Avg cost / conversation | $0.101693 | $0.123038 |
| Monthly AI cost | $915.2325 | $4,429.3500 |
| Human baseline | $4,500 | $18,000 |
| AI rẻ hơn human | 4.92× | 4.06× |
| Savings % | 79.66% | 75.39% |

### Sanity check

```text
Premium Concierge đắt nhất vì dùng GPT-5.5, bật web search broad và giữ full history.
Dù vậy, chi phí vẫn thấp hơn human baseline khoảng 4–5 lần.
Config này chỉ nên dùng khi chất lượng có giá trị kinh doanh rõ ràng, ví dụ khách VIP hoặc booking giá trị cao.
```

---

# 4. Bảng tổng hợp 3 configs

| Config | Scenario A cost/conv | Scenario A monthly | Scenario B cost/conv | Scenario B monthly | Nhận xét |
|---|---:|---:|---:|---:|---|
| Budget Bot | $0.001000 | $8.9964 | $0.001196 | $43.0650 | Rẻ nhất nhưng rủi ro quality cao |
| Smart Mix | $0.012990 | $116.9089 | $0.016260 | $585.3591 | Cân bằng cost và quality |
| Premium Concierge | $0.101693 | $915.2325 | $0.123038 | $4,429.3500 | Chất lượng cao nhưng cost cao |

---

# 5. Insight chính từ phần tính cost

## Insight 1 — Model tier ảnh hưởng cost rất mạnh

```text
Budget Bot dùng Gemini Flash-Lite nên monthly cost cực thấp.
Premium Concierge dùng GPT-5.5 nên cost tăng mạnh dù cùng số turn.
Điều này xác nhận model tier là knob ảnh hưởng cost lớn nhất.
```

## Insight 2 — Web search làm cost tăng rõ ở Visa và Weather

```text
Smart Mix bật web search cho Visa và Weather nên cost của 2 intent này cao hơn Guide rất nhiều.
Tuy nhiên, đây là khoản chi hợp lý vì Visa và Weather cần thông tin mới.
```

## Insight 3 — Scenario B không chỉ đơn giản là Scenario A ×4

```text
Scenario B có volume cao hơn 4 lần và conversation dài hơn 7 turns thay vì 4 turns.
Tuy nhiên Booking và Complaint chiếm 45% trong Scenario B, mà hai intent này chỉ handoff/escalate nên không tính full LLM conversation.
Vì vậy monthly cost không tăng đúng theo tỷ lệ volume × turns.
```

## Insight 4 — Smart Mix là ứng viên tốt nhất để recommend

```text
Budget Bot rẻ nhất nhưng có rủi ro trả lời sai thông tin real-time.
Premium Concierge tốt nhất về quality nhưng có thể overkill cho toàn bộ traffic.
Smart Mix giữ cost thấp hơn human rất nhiều, đồng thời bật web search ở đúng intent quan trọng.
```
