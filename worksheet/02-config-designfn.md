# 02 · Configuration Design — Đặt tên + Chốt knobs cho ≥3 Configs

> Mục tiêu: Thiết kế ít nhất 3 cấu hình chatbot AI khác nhau để so sánh chi phí, chất lượng và rủi ro triển khai.

Nhóm sử dụng 3 knobs chính:

1. **Model tier** — chọn model rẻ / cân bằng / mạnh
2. **Web search** — tắt, bật chọn lọc, hoặc bật rộng
3. **History management** — chatbot nhớ bao nhiêu lượt chat trước đó

Các config được thiết kế dựa trên base flow đã thống nhất:

```text
Tourist message → Intent classification → Route theo intent → Context assembly → Response generation
```

Booking và Complaint sẽ được chuyển sang người phụ trách, không tính như một full LLM conversation.

---

## Config 1 — Budget Bot

### Tên config

```text
Budget Bot
```

### 3 Knobs

**① Model tier**

```text
Response model: Gemini 2.5 Flash-Lite
Input price: $0.10 / 1M tokens
Output price: $0.40 / 1M tokens

Classifier model: Keyword / Regex
Classifier cost: $0
```

**② Web search**

```text
OFF
```

**③ History management**

```text
Last 3 turns
```

### Lý do nhóm chọn config này

```text
Budget Bot được thiết kế để kiểm tra mức chi phí thấp nhất mà chatbot có thể vận hành.
Config này phù hợp với low season, khi lượng khách không quá phức tạp và phần lớn câu hỏi là FAQ hoặc guide cơ bản.
Nhóm chọn model cheap, tắt web search và chỉ giữ 3 lượt history gần nhất để tối ưu chi phí trên mỗi conversation.
```

### Trade-off chính

```text
Đổi lại, chất lượng câu trả lời có thể thấp hơn ở các câu hỏi phức tạp.
Visa hoặc weather có thể bị outdated vì không bật web search.
Chatbot cũng có thể quên thông tin người dùng đã nói ở đầu cuộc trò chuyện nếu conversation dài hơn 3 lượt.
```

### Rủi ro lớn nhất

```text
Rủi ro lớn nhất là bot trả lời sai hoặc thiếu cập nhật cho các intent cần thông tin mới như visa và weather.
```

### Best for

```text
Low season, simple FAQ, traffic lớn nhưng câu hỏi đơn giản, mục tiêu tiết kiệm chi phí.
```

---

## Config 2 — Smart Mix

### Tên config

```text
Smart Mix
```

### 3 Knobs

**① Model tier**

```text
Response model: GPT-4o-mini
Input price: $0.15 / 1M tokens
Output price: $0.60 / 1M tokens

Classifier model: LLM classifier
Classifier input: 150 tokens
Classifier output: 20 tokens
```

**② Web search**

```text
ON selective — bật cho intent:
- Visa / Policy
- Weather / Event
```

**③ History management**

```text
Last 5 turns
```

### Lý do nhóm chọn config này

```text
Smart Mix là phương án cân bằng giữa chi phí và chất lượng.
Nhóm không bật web search cho mọi intent, mà chỉ bật cho Visa và Weather vì đây là hai nhóm thông tin có tính thời điểm cao.
History Last 5 giúp chatbot nhớ đủ ngữ cảnh như budget, ngày đi, nhóm khách và sở thích mà vẫn không quá tốn token.
```

### Trade-off chính

```text
Config này đắt hơn Budget Bot vì có LLM classifier, web search selective và history dài hơn.
Tuy nhiên, chi phí tăng có lý do vì nó giảm rủi ro trả lời sai ở các intent quan trọng.
So với Premium Concierge, Smart Mix vẫn tiết kiệm hơn nhiều vì không dùng model premium và không bật web search broad.
```

### Rủi ro lớn nhất

```text
Rủi ro lớn nhất là GPT-4o-mini có thể chưa đủ mạnh cho một số câu hỏi rất phức tạp như lịch trình luxury, visa nhiều điều kiện hoặc yêu cầu cá nhân hóa cao.
```

### Best for

```text
Triển khai thực tế quanh năm, cân bằng giữa cost, quality và reliability.
```

