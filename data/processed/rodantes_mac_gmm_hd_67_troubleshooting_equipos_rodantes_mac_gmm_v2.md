# Página 1

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    2/14 Troubleshooting

Procedimiento

1.  Link fail

Problema con la comunicación serie entre el controlador principal S77 y el touch screen.

1.  Verificar que el cable serie está correctamente conectado a la ficha CN10 en la placa

S77. Verificar que todos los cables que llegan a la placa estén conectados y no estén dañados.

2.  Verificar que el mismo cable esté correctamente conetado en el touch screen.

Verificar que los cables estén conectados y no estén dañados

```metadata
pagina: 1
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P1_I0.png
contexto: 
```

![Imagen página 1 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P1_I0.png)



# Página 2

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    3/14 Troubleshooting

2.  Inverter fail

Antes de apagar el sistema, verificar en la placa S19 (código 94774) qué led rojo está

encendido. Controlar también que los 4 leds de la placa S29 (94761) estén encendidos.

Luego apagar el equipo y esperar a que los capacitores se descarguen totalmente.

Antes de continuar verificar que todos los cables estén correctamente conectados en

sus conectores.

```metadata
pagina: 2
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P2_I0.png
contexto: 
```

![Imagen página 2 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P2_I0.png)

```metadata
pagina: 2
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P2_I1.png
contexto: 
```

![Imagen página 2 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P2_I1.png)



# Página 3

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    4/14 Troubleshooting

```metadata
pagina: 3
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P3_I0.png
contexto: 
```

![Imagen página 3 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P3_I0.png)

```metadata
pagina: 3
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P3_I1.png
contexto: 
```

![Imagen página 3 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P3_I1.png)



# Página 4

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    5/14 Troubleshooting

Led 2 Delta KV

MAX

1. Controlar que los cables están correctamente conectados a S19 y

quedan fijos.

Led 3 KV> 110%

1. Si el problema ocurre 1 sola vez, la corriente se descargó del

cabezal, el sistema debería funcionar adecuadamente. 2. Si el problema ocurre regularmente en 120 / 125 kV, realizar la

calibración de foco fino y foco grueso en el test point de kV feedback. Led 4 KV MIN

1. Si el problema ocurre solo a 40 KV, realizar la calibración de foco

fino y foco grueso en el test point de kV feedback. 2. Controlar que hay continuidad en el fusible de la placa inverter

(fuse100 A code 82845) 3. Controlar la integridad del fusible F9 en la placa S29 (500 mA).

```metadata
pagina: 4
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P4_I0.png
contexto: 
```

![Imagen página 4 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P4_I0.png)



# Página 5

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    6/14 Troubleshooting

4. Controlar que no hay continuidad en los 4 IGBT de la placa Inverter.

Código del Inverter: 94587.

(La imagen es de referencia, sobre 1 IGBT, repetir la misma operación sobre los otros IGBT) 5. Controlar que el cable está correctamente conectado y fijo en la

placa Inverter (CF1 placa S29)

```metadata
pagina: 5
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P5_I0.png
contexto: 
```

![Imagen página 5 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P5_I0.png)

```metadata
pagina: 5
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P5_I1.png
contexto: 
```

![Imagen página 5 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P5_I1.png)



# Página 6

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    7/14 Troubleshooting

2.1 Reemplazo del cabezal

2.1.1 Menú de service (Service Menu) Acceder al menú de service utilizando los comandos propios para navegar los sub- menúes.

Para equipos con teclado:

 Presionar la combinación KV UP + KV DOWN + LIGHT para acceder al setup.  Presionar la combinación mAs UP + prog UP + Potter para acceder al menú de service

Para equipos MAC-R32 utilizar la clave 1202, para setup config utilizar 1234.

```metadata
pagina: 6
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P6_I0.png
contexto: 
```

![Imagen página 6 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P6_I0.png)

```metadata
pagina: 6
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P6_I1.png
contexto: 
```

![Imagen página 6 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P6_I1.png)



# Página 7

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    8/14 Troubleshooting

Nota: en caso de otros equipos consultar contraseña a diseño en documento: MAC-R32 & MAC- R32D Passwords List, en la ruta Diseño\Bibliografia\Circuitos Equipos\Multi_Marcas\Merate\Rodante.

2.1.1.1 Ajuste ADC KV

Acceder al sub-menu con el comando de confirmación KV40: asegúrese que el valor es 200 KV120: asegúrese que el valor es 200 2.1.1.2 Ajuste DAC FIL

Acceder al sub-menu con el comando de confirmación. Utilizar un multímetro para medir la tensión DC entre TP0 y TP9 en la placa S73.

