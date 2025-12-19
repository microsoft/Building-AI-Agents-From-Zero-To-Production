<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "df86a71d9a4a65d134d60f783a2aba86",
  "translation_date": "2025-12-18T14:21:21+00:00",
  "source_file": "README.md",
  "language_code": "ko"
}
-->
# 제로에서 프로덕션까지 AI 에이전트 구축

![Building AI Agents from Zero to Production](../../translated_images/repo-thumbnail.083b24afed61b6dd27a7fc53798bebe9edf688a41031163a1fca9f61c64d63ec.ko.png)

### 🌐 다국어 지원

#### GitHub Action을 통한 지원 (자동화 및 항상 최신 상태 유지)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[아랍어](../ar/README.md) | [벵골어](../bn/README.md) | [불가리아어](../bg/README.md) | [버마어 (미얀마)](../my/README.md) | [중국어 (간체)](../zh/README.md) | [중국어 (번체, 홍콩)](../hk/README.md) | [중국어 (번체, 마카오)](../mo/README.md) | [중국어 (번체, 대만)](../tw/README.md) | [크로아티아어](../hr/README.md) | [체코어](../cs/README.md) | [덴마크어](../da/README.md) | [네덜란드어](../nl/README.md) | [에스토니아어](../et/README.md) | [핀란드어](../fi/README.md) | [프랑스어](../fr/README.md) | [독일어](../de/README.md) | [그리스어](../el/README.md) | [히브리어](../he/README.md) | [힌디어](../hi/README.md) | [헝가리어](../hu/README.md) | [인도네시아어](../id/README.md) | [이탈리아어](../it/README.md) | [일본어](../ja/README.md) | [칸나다어](../kn/README.md) | [한국어](./README.md) | [리투아니아어](../lt/README.md) | [말레이어](../ms/README.md) | [말라얄람어](../ml/README.md) | [마라티어](../mr/README.md) | [네팔어](../ne/README.md) | [나이지리아 피진어](../pcm/README.md) | [노르웨이어](../no/README.md) | [페르시아어 (파르시)](../fa/README.md) | [폴란드어](../pl/README.md) | [포르투갈어 (브라질)](../br/README.md) | [포르투갈어 (포르투갈)](../pt/README.md) | [펀자브어 (구르무키)](../pa/README.md) | [루마니아어](../ro/README.md) | [러시아어](../ru/README.md) | [세르비아어 (키릴문자)](../sr/README.md) | [슬로바키아어](../sk/README.md) | [슬로베니아어](../sl/README.md) | [스페인어](../es/README.md) | [스와힐리어](../sw/README.md) | [스웨덴어](../sv/README.md) | [타갈로그어 (필리핀어)](../tl/README.md) | [타밀어](../ta/README.md) | [텔루구어](../te/README.md) | [태국어](../th/README.md) | [터키어](../tr/README.md) | [우크라이나어](../uk/README.md) | [우르두어](../ur/README.md) | [베트남어](../vi/README.md)
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

## AI 에이전트 개발 수명 주기의 기본을 가르치는 강의

