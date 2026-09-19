# Bài học 3: Đánh giá tác nhân với Microsoft Foundry

Chào mừng bạn đến với bài học thứ ba của khóa học **"Xây dựng Tác nhân AI từ con số 0 đến Sản xuất"**!

Trong [Bài học 2](../lesson-2-agent-development/README.md) bạn đã xây dựng các tác nhân. Trong bài học này, bạn
sẽ học cách trả lời một câu hỏi khó hơn nhiều: **chúng có tốt không?** Việc phát hành một tác nhân
hoạt động thì dễ dàng; biết được nó dẫn hướng đúng cách, duy trì sự gắn kết với dữ liệu của bạn, và sử dụng các
công cụ đúng cách là điều phân biệt giữa một bản demo và một hệ thống sản xuất.

Trong bài học này, chúng ta sẽ đề cập đến:

- Tại sao việc đánh giá tác nhân lại quan trọng và nó khác với kiểm thử truyền thống như thế nào
- Sự khác biệt giữa **quan sát**, **kiểm thử khói**, và **đánh giá**
- Quy trình làm việc đa tác nhân mà chúng ta sẽ đo lường
- Các **bộ đánh giá Microsoft Foundry** tích hợp sẵn (độ liên quan, độ gắn kết, độ chính xác gọi công cụ, sử dụng đầu ra công cụ)
- Hướng dẫn từng bước quy trình đánh giá trong [`agent-evals.py`](../../../lesson-3-agent-evals/agent-evals.py)
- Cách chạy nó và đọc kết quả

---

## Tại sao phải đánh giá tác nhân?

Một bài kiểm thử đơn vị truyền thống xác nhận rằng `add(2, 2) == 4`. Tác nhân không hoạt động theo cách đó — cùng một
lời nhắc có thể tạo ra các cách diễn đạt khác nhau mỗi lần chạy, các công cụ có thể được gọi theo thứ tự khác nhau, và
"đúng" thường là vấn đề về mức độ hơn là một giá trị boolean. Bạn không thể khẳng định trên các chuỗi chính xác.

Thay vào đó, bạn đánh giá các tác nhân theo các **chiều chất lượng** sử dụng *bộ đánh giá* dựa trên mô hình (còn gọi là
"LLM-as-a-judge") cộng với các kiểm tra xác định về việc sử dụng công cụ. Điều này cho bạn biết những điều như:

- Câu trả lời có thực sự giải quyết được câu hỏi không? (**độ liên quan**)
- Câu trả lời có được hỗ trợ bởi dữ liệu truy xuất hay tác nhân đã tưởng tượng? (**độ gắn kết**)
- Tác nhân có gọi đúng công cụ với đối số đúng không? (**độ chính xác gọi công cụ**)
- Tác nhân có thực sự sử dụng kết quả mà công cụ trả về không? (**sử dụng đầu ra công cụ**)

### Ba lớp chất lượng bổ sung cho nhau

Đây không phải là các kỹ thuật cạnh tranh — một tác nhân sản xuất sử dụng cả ba:

| Lớp  | Câu hỏi nó trả lời | Chi phí | Khi nào chạy | Đề cập trong |
|-------|--------------------|------|--------------|------------|
| **Quan sát / theo dõi** | *Tác nhân đã làm gì, từng bước?* | Miễn phí (luôn bật) | Liên tục trong sản xuất | Bài học này |
| **Kiểm thử khói** | *Tác nhân có thể truy cập và tuân theo lời nhắc cơ bản không?* | Rẻ, vài giây | Mỗi lần triển khai | [Bài học 4](../lesson-4-agentdeployment/README.md#smoke-testing-the-hosted-agent-ci-gate) |
| **Đánh giá** | *Các phản hồi có **tốt** không?* | Chậm hơn, tính theo số lần dùng mô hình | Khi cần / hàng đêm / trước khi phát hành | Bài học này |

Kiểm thử khói trả lời câu hỏi "nó có bị hỏng không?"; đánh giá trả lời câu hỏi "nó có tốt không?". Bạn cần cả hai.

---

## Điều kiện tiên quyết

1. Hoàn thành [Bài học 2](../lesson-2-agent-development/README.md) (tác nhân + kho vector).
2. Một dự án **Microsoft Foundry**.
3. Xác thực **Azure CLI**: `az login`.
4. **Python 3.12+** và các phụ thuộc của khóa học đã được cài đặt:

   ```bash
   pip install -r ../requirements.txt
   ```


5. Biến môi trường (tạo một tệp `.env` trong thư mục này hoặc xuất chúng):

   | Biến | Mục đích |
   |----------|---------|
   | `FOUNDRY_PROJECT_ENDPOINT` | Điểm cuối dự án Foundry của bạn (`https://<account>.services.ai.azure.com/api/projects/<project>`). Được đọc bởi `FoundryChatClient` của các tác nhân **và** trợ giúp đánh giá. |
   | `FOUNDRY_MODEL` | Triển khai mô hình mà các **tác nhân** chạy trên đó (ví dụ `gpt-5.1`). |
   | `VECTOR_STORE_ID` | Cửa hàng vector danh bạ nhân viên được tạo trong Bài học 2 |
   | `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Triển khai mô hình được sử dụng **bởi bộ đánh giá** (mặc định là `FOUNDRY_MODEL`, sau đó là `gpt-5.1`) |

> Các tác nhân sử dụng `FoundryChatClient`, đọc cấu hình từ các biến có tiền tố `FOUNDRY_`
> (`FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL`). Trợ giúp đánh giá trên đám mây
> sử dụng SDK `azure-ai-projects` và sẽ quay lại sử dụng `FOUNDRY_PROJECT_ENDPOINT` nếu
> không thiết lập `AZURE_AI_PROJECT_ENDPOINT` — vì vậy chỉ cần hai biến `FOUNDRY_` là đủ để
> chạy toàn bộ bài học.
>
> Các bộ đánh giá tự chúng được cung cấp bởi một mô hình, nên `AZURE_AI_MODEL_DEPLOYMENT_NAME`
> kiểm soát việc triển khai nào làm công việc đánh giá — nó không nhất thiết phải là cùng mô hình mà các
> tác nhân của bạn sử dụng.

---

## Quy trình làm việc mà chúng ta đang đánh giá

Để đánh giá điều gì đó, trước hết bạn phải chạy nó. Bài học này tái sử dụng quy trình đa tác nhân **Đưa nhân viên vào công việc**: một điều phối viên **phân loại** chuyển tiếp cho ba chuyên gia.


Quy trình làm việc được xây dựng với sự điều phối **chuyển giao** của Microsoft Agent Framework. Ý tưởng chính
cho đánh giá là **mỗi lượt tác nhân được lưu trên máy chủ** và được xác định bằng một
`response_id`. Những ID đó là những gì chúng ta cung cấp cho dịch vụ đánh giá.


---

## Quy trình đánh giá, từng bước

[`agent-evals.py`](../../../lesson-3-agent-evals/agent-evals.py) triển khai một quy trình sáu bước. Dưới đây là những gì mỗi bước làm
và lý do tại sao.

### Bước 1 — Chạy quy trình và theo dõi các response ID

Quy trình được thực thi với `run_stream(...)`, và khi các sự kiện trả về dòng dữ liệu, mã ghi lại
`response_id` và `conversation_id` được tạo ra bởi mỗi tác nhân. Các phản hồi được lưu là
tài liệu gốc để đánh giá — bạn đang đánh giá các phản hồi *thực* có hình dạng như sản phẩm thật, không phải các phản hồi được tạo lại.


### Bước 2 — Tóm tắt những gì đã ghi nhận

Một bản tóm tắt nhanh in ra số lượng phản hồi mà mỗi tác nhân tạo ra, để bạn có thể xác nhận quy trình
thực sự vận hành những tác nhân mà bạn dự định đánh giá.

### Bước 3 — Lấy các phản hồi cuối cùng

Đối với từng tác nhân, `response_id` cuối cùng được truy xuất thông qua client tương thích OpenAI của dự án
(`project_client.get_openai_client().responses.retrieve(...)`) để bạn có thể xem trước
văn bản sẽ được đánh giá.

### Bước 4 — Tạo đánh giá

Một đánh giá được tạo với bốn **bộ đánh giá Foundry tích hợp sẵn**:

| Bộ đánh giá | `evaluator_name` | Đo lường điều gì |
|-----------|------------------|------------------|
| Phù hợp | `builtin.relevance` | Phản hồi có đáp ứng yêu cầu của người dùng không? |
| Độ xác thực | `builtin.groundedness` | Phản hồi có được hỗ trợ bởi dữ liệu/truyền công cụ truy xuất không (không bị ảo giác)? |
| Độ chính xác gọi công cụ | `builtin.tool_call_accuracy` | Công cụ được gọi có đúng với đối số đúng không? |
| Sử dụng kết quả công cụ | `builtin.tool_output_utilization` | Đại lý có thực sự sử dụng kết quả công cụ trong câu trả lời của nó không? |

Mỗi trình đánh giá được khởi tạo với bản triển khai được đặt tên bởi `AZURE_AI_MODEL_DEPLOYMENT_NAME`.

> **Tại sao lại là bốn yếu tố này?** Tính liên quan và độ xác thực đánh giá *chất lượng câu trả lời*; hai trình đánh giá công cụ đánh giá *hành vi đại lý* — phần mà các chỉ số NLP truyền thống hoàn toàn bỏ qua. Đối với một hệ thống đa đại lý sử dụng công cụ, các chỉ số công cụ thường là nơi ẩn các sự suy giảm thực sự.



### Bước 5 — Chạy đánh giá

Các `response_id` đã được ghi lại sẽ được truyền vào `evals.runs.create(...)` làm nguồn dữ liệu. Dịch vụ sẽ phát lại từng phản hồi đã lưu qua mọi trình đánh giá.


### Bước 6 — Giám sát và đọc kết quả

Mã sẽ liên tục kiểm tra trạng thái chạy cho đến khi nó `completed` hoặc `failed`, sau đó in ra số lượng kết quả và một **`report_url`** — một liên kết sâu vào cổng Foundry nơi bạn có thể kiểm tra điểm số theo từng chỉ số, số lượng đỗ/trượt, và các phản hồi được đánh giá riêng lẻ.



---

## Chạy thử

```bash
cd lesson-3-agent-evals
python agent-evals.py
```

Mặc định sẽ đánh giá truy vấn ví dụ đầu tiên
(`"Tôi mới đến đây! Có ai từng làm việc tại Microsoft ở đây không?"`). Hai truy vấn ví dụ thêm với đa ý định
cũng có trong `run_evaluation_workflow()` — đổi biến `query` để thử các kịch bản điều phối
kích hoạt nhiều đại lý trong một lần chạy.

Luồng console mong đợi:

```
Step 1: Running Developer Onboarding Workflow
Step 2: Response Data Summary
Step 3: Fetching Agent Responses
Step 4: Creating Evaluation
Step 5: Running Evaluation
Step 6: Monitoring Evaluation
  Status: running ...
  Evaluation completed successfully
  Report URL: https://...   <-- open this in the Foundry portal
```

---

## Khả năng quan sát và truy vết

Việc đánh giá cho bạn biết *phản hồi tốt đến mức nào*; **khả năng quan sát** cho bạn biết *điều gì đã xảy ra* để tạo ra chúng — mọi bước nhảy đại lý, gọi công cụ, đếm token, và độ trễ. Trong Microsoft Foundry,
các lần chạy đại lý phát ra các truy vết OpenTelemetry bạn có thể xem trong cổng, và Agent Framework có thể
xuất chúng sang Azure Monitor / Application Insights chỉ với một lệnh gọi duy nhất:


Sử dụng truy vết để **gỡ lỗi** điểm đánh giá xấu: khi groundedness giảm, truy vết cho bạn biết
công cụ tìm kiếm tệp không trả về gì, hoặc trả về dữ liệu mà đại lý đã bỏ qua (điều mà
chính là điểm mà sử dụng kết quả công cụ đang đánh giá).


---

## Từ "chạy" đến "tốt": cách áp dụng trong thực tế

- **Cổng tiền phát hành.** Chạy đánh giá với bộ truy vấn đại diện cố định trước khi
  nâng cấp prompt hoặc mô hình mới. So sánh điểm số với phiên bản trước đó — xem giảm điểm là
  một sự suy giảm.
- **Tín hiệu chất lượng hàng đêm.** Lên lịch đánh giá để phát hiện sự trôi dạt dữ liệu hoặc thay đổi phụ thuộc.
- **Kết hợp với kiểm thử nhanh.** [Bài kiểm thử nhanh bài 4](../lesson-4-agentdeployment/README.md#smoke-testing-the-hosted-agent-ci-gate)
  là cổng nhanh mỗi lần triển khai; đánh giá là cổng chất lượng chậm hơn và sâu hơn. Chạy cái rẻ
  trên mỗi lần gộp và cái tốn kém theo lịch hoặc trước phát hành.


---

## Ghi chú hiện đại hóa

Mẫu này đang được chuyển sang API hiện tại của Microsoft Agent Framework Foundry
(`agent_framework.foundry`). Nếu bạn đang cập nhật mã, hãy xem
[`MIGRATION-GUIDE.md`](../MIGRATION-GUIDE.md) tại thư mục gốc kho lưu trữ để biết các ánh xạ nhập khẩu và client đã xác minh trước/sau
(ví dụ `AzureAIClient` -> `FoundryChatClient`, và việc tạo công cụ hosted-tool thông qua
`client.get_file_search_tool(...)` / `client.get_mcp_tool(...)`). Các khái niệm đánh giá và
pipeline sáu bước ở trên không thay đổi bởi việc di chuyển này.

---

## Tài nguyên

- [Đánh giá mô hình và ứng dụng AI tạo sinh (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai)
- [Các trình đánh giá tích hợp cho AI tạo sinh](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Khả năng quan sát trong Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/observability)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Điều phối bàn giao đại lý](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->