mV 3600: modificar el valor hasta medir una tensión de 3.6 Vdc mV 4800: modificar el valor hasta medir una tensión de 4.8 Vdc 2.1.1.3 Ajuste tensión de batería

Acceder al sub-menú con el comando de confirmación. Modificar el valor hasta que la lectura leída sea de una valor de 332 Vdc. 2.1.1.4 Configuración

Acceder al sub-menú con el comando de confirmación. Navegar los ítems del menú y verificar que los parámetros límites son correctos (KV BOUND, MA BOUND, KW BOUND)

2.1.2 Menú de fábrica (Factory menu) Para acceder al menú de fábrica utilizar los comandos para navegar los sub- menúes.

Para equipos con teclado:

 Presionar la combinación KV UP + KV DOWN + LIGHT para acceder al setup.  Presionar la combinación mAs DOWN + prog DOWN + Confirm para acceder al menú de fábrica.

Para equipos MAC-R32 utilizar la clave 1203, para setup config utilizar 1234. 2.1.2.1 KV Feedback

Acceder al sub-menú con el comando de calibración. Esta sección requiere el uso de un medidor de kV. KV40: realizar una exposición. Insertar el valor de kV leído desde el medidor de kV y presionar Confirm. Repetir hasta que el valor del instrumento esté cerca del valor deseado (40 kV) y el valor leído por el sistema (ver figura)

```metadata
pagina: 7
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P7_I0.png
contexto: 
```

![Imagen página 7 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P7_I0.png)



# Página 8

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    9/14 Troubleshooting

KV120: realizar una exposición. Insertar el valor de kV leído desde el medidor de kV y presionar Confirm. Repetir hasta que el valor del instrumento esté cerca del valor deseado (120 kV) y el valor leído por el sistema. No debería haber errores en la señal durante esta fase, en caso de que eso ocurra referirse al apartado de troubleshooting. 2.1.2.2 Ajuste de filamento fino

2.1.2.2.1 Autocalibración Para acceder al modo automático es necesario hacer un corto circuito entre los pines 1 y 2 del CN8 en la placa S77 antes de entrar al menú. En caso de sistemas veterinarios, sería suficiente mantener el pedal presionado mientras se accede al menú. Mantener presionado el pulsador de disparo (PREP+RAD) hasta completar el procedimiento. Una vez que el procedimiento está completo, el sistema saldrá del menú automáticamente.

No debería haber errores en la señal durante esta fase, en caso de que eso ocurra referirse al apartado de troubleshooting. 2.1.2.2.2 Calibración Manual Para acceder al menú de calibración manual, asegurarse que no hay un corto circuito entre pines 1 y 2 del CN8 de la placa S77, luego presionar Confirm. Utilizar los 7 puntos de calibración, cada uno identificado por

 Valor de KV deseado  Valor de mA deseado  mV de filamento Nota: referirse a la página 37 del manual de service (Código 62353) para observar los valores de tabla. Para cada punto:

 Realizar una exposición.  Comprar valor de mA medido y valor de mA deseado.  Incrementar/decrementar valor de mV para incrementar/decrementar mA en el set point.  Repetir hasta que mA esté cercano al valor deseado (± 20 %).  Guardar el nuevo valor de mV presionando el botón de confirmación.  Mover al siguiente punto de calibración.



# Página 9

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    10/14 Troubleshooting

2.1.2.3 Ajuste de filamento grueso

2.1.2.3.1 Autocalibración Para acceder al modo automático es necesario hacer un corto circuito entre los pines 1 y 2 del CN8 en la placa S77 antes de entrar al menú. En caso de sistemas veterinarios, sería suficiente mantener el pedal presionado mientras se accede al menú. Mantener presionado el pulsador de disparo (PREP+RAD) hasta completar el procedimiento. Una vez que el procedimiento está completo, el sistema saldrá del menú automáticamente.

