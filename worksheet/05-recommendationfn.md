# 05 · Recommendation + Justification — Kết luận & Chuẩn bị Present

> Mục tiêu: Chọn config nhóm recommend deploy, giải thích bằng số liệu, nêu rủi ro và chuẩn bị phần present 5 phút.

---

## 1. Recommend config nào?

```text
Nhóm recommend Smart Mix làm default config cho chatbot AI của travel agency.
Lý do là Smart Mix cân bằng tốt nhất giữa cost, quality và reliability: chi phí vẫn thấp hơn human baseline rất nhiều, nhưng không rủi ro như Budget Bot vì có web search selective cho Visa và Weather.
Ở Scenario A, Smart Mix chỉ tốn khoảng $116.91/tháng so với human baseline $4,500/tháng.
Ở Scenario B, Smart Mix tốn khoảng $585.36/tháng so với human baseline $18,000/tháng.
```

**Kết luận ngắn:**

```text
Smart Mix là phương án phù hợp nhất để triển khai thực tế quanh năm.
```

---

## 2. Vì sao không chọn Budget Bot?

```text
Budget Bot là config rẻ nhất, chỉ khoảng $8.9964/tháng ở Scenario A và $43.0650/tháng ở Scenario B.
Tuy nhiên, Budget Bot tắt web search và dùng keyword classifier, nên có rủi ro trả lời sai hoặc thiếu cập nhật ở các câu hỏi Visa và Weather.
Với travel agency phục vụ khách quốc tế, thông tin visa hoặc thời tiết sai có thể làm giảm niềm tin, gây trải nghiệm xấu và ảnh hưởng đến khả năng booking.
```

**Kết luận:**

```text
Budget Bot phù hợp làm baseline hoặc dùng cho FAQ đơn giản, nhưng không nên làm default config cho toàn bộ chatbot.
```

---

## 3. Vì sao không chọn Premium Concierge làm default?

```text
Premium Concierge có quality cao nhất vì dùng GPT-5.5, bật web search broad và giữ full history.
Tuy nhiên, chi phí cao hơn Smart Mix khá nhiều: ở Scenario B, Premium Concierge tốn $4,429.35/tháng, trong khi Smart Mix chỉ tốn $585.36/tháng.
Tức Premium Concierge đắt hơn Smart Mix khoảng 7.57 lần ở high season.
Nếu phần lớn khách chỉ hỏi guide, FAQ, thời tiết hoặc visa cơ bản, dùng Premium cho mọi conversation là over-engineering.
```

**Kết luận:**

```text
Premium Concierge nên dùng chọn lọc cho khách VIP, luxury travel hoặc high-value booking, không nên dùng mặc định cho tất cả traffic.
```

---

## 4. So với human baseline tiết kiệm bao nhiêu?

### Smart Mix

| Scenario | AI monthly cost | Human baseline | Savings | AI rẻ hơn human |
|---|---:|---:|---:|---:|
| Scenario A — Low season | $116.9089 | $4,500 | 97.40% | 38.49× |
| Scenario B — High season | $585.3591 | $18,000 | 96.75% | 30.75× |

### Nhận xét

```text
Smart Mix tiết kiệm khoảng 97.40% ở low season và 96.75% ở high season so với human baseline.
Không có config nào trong 3 config đắt hơn human baseline.
Tuy nhiên, AI không thay thế hoàn toàn con người vì Booking và Complaint vẫn cần sales hoặc manager xử lý.
AI tạo giá trị chính ở việc trả lời 24/7, xử lý volume lớn, hỗ trợ đa ngôn ngữ và giảm tải cho nhân viên.
```

---

## 5. Khi nào nên upgrade hoặc downgrade config?

### Nên upgrade lên Premium Concierge khi:

```text
- Khách thuộc nhóm VIP hoặc luxury travel
- Conversation có giá trị booking cao
- Khách yêu cầu custom itinerary phức tạp
- Quality complaint rate tăng cao
- Bot thường xuyên không xử lý tốt các câu hỏi nhiều điều kiện
- Mùa cao điểm có nhiều khách high-value và conversion rate quan trọng hơn cost saving
```

### Nên downgrade về Budget Bot khi:

```text
- Low season
- Traffic chủ yếu là FAQ đơn giản
- Câu hỏi không cần thông tin real-time
- Doanh nghiệp muốn tối ưu chi phí tối đa
- Chatbot chỉ dùng để trả lời guide cơ bản và chuyển booking sang người thật
```

