<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:39:41+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "vi"
}
-->
# Các bước tiếp theo sau `azd init`

## Mục lục

1. [Các bước tiếp theo](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Cung cấp hạ tầng](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Chỉnh sửa hạ tầng](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Đưa đến trạng thái sẵn sàng sản xuất](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Thanh toán](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Khắc phục sự cố](../../../../lesson-4-agentdeployment/hosted-agent)

## Các bước tiếp theo

### Cung cấp hạ tầng và triển khai mã ứng dụng

Chạy `azd up` để cung cấp hạ tầng và triển khai lên Azure trong một bước (hoặc chạy `azd provision` rồi `azd deploy` để thực hiện các tác vụ riêng biệt). Truy cập các điểm cuối dịch vụ được liệt kê để xem ứng dụng của bạn đang hoạt động!

Để khắc phục sự cố, xem [khắc phục sự cố](../../../../lesson-4-agentdeployment/hosted-agent).

### Chỉnh sửa hạ tầng

Để mô tả hạ tầng và ứng dụng, `azure.yaml` đã được thêm vào. Tệp này chứa tất cả các dịch vụ và tài nguyên mô tả ứng dụng của bạn.

Để thêm dịch vụ hoặc tài nguyên mới, chạy `azd add`. Bạn cũng có thể chỉnh sửa trực tiếp tệp `azure.yaml` nếu cần.

### Đưa đến trạng thái sẵn sàng sản xuất

Khi cần, `azd` tạo ra hạ tầng dưới dạng mã trong bộ nhớ và sử dụng nó. Nếu bạn muốn xem hoặc chỉnh sửa hạ tầng mà `azd` sử dụng, chạy `azd infra gen` để lưu nó vào đĩa.

Nếu bạn làm điều này, một số thư mục bổ sung sẽ được tạo:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Lưu ý*: Khi bạn đã tạo hạ tầng ra đĩa, các tệp đó là nguồn sự thật cho azd. Bất kỳ thay đổi nào được thực hiện trong `azure.yaml` (chẳng hạn như qua `azd add`) sẽ không được phản ánh trong hạ tầng cho đến khi bạn tạo lại nó bằng `azd infra gen` một lần nữa. Nó sẽ nhắc bạn trước khi ghi đè tệp. Bạn có thể sử dụng `--force` để buộc `azd infra gen` ghi đè các tệp mà không cần nhắc.

Cuối cùng, chạy `azd pipeline config` để cấu hình một pipeline triển khai CI/CD.

## Thanh toán

Truy cập trang *Quản lý Chi phí + Thanh toán* trong Azure Portal để theo dõi chi tiêu hiện tại. Để biết thêm thông tin về cách bạn được tính phí và cách bạn có thể giám sát chi phí phát sinh trong các đăng ký Azure của mình, hãy truy cập [tổng quan về thanh toán](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Khắc phục sự cố

Hỏi: Tôi đã truy cập điểm cuối dịch vụ được liệt kê, nhưng tôi thấy trang trắng, trang chào mừng chung hoặc trang lỗi.

Đáp: Dịch vụ của bạn có thể đã không khởi động được, hoặc có thể thiếu một số cài đặt cấu hình. Để điều tra thêm:

1. Chạy `azd show`. Nhấp vào liên kết dưới "Xem trong Azure Portal" để mở nhóm tài nguyên trong Azure Portal.
2. Điều hướng đến dịch vụ Container App cụ thể đang gặp sự cố triển khai.
3. Nhấp vào phiên bản bị lỗi dưới "Các phiên bản có sự cố".
4. Xem "Chi tiết trạng thái" để biết thêm thông tin về loại lỗi.
5. Quan sát các đầu ra nhật ký từ luồng nhật ký Console và luồng nhật ký Hệ thống để xác định lỗi.
6. Nếu nhật ký được ghi vào đĩa, sử dụng *Console* trong điều hướng để kết nối với shell bên trong container đang chạy.

Để biết thêm thông tin khắc phục sự cố, truy cập [Khắc phục sự cố Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Thông tin bổ sung

Để biết thêm thông tin về cách thiết lập dự án `azd` của bạn, hãy truy cập tài liệu chính thức của chúng tôi tại [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố từ chối trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ gốc của nó nên được coi là nguồn chính xác và đáng tin cậy. Đối với các thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp do con người thực hiện. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->