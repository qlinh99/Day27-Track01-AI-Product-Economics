# 00 · User Journey Simulation — Đóng vai Tourist

> **Mục tiêu**: Trước khi tính chi phí, nhóm phải hình dung được khách hàng thật sự hỏi gì, hỏi như thế nào, và 1 conversation thực tế trông ra sao.
>
> **Thời gian**: 8 phút (trong 15 phút phần Setup)

---

## Bước 1 — Mỗi người đóng vai 1 tourist

### Tourist #1 (Tên thành viên: Hứa Quang Linh)

```text
1. I am visiting Vietnam for the first time in July. Should I start in Hanoi or Ho Chi Minh City?
2. Do US citizens need a visa for a 12-day trip to Vietnam?
3. Can you suggest a 7-day itinerary for Hanoi, Ha Long Bay, and Hoi An?
4. What is the weather like in Da Nang next week?
5. Is it safe to take overnight trains in Vietnam as a solo female traveler?
6. Can I book a private airport transfer from Noi Bai to my hotel through your company?
7. I am from the UK and want to stay 45 days. What visa option should I choose?
8. Are there any festivals or public holidays in Vietnam during late January?
9. Can you recommend a less crowded beach destination than Phu Quoc?
```

### Tourist #2 (Tên thành viên: Dương Khoa Điềm)

```text
1. We are a family of four from Australia. What kid-friendly tours do you recommend in Vietnam?
2. What is the best time of year to visit Sapa without too much rain?
3. Can your team help us book a Mekong Delta day tour from Ho Chi Minh City?
4. Are there any food tours that can handle peanut allergies?
5. How much should we budget per day for a comfortable family trip?
6. I paid for a tour but have not received confirmation. Can someone check this now?
7. I only have 3 days in Central Vietnam. Should I choose Hue, Hoi An, or Da Nang?
8. Can I customize a luxury honeymoon package with boutique hotels?
9. My driver was late and I missed part of the tour. I want to complain to a manager.
```

---

## Bước 2 — Gom lại và phân loại

| # | Câu hỏi (1 dòng) | Intent thuộc loại nào | Cần bao nhiêu lượt chat để xong? | Bot trả lời hay chuyển người? |
|---|---|---|---|---|
| 1 | Do US citizens need a visa for a 12-day trip to Vietnam? | Visa/Policy | 3 | Bot |
| 2 | I am from the UK and want to stay 45 days. What visa option should I choose? | Visa/Policy | 4 | Bot |
| 3 | Can you suggest a 7-day itinerary for Hanoi, Ha Long Bay, and Hoi An? | Điểm đến/Guide | 5 | Bot |
| 4 | I only have 3 days in Central Vietnam. Should I choose Hue, Hoi An, or Da Nang? | Điểm đến/Guide | 4 | Bot |
| 5 | Can you recommend a less crowded beach destination than Phu Quoc? | Điểm đến/Guide | 3 | Bot |
| 6 | What is the weather like in Da Nang next week? | Thời tiết/Sự kiện | 2 | Bot |
| 7 | Are there any festivals or public holidays in Vietnam during late January? | Thời tiết/Sự kiện | 3 | Bot |
| 8 | Can I book a private airport transfer from Noi Bai to my hotel through your company? | Tour/Booking | 1 | Người |
| 9 | Can I customize a luxury honeymoon package with boutique hotels? | Tour/Booking | 1 | Người |
| 10 | My driver was late and I missed part of the tour. I want to complain to a manager. | Khiếu nại | 1 | Người |

---

## Bước 3 — Rút insight cho nhóm

**Tổng số câu hỏi nhóm gom được**:

```text
18 câu hỏi gốc; chọn 10 câu tiêu biểu để phân loại trong bảng.
```

**Phân bố intent thực tế của nhóm** (% mỗi intent):

```text
Guide: 30%
Visa: 20%
Weather: 20%
Booking: 20%
Khiếu nại: 10%
```

**Số lượt chat trung bình để xong 1 chủ đề**:

```text
Info/guide thường cần 3-5 lượt vì phải hỏi thêm budget, thời gian, sở thích.
Visa/policy cần khoảng 3-4 lượt vì phải xác nhận quốc tịch, số ngày ở lại, số lần nhập cảnh.
Weather/event cần 2-3 lượt nếu có web search.
Booking và khiếu nại chỉ cần 1 lượt để nhận diện rồi chuyển người phụ trách.
```

**Đối chiếu với đề bài** (Scenario A = 4 lượt, Scenario B = 7 lượt):

```text
Hợp lý vì các câu hỏi info phổ biến rơi vào khoảng 3-5 lượt, gần Scenario A.
Scenario B phù hợp với conversation phức tạp hơn: khách hỏi itinerary, budget, visa, thời tiết và thay đổi yêu cầu trong cùng một cuộc chat.
Booking và khiếu nại không nên tính như full LLM conversation vì route sang người thật gần như ngay lập tức.
```

**Insight bất ngờ — điều gì nhóm chỉ hiểu sau khi đóng vai?**

```text
Tourist thường trộn nhiều intent trong cùng một hành trình: họ hỏi itinerary nhưng sẽ kéo theo weather, visa, budget và booking.
Các intent cần thông tin mới như visa/weather tạo rủi ro chất lượng lớn hơn guide thông thường, nên không nên chỉ tối ưu theo giá model.
```

---

## Bảng kiểm trước khi sang file tiếp theo

- [x] Mỗi người trong nhóm đã viết ≥5 câu hỏi tourist
- [x] Đã gom + phân loại intent cho ≥10 câu
- [x] Đã có phân bố intent % của nhóm
- [x] Có ít nhất 1 insight về cách tourist thật sự dùng chatbot

Xong → mở `01-base-flow.md`.
