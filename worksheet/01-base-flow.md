# 01 · Base Flow + Chốt 3 Knobs

> **Mục tiêu**: Hiểu chatbot hoạt động ra sao ở mức base và xác định 3 knobs nhóm sẽ tweak ở các bước sau.
>
> **Thời gian**: 7 phút (trong 15 phút phần Setup)

---

## Bước 1 — Đọc base flow trong cost reference card

Đã đọc mục **2. Base Flow** và **3. Decision Points** trong `cost-reference-card.md`.

Các điểm nhóm chốt:

- Tin nhắn đầu tiên được phân loại intent.
- Visa/Policy, Guide/Destination và Weather/Event có thể đi qua RAG/web rồi generate response bằng LLM.
- Tour/Booking chuyển sales và Complaint chuyển manager, tính `$0` LLM cost cho phần trả lời chính.
- Sau khi route, chatbot ráp system prompt, history, RAG chunks, web results nếu có, và user message để generate response.

---

## Bước 2 — Vẽ lại flow theo cách hiểu của nhóm

```text
Tourist message
      |
      v
[Intent classification]
      |
      +--> Visa/Policy --------+
      |                        |
      |                        v
      +--> Guide/Destination -> [Knowledge lookup: RAG top chunks]
      |                        |
      |                        +--> optional web search for fresh policy/info
      |
      +--> Weather/Event -----> [Web search for real-time info]
      |
      +--> Tour/Booking -----> [Handoff to sales] -> $0 LLM generation cost
      |
      +--> Complaint --------> [Escalate to manager] -> $0 LLM generation cost

For bot-handled intents:

Knowledge/web result
      |
      v
[Context assembly]
System prompt + selected history + RAG chunks + web results + user message
      |
      v
[Response generation]
Chosen model writes answer for tourist
```

Flow có đủ 4 điểm:

1. Intent classification
2. Route theo intent
3. Context assembly
4. Response generation

---

## Bước 3 — Xác định 3 Knobs

### Knob 1 — Model tier

**Câu hỏi:** Chất lượng câu trả lời ở mức nào?

Options:

```text
□ Cheap        (Gemini Flash-Lite / DeepSeek V4 Flash / GPT-4o-mini)
□ Mid          (Gemini Flash / Claude Haiku 4.5)
□ Strong       (DeepSeek V4 Pro / Claude Sonnet 4.6)
□ Premium      (Claude Opus 4.7 / GPT-5.5)
□ Mix          (model khác nhau cho intent khác nhau)
```

```text
Nhóm muốn thử đủ 3 hướng: một config cheap để kiểm tra sàn chi phí, một config premium để thấy trần chất lượng, và một config mix để dùng model mạnh cho câu hỏi có rủi ro cao như visa/complex itinerary.
Cheap có thể đủ cho FAQ/guide đơn giản, nhưng không nên dùng cho mọi intent vì câu trả lời sai về visa hoặc lịch trình phức tạp có thể làm mất niềm tin.
```

### Knob 2 — Web search

**Câu hỏi:** Có cần thông tin real-time không?

Options:

```text
□ OFF              (chỉ dùng RAG — knowledge base có sẵn)
□ ON selective     (bật cho 1-2 intent cần real-time: visa, weather)
□ ON broad         (bật cho hầu hết intent)
```

```text
Nhóm nghiêng về web search selective cho phương án cân bằng vì weather và visa/policy có tính thời điểm.
Web OFF phù hợp với config budget nhưng có rủi ro outdated.
Web broad có thể tăng niềm tin cho khách nhưng dễ đội cost vì mỗi search thêm API cost và khoảng 800 input tokens.
```

### Knob 3 — History management

**Câu hỏi:** Chatbot cần nhớ bao nhiêu context của conversation?

Options:

```text
□ Last 3 turns
□ Last 5 turns
□ Full history
□ Summarize every 5
```

```text
Last 3 turns rẻ nhưng có nguy cơ quên budget, dates hoặc traveler profile.
Last 5 turns là lựa chọn cân bằng cho Scenario A và đa số hội thoại ngắn.
Full history hợp với premium hoặc honeymoon/custom itinerary vì khách thường tham chiếu thông tin đã nói từ đầu.
Summarize every 5 đáng thử cho smart mix nếu conversation dài nhưng cần tính thêm LLM call phụ.
```

---

## Bước 4 — Sơ bộ nhóm muốn thử những combo nào?

**Combo 1 (định hướng cheap)**:

```text
Model: Cheap / GPT-4o-mini hoặc Gemini Flash-Lite
Web: OFF
History: Last 3 turns
Tên dự kiến: Budget FAQ
```

**Combo 2 (định hướng premium)**:

```text
Model: Premium / GPT-5.5 hoặc Claude Opus 4.7
Web: ON broad
History: Full history
Tên dự kiến: Premium Concierge
```

**Combo 3 (định hướng balanced / smart mix)**:

```text
Model: Mix - cheap for classification/simple guide, strong for visa and complex itinerary
Web: ON selective for visa and weather/event
History: Last 5 turns
Tên dự kiến: Smart Mix
```

**Combo 4** (optional):

```text
Model: Mid / Claude Haiku 4.5 hoặc Gemini Flash
Web: ON selective for weather only
History: Summarize every 5 turns
Tên dự kiến: Efficient Advisor
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Đã vẽ flow base có đủ 4 bước (Intent → Route → Context → Response)
- [x] Hiểu Booking + Khiếu nại = $0 LLM cost (chuyển con người)
- [x] Đã phác thảo ≥3 combo khác nhau
- [x] Nhóm đồng thuận về hướng đi mỗi combo

Xong → 10:25 chuyển sang **Main phase**. Mở `02-config-design.md`.
