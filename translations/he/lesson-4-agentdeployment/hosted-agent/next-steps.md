<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:39:17+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "he"
}
-->
# השלבים הבאים לאחר `azd init`

## תוכן העניינים

1. [השלבים הבאים](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [הקמת תשתית](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [שינוי תשתית](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [הגעה למצב ייצור](../../../../lesson-4-agentdeployment/hosted-agent)
2. [חיוב](../../../../lesson-4-agentdeployment/hosted-agent)
3. [פתרון בעיות](../../../../lesson-4-agentdeployment/hosted-agent)

## השלבים הבאים

### הקמת תשתית ופריסת קוד היישום

הרץ `azd up` כדי להקים את התשתית שלך ולפרוס ל-Azure בשלב אחד (או הרץ `azd provision` ואז `azd deploy` כדי לבצע את המשימות בנפרד). בקר בנקודות הקצה של השירות המפורטות כדי לראות את היישום שלך פועל!

כדי לפתור בעיות, ראה [פתרון בעיות](../../../../lesson-4-agentdeployment/hosted-agent).

### שינוי תשתית

כדי לתאר את התשתית והיישום, נוסף הקובץ `azure.yaml`. קובץ זה מכיל את כל השירותים והמשאבים המתארים את היישום שלך.

כדי להוסיף שירותים או משאבים חדשים, הרץ `azd add`. ניתן גם לערוך את הקובץ `azure.yaml` ישירות במידת הצורך.

### הגעה למצב ייצור

כאשר יש צורך, `azd` מייצר את התשתית הנדרשת כקוד בזיכרון ומשתמש בה. אם ברצונך לראות או לשנות את התשתית ש-`azd` משתמש בה, הרץ `azd infra gen` כדי לשמור אותה לדיסק.

אם תעשה זאת, ייווצרו כמה ספריות נוספות:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*הערה*: ברגע שיצרת את התשתית שלך לדיסק, הקבצים האלה הם המקור האמיתי ל-azd. כל שינוי שייעשה ב-`azure.yaml` (כגון דרך `azd add`) לא ישתקף בתשתית עד שתיצור אותה מחדש עם `azd infra gen`. תתבקש לפני שהקבצים יוחלפו. ניתן להעביר את `--force` כדי לאלץ את `azd infra gen` להחליף את הקבצים ללא בקשת אישור.

לבסוף, הרץ `azd pipeline config` כדי להגדיר צינור פריסה CI/CD.

## חיוב

בקר בדף *ניהול עלויות + חיוב* בפורטל Azure כדי לעקוב אחר ההוצאות הנוכחיות. למידע נוסף על אופן החיוב וכיצד ניתן לעקוב אחר העלויות שנגרמות במנויי Azure שלך, בקר ב-[סקירת חיוב](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## פתרון בעיות

ש: ביקרתי בנקודת הקצה של השירות המפורטת, ואני רואה דף ריק, דף קבלת פנים כללי, או דף שגיאה.

ת: ייתכן שהשירות שלך נכשל בהפעלה, או שחסרות הגדרות תצורה מסוימות. כדי לחקור יותר לעומק:

1. הרץ `azd show`. לחץ על הקישור תחת "View in Azure Portal" כדי לפתוח את קבוצת המשאבים בפורטל Azure.
2. נווט לשירות Container App הספציפי שנכשל בפריסה.
3. לחץ על הגרסה הכושלת תחת "Revisions with Issues".
4. סקור את "Status details" למידע נוסף על סוג הכישלון.
5. צפה בפלטי הלוג מזרם לוג הקונסולה וזרם לוג המערכת כדי לזהות שגיאות.
6. אם הלוגים נכתבים לדיסק, השתמש ב-*Console* בניווט כדי להתחבר ל-shell בתוך המכולה הפועלת.

למידע נוסף על פתרון בעיות, בקר ב-[פתרון בעיות Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting).

### מידע נוסף

למידע נוסף על הגדרת פרויקט `azd` שלך, בקר בתיעוד הרשמי שלנו ב-[docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי אדם. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->