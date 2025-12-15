<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "2799ceaaefbd8571688459ac03eac5aa",
  "translation_date": "2025-12-12T17:05:11+00:00",
  "source_file": "README.md",
  "language_code": "he"
}
-->
# בניית סוכני בינה מלאכותית מאפס ועד הפקה

![בניית סוכני בינה מלאכותית מאפס ועד הפקה](../../translated_images/repo-thumbnail.083b24afed61b6dd27a7fc53798bebe9edf688a41031163a1fca9f61c64d63ec.he.png)

## קורס המלמד את יסודות מחזור חיי פיתוח סוכני בינה מלאכותית

[![רישיון GitHub](https://img.shields.io/github/license/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/blob/master/LICENSE?WT.mc_id=academic-105485-koreyst)
[![תורמים ב-GitHub](https://img.shields.io/github/contributors/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/graphs/contributors/?WT.mc_id=academic-105485-koreyst)
[![בעיות ב-GitHub](https://img.shields.io/github/issues/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/issues/?WT.mc_id=academic-105485-koreyst)
[![בקשות משיכה ב-GitHub](https://img.shields.io/github/issues-pr/microsoft/Building-AI-Agents-From-Zero-To-Production.svg)](https://GitHub.com/microsoft/Building-AI-Agents-From-Zero-To-Production/pulls/?WT.mc_id=academic-105485-koreyst)
[![ברוכים הבאים לבקשות משיכה](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com?WT.mc_id=academic-105485-koreyst)

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

## 🌱 התחלה

קורס זה כולל שיעורים המכסים את יסודות בניית והפצת סוכני בינה מלאכותית.

כל שיעור בונה על השיעור הקודם, לכן אנו ממליצים להתחיל מההתחלה ולעבוד עד הסוף.

אם ברצונך לחקור עוד על נושאי סוכני בינה מלאכותית, תוכל לבדוק את [קורס סוכני בינה מלאכותית למתחילים](https://aka.ms/ai-agents-beginners).

### פגוש לומדים אחרים, קבל תשובות לשאלותיך

אם תיתקל בקשיים או יש לך שאלות לגבי בניית סוכני בינה מלאכותית, הצטרף לערוץ ה-Discord הייעודי שלנו ב-[Microsoft Foundry Discord](https://discord.gg/Kuaw3ktsu6).

### מה אתה צריך

לכל שיעור יש דוגמת קוד משלו שניתן להריץ מקומית. תוכל [לשכפל את המאגר הזה](https://github.com/microsoft/Building-AI-Agents-From-Zero-To-Production/fork) כדי ליצור עותק משלך.

קורס זה משתמש כרגע ב:

- [מסגרת סוכנים של מיקרוסופט (MAF)](https://aka.ms/ai-agents-beginners/agent-framework)
- [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry)
- [שירות Azure OpenAI](https://azure.microsoft.com/products/ai-foundry/models/openai)
- [Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli?view=azure-cli-latest)

אנא ודא שיש לך גישה לשירותים אלה לפני ההתחלה.

אפשרויות נוספות לאירוח מודלים ושירותים יגיעו בקרוב.

## 🗃️ שיעורים

| **שיעור**         | **תיאור**                                                                                  |
|--------------------|--------------------------------------------------------------------------------------------------|
| [עיצוב סוכן](./lesson-1-agent-design/README.md)       | מבוא למקרה השימוש "הכנסת מפתחים" של הסוכן שלנו ואיך לעצב סוכנים יעילים  |
| [פיתוח סוכן](./lesson-2-agent-development/README.md)  | שימוש במסגרת סוכנים של מיקרוסופט (MAF), יצירת 3 סוכנים שיעזרו למפתחים חדשים להיכנס למערכת.       |
| [הערכת סוכן](./lesson-3-agent-evals/README.md)  | שימוש ב-Microsoft Foundry, לגלות עד כמה הסוכנים שלנו מתפקדים ואיך לשפר אותם. |
| [הפצת סוכן](./lesson-4-agent-deployment/README.md)   | שימוש בסוכנים מאוחסנים ו-OpenAI Chatkit, לראות איך לפרוס סוכן בינה מלאכותית לייצור.       |

## תרומה

פרויקט זה מקבל בברכה תרומות והצעות. רוב התרומות דורשות שתסכים להסכם רישיון תורם (CLA) המצהיר שיש לך את הזכות, ושאתה אכן מעניק לנו את הזכויות להשתמש בתרומתך. לפרטים, בקר בכתובת <https://cla.opensource.microsoft.com>.

כאשר אתה מגיש בקשת משיכה, בוט CLA יקבע אוטומטית אם עליך לספק CLA ויעטר את בקשת המשיכה בהתאם (למשל, בדיקת סטטוס, תגובה). פשוט עקוב אחר ההוראות שמספק הבוט. תצטרך לעשות זאת רק פעם אחת בכל המאגרי הקוד שמשתמשים ב-CLA שלנו.

פרויקט זה אימץ את [קוד ההתנהגות של מיקרוסופט בקוד פתוח](https://opensource.microsoft.com/codeofconduct/).
למידע נוסף ראה את [שאלות נפוצות על קוד ההתנהגות](https://opensource.microsoft.com/codeofconduct/faq/) או צור קשר ב-[opencode@microsoft.com](mailto:opencode@microsoft.com) עם שאלות או הערות נוספות.

## סימני מסחר

פרויקט זה עשוי להכיל סימני מסחר או לוגואים של פרויקטים, מוצרים או שירותים. שימוש מורשה בסימני המסחר או בלוגואים של מיקרוסופט כפוף וצריך לעקוב אחרי
[הנחיות סימני המסחר והמותג של מיקרוסופט](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general).
שימוש בסימני המסחר או בלוגואים של מיקרוסופט בגרסאות מותאמות של פרויקט זה לא יגרום לבלבול או יביע חסות של מיקרוסופט.
כל שימוש בסימני מסחר או לוגואים של צד שלישי כפוף למדיניות של אותם צדדים שלישיים.

## קבלת עזרה

אם תיתקל בקשיים או יש לך שאלות לגבי בניית אפליקציות בינה מלאכותית, הצטרף:

[![Microsoft Foundry Discord](https://dcbadge.limes.pink/api/server/nTYy5BXMWG)](https://discord.gg/Kuaw3ktsu6)

אם יש לך משוב על המוצר או שגיאות בזמן הבנייה, בקר ב:

[![פורום מפתחי Microsoft Foundry ב-GitHub](https://img.shields.io/badge/GitHub-Microsoft_Foundry_Developer_Forum-blue?style=for-the-badge&logo=github&color=000000&logoColor=fff)](https://aka.ms/foundry/forum)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי אדם. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->