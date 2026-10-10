# 10. Are.na: un atlas que la mano cura y la máquina lee

Es una propuesta y todavía no hay conexión: el entorno donde trabaja la máquina bloquea `api.are.na` (§10.4).

## 10.1. Por qué rima

Are.na no ordena por algoritmo. Guarda **bloques** sueltos en **canales**, y un mismo bloque puede estar en varios canales sin copiarse: se *conecta*. Es la lógica de la caja:

- las placas son sueltas;
- componer es distribuir;
- *distribuir* es devolver cada tipo a su celda;
- una placa no se duplica: cada «a» es otra.

## 10.2. El reparto: la mano cura, la máquina lee

Es la misma regla de la simulación: la máquina confronta, no forma.

- **La mano cura.** Tú agregas los bloques en Are.na, a mano.
- **La máquina lee**, con un token de solo lectura. Hace tres cosas:
  - coteja cada bloque con los documentos: citas con página, nombres, fechas;
  - propone con qué verso o decisión rima;
  - redacta textos de bloque en un archivo local, y tú decides si los pegas.
- **Escribir por la API**, si algún día hace falta, pide un token con permiso de escritura (los tokens son de solo lectura por defecto). Además, cada envío se muestra antes de mandarlo y espera tu confirmación.

## 10.3. Los canales

Siguen la estructura del proyecto, no una nueva.

| Canal | Qué guarda | Visibilidad |
|---|---|---|
| `contenida` | La matriz: conecta los demás | Privado |
| `contenida · desenterrar` | Acciones 0 a 3: el pie, el frotado de la pared, los calcos | Privado |
| `contenida · contener` | Acciones 4 a 7: placas, caja, cinta, signo final | Privado |
| `contenida · devolver` | Acciones 8 a 12: frotados, agua, voz, composición | Privado |
| `contenida · la caja` | 56 bloques, uno por celda, en orden: la caja de 8 × 7 | Privado |
| `contenida · la máquina` | Lo que propone la simulación y la aplicación, rotulado como tal | Privado |
| `contenida · fuentes` | Citas breves con autor y página; materiales, herramientas, procedimientos | Privado |
| `contenida · la obra` | Solo lo que Rebeca autorice, por escrito | **Siempre privado** |

**Cómo se titula cada bloque.** Con la acción y la placa, por ejemplo «A4 · Repujar · a.03». En la descripción va la ficha.

**Conectar en lugar de copiar.** Una placa vive en su cuaderno y, conectada, también en `la caja`.

## 10.4. Para conectarlo

1. **Abrir la red.** En la configuración del entorno (el menú del entorno en la barra del título de la sesión, después *Edit*), en *Network access*, agregar `api.are.na` a los dominios permitidos, sin destildar los gestores de paquetes.
2. **Crear un token de solo lectura.** Se hace en Are.na, en `are.na/settings/oauth`, en la sección de tokens de acceso personal.
3. **Guardar el token en el entorno.** Va en la misma configuración, como secreto de red o como variable de entorno llamada `ARENA_TOKEN`. Una sesión nueva lo toma. **El token nunca se pega en el chat ni se sube al repositorio.**
4. **Escribir el lector.** Con eso, la máquina escribe y prueba un lector mínimo (`herramientas/arena.py`) contra la API v3, con la documentación a la vista.

## 10.5. Lo que se corrige de la propuesta recibida

- **No hay servidor MCP de Are.na publicado.** `arena-mcp` (PyPI) y `@modelcontextprotocol/server-arena` (npm) no existen: los dos registros responden 404.
- **La API v2 está obsoleta.** La vigente es la v3, en `api.are.na`.
- **«Closed» no es privado.** Un canal *closed* lo ve todo el mundo; solo restringe quién agrega. Si se lo crea con esa idea, se publica lo que se quería guardar. Además, un canal visible dentro de un grupo hace visible el perfil del grupo. Todo empieza privado.
- **La cinta no es negra.** Es masking blanca, tirando a hueso, sobre plástico negro.
- **El pavimento de losas de la cloaca** está en la plaza del pueblo de Tiwanaku (Posnansky, p. 60). La Paz se construyó con piedra de Tiwanaku (p. 59), que es otra cosa.
- **«El Desaguadero no tiene agua»** es lo que dice Posnansky en 1945 (p. 40), no un dato de hoy.
- **El dato del signo final es correcto:** la simulación da 0 frotadas legibles para el ¶. Pero la explicación del «domo del pulgar» es de esa IA. Lo que dice la ficha es más simple: «una presión de pulgar genérico: la máquina no tiene dedos».
- **No se buscan relieves de piedra para coleccionar motivos** (la búsqueda «latin american stone relief»). Es el exotismo que el proyecto rechaza: de las fuentes se toman materiales, herramientas y procedimientos.
- **No se descargan imágenes de canales ajenos** («epigrafía andina», frotados arqueológicos) para usarlas como referencia de forma. Tienen dueño, y copiarlas es tomar motivos.
- **No se suben los PDF** de las tesis, de Posnansky ni de los artículos, **ni el borrador inédito de Cárcamo**. Solo citas breves con su página.
- **Las fotos y videos del cuerpo de Rebeca** no entran en ningún canal sin su permiso escrito. Tampoco en uno privado, porque Are.na es un tercero.