[![GitHub license](https://img.shields.io/github/license/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/blob/master/LICENSE?WT.mc_id=academic-105485-koreyst)
[![GitHub contributors](https://img.shields.io/github/contributors/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/graphs/contributors/?WT.mc_id=academic-105485-koreyst)
[![GitHub issues](https://img.shields.io/github/issues/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/issues/?WT.mc_id=academic-105485-koreyst)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/pulls/?WT.mc_id=academic-105485-koreyst)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com?WT.mc_id=academic-105485-koreyst)

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

## 🌱 시작하기

이 강의는 AI 에이전트 구축 및 배포의 기본을 다루는 수업들로 구성되어 있습니다.

각 수업은 이전 수업을 기반으로 하므로 처음부터 시작하여 끝까지 차근차근 진행하는 것을 권장합니다.

AI 에이전트 주제에 대해 더 탐구하고 싶다면 [AI Agents For Beginners Course](https://aka.ms/ai-agents-beginners)를 확인하세요.

### 다른 학습자 만나기, 질문 해결하기

AI 에이전트 구축 중 막히거나 질문이 있으면 [Microsoft Foundry Discord](https://discord.gg/Kuaw3ktsu6)의 전용 Discord 채널에 참여하세요.

### 필요한 것

각 수업에는 로컬에서 실행할 수 있는 자체 코드 샘플이 있습니다. [이 저장소를 포크](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/fork)하여 자신의 복사본을 만들 수 있습니다.

이 강의는 현재 다음을 사용합니다:

- [Microsoft Agent Framework (MAF)](https://aka.ms/ai-agents-beginners/agent-framework)
- [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry)
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-foundry/models/openai)
- [Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli?view=azure-cli-latest)

시작하기 전에 이 서비스들에 접근할 수 있는지 확인하세요.

모델 호스팅 및 서비스에 관한 추가 옵션이 곧 제공될 예정입니다.

## 🗃️ 수업 목록

| **수업**         | **설명**                                                                                  |
|------------------|-------------------------------------------------------------------------------------------|
| [에이전트 설계](./lesson-1-agent-design/README.md)       | "개발자 온보딩" 에이전트 사용 사례 소개 및 효과적인 에이전트 설계 방법                      |
| [에이전트 개발](./lesson-2-agent-development/README.md)  | Microsoft Agent Framework (MAF)를 사용하여 신규 개발자 온보딩을 돕는 3개의 에이전트 생성       |
| [에이전트 평가](./lesson-3-agent-evals/README.md)        | Microsoft Foundry를 사용하여 AI 에이전트의 성능을 평가하고 개선 방법 알아보기                 |
| [에이전트 배포](./lesson-4-agent-deployment/README.md)   | 호스팅된 에이전트와 OpenAI Chatkit을 사용하여 AI 에이전트를 프로덕션에 배포하는 방법          |

## 기여하기

이 프로젝트는 기여와 제안을 환영합니다. 대부분의 기여는 기여자가 기여물 사용 권한을 실제로 보유하고 있음을 선언하는
기여자 라이선스 계약(CLA)에 동의해야 합니다. 자세한 내용은 <https://cla.opensource.microsoft.com>을 참조하세요.

풀 리퀘스트를 제출하면 CLA 봇이 자동으로 CLA 제출 필요 여부를 판단하고 PR에 적절한 표시(예: 상태 검사, 댓글)를 합니다.
봇의 지시에 따라 진행하면 됩니다. 모든 저장소에서 CLA는 한 번만 제출하면 됩니다.

이 프로젝트는 [Microsoft 오픈 소스 행동 강령](https://opensource.microsoft.com/codeofconduct/)을 채택했습니다.
자세한 내용은 [행동 강령 FAQ](https://opensource.microsoft.com/codeofconduct/faq/)를 참조하거나
추가 질문이나 의견이 있으면 [opencode@microsoft.com](mailto:opencode@microsoft.com)으로 문의하세요.

## 상표

이 프로젝트에는 프로젝트, 제품 또는 서비스의 상표나 로고가 포함될 수 있습니다. Microsoft 상표 또는 로고의
공인 사용은 [Microsoft 상표 및 브랜드 가이드라인](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general)을
준수해야 합니다.
이 프로젝트의 수정된 버전에서 Microsoft 상표 또는 로고를 사용하는 경우 혼동을 일으키거나 Microsoft 후원을 암시해서는 안 됩니다.
서드파티 상표 또는 로고 사용은 해당 서드파티의 정책을 따릅니다.

## 도움 받기

AI 앱 구축 중 막히거나 질문이 있으면 다음에 참여하세요:

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

제품 피드백이나 빌드 중 오류가 있으면 다음을 방문하세요:

[![Microsoft Foundry Developer Forum](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있으나, 자동 번역에는 오류나 부정확한 부분이 있을 수 있음을 유의해 주시기 바랍니다. 원문 문서가 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->