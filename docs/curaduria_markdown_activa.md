# Curaduría del corpus Markdown activo para RAG

## Proyecto

Asistente IA para Ingeniería Clínica HRRG
Rama de trabajo: `prueba-markdown-dario`
Commit asociado: `4d2bace chore(rag): cerrar curaduria markdown activa`

## Objetivo de la curaduría

El objetivo de esta etapa fue definir qué documentos Markdown deben formar parte del corpus activo que alimentará la base vectorial ChromaDB del asistente RAG.

La decisión se tomó sobre los 73 archivos Markdown reales ubicados en `data/markdown`, ya previamente filtrados, normalizados e incorporados como corpus útil del prototipo.

No se buscó eliminar documentación del repositorio, sino definir qué fuentes deben participar en la ingesta activa del asistente y cuáles deben quedar fuera para evitar ruido documental, duplicación, respuestas poco precisas o uso de fuentes secundarias frente a manuales técnicos más adecuados.

## Criterio general aplicado

Se priorizaron como fuentes activas:

* manuales técnicos;
* manuales de servicio;
* manuales de mantenimiento;
* manuales de usuario con utilidad operativa;
* documentos de troubleshooting;
* checklists técnicos;
* planos o documentos técnicos complementarios claramente útiles.

Se excluyeron del corpus activo:

* folletos comerciales;
* brochures;
* material educativo secundario;
* capacitaciones generales;
* entrevistas;
* documentos redundantes;
* archivos introductorios;
* archivos ambiguos o mal nombrados cuando existía una fuente técnica más clara;
* documentos que podían degradar la precisión del RAG frente a fuentes principales.

## Resultado final

Sobre un total de 73 archivos Markdown:

| Estado final                | Cantidad |
| --------------------------- | -------: |
| Incluir en curaduría activa |       59 |
| Revisar                     |        0 |
| Excluir del corpus activo   |       14 |
| Total                       |       73 |

La curaduría activa quedó registrada en:

`data/inventory/curaduria_activa.csv`

La base completa de decisiones quedó registrada en:

`data/inventory/curaduria_base_73_curada_v1.csv`

## Significado de cada estado

### Incluir

El documento queda habilitado para la ingesta activa del RAG.
Estos archivos integran `curaduria_activa.csv` y serán utilizados para reconstruir ChromaDB.

### Excluir

El documento no se elimina del repositorio, pero queda fuera de la ingesta activa.
La exclusión se aplica para evitar que el asistente recupere información secundaria, comercial, redundante, ambigua o menos confiable cuando existen fuentes técnicas principales.

### Revisar

Al cierre de esta etapa no quedaron documentos en estado `revisar`.
Los dos documentos que inicialmente estaban pendientes fueron resueltos durante la curaduría final.

## Documentos excluidos y motivo

| Archivo                                                                                              | Equipo                         | Motivo de exclusión                                                                                          |
| ---------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `bilirrubinometro_drager_jm105_material_educativo_bilirrubinometro_drager_jm_105_ingles.md`          | Bilirrubinómetro Dräger JM-105 | Material educativo secundario; no se prioriza para respuesta técnica del asistente.                          |
| `draguer_respirador_draeger_vn500_brochure_folleto_cc_other_br_9066227_es.md`                        | Respirador Dräger VN500        | Folleto comercial/secundario; no se incorpora al corpus activo para evitar ruido.                            |
| `draguer_respirador_draeger_vn500_brochure_folleto_cc_other_br_9066343_es.md`                        | Respirador Dräger VN500        | Folleto comercial/secundario; no se incorpora al corpus activo para evitar ruido.                            |
| `draguer_respirador_draeger_vn500_brochure_folleto_cc_other_br_9066364_en.md`                        | Respirador Dräger VN500        | Folleto comercial/secundario; no se incorpora al corpus activo para evitar ruido.                            |
| `draguer_respirador_draeger_vn500_brochure_folleto_cc_other_br_9066465_es.md`                        | Respirador Dräger VN500        | Folleto comercial/secundario; no se incorpora al corpus activo para evitar ruido.                            |
| `draguer_respirador_draeger_vn500_brochure_folleto_pdf1805_ad_babylog_vn500_spanisch_30112009_k2.md` | Respirador Dräger VN500        | Folleto/brochure secundario; no se incorpora al corpus activo.                                               |
| `draguer_respirador_draeger_vn500_capacitacion_1_3_training_gs500_en_01_2017.md`                     | Respirador Dräger VN500        | Material de capacitación; se aparta del corpus activo inicial para priorizar manuales técnicos y de usuario. |
| `draguer_respirador_draeger_vn500_capacitacion_2_1_training_ps500_withm7_3plus_en_06_2017.md`        | Respirador Dräger VN500        | Material de capacitación; se aparta del corpus activo inicial para priorizar manuales técnicos y de usuario. |
| `draguer_respirador_draeger_vn500_manual_9066667_babyflow_es_finit.md`                               | Respirador Dräger VN500        | Documento redundante respecto de BabyFlow ya incluido con nombre más normalizado.                            |
| `draguer_respirador_draeger_vn500_manual_other_volumeguarantee_interview_dr_m_keszler_en.md`         | Respirador Dräger VN500        | Entrevista/material secundario; no se incorpora al corpus técnico activo.                                    |
| `tp_100_fg_tp_80.md`                                                                                 | TP100                          | Archivo ambiguo; el nombre mezcla TP100/TP80 y no se incorpora al corpus activo sin validación documental.   |
| `ventilador_engstrom_guia_rapida_para_enfermeras.md`                                                 | Ventilador Engström            | Guía rápida para enfermería; secundaria frente a manual técnico y manual de usuario.                         |
| `ventilador_neumovent_respimeradores.md`                                                             | Ventilador Neumovent GraphNet  | Archivo ambiguo/mal nombrado; se excluye hasta revisión documental específica.                               |
| `ventilador_newport_ht70_introduccion_newport_ht_70_plus.md`                                         | Ventilador Newport HT70        | Documento introductorio; se excluye del corpus activo inicial frente al manual de servicio.                  |