### Nên giữ Smart Mix khi:

```text
- Doanh nghiệp cần triển khai ổn định quanh năm
- Cần cân bằng giữa chi phí thấp và thông tin đủ tin cậy
- Visa và Weather vẫn là intent quan trọng cần cập nhật
- Chưa có bằng chứng rõ ràng rằng Premium tạo thêm đủ doanh thu để bù chi phí
```

---

## 6. Rủi ro lớn nhất của config được chọn

### Rủi ro chính của Smart Mix

```text
Rủi ro lớn nhất là model GPT-4o-mini có thể chưa đủ mạnh cho một số case phức tạp như luxury honeymoon, custom itinerary nhiều điều kiện hoặc visa case đặc biệt.
Ngoài ra, nếu web search bị trigger quá nhiều, chi phí có thể tăng ngoài dự kiến.
```

### Mitigation plan

```text
1. Dùng Smart Mix làm default cho phần lớn traffic.
2. Nếu intent là Visa/Weather thì bật web search selective.
3. Nếu câu hỏi có dấu hiệu high-value hoặc phức tạp, escalate lên Premium Concierge hoặc chuyển human.
4. Monitor monthly cost, web search count và quality complaint rate.
5. Đặt rule fallback: nếu confidence thấp hoặc khách nhắc đến refund/complaint/booking, chuyển người thật.
```

---

## 7. Final recommendation paragraph

```text
Nhóm recommend Smart Mix làm default config cho chatbot AI của travel agency. Config này dùng GPT-4o-mini, bật web search selective cho Visa và Weather, giữ Last 5 turns history và dùng LLM classifier để route intent tốt hơn keyword. Về chi phí, Smart Mix chỉ tốn khoảng $116.91/tháng ở Scenario A và $585.36/tháng ở Scenario B, tiết kiệm lần lượt 97.40% và 96.75% so với human baseline. Budget Bot rẻ hơn nhưng rủi ro cao vì web search OFF, đặc biệt với visa và thời tiết. Premium Concierge có chất lượng cao nhất nhưng đắt hơn Smart Mix khoảng 7.57 lần ở high season, nên chỉ phù hợp cho khách VIP hoặc high-value booking. Vì vậy, Smart Mix là lựa chọn cân bằng nhất để triển khai thực tế, còn Budget và Premium nên dùng như fallback theo từng loại traffic.
```

---

# 8. Chuẩn bị Present 5 phút

## Nhịp 0:00 – 0:30 — Base flow + 3 knobs

**Ai trình bày:** A Linh

**Nói gì:**

```text
Nhóm thiết kế chatbot AI cho travel agency Việt Nam phục vụ khách quốc tế. Flow cơ bản là tourist gửi tin nhắn, chatbot phân loại intent, route sang RAG/web search/handoff/escalate, sau đó ráp context và generate response.
Ba knobs nhóm dùng để thiết kế config là model tier, web search strategy và history management.
```

---

## Nhịp 0:30 – 1:00 — Config overview

**Ai trình bày:** Điềm

**Nói gì:**

```text
Nhóm so sánh 3 config chính.
Budget Bot dùng Gemini Flash-Lite, web OFF và Last 3 để tối ưu chi phí.
Smart Mix dùng GPT-4o-mini, web search selective cho Visa/Weather và Last 5 để cân bằng cost-quality.
Premium Concierge dùng GPT-5.5, web broad và full history để tối ưu chất lượng.
```

---

## Nhịp 1:00 – 2:00 — Cost comparison

**Ai trình bày:** Điềm

**Nói gì:**

```text
Ở Scenario A, Budget Bot tốn khoảng $8.9964/tháng, Smart Mix tốn $116.9089/tháng và Premium Concierge tốn $915.2325/tháng.
Ở Scenario B, Budget Bot tốn $43.0650/tháng, Smart Mix tốn $585.3591/tháng và Premium Concierge tốn $4,429.3500/tháng.
Tất cả đều rẻ hơn human baseline, nhưng mức chênh lệch giữa các config rất lớn.
```

---

## Nhịp 2:00 – 3:00 — Key insight

**Ai trình bày:** Điềm

**Nói gì:**

