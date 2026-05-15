# 04 · Comparison Table — Bảng so sánh đầy đủ

> Mục tiêu: Tổng hợp tất cả số đã tính ở `03-cost-calculation.md` thành 1 bảng so sánh duy nhất để dùng khi present và ra quyết định deploy.

---

## 1. Bảng so sánh chính

| Tiêu chí | Config 1 | Config 2 | Config 3 |
|---|---|---|---|
| **Tên** | Budget Bot | Smart Mix | Premium Concierge |
| **Model** | Gemini 2.5 Flash-Lite | GPT-4o-mini | GPT-5.5 |
| **Model tier** | Cheap | Balanced / low-cost | Premium |
| **Input price** | $0.10 / 1M tokens | $0.15 / 1M tokens | $5.00 / 1M tokens |
| **Output price** | $0.40 / 1M tokens | $0.60 / 1M tokens | $30.00 / 1M tokens |
| **Web search** | OFF | ON selective: Visa + Weather | ON broad: Guide + Visa + Weather |
| **History** | Last 3 turns | Last 5 turns | Full history |
| **Intent classifier** | Keyword / Regex = $0 | LLM classifier | LLM classifier |
| **Cost / conv — Scenario A** | $0.001000 | $0.012990 | $0.101693 |
| **Cost / conv — Scenario B** | $0.001196 | $0.016260 | $0.123038 |
| **Monthly A** | $8.9964 | $116.9089 | $915.2325 |
| **Monthly B** | $43.0650 | $585.3591 | $4,429.3500 |
| **Human baseline A** | $4,500 | $4,500 | $4,500 |
| **Human baseline B** | $18,000 | $18,000 | $18,000 |
| **vs human A** | rẻ 500.20× | rẻ 38.49× | rẻ 4.92× |
| **vs human B** | rẻ 417.97× | rẻ 30.75× | rẻ 4.06× |
| **Savings A** | 99.80% | 97.40% | 79.66% |
| **Savings B** | 99.76% | 96.75% | 75.39% |
| **Quality estimate** | Low-Medium | Medium-High | High |
| **Speed estimate** | High | Medium | Low-Medium |
| **Điểm yếu chính** | Rủi ro outdated info vì web OFF | Chưa tối ưu cho case rất phức tạp | Cost cao, có thể overkill |
| **Best for** | Low season, FAQ đơn giản, tối ưu chi phí | Triển khai thực tế quanh năm | VIP / high-value customers |

---

## 2. Quan sát nhanh từ bảng

### Câu 1 — Config rẻ nhất là gì? Đắt nhất là gì?

```text
Rẻ nhất: Budget Bot
- Monthly A = $8.9964
- Monthly B = $43.0650

Đắt nhất: Premium Concierge
- Monthly A = $915.2325
- Monthly B = $4,429.3500

Chênh lệch ở Scenario B:
Premium Concierge / Budget Bot = $4,429.3500 / $43.0650 ≈ 102.84×
```

**Nhận xét:**

```text
Budget Bot rẻ vượt trội vì dùng model cheap, web OFF, history Last 3 và classifier keyword.
Premium Concierge đắt nhất vì dùng GPT-5.5, bật web search broad và giữ full history.
```

---

### Câu 2 — Knob nào ảnh hưởng cost nhiều nhất?

```text
Knob ảnh hưởng cost nhiều nhất là Model tier.
Khi đổi từ Gemini 2.5 Flash-Lite sang GPT-5.5, giá input tăng từ $0.10 lên $5.00 / 1M tokens, tức tăng 50×.
Giá output tăng từ $0.40 lên $30.00 / 1M tokens, tức tăng 75×.
```

**Xếp hạng mức ảnh hưởng cost:**

```text
1. Model tier — ảnh hưởng lớn nhất
2. Web search — tăng mạnh ở intent Visa/Weather vì mỗi query thêm $0.008 + 800 input tokens
3. History — tăng dần theo số turn, rõ nhất ở Scenario B 7 turns
4. Classifier — có ảnh hưởng nhỏ, nhưng LLM classifier giúp routing tốt hơn keyword
```

---

### Câu 3 — Tại sao Scenario B không đắt đúng bằng Scenario A ×4 hoặc ×7?

```text
Scenario B có volume cao hơn Scenario A 4 lần và số lượt chat dài hơn: 7 turns thay vì 4 turns.
Tuy nhiên Scenario B có Booking + Complaint = 45% tổng intent.
Hai intent này được handoff/escalate sang người thật, chỉ tính classifier/handoff cost chứ không tính full LLM response generation.
Vì vậy monthly cost không tăng đúng theo tỷ lệ volume × turns.
```

**Ví dụ:**

```text
Smart Mix:
Monthly A = $116.9089
Monthly B = $585.3591

Scenario B cao hơn A khoảng 5.01×, không phải 7×, vì nhiều conversation ở Scenario B là Booking/Complaint và được chuyển người sớm.
```

---

### Câu 4 — Có config nào AI đắt hơn human không?

```text
Không có config nào đắt hơn human baseline.
Ngay cả Premium Concierge, config đắt nhất, vẫn rẻ hơn human:
- Scenario A: rẻ hơn 4.92×
- Scenario B: rẻ hơn 4.06×
```

**Tuy nhiên:**

```text
Không nên kết luận cứ chọn Premium vì vẫn rẻ hơn human.
Premium có thể overkill nếu phần lớn khách chỉ hỏi FAQ, điểm đến hoặc thông tin cơ bản.
Cần chọn config dựa trên cả cost, quality, rủi ro và loại khách hàng.
```

---

## 3. So sánh chi tiết theo góc nhìn PM

### Budget Bot

```text
Ưu điểm:
- Rẻ nhất
- Nhanh nhất
- Dễ triển khai
- Phù hợp traffic lớn và câu hỏi đơn giản

Nhược điểm:
- Web OFF nên visa/weather có thể outdated
- Keyword classifier dễ miss multi-intent hoặc câu hỏi phức tạp
- Last 3 turns có thể quên budget, ngày đi hoặc profile khách trong conversation dài

Kết luận:
Budget Bot phù hợp làm baseline hoặc dùng trong low season, nhưng rủi ro nếu deploy cho toàn bộ traffic.
```

### Smart Mix

```text
Ưu điểm:
- Cost vẫn rất thấp so với human baseline
- Bật web search đúng intent cần fresh information: Visa và Weather
- Last 5 turns đủ tốt cho hầu hết conversation du lịch
- LLM classifier giúp nhận diện intent tốt hơn keyword

Nhược điểm:
- Đắt hơn Budget Bot
- GPT-4o-mini có thể chưa đủ mạnh cho case cực kỳ phức tạp hoặc khách VIP
- Nếu web search bị dùng quá nhiều, cost có thể tăng

Kết luận:
Smart Mix là phương án cân bằng nhất giữa cost, quality và khả năng triển khai thực tế.
```

### Premium Concierge

```text
Ưu điểm:
- Chất lượng cao nhất
- Full history giúp cá nhân hóa tốt hơn
- Web search broad giảm rủi ro outdated information
- Phù hợp khách VIP, luxury travel hoặc booking giá trị cao

Nhược điểm:
- Cost cao nhất
- Web broad có thể lãng phí với câu hỏi đơn giản
- Full history làm cost tăng mạnh ở conversation dài
- Có thể over-engineering nếu dùng cho toàn bộ traffic

Kết luận:
Premium Concierge phù hợp dùng có chọn lọc cho khách VIP hoặc high-value booking, không nên dùng mặc định cho tất cả conversation.
```

---

## 4. Key insights để đưa vào present

### Insight 1 — Rẻ nhất chưa chắc tốt nhất

```text
Budget Bot tiết kiệm nhất nhưng trade-off lớn về chất lượng.
Đặc biệt với Visa và Weather, thông tin outdated có thể làm khách mất niềm tin hoặc gây rủi ro vận hành.
```

### Insight 2 — Đắt nhất chưa chắc đáng chọn

```text
Premium Concierge cho trải nghiệm tốt nhất nhưng chi phí cao hơn Smart Mix khoảng 7.57× ở Scenario B.
Nếu phần lớn khách chỉ hỏi thông tin cơ bản, dùng Premium cho mọi người là overkill.
```

### Insight 3 — Smart Mix là điểm cân bằng tốt nhất

```text
Smart Mix vẫn tiết kiệm 97.40% ở Scenario A và 96.75% ở Scenario B so với human baseline.
Đồng thời, nó xử lý tốt hơn Budget Bot ở các intent cần thông tin mới như Visa và Weather.
```

### Insight 4 — Nên deploy theo tầng thay vì một config cứng

```text
Một hướng triển khai tốt là dùng Smart Mix làm default.
Budget Bot có thể dùng cho simple FAQ / low-risk guide.
Premium Concierge chỉ bật cho khách VIP hoặc high-value booking.
```

---

## 5. Bảng chốt để chuyển sang Recommendation

| Câu hỏi PM | Câu trả lời ngắn |
|---|---|
| Config nào rẻ nhất? | Budget Bot |
| Config nào chất lượng cao nhất? | Premium Concierge |
| Config nào cân bằng nhất? | Smart Mix |
| Config nào nên recommend? | Smart Mix |
| Vì sao không chọn Budget Bot? | Rủi ro outdated info và intent routing kém hơn |
| Vì sao không chọn Premium cho tất cả? | Cost cao và overkill cho traffic phổ thông |
| Có AI config nào đắt hơn human không? | Không |
| Knob ảnh hưởng cost nhiều nhất? | Model tier |
| Knob ảnh hưởng reliability nhiều nhất? | Web search selective + classifier |
| Rủi ro chính cần monitor? | Web search overuse, outdated visa info, quality complaint rate |

---

## 6. Draft câu nói khi present bảng

```text
Nhóm so sánh 3 config theo cùng một flow chatbot và cùng hai scenario. Budget Bot là phương án rẻ nhất, chỉ khoảng $43/tháng ở high season, nhưng rủi ro chất lượng cao vì không bật web search. Premium Concierge cho chất lượng tốt nhất nhưng cost lên khoảng $4,429/tháng ở high season, cao hơn Smart Mix khoảng 7.57 lần. Smart Mix là điểm cân bằng tốt nhất: chỉ khoảng $585/tháng ở high season, vẫn tiết kiệm 96.75% so với human baseline nhưng có web search selective cho Visa và Weather. Vì vậy nhóm sẽ recommend Smart Mix làm default config.
```