## Decisiones específicas resueltas al cierre

Durante la revisión final se resolvieron dos documentos que habían quedado pendientes:

| Archivo                                          | Decisión final | Motivo                                                                                                                 |
| ------------------------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `tp_100_fg_tp_80.md`                             | Excluir        | Archivo ambiguo; el nombre mezcla TP100/TP80 y no se incorpora sin validación documental.                              |
| `ventilador_engstrom_ventilacion_no_invasiva.md` | Incluir        | Documento específico de ventilación no invasiva; se considera fuente operativa complementaria del ventilador Engström. |

## Criterio técnico para la próxima ingesta

La próxima reconstrucción de ChromaDB debe realizarse únicamente con las fuentes presentes en:

`data/inventory/curaduria_activa.csv`

La ingesta debe considerar solo archivos que cumplan:

* `decision_curaduria = incluir`
* `estado_producto = activo`, `validado` o `aprobado`

De esta manera, el RAG no indexará documentos excluidos ni documentos pendientes.

## Justificación técnica

Esta curaduría busca mejorar la calidad del recuperador semántico. En sistemas RAG, incorporar más documentos no siempre mejora las respuestas. Si se indexan folletos, capacitaciones, documentos redundantes o fuentes secundarias junto con manuales técnicos principales, el recuperador puede traer fragmentos menos precisos y el modelo puede generar respuestas incompletas o apoyadas en documentación débil.

Por ese motivo, esta etapa prioriza calidad documental sobre cantidad de archivos. El objetivo es que el asistente responda con respaldo técnico, trazabilidad y menor riesgo de mezclar fuentes no pertinentes.

## Estado al cierre

* Corpus Markdown real revisado: 73 archivos.
* Fuentes activas definidas: 59.
* Fuentes excluidas: 14.
* Pendientes de revisión: 0.
* `curaduria_activa.csv` actualizado.
* `curaduria_base_73_curada_v1.csv` generado como respaldo completo de decisiones.
* Commit subido a GitHub en la rama `prueba-markdown-dario`.

## Próximo paso

Reconstruir ChromaDB desde cero utilizando únicamente las 59 fuentes activas definidas en `curaduria_activa.csv`.

Luego se deberá validar:

* cantidad de documentos efectivamente procesados;
* cantidad de chunks generados;
* ausencia de documentos excluidos en la base vectorial;
* recuperación por equipo;
* calidad de respuestas en preguntas críticas;
* comportamiento del fallback documental;
* respeto del prompt técnico seguro.

## Reingesta posterior a la curaduría activa

Luego de cerrar la curaduría v1, se actualizó `data/inventory/curaduria_activa.csv` con las 59 fuentes activas definitivas.

Posteriormente se eliminó la base local `data/chroma` y se ejecutó una reingesta forzada para reconstruir ChromaDB únicamente con las fuentes activas.

Resultado de control posterior:

- Fuentes activas en `curaduria_activa.csv`: 59.
- Chunks generados en ChromaDB: 8023.
- Colección ChromaDB: `manuales_hrrg`.

Este resultado confirma que la base vectorial fue reconstruida después de aplicar la curaduría documental y que ya no trabaja sobre los 73 Markdown completos, sino sobre el subconjunto activo definido para el producto.