---

## Config 3 — Premium Concierge

### Tên config

```text
Premium Concierge
```

### 3 Knobs

**① Model tier**

```text
Response model: GPT-5.5
Input price: $5.00 / 1M tokens
Output price: $30.00 / 1M tokens

Classifier model: LLM classifier
Classifier input: 150 tokens
Classifier output: 20 tokens
```

**② Web search**

```text
ON broad — bật cho hầu hết intent bot-handled:
- Guide / Destination
- Visa / Policy
- Weather / Event
```

**③ History management**

```text
Full history
```

### Lý do nhóm chọn config này

```text
Premium Concierge được thiết kế để kiểm tra trần chất lượng cao nhất.
Config này phù hợp với khách VIP, luxury honeymoon, custom itinerary hoặc các booking có giá trị cao.
Nhóm chọn model premium, bật web search rộng và giữ full history để chatbot có thể trả lời cá nhân hóa và ít mất ngữ cảnh nhất.
```

### Trade-off chính

```text
Trade-off lớn nhất là chi phí cao.
Full history làm input tokens tăng mạnh ở conversation dài, đặc biệt trong Scenario B có trung bình 7 turns.
Web search broad cũng làm cost tăng vì nhiều lượt phải gọi API và thêm 800 tokens vào context.
```

### Rủi ro lớn nhất

```text
Rủi ro lớn nhất là over-engineering: chi phí cao hơn nhiều nhưng không phải mọi khách hàng đều cần chất lượng premium.
```

### Best for

```text
Khách VIP, high-value booking, luxury travel, hoặc giai đoạn cần tối đa chất lượng trải nghiệm.
```

---

## Kiểm tra 3 configs có đủ khác biệt không?

| Tiêu chí | Budget Bot | Smart Mix | Premium Concierge |
|---|---|---|---|
| Model | Cheap | Balanced / low-cost strong enough | Premium |
| Web search | OFF | Selective: Visa + Weather | Broad |
| History | Last 3 | Last 5 | Full |
| Classifier | Keyword | LLM | LLM |
| Cost | Thấp nhất | Trung bình | Cao nhất |
| Quality | Low-Medium | Medium-High | High |
| Speed | Nhanh | Trung bình | Chậm hơn |
| Rủi ro chính | Outdated info | Chưa đủ mạnh cho case rất phức tạp | Cost cao / overkill |

Nhóm đánh giá 3 configs đã đủ khác biệt vì khác nhau ở cả 3 knobs: model, web search và history.

---

## Vì sao không chọn chỉ một model cho mọi trường hợp?

```text
Tourist không chỉ hỏi một loại câu hỏi. Có câu đơn giản như gợi ý điểm đến, nhưng cũng có câu cần thông tin mới như visa/weather hoặc cần chuyển người như booking/complaint.
Nếu dùng model quá rẻ cho mọi intent, rủi ro chất lượng tăng.
Nếu dùng model premium cho mọi intent, chi phí có thể không hợp lý.
Vì vậy nhóm cần so sánh Budget Bot, Smart Mix và Premium Concierge để tìm điểm cân bằng tốt nhất.
```

---

## Config nhóm sẽ dùng để tính cost ở bước tiếp theo

```text
Config 1: Budget Bot
- Model: Gemini 2.5 Flash-Lite
- Web search: OFF
- History: Last 3
- Classifier: Keyword

Config 2: Smart Mix
- Model: GPT-4o-mini
- Web search: ON selective for Visa and Weather
- History: Last 5
- Classifier: LLM

Config 3: Premium Concierge
- Model: GPT-5.5
- Web search: ON broad
- History: Full
- Classifier: LLM
```

---

## Ghi chú để tính cost

```text
Ở bước cost calculation, nhóm vẫn dùng intent mix chính thức của đề bài cho Scenario A và Scenario B.

Scenario A:
Guide 50%, Visa 25%, Weather 10%, Booking 10%, Complaint 5%

Scenario B:
Guide 30%, Visa 15%, Weather 10%, Booking 35%, Complaint 10%

Booking và Complaint chỉ tính 1 turn handoff/escalation, không tính như full chatbot conversation.
```
