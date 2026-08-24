# జీరో నుండి ప్రొడక్షన్ వరకు AI ఏజెంట్ల నిర్మాణం

![జీరో నుండి ప్రొడక్షన్ వరకు AI ఏజెంట్ల నిర్మాణం](../../translated_images/te/repo-thumbnail.083b24afed61b6dd.webp)

### 🌐 బహుభాషా మద్దతు

#### గిట్‌హబ్ యాక్షన్ ద్వారా మద్దతు (స్వయంచాలక మరియు ఎల్లప్పుడూ ప 최신)  

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](./README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **స్థానికంగా క్లోన్ చేయాలనుకుంటున్నారా?**
>
> ఈ రిపొజిటరీ 50+ భాషా అనువాదాలను కలిగి ఉంది, ఇది డౌన్‌లోడ్ పరిమాణాన్ని గణనీయంగా పెంచుతుంది. అనువాదాలు లేకుండా క్లోన్ చేయాలంటే, స్పార్స్ చెకౌట్ ఉపయోగించండి:
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
> ఇది కోర్స్‌ను పూర్తి చేసేందుకు మీరు అవసరమైన అన్ని విషయాలను వేగవంతమైన డౌన్‌లోడ్‌తో అందిస్తుంది.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

## AI ఏజెంట్ అభివృద్ధి జీవన చక్రం యొక్క మూలాలను నేర్పించే కోర్స్

[![GitHub license](https://img.shields.io/github/license/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/blob/master/LICENSE?WT.mc_id=academic-105485-koreyst)
[![GitHub contributors](https://img.shields.io/github/contributors/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/graphs/contributors/?WT.mc_id=academic-105485-koreyst)
[![GitHub issues](https://img.shields.io/github/issues/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/issues/?WT.mc_id=academic-105485-koreyst)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/pulls/?WT.mc_id=academic-105485-koreyst)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com?WT.mc_id=academic-105485-koreyst)

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

## 🌱 ప్రారంభం

ఈ కోర్స్ AI ఏజెంట్లను నిర్మించటం మరియు విడుదల చేయటం యొక్క మూలాలను కవర్ చేసే పాఠాలు కలిగి ఉంది.

ప్రతి పాఠం ముందటి పాఠంపై ఆధారపడి ఉంటుంది, కాబట్టి ప్రారంభం నుండి ప్రారంభించి చివరి వరకు కొనసాగాలని మేము సలహా ఇస్తున్నాం.

మీరు AI ఏజెంట్ అంశాల గురించి మరింత అన్వేషించాలనుకుంటే, [AI Agents For Beginners Course](https://aka.ms/ai-agents-beginners) చూడవచ్చు.

### ఇతర అభ్యర్థులని కలవండి, మీ ప్రశ్నలకు సమాధానం పొందండి

మీరు అడ్డుకుపడినట్లయితే లేదా AI ఏజెంట్ల నిర్మాణంపై ఏవైనా ప్రశ్నలు ఉంటే, మా ప్రత్యేక డిస్కార్డ్ చానెల్ Microsoft Foundry Discordలో కలిసిపోండి ([Microsoft Foundry Discord](https://discord.gg/Kuaw3ktsu6)).

### మీరు కావాల్సింది


ప్రతి పాఠానికి మీరు స్థానికంగా నడుపుకోగల స్వంత కోడ్ నమూనా ఉంటుంది. మీరు [ఈ రిపోను ఫోర్క్ చేయవచ్చు](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/fork) మీ స్వంత కాపీ సృష్టించుకోవడానికి.  

ఈ కోర్స్ ప్రస్తుతం క్రింది వాటిని ఉపయోగిస్తోంది:  

- [Microsoft Agent Framework (MAF)](https://aka.ms/ai-agents-beginners/agent-framework)  
- [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry) — ఒక ప్రాజెక్ట్ అనుసరించి **GPT-5 సిరీస్** మోడల్ (ఉదాహరణకు `gpt-5.1`). పూర్తి అయిన GPT-4o / GPT-4.1 మోడల్స్ ని **వినియోగించకండి**.  
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-foundry/models/openai)  
- [Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli?view=azure-cli-latest) — ఏ నమూనా నడపక ముందు `az login` తో సైన్ ఇన్ అవ్వండి  
- **Python 3.12 లేదా తదుపరి**  

ప్రారంభించడానికి ముందు ఈ సేవలకు మీకు యాక్సెస్ ఉన్నదని నిర్ధారించుకోండి.  

> **💰 ఖర్చు & శుభ్రపరిచడం.** ఈ ప్రాక్టికల్ పాఠాలు వాస్తవ Azure వనరులు సృష్టిస్తాయి — Microsoft Foundry  
> ప్రాజెక్టు, మోడల్ డిప్లాయ్‌మెంట్, వెక్టర్ స్టోర్, మరియు (పాఠాలు 4–6లో) హోస్టెడ్ ఏజెంట్లు మరియు టూల్‌బాక్స్‌లు.  
> ఇవి ఉన్న వాళ్లతో ఖర్చు వస్తుంటుంది. మీరు పాఠం లేదా కోర్స్ పూర్తయిన తర్వాత —  
> మీరు అవసరం లేని వనరులు తొలగించండి. సరళమైన పద్ధతి ఏమిటంటే అన్ని వనరులు ఒక ప్రత్యేక రిసోర్స్ గ్రూపులో ఉంచి,  
> మీరు పూర్తయినప్పుడు ఆ గ్రూపును మొత్తం తొలగించడం.  
>
> ```bash
> az group delete --name <your-resource-group> --yes --no-wait
> ```
>
> మీరు Foundry పోర్టల్ నుండి వ్యక్తిగత ఏజెంట్లు, వెక్టర్ స్టోర్‌లు, టూల్‌బాక్స్‌లను కూడా తొలగించవచ్చు.  

> **మోడల్స్ గురించి గమనిక.** ఈ కోర్స్ అన్ని మోడల్స్ **Microsoft Foundry** ద్వారా అందజేస్తుంది. ఇది **GitHub Models** ను ఉపయోగించదు, ఇది **Jూలై 30, 2026** న రిటైర్ అవుతుంది — Microsoft Foundry అటు అధికారిక మార్గం. మీరు పాత కోడ్ ఉపయోగిస్తే, దాన్ని GitHub Models కంటే వుండిపోతే, ప్రతి దగ్గర Foundry మోడల్ డిప్లాయ్‌మెంట్ పాయింట్ చేయండి.  




మోడల్ హోస్టింగ్ మరియు సేవల గురించి మరిన్ని ఎంపికలు త్వరలో అందుబాటులో ఉంటాయి.  

## 🗃️ పాఠాలు  

| **పాఠం**         | **వివరణ**                                                                                  |  
|--------------------|--------------------------------------------------------------------------------------------------|  
| [ఏజెంట్ డిజైన్](./lesson-1-agent-design/README.md)       | మన "డెవలపర్ ఆన్‌బోర్డింగ్" ఏజెంట్ వాడుక కేస్ పరిచయం మరియు సమర్ధవంతమైన ఏజెంట్ల రూపకల్పన ఎలా చేయాలో  |  
| [ఏజెంట్ అభివృద్ధి](./lesson-2-agent-development/README.md)  | Microsoft Agent Framework (MAF) ఉపయోగించి కొత్త డెవలపర్లకు సహాయపడే ప్రత్యేక ఏజెంట్ల సమూహాన్ని నిర్మించండి.       |  
| [ఏజెంట్ మూల్యాంకనాలు](./lesson-3-agent-evals/README.md)  | Microsoft Foundry ఉపయోగించి మన AI ఏజెంట్లు ఎంతవరకు పనితీరు చూపుతున్నాయో తెలుసుకోండి మరియు అభివృద్ధి చేయండి. |  
| [ఏజెంట్ డిప్లాయ్‌మెంట్](./lesson-4-agentdeployment/README.md)   | Microsoft Foundry హోస్టెడ్ ఏజెంట్లు మరియు OpenAI ChatKit ఉపయోగించి AI ఏజెంట్‌ను ప్రొడక్షన్‌లో ఎలా అమలు చేయాలో తెలుసుకోండి.       |  
| [ప్రొడక్షన్ హోస్టెడ్ ఏజెంట్లు](./lesson-5-hosted-agents-production/README.md)   | హోస్టెడ్ ఏజెంట్‌ను ఎంటర్ప్రైజ్ ప్రొడక్షన్‌కు తీసుకెళ్లండి: Hosted Agents vs Capability Hosts, మీ తదుపరి స్టోరేజ్, మెమోరీ, గ‌వ‌ర్నెన్స్.       |  
| [Microsoft టూల్‌బాక్స్](./lesson-6-toolbox/README.md)   | సాధనాలు ఒకసారి నిర్వచించి వాటిని కేంద్రంగా పాలించు: toolbox నిర్మించండి, ఒక ఏజెంట్ నుండి ఒక MCP ఎండ్పాయింట్ ద్వారా ఉపయోగించండి, మరియు సాధనల వెర్షన్‌ను భద్రపరచండి.       |  
| [మల్టీ-ఏజెంట్ & A2A](./lesson-7-multi-agent-a2a/README.md)   | ఏజెంట్లను నెట్‌వర్క్ సేవలుగా కంపోజ్ చేయండి: Agent-to-Agent (A2A) ఓపెన్ ప్రోటోకాల్ ద్వారా ఏజెంట్‌ను ప్రమాణీకరించండి మరియు రిమోట్ ఏజెంట్‌ను పీర్‌గా ఉపయోగించండి.       |  


## 🎒 ఇతర కోర్సులు  

మా టీమ్ ఇతర కోర్సులను కూడా ఉత్పత్తి చేస్తోంది! చూడండి:  

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

[![ప్రారంభకులకు జననాత్మక AI](https://img.shields.io/badge/Generative%20AI%20for%20Beginners-8B5CF6?style=for-the-badge&labelColor=E5E7EB&color=8B5CF6)](https://github.com/microsoft/generative-ai-for-beginners?WT.mc_id=academic-105485-koreyst)
[![జననాత్మక AI (.NET)](https://img.shields.io/badge/Generative%20AI%20(.NET)-9333EA?style=for-the-badge&labelColor=E5E7EB&color=9333EA)](https://github.com/microsoft/Generative-AI-for-beginners-dotnet?WT.mc_id=academic-105485-koreyst)
[![జననాత్మక AI (Java)](https://img.shields.io/badge/Generative%20AI%20(Java)-C084FC?style=for-the-badge&labelColor=E5E7EB&color=C084FC)](https://github.com/microsoft/generative-ai-for-beginners-java?WT.mc_id=academic-105485-koreyst)
[![జననాత్మక AI (JavaScript)](https://img.shields.io/badge/Generative%20AI%20(JavaScript)-E879F9?style=for-the-badge&labelColor=E5E7EB&color=E879F9)](https://github.com/microsoft/generative-ai-with-javascript?WT.mc_id=academic-105485-koreyst)

---
 
### ప్రాథమిక అభ్యాస్
[![ప్రారంభకులకు ML](https://img.shields.io/badge/ML%20for%20Beginners-22C55E?style=for-the-badge&labelColor=E5E7EB&color=22C55E)](https://aka.ms/ml-beginners?WT.mc_id=academic-105485-koreyst)
[![ప్రారంభకులకు డేటా సైన్స్](https://img.shields.io/badge/Data%20Science%20for%20Beginners-84CC16?style=for-the-badge&labelColor=E5E7EB&color=84CC16)](https://aka.ms/datascience-beginners?WT.mc_id=academic-105485-koreyst)
[![ప్రారంభకులకు AI](https://img.shields.io/badge/AI%20for%20Beginners-A3E635?style=for-the-badge&labelColor=E5E7EB&color=A3E635)](https://aka.ms/ai-beginners?WT.mc_id=academic-105485-koreyst)
[![ప్రారంభకులకు సైబర్‌సెక్యూరిటీ](https://img.shields.io/badge/Cybersecurity%20for%20Beginners-F97316?style=for-the-badge&labelColor=E5E7EB&color=F97316)](https://github.com/microsoft/Security-101?WT.mc_id=academic-96948-sayoung)
[![ప్రారంభకులకు వెబ్ డెవలప్‌మెంట్](https://img.shields.io/badge/Web%20Dev%20for%20Beginners-EC4899?style=for-the-badge&labelColor=E5E7EB&color=EC4899)](https://aka.ms/webdev-beginners?WT.mc_id=academic-105485-koreyst)
[![ప్రారంభకులకు IoT](https://img.shields.io/badge/IoT%20for%20Beginners-14B8A6?style=for-the-badge&labelColor=E5E7EB&color=14B8A6)](https://aka.ms/iot-beginners?WT.mc_id=academic-105485-koreyst)
[![ప్రారంభకులకు XR డెవలప్‌మెంట్](https://img.shields.io/badge/XR%20Development%20for%20Beginners-38BDF8?style=for-the-badge&labelColor=E5E7EB&color=38BDF8)](https://github.com/microsoft/xr-development-for-beginners?WT.mc_id=academic-105485-koreyst)

---
 
### కోపిలట్ సిరీస్
[![AI కలసి ప్రోగ్రామింగ్ కోసం కోపిలట్](https://img.shields.io/badge/Copilot%20for%20AI%20Paired%20Programming-FACC15?style=for-the-badge&labelColor=E5E7EB&color=FACC15)](https://aka.ms/GitHubCopilotAI?WT.mc_id=academic-105485-koreyst)
[![C#/.NET కొరకు కోపిలట్](https://img.shields.io/badge/Copilot%20for%20C%23/.NET-FBBF24?style=for-the-badge&labelColor=E5E7EB&color=FBBF24)](https://github.com/microsoft/mastering-github-copilot-for-dotnet-csharp-developers?WT.mc_id=academic-105485-koreyst)
[![కోపిలట్ అడ్వెంచర్](https://img.shields.io/badge/Copilot%20Adventure-FDE68A?style=for-the-badge&labelColor=E5E7EB&color=FDE68A)](https://github.com/microsoft/CopilotAdventures?WT.mc_id=academic-105485-koreyst)
<!-- CO-OP TRANSLATOR OTHER COURSES END -->

## దానం చేయడం

ఈ ప్రాజెక్ట్ దానాలు మరియు సలహాలను స్వాగతిస్తుంది. ఎక్కువ భాగం దానాలు మీరు ఒక
దాత లైసెన్స్ ఒప్పందం (CLA)కు అంగీకరించాల్సి ఉంటుంది, మీరు హక్కులు కలిగి ఉన్నారు మరియు వాస్తవానికి
మీ దాణాన్ని ఉపయోగించడానికి హక్కులు మాకు ఇస్తున్నారని ప్రకటించే CLA. వివరాలకు, సందర్శించండి <https://cla.opensource.microsoft.com>.

మీరు ఒక పుల్ రిక్వెస్ట్ సమర్పించినప్పుడు, CLA బాట్ ఆటోమాటిక్‌గా మీరు CLA అందించాల్సిన అవసరముందో లేదో నిర్ణయిస్తుంది
మరియు PRను అనుగుణంగా అలంకరిస్తుంది (ఉదా: స్థితి తనిఖీ, వ్యాఖ్య). బాట్ అందించిన సూచనలను
అనుసరించండి. మా CLA ఉపయోగించే అన్ని రిపోల్లో మీరు ఇది ఒక్కసారి మాత్రమే చేయాలి.

ఈ ప్రాజెక్ట్ [మైక్రోసాఫ్ట్ ఓపెన్ సోర్స్ కోడ్ ఆఫ్ కండక్ట్](https://opensource.microsoft.com/codeofconduct/)ను ఆమోదించింది.
మరిన్ని వివరాలకు [కోడ్ ఆఫ్ కండక్ట్ FAQ](https://opensource.microsoft.com/codeofconduct/faq/) ని చూడండి లేదా
ఎలాంటి అదనపు ప్రశ్నలు లేదా వ్యాఖ్యల కోసం [opencode@microsoft.com](mailto:opencode@microsoft.com) కు సంప్రదించండి.

## ట్రేడ్మార్కులు

ఈ ప్రాజెక్ట్ ప్రాజెక్టులు, ఉత్పత్తులు, లేదా సేవల కోసం ట్రేడ్మార్కులు లేదా లోగోలు కలిగి ఉండవచ్చు. మైక్రోసాఫ్ట్
ట్రేడ్మార్కులు లేదా లోగోల అధికారిక ఉపయోగం కింది నియమాలకు బద్ధమైనది మరియు పాటించాల్సినది:
[మైక్రోసాఫ్ట్ ట్రేడ్మార్క్ & బ్రాండ్ గైడ్‌లైన్స్](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
ఈ ప్రాజెక్ట్ మార్పు చేసిన సంస్కరణలలో మైక్రోసాఫ్ట్ ట్రేడ్మార్కులు లేదా లోగోల ఉపయోగం గందరగోళం సృష్టించకూడదు లేదా మైక్రోసాఫ్ట్ ప్రాయోజకత్వం సూచించకూడదు.
మూడవ పక్ష ట్రేడ్మార్కులు లేదా లోగోల ఏమైనా ఉపయోగం ఆ ఆత్ర పక్షాల విధానాలకు అనుగుణంగా ఉంటుంది.

## సాయం పొందడం

మీరు ఎక్కడైనా చిక్కుకున్నారో లేదా AI యాప్స్ తయారీలో ఎక్కడైనా సందేహం ఉంటే, స్వయంగా చేరండి:

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

ఉత్పత్తి ఫీడ్బ్యాక్ లేదా సమస్యలు ఉంటే సందర్శించండి:

[![Microsoft Foundry Developer Forum](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్వీకరణ**:
ఈ పత్రం AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నిస్తున్నప్పటికీ, ఆటోమేటెడ్ అనువాదాలు తప్పులు లేదా అసమగ్రతలను కలిగి ఉండవచ్చు. దాని స్వదేశ భాషలో ఉన్న అసలు పత్రాన్ని అధికారం కలిగిన మూలంగా పరిగణించాలి. కీలకమైన సమాచారం కోసం, ప్రొఫెషనల్ మానవ అనువాదాన్ని సిఫారసు చేస్తాము. ఈ అనువాదం ఉపయోగం వల్ల కలిగే ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->