No debería haber errores en la señal durante esta fase, en caso de que eso ocurra referirse al apartado de troubleshooting. 2.1.2.3.2 Calibración Manual Para acceder al menú de calibración manual, asegurarse que no hay un corto circuito entre pines 1 y 2 del CN8 de la placa S77, luego presionar Confirm. Utilizar los 7 puntos de calibración, cada uno identificado por

 Valor de KV deseado  Valor de mA deseado  mV de filamento Nota: referirse a la página 37 del manual de service (Código 62353) para observar los valores de tabla. Para cada punto:

 Realizar una exposición.  Comprar valor de mA medido y valor de mA deseado.  Incrementar/decrementar valor de mV para incrementar/decrementar mA en el set point.  Repetir hasta que mA esté cercano al valor deseado (± 20 %).  Guardar el nuevo valor de mV presionando el botón de confirmación.  Mover al siguiente punto de calibración. 2.1.3 Troubleshooting Esta sección explica cómo manejar posibles errores durante las secciones tratadas en menú de fábrica. Los errores que ocurren en otra fase probablemente estén relacionados con mal funcionamiento de componentes del sistema o un problema de calibración. 2.1.3.1 Errores durante la calibración de KV Feedback

 Apagar el sistema.  Asegurarse que no hay un corto circuito en CN8 placa S77.  Encender el sistema.  Acceder al menú de service  Verificar que los valores de ajuste de KV están dentro del 20 % de tolerancia con respecto al valor de defecto (KV40: 650, KV80: 1200,



# Página 10

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    11/14 Troubleshooting

KV120: 1750). En caso de que lo estén, por favor setee manualmente los valores de defecto.  Verificar que los valores de ajuste de ADC KV están dentro del 20 % de tolerancia con respecto al valor de defecto (200). En caso de que lo estén, por favor setee manualmente los valores de defecto.  Acceder al menú de fabrica.  Acceder al sub-menu ajuste de filamento fino, navegar en los ítem “KV = 40 mA = 150 mV =…”, bajar el valor por debajo del 10 %.  Acceder al sub-menú KV Feedback y continuar el procedimiento. 2.1.3.2 Errores durante la autocalibración

 En caso de ocurrir un error durante el proceso de auto-calibración (Ajuste de filamento fino/grueso):  Liberar el pulsador de disparo (PREP+RAD).  Apagar, luego encender el sistema.  Acceder al menú de fábrica.  Acceder en modo automática (referirse a las secciones ajuste de filamento/kV feedback) en el sub-menu de ajuste de filamento en el caul ocurre la situación de error.  Mantener presionado el pulsador de disparo (PREP+RAD) hasta completar el proceso de calibración. En caso de que el error ocurriera mas de 3 veces, por favor asegurarse de que los pasos previos se siguieron correctamente y en el orden que fueron listados aquí. Si ese fuera el caso, por favor asegurarse de trabajar en condiciones correctas del sistema y cableado.

3.  Falla estator

Se queda girando el estator con posible recalentamiento del mismo. El triac de la placa estator no detecta que el estator queda girando y se produce un recalentamiento, esto fue una falla de diseño porque no tenía colocado un térmico que detectara este problema. Lo que se realizó fue cambiar un cable térmico en el estator. Los cables fueron enviados por el fabricante. El error se produjo en una partida de equipos en el año 2015 aproximadamente.

4.  Filament failure

Los pasos para chequear este equipo en caso que presente esta falla son los siguientes. Controla que los leds LD1 y LD3 en la placa S73 están encendidos. Apague el sistema y espere a que los capacitores se descarguen. 1. Controlar que los cables conectados a las placas S73, S74 y S77 están conectados

y fijados correctamente a cada conector. Controlar que el conector J5 está correctamente fijado al cabezal. Controlar que el jumper en JP3 está posicionado a



# Página 11

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    12/14 Troubleshooting

la izquierda (en la dirección del TP9 en la placa S73). Chequear también los cables de protección.

```metadata
pagina: 11
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I0.png
contexto: 
```

![Imagen página 11 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I0.png)

CP5 S73

CP1 S73

CP6 S73

```metadata
pagina: 11
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I1.png
contexto: 
```

![Imagen página 11 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I1.png)

```metadata
pagina: 11
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I2.png
contexto: 
```

![Imagen página 11 - 2](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P11_I2.png)

J5 MBK

El conector podría tener 3 o

5 polos

CN5 S74/S77



# Página 12

**Equipo:** Rodantes MAC GMM

Rodantes MAC GMM Código: HD-67 Versión: 002 Página:    13/14 Troubleshooting

2. Controlar la integridad del fusible F1 en la placa S73 (3,15 A código 52604) y la

integridad del fusible 230 V (2A código 32831) y 135 V (1 A código 00627) en el lado derecho del equipo.

3. Encender el sistema y controlar en el conector CP1 placa S73 la presencia de 135

Vac durante la carga de los capacitores.

4. En caso que las operaciones previas no resuelvan el problema, desarmar el

colimador y verificar que el filamento se encienda durante la carga.

```metadata
pagina: 12
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P12_I0.png
contexto: 
```

![Imagen página 12 - 0](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P12_I0.png)

```metadata
pagina: 12
imagen: data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P12_I1.png
contexto: 
```

![Imagen página 12 - 1](data/images/rodantes_mac_gmm_hd_67_troubleshooting_equipos_rodantes_mac_gmm_v2/P12_I1.png)



