# การสร้างเอเจนต์ AI จากศูนย์สู่การผลิต

![Building AI Agents from Zero to Production](../../translated_images/th/repo-thumbnail.083b24afed61b6dd.webp)

### 🌐 รองรับหลายภาษา

#### สนับสนุนผ่าน GitHub Action (อัตโนมัติ & อัปเดตตลอดเวลา)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](./README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ต้องการโคลนแบบโลคอลไหม?**
>
> รีโพสนี้รวมรายการแปลภาษา 50+ ภาษา ซึ่งเพิ่มขนาดการดาวน์โหลดมาก ถ้าต้องการโคลนโดยไม่รวมการแปล ให้ใช้ sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production.git
> cd Building-AI-Agents-From-Zero-To-Production
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production.git
> cd Building-AI-Agents-From-Zero-To-Production
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> วิธีนี้จะให้ทุกอย่างที่คุณต้องการเพื่อจบคอร์สด้วยการดาวน์โหลดที่เร็วกว่ามาก
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

## คอร์สสอนพื้นฐานของวงจรชีวิตการพัฒนาเอเจนต์ AI

[![GitHub license](https://img.shields.io/github/license/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/blob/master/LICENSE?WT.mc_id=academic-105485-koreyst)
[![GitHub contributors](https://img.shields.io/github/contributors/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/graphs/contributors/?WT.mc_id=academic-105485-koreyst)
[![GitHub issues](https://img.shields.io/github/issues/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/issues/?WT.mc_id=academic-105485-koreyst)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/pulls/?WT.mc_id=academic-105485-koreyst)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com?WT.mc_id=academic-105485-koreyst)

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

## 🌱 การเริ่มต้น

คอร์สนี้ประกอบด้วยบทเรียนที่ครอบคลุมพื้นฐานของการสร้างและปรับใช้เอเจนต์ AI

แต่ละบทเรียนสร้างจากบทเรียนก่อนหน้า ดังนั้นเราขอแนะนำให้เริ่มตั้งแต่ต้นและทำตามจนจบ

หากคุณต้องการสำรวจเพิ่มเติมเกี่ยวกับหัวข้อเอเจนต์ AI คุณสามารถดู [คอร์ส AI Agents For Beginners](https://aka.ms/ai-agents-beginners)

### พบเพื่อนผู้เรียนคนอื่น ๆ และรับคำตอบสำหรับคำถามของคุณ

หากคุณติดขัดหรืมีคำถามเกี่ยวกับการสร้างเอเจนต์ AI เข้าร่วมช่องทาง Discord เฉพาะของเราใน [Microsoft Foundry Discord](https://discord.gg/Kuaw3ktsu6)

### สิ่งที่คุณต้องมี

แต่ละบทเรียนมีตัวอย่างโค้ดของตัวเองที่คุณสามารถรันได้ในเครื่อง คุณสามารถ [fork รีโพนี้](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/fork) เพื่อสร้างสำเนาของคุณเอง

คอร์สนี้ใช้เทคโนโลยีต่อไปนี้:

- [Microsoft Agent Framework (MAF)](https://aka.ms/ai-agents-beginners/agent-framework)
- [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry) — โครงการที่มีการปรับใช้โมเดล **GPT-5 series** (เช่น `gpt-5.1`) โปรด **อย่า** ใช้โมเดล GPT-4o / GPT-4.1 ที่เลิกใช้งานแล้ว
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-foundry/models/openai)
- [Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli?view=azure-cli-latest) — ลงชื่อเข้าใช้ด้วย `az login` ก่อนรันตัวอย่างใด ๆ
- **Python 3.12 ขึ้นไป**

โปรดตรวจสอบว่าคุณมีสิทธิ์เข้าถึงบริการเหล่านี้ก่อนเริ่ม

> **💰 ค่าใช้จ่าย & การล้างข้อมูล.** บทเรียนแบบลงมือปฏิบัตินี้สร้างทรัพยากร Azure จริง — โครงการ Microsoft Foundry
> การปรับใช้โมเดล, ที่เก็บข้อมูลเวกเตอร์ และ (ในบทเรียนที่ 4–6) เอเจนต์โฮสต์และกล่องเครื่องมือ
> สิ่งเหล่านี้อาจทำให้เกิดค่าใช้จ่ายในขณะที่ยังมีอยู่ เมื่อคุณทำบทเรียนเสร็จ — หรือคอร์สจบ — ให้ลบทิ้ง
> ทรัพยากรที่คุณไม่ต้องการอีก วิธีที่ง่ายที่สุดคือรวมทุกอย่างไว้ในกลุ่มทรัพยากรเฉพาะ
> และลบทั้งกลุ่มเมื่อเสร็จแล้ว:
>
> ```bash
> az group delete --name <your-resource-group> --yes --no-wait
> ```
>
> คุณยังสามารถลบเอเจนต์ ตัวเก็บเวกเตอร์ และกล่องเครื่องมือแต่ละตัวผ่านพอร์ทัล Foundry

> **หมายเหตุเกี่ยวกับโมเดล** คอร์สนี้ให้บริการโมเดลทั้งหมดผ่าน **Microsoft Foundry** ซึ่งไม่ใช้ *GitHub Models* ซึ่งจะเลิกใช้งานในวันที่ **30 กรกฎาคม 2026** — Microsoft Foundry เป็นเส้นทางการย้ายอย่างเป็นทางการ หากคุณมีโค้ดเก่าที่เรียกใช้ GitHub Models ให้ชี้ไปที่การปรับใช้โมเดล Foundry แทน




ตัวเลือกเพิ่มเติมเกี่ยวกับโฮสต์และบริการโมเดลกำลังจะมาเร็ว ๆ นี้

## 🗃️ บทเรียน

| **บทเรียน**         | **คำอธิบาย**                                                                                  |
|--------------------|--------------------------------------------------------------------------------------------------|
| [Agent Design](./lesson-1-agent-design/README.md)       | การแนะนำการใช้งานเอเจนต์ "Developer Onboarding" และวิธีออกแบบเอเจนต์ที่มีประสิทธิภาพ  |
| [Agent Development](./lesson-2-agent-development/README.md)  | ใช้ Microsoft Agent Framework (MAF) สร้างชุดเอเจนต์เฉพาะทางเพื่อช่วยนักพัฒนามือใหม่เริ่มต้น       |
| [Agent Evaluations](./lesson-3-agent-evals/README.md)  | ใช้ Microsoft Foundry เพื่อดูว่าเอเจนต์ AI ของเราทำงานดีแค่ไหนและวิธีปรับปรุง               |
| [Agent Deployment](./lesson-4-agentdeployment/README.md)   | ใช้เอเจนต์โฮสต์ Microsoft Foundry และ OpenAI ChatKit เพื่อดูวิธีการปรับใช้เอเจนต์ AI ในการผลิต    |
| [Production Hosted Agents](./lesson-5-hosted-agents-production/README.md)   | นำเอเจนต์ที่โฮสต์ไปสู่การผลิตในองค์กร: เอเจนต์โฮสต์กับ Capability Hosts, นำที่เก็บข้อมูล ความจำ และการกำกับดูแลของคุณเองมาใช้   |
| [Microsoft Toolbox](./lesson-6-toolbox/README.md)   | กำหนดเครื่องมือครั้งเดียวและควบคุมส่วนกลาง: สร้างกล่องเครื่องมือ ใช้จากเอเจนต์ผ่านจุดเชื่อมต่อ MCP เดียว และจัดการเวอร์ชันเครื่องมืออย่างปลอดภัย |
| [Multi-Agent & A2A](./lesson-7-multi-agent-a2a/README.md)   | ร้อยเรียงเอเจนต์เป็นบริการเครือข่าย: เปิดเผยเอเจนต์ผ่านโปรโตคอล Agent-to-Agent (A2A) แบบเปิด และใช้เอเจนต์จากระยะไกลเป็นเพื่อนร่วมงาน  |


## 🎒 คอร์สอื่น ๆ

ทีมงานของเรามีคอร์สอื่น ๆ ให้เลือกชม! ดูได้ที่:

<!-- CO-OP TRANSLATOR OTHER COURSES START -->
### LangChain
[![LangChain4j for Beginners](https://img.shields.io/badge/LangChain4j%20for%20Beginners-22C55E?style=for-the-badge&&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchain4j-for-beginners)
[![LangChain.js for Beginners](https://img.shields.io/badge/LangChain.js%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://aka.ms/langchainjs-for-beginners?WT.mc_id=m365-94501-dwahlin)
[![LangChain for Beginners](https://img.shields.io/badge/LangChain%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=0553D6)](https://github.com/microsoft/langchain-for-beginners?WT.mc_id=m365-94501-dwahlin)
---

### Azure / Edge / MCP / Agents
[![AZD for Beginners](https://img.shields.io/badge/AZD%20for%20Beginners-0078D4?style=for-the-badge&labelColor=E5E7EB&color=0078D4)](https://github.com/microsoft/AZD-for-beginners?WT.mc_id=academic-105485-koreyst)
[![Edge AI for Beginners](https://img.shields.io/badge/Edge%20AI%20for%20Beginners-00B8E4?style=for-the-badge&labelColor=E5E7EB&color=00B8E4)](https://github.com/microsoft/edgeai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![MCP for Beginners](https://img.shields.io/badge/MCP%20for%20Beginners-009688?style=for-the-badge&labelColor=E5E7EB&color=009688)](https://github.com/microsoft/mcp-for-beginners?WT.mc_id=academic-105485-koreyst)
[![AI Agents for Beginners](https://img.shields.io/badge/AI%20Agents%20for%20Beginners-00C49A?style=for-the-badge&labelColor=E5E7EB&color=00C49A)](https://github.com/microsoft/ai-agents-for-beginners?WT.mc_id=academic-105485-koreyst)

---
 
### Generative AI Series

[![Generative AI for Beginners](https://img.shields.io/badge/Generative%20AI%20for%20Beginners-8B5CF6?style=for-the-badge&labelColor=E5E7EB&color=8B5CF6)](https://github.com/microsoft/generative-ai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![Generative AI (.NET)](https://img.shields.io/badge/Generative%20AI%20(.NET)-9333EA?style=for-the-badge&labelColor=E5E7EB&color=9333EA)](https://github.com/microsoft/Generative-AI-for-beginners-dotnet?WT.mc_id=academic-105485-koreyst)
[![Generative AI (Java)](https://img.shields.io/badge/Generative%20AI%20(Java)-C084FC?style=for-the-badge&labelColor=E5E7EB&color=C084FC)](https://github.com/microsoft/generative-ai-for-beginners-java?WT.mc_id=academic-105485-koreyst)
[![Generative AI (JavaScript)](https://img.shields.io/badge/Generative%20AI%20(JavaScript)-E879F9?style=for-the-badge&labelColor=E5E7EB&color=E879F9)](https://github.com/microsoft/generative-ai-with-javascript?WT.mc_id=academic-105485-koreyst)

---
 
### การเรียนรู้หลัก
[![ML for Beginners](https://img.shields.io/badge/ML%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=22C55E)](https://aka.ms/ml-beginners?WT.mc_id=academic-105485-koreyst)
[![Data Science for Beginners](https://img.shields.io/badge/Data%20Science%20for%20Beginners-84CC16?style=for-the-badge&labelColor=E5E7EB&color=84CC16)](https://aka.ms/datascience-beginners?WT.mc_id=academic-105485-koreyst)
[![AI for Beginners](https://img.shields.io/badge/AI%20for%20Beginners-A3E635?style=for-the-badge&labelColor=E5E7EB&color=A3E635)](https://aka.ms/ai-beginners?WT.mc_id=academic-105485-koreyst)
[![Cybersecurity for Beginners](https://img.shields.io/badge/Cybersecurity%20for%20Beginners-F97316?style=for-the-badge&labelColor=E5E7EB&color=F97316)](https://github.com/microsoft/Security-101?WT.mc_id=academic-96948-sayoung)
[![Web Dev for Beginners](https://img.shields.io/badge/Web%20Dev%20for%20Beginners-EC4899?style=for-the-badge&labelColor=E5E7EB&color=EC4899)](https://aka.ms/webdev-beginners?WT.mc_id=academic-105485-koreyst)
[![IoT for Beginners](https://img.shields.io/badge/IoT%20for%20Beginners-14B8A6?style=for-the-badge&labelColor=E5E7EB&color=14B8A6)](https://aka.ms/iot-beginners?WT.mc_id=academic-105485-koreyst)
[![XR Development for Beginners](https://img.shields.io/badge/XR%20Development%20for%20Beginners-38BDF8?style=for-the-badge&labelColor=E5E7EB&color=38BDF8)](https://github.com/microsoft/xr-development-for-beginners?WT.mc_id=academic-105485-koreyst)

---
 
### ชุด Copilot
[![Copilot for AI Paired Programming](https://img.shields.io/badge/Copilot%20for%20AI%20Paired%20Programming-FACC15?style=for-the-badge&labelColor=E5E7EB&color=FACC15)](https://aka.ms/GitHubCopilotAI?WT.mc_id=academic-105485-koreyst)
[![Copilot for C#/.NET](https://img.shields.io/badge/Copilot%20for%20C%23/.NET-FBBF24?style=for-the-badge&labelColor=E5E7EB&color=FBBF24)](https://github.com/microsoft/mastering-github-copilot-for-dotnet-csharp-developers?WT.mc_id=academic-105485-koreyst)
[![Copilot Adventure](https://img.shields.io/badge/Copilot%20Adventure-FDE68A?style=for-the-badge&labelColor=E5E7EB&color=FDE68A)](https://github.com/microsoft/CopilotAdventures?WT.mc_id=academic-105485-koreyst)
<!-- CO-OP TRANSLATOR OTHER COURSES END -->

## การมีส่วนร่วม

โปรเจกต์นี้ยินดีต้อนรับการมีส่วนร่วมและคำแนะนำ ส่วนใหญ่การมีส่วนร่วมจะต้องให้คุณตกลง
ข้อตกลงสิทธิ์ผู้ร่วม (Contributor License Agreement - CLA) ที่ระบุว่าคุณมีสิทธิ์และได้ให้สิทธิ์กับเรา
ในการใช้ผลงานที่คุณมีส่วนร่วม รายละเอียดเพิ่มเติม ดูได้ที่ <https://cla.opensource.microsoft.com>.

เมื่อคุณส่งคำขอดึง (pull request) ระบบหุ่นยนต์ CLA จะตรวจสอบโดยอัตโนมัติว่าคุณต้องจัดเตรียม
CLA หรือไม่ และประทับสถานะที่เหมาะสมกับ PR (เช่น การตรวจสอบสถานะ, ความเห็น) เพียงปฏิบัติตามคำแนะนำ
ที่ระบบหุ่นยนต์ให้มา คุณจะต้องทำเพียงครั้งเดียวสำหรับทุกรีโปที่ใช้ CLA ของเรา

โปรเจกต์นี้ได้นำ [หลักเกณฑ์ประพฤติปฏิบัติของ Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/) มาใช้
สำหรับข้อมูลเพิ่มเติม ดู [คำถามที่พบบ่อยเกี่ยวกับหลักเกณฑ์ประพฤติปฏิบัติ (Code of Conduct FAQ)](https://opensource.microsoft.com/codeofconduct/faq/) หรือ
ติดต่อที่ [opencode@microsoft.com](mailto:opencode@microsoft.com) หากมีคำถามหรือข้อคิดเห็นเพิ่มเติม

## เครื่องหมายการค้า

โปรเจกต์นี้อาจมีเครื่องหมายการค้าหรือโลโก้ของโปรเจกต์ ผลิตภัณฑ์ หรือบริการ การใช้งานเครื่องหมายการค้าหรือโลโก้ของ Microsoft
ที่ได้รับอนุญาตจะต้องเป็นไปตามและปฏิบัติตาม
[แนวทางเครื่องหมายการค้าและแบรนด์ของ Microsoft](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general)
การใช้เครื่องหมายการค้าหรือโลโก้ของ Microsoft ในเวอร์ชันที่แก้ไขดัดแปลงของโปรเจกต์นี้ต้องไม่ทำให้เกิดความสับสนหรือละเมิดต่อผู้สนับสนุนของ Microsoft
การใช้เครื่องหมายการค้าหรือโลโก้ของบุคคลที่สามจะต้องเป็นไปตามนโยบายของบุคคลที่สามเหล่านั้น

## ขอความช่วยเหลือ

หากคุณติดปัญหาหรือมีคำถามเกี่ยวกับการสร้างแอป AI เข้าร่วมได้ที่:

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

หากคุณมีข้อเสนอแนะเกี่ยวกับผลิตภัณฑ์หรือพบข้อผิดพลาดขณะสร้างโปรเจกต์ เยี่ยมชม:

[![Microsoft Foundry Developer Forum](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->