```text
Insight lớn nhất là model tier ảnh hưởng cost nhiều nhất: từ Gemini Flash-Lite lên GPT-5.5, giá input tăng 50 lần và output tăng 75 lần.
Web search cũng làm cost tăng rõ, nhưng nếu bật selective cho Visa và Weather thì khoản tăng này hợp lý vì đây là thông tin real-time.
Scenario B không tăng đúng bằng volume nhân turns vì Booking và Complaint chiếm 45%, hai intent này được chuyển người sớm nên không tính full LLM response.
```

---

## Nhịp 3:00 – 4:30 — Recommendation + justification

**Ai trình bày:** Điềm hoặc người nói tốt nhất nhóm

**Nói gì:**

```text
Nhóm recommend Smart Mix làm default config. Lý do là Smart Mix giữ chi phí thấp hơn human baseline rất nhiều nhưng vẫn giảm rủi ro ở các intent quan trọng như Visa và Weather nhờ web search selective. Ở Scenario A, Smart Mix tiết kiệm 97.40% so với human baseline; ở Scenario B, tiết kiệm 96.75%. Budget Bot rẻ nhất nhưng rủi ro outdated info cao. Premium Concierge chất lượng cao nhất nhưng đắt hơn Smart Mix khoảng 7.57 lần ở high season, nên chỉ nên dùng cho khách VIP hoặc high-value booking.
```

---

## Nhịp 4:30 – 5:00 — Hardest question prep

**Ai trình bày:** A Linh hoặc Điềm

### Câu hỏi khó dự đoán

```text
Nếu Smart Mix đã tiết kiệm hơn human rất nhiều, tại sao không dùng Premium Concierge luôn vì nó cũng vẫn rẻ hơn human?
```

### Câu trả lời sẵn

```text
Premium Concierge đúng là vẫn rẻ hơn human, nhưng PM không chỉ tối ưu theo việc rẻ hơn người mà còn phải tối ưu unit economics. Ở high season, Premium tốn $4,429.35/tháng, cao hơn Smart Mix khoảng 7.57 lần. Nếu phần lớn khách chỉ hỏi guide, visa hoặc weather cơ bản, khoản chênh này chưa chắc tạo thêm đủ booking hoặc revenue để justify. Vì vậy nhóm chọn Smart Mix làm default và chỉ dùng Premium cho khách VIP hoặc case high-value.
```

---

# 9. Q&A chuẩn bị nhanh

## Câu 1 — Knob nào ảnh hưởng cost nhiều nhất?

```text
Model tier ảnh hưởng lớn nhất. Ví dụ input price tăng từ $0.10 của Gemini Flash-Lite lên $5.00 của GPT-5.5, tức 50 lần; output price tăng từ $0.40 lên $30.00, tức 75 lần.
```

## Câu 2 — Tại sao Booking và Complaint không tính full LLM cost?

```text
Vì theo routing của bài, Booking được handoff sang sales và Complaint được escalate sang manager. Chatbot chỉ cần nhận diện intent rồi chuyển người, không nên tự xử lý toàn bộ vì có rủi ro về doanh thu, pháp lý và trải nghiệm khách hàng.
```

## Câu 3 — Tại sao Smart Mix bật web search cho Visa và Weather?

```text
Vì Visa và Weather là hai intent có tính thời điểm cao. Nếu chỉ dùng RAG cố định, chatbot có thể trả lời outdated. Web search selective tăng cost nhưng giảm rủi ro thông tin sai.
```

## Câu 4 — Có nên dùng Budget Bot không?

```text
Có, nhưng chỉ nên dùng cho low-risk FAQ hoặc low season. Không nên dùng làm default vì web OFF và keyword classifier có thể fail ở câu hỏi phức tạp hoặc multi-intent.
```

## Câu 5 — Có nên dùng Premium Concierge không?

```text
Có, nhưng dùng chọn lọc. Premium phù hợp khách VIP, luxury travel hoặc high-value booking. Không nên dùng cho toàn bộ traffic vì cost cao và dễ overkill.
```

---

# 10. Final one-slide summary

```text
Recommendation: Deploy Smart Mix as the default chatbot configuration.

Why:
- Cost remains very low compared to human baseline.
- Scenario A: $116.91/month vs $4,500 human baseline → 97.40% savings.
- Scenario B: $585.36/month vs $18,000 human baseline → 96.75% savings.
- Web search is used only where it matters most: Visa and Weather.
- Last 5 history balances context memory and token cost.
- Premium should be reserved for VIP/high-value cases; Budget should be reserved for simple FAQ or low-risk traffic.
```
