<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:25:34+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "es"
}
-->
# Próximos pasos después de `azd init`

## Tabla de contenido

1. [Próximos pasos](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionar infraestructura](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modificar infraestructura](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Prepararse para producción](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Facturación](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Solución de problemas](../../../../lesson-4-agentdeployment/hosted-agent)

## Próximos pasos

### Provisionar infraestructura y desplegar código de la aplicación

Ejecute `azd up` para provisionar su infraestructura y desplegar en Azure en un solo paso (o ejecute `azd provision` y luego `azd deploy` para realizar las tareas por separado). ¡Visite los puntos finales del servicio listados para ver su aplicación en funcionamiento!

Para solucionar cualquier problema, consulte [solución de problemas](../../../../lesson-4-agentdeployment/hosted-agent).

### Modificar infraestructura

Para describir la infraestructura y la aplicación, se agregó `azure.yaml`. Este archivo contiene todos los servicios y recursos que describen su aplicación.

Para agregar nuevos servicios o recursos, ejecute `azd add`. También puede editar el archivo `azure.yaml` directamente si es necesario.

### Prepararse para producción

Cuando sea necesario, `azd` genera la infraestructura como código requerida en memoria y la utiliza. Si desea ver o modificar la infraestructura que `azd` usa, ejecute `azd infra gen` para guardarla en disco.

Si hace esto, se crearán algunos directorios adicionales:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Nota*: Una vez que haya generado su infraestructura en disco, esos archivos son la fuente de verdad para azd. Cualquier cambio realizado en `azure.yaml` (como a través de `azd add`) no se reflejará en la infraestructura hasta que la regenere con `azd infra gen` nuevamente. Le preguntará antes de sobrescribir archivos. Puede pasar `--force` para forzar que `azd infra gen` sobrescriba los archivos sin preguntar.

Finalmente, ejecute `azd pipeline config` para configurar una canalización de despliegue CI/CD.

## Facturación

Visite la página *Cost Management + Billing* en el Portal de Azure para rastrear el gasto actual. Para obtener más información sobre cómo se le factura y cómo puede monitorear los costos incurridos en sus suscripciones de Azure, visite [visión general de facturación](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Solución de problemas

P: Visité el punto final del servicio listado y veo una página en blanco, una página de bienvenida genérica o una página de error.

R: Su servicio puede haber fallado al iniciar o puede que le falten algunas configuraciones. Para investigar más a fondo:

1. Ejecute `azd show`. Haga clic en el enlace bajo "View in Azure Portal" para abrir el grupo de recursos en el Portal de Azure.
2. Navegue al servicio específico de Container App que está fallando en desplegar.
3. Haga clic en la revisión que falla bajo "Revisions with Issues".
4. Revise los "Status details" para más información sobre el tipo de fallo.
5. Observe las salidas de los registros de Console log stream y System log stream para identificar errores.
6. Si los registros se escriben en disco, use *Console* en la navegación para conectarse a una shell dentro del contenedor en ejecución.

Para más información sobre solución de problemas, visite [solución de problemas de Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Información adicional

Para información adicional sobre cómo configurar su proyecto `azd`, visite nuestra [documentación oficial](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automáticas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional realizada por humanos. No nos hacemos responsables de malentendidos o interpretaciones erróneas derivadas del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->