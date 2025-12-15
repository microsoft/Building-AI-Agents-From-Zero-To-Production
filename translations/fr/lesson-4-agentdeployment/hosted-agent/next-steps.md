<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:25:10+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "fr"
}
-->
# Étapes suivantes après `azd init`

## Table des matières

1. [Étapes suivantes](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionner l'infrastructure](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modifier l'infrastructure](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Atteindre la production](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Facturation](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Dépannage](../../../../lesson-4-agentdeployment/hosted-agent)

## Étapes suivantes

### Provisionner l'infrastructure et déployer le code de l'application

Exécutez `azd up` pour provisionner votre infrastructure et déployer sur Azure en une seule étape (ou exécutez `azd provision` puis `azd deploy` pour accomplir les tâches séparément). Visitez les points de terminaison du service listés pour voir votre application en fonctionnement !

Pour résoudre tout problème, consultez la section [dépannage](../../../../lesson-4-agentdeployment/hosted-agent).

### Modifier l'infrastructure

Pour décrire l'infrastructure et l'application, `azure.yaml` a été ajouté. Ce fichier contient tous les services et ressources qui décrivent votre application.

Pour ajouter de nouveaux services ou ressources, exécutez `azd add`. Vous pouvez également modifier directement le fichier `azure.yaml` si nécessaire.

### Atteindre la production

Lorsque cela est nécessaire, `azd` génère l'infrastructure requise en tant que code en mémoire et l'utilise. Si vous souhaitez voir ou modifier l'infrastructure que `azd` utilise, exécutez `azd infra gen` pour la sauvegarder sur disque.

Si vous faites cela, certains répertoires supplémentaires seront créés :

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Remarque* : Une fois que vous avez généré votre infrastructure sur disque, ces fichiers deviennent la source de vérité pour azd. Toute modification apportée à `azure.yaml` (comme via `azd add`) ne sera pas reflétée dans l'infrastructure tant que vous ne la régénérez pas avec `azd infra gen`. Il vous demandera confirmation avant d'écraser les fichiers. Vous pouvez passer `--force` pour forcer `azd infra gen` à écraser les fichiers sans demander de confirmation.

Enfin, exécutez `azd pipeline config` pour configurer un pipeline de déploiement CI/CD.

## Facturation

Visitez la page *Gestion des coûts + Facturation* dans le portail Azure pour suivre les dépenses actuelles. Pour plus d'informations sur la facturation et comment surveiller les coûts encourus dans vos abonnements Azure, consultez [aperçu de la facturation](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Dépannage

Q : J'ai visité le point de terminaison du service listé, et je vois une page blanche, une page d'accueil générique ou une page d'erreur.

R : Votre service a peut-être échoué à démarrer, ou il peut manquer certaines configurations. Pour enquêter davantage :

1. Exécutez `azd show`. Cliquez sur le lien sous "View in Azure Portal" pour ouvrir le groupe de ressources dans le portail Azure.
2. Naviguez vers le service Container App spécifique qui échoue à se déployer.
3. Cliquez sur la révision en échec sous "Revisions with Issues".
4. Consultez les "Status details" pour plus d'informations sur le type d'échec.
5. Observez les sorties des journaux depuis Console log stream et System log stream pour identifier les erreurs.
6. Si des journaux sont écrits sur disque, utilisez *Console* dans la navigation pour vous connecter à un shell à l'intérieur du conteneur en cours d'exécution.

Pour plus d'informations de dépannage, consultez [dépannage des Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting).

### Informations supplémentaires

Pour plus d'informations sur la configuration de votre projet `azd`, consultez notre [documentation officielle](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :  
Ce document a été traduit à l’aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçons d’assurer l’exactitude, veuillez noter que les traductions automatiques peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d’origine doit être considéré comme la source faisant foi. Pour les informations critiques, une traduction professionnelle réalisée par un humain est recommandée. Nous déclinons toute responsabilité en cas de malentendus ou de mauvaises interprétations résultant de l’utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->