<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:30:17+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "ko"
}
-->
# `azd init` 후 다음 단계

## 목차

1. [다음 단계](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [인프라 프로비저닝](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [인프라 수정](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [프로덕션 준비](../../../../lesson-4-agentdeployment/hosted-agent)
2. [청구](../../../../lesson-4-agentdeployment/hosted-agent)
3. [문제 해결](../../../../lesson-4-agentdeployment/hosted-agent)

## 다음 단계

### 인프라 프로비저닝 및 애플리케이션 코드 배포

`azd up`을 실행하여 인프라를 프로비저닝하고 한 번에 Azure에 배포하세요(또는 `azd provision`을 실행한 후 `azd deploy`를 실행하여 작업을 별도로 수행할 수 있습니다). 나열된 서비스 엔드포인트를 방문하여 애플리케이션이 실행 중인지 확인하세요!

문제가 발생하면 [문제 해결](../../../../lesson-4-agentdeployment/hosted-agent)을 참조하세요.

### 인프라 수정

인프라와 애플리케이션을 설명하기 위해 `azure.yaml`이 추가되었습니다. 이 파일에는 애플리케이션을 설명하는 모든 서비스와 리소스가 포함되어 있습니다.

새 서비스나 리소스를 추가하려면 `azd add`를 실행하세요. 필요에 따라 `azure.yaml` 파일을 직접 편집할 수도 있습니다.

### 프로덕션 준비

필요할 때 `azd`는 메모리 내에서 필요한 인프라를 코드로 생성하고 사용합니다. `azd`가 사용하는 인프라를 보고 수정하려면 `azd infra gen`을 실행하여 디스크에 저장하세요.

이 작업을 수행하면 몇 가지 추가 디렉터리가 생성됩니다:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*참고*: 인프라를 디스크에 생성한 후에는 해당 파일들이 azd의 진실 소스가 됩니다. `azure.yaml`에 대한 변경 사항(예: `azd add`를 통해)이 인프라에 반영되려면 다시 `azd infra gen`으로 재생성해야 합니다. 파일을 덮어쓰기 전에 프롬프트가 표시됩니다. `--force`를 전달하면 프롬프트 없이 `azd infra gen`이 파일을 강제로 덮어씁니다.

마지막으로 `azd pipeline config`를 실행하여 CI/CD 배포 파이프라인을 구성하세요.

## 청구

Azure 포털의 *비용 관리 + 청구* 페이지를 방문하여 현재 지출을 추적하세요. 청구 방식과 Azure 구독에서 발생하는 비용을 모니터링하는 방법에 대한 자세한 내용은 [청구 개요](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing)를 참조하세요.

## 문제 해결

Q: 나열된 서비스 엔드포인트를 방문했는데 빈 페이지, 일반 환영 페이지 또는 오류 페이지가 표시됩니다.

A: 서비스가 시작하지 못했거나 일부 구성 설정이 누락되었을 수 있습니다. 자세히 조사하려면:

1. `azd show`를 실행하세요. "Azure Portal에서 보기" 아래의 링크를 클릭하여 Azure 포털에서 리소스 그룹을 엽니다.
2. 배포에 실패한 특정 Container App 서비스를 찾습니다.
3. "문제가 있는 리비전" 아래에서 실패한 리비전을 클릭합니다.
4. 실패 유형에 대한 자세한 정보를 보려면 "상태 세부 정보"를 검토하세요.
5. 오류를 식별하기 위해 콘솔 로그 스트림과 시스템 로그 스트림의 로그 출력을 관찰하세요.
6. 로그가 디스크에 기록된 경우, 탐색 메뉴의 *콘솔*을 사용하여 실행 중인 컨테이너 내 셸에 연결하세요.

추가 문제 해결 정보는 [Container Apps 문제 해결](https://learn.microsoft.com/azure/container-apps/troubleshooting)을 방문하세요.

### 추가 정보

`azd` 프로젝트 설정에 대한 추가 정보는 공식 [문서](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert)를 참조하세요.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있으나, 자동 번역에는 오류나 부정확성이 포함될 수 있음을 유의하시기 바랍니다. 원문 문서가 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역 사용으로 인한 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->