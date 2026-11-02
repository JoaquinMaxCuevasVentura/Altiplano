# 10. Are.na: un atlas que la mano cura y la máquina lee

**Conectado el 10.10.2026** por el conector MCP de Are.na (§10.4, camino A), con la cuenta `joaquin-cuevas` (plan gratuito, 120 pedidos por minuto). Todavía no tiene canales.

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

### Camino A, recomendado: el conector MCP de Are.na

Are.na ofrece un servidor MCP propio, alojado en `https://mcp.are.na/mcp` (*Developers → Resources → Are.na MCP Server*). Se conecta como conector de Claude y se autoriza con la cuenta de Are.na (OAuth).

- No hay token que copiar ni secreto que guardar.
- No hace falta abrir la red del entorno: el tráfico de los conectores pasa por los servidores de Anthropic.

1. Entrar a `claude.ai/customize/connectors` (en el teléfono, desde Chrome).
2. Tocar **Add custom connector** y escribir:
   - **Name:** `Are.na`;
   - **Remote MCP server URL:** `https://mcp.are.na/mcp`.
3. Dejar vacíos los campos de *OAuth Client ID* y *Secret*: el servidor se registra solo. Tocar **Add**.
4. **Autorizar con la cuenta de Are.na.** Leer qué permiso pide la pantalla: si deja elegir, solo **lectura** (*read*). La API, si no se le pide otra cosa, da lectura. Con lectura, cualquier intento de escribir recibe `403`.
5. **Abrir una sesión nueva:** los conectores se leen cuando la sesión empieza.

### Camino B: token de lectura y secreto de red

**1 · El token, en Are.na.**

1. En are.na, con tu cuenta: **Developers → Personal Access Tokens** («Create and manage one-off access tokens»). Desde el teléfono, la dirección `are.na/settings/oauth` dio «Page not found»; se llega desde el menú de *Developers*.
2. En **Create token**:
   - **Token name:** `contenida (lectura)`;
   - **Expiration:** un plazo, no *Never*, para que el token se apague solo si queda olvidado;
   - **Access level:** dejar **Read-only**.
3. Tocar **Create token** y copiar el token. No guardarlo en ningún archivo del proyecto.

**2 · El secreto, en el entorno de la nube** (planes Pro y Max).

1. Entrar a `claude.ai/code`.
2. En la fila de arriba del cuadro de mensaje, tocar el botón con el ícono de nube y el nombre del entorno. Elegir **Cloud**, pasar el puntero sobre el entorno de este proyecto y tocar el ícono de engranaje.
3. En el diálogo **Edit environment**, ir a la sección **Network secrets** y tocar **Add secret**:
   - **Credential type:** dejar **Bearer**;
   - **Name:** `Are.na (lectura)`;
   - **Allowed websites:** `api.are.na`;
   - **Custom headers:** dejar la fila que trae, con **Name** `Authorization` y **Prefix** `Bearer`, y pegar el token en **Value**.
4. Tocar **Connect**. El secreto queda guardado y no se puede volver a ver.

Con el secreto, la máquina nunca ve el token: el proxy lo agrega a cada pedido a `api.are.na`, y ese dominio queda habilitado aunque la red no lo liste.

**3 · La documentación de Are.na** (opcional, para escribir el lector con la referencia a la vista).

1. En el mismo diálogo, cambiar **Network access** a **Custom**.
2. En **Allowed domains** escribir `www.are.na`.
3. Dejar marcada **Also include default list of common package managers**.
4. Tocar **Save changes**. Las sesiones abiertas toman el cambio en un minuto.

**Si la sección Network secrets no aparece** (planes Team o Enterprise):

1. Poner **Network access** en **Custom**, con `api.are.na` y `www.are.na` en **Allowed domains**.
2. En **Environment variables** agregar una línea: `ARENA_TOKEN=` y el token.
3. Tener en cuenta que quien use ese entorno puede leer esa variable. Por eso el token tiene que ser de solo lectura.
4. Una sesión nueva lee la variable.

**4 · El lector.** Con eso, la máquina escribe y prueba `herramientas/arena.py` contra la API v3. Si hay variable `ARENA_TOKEN`, la usa; si no, confía en el secreto del proxy.

**Las reglas del lector**, tomadas de las buenas prácticas de la API v3 (Are.na, *Developers → API Documentation*):

- **Pagina, no enumera.** Usa `page` y `per`: por defecto 24 por página, máximo 100. Lee una página y pide la siguiente solo si hace falta (`meta.has_more_pages`). Nunca recorre un canal entero al arrancar.
- **Primero el resumen, después el detalle.** Lee la primera página de un canal y abre un bloque solo cuando se lo pide.
- **Guarda lo que ya leyó.** Cada respuesta trae `ETag`. Al volver a pedir algo, lo manda como `If-None-Match`: si no cambió, la API responde `304` sin cuerpo. Igual cuenta para el límite.
- **Respeta el límite.** Mira `X-RateLimit-Limit` y `X-RateLimit-Reset`. Ante un `429` espera hasta el reinicio, con espera creciente, y deja de 200 a 500 ms entre pedidos.
- **No escribe en ráfagas.** No crea ni conecta bloques en serie: escribir es cosa de la mano.
- **No cosecha.** Las condiciones de uso de la API prohíben rastrear, descargar contenido en forma sistemática o recolectar datos en bloque. Coincide con lo que ya decidió el proyecto: no se descargan canales ajenos.
- **Los límites, por minuto:** 30 pedidos sin token, 120 con cuenta gratuita, 300 con *Premium* y 600 con *Supporter*. Un token de solo lectura que intenta escribir recibe `403`.
- **Para probar la conexión:** `/v3/ping` responde sin token, y `/v3/me` solo responde con un token válido (sin él, devuelve `401`).
- **Los errores** llegan en JSON (`error`, `code` y `details.message`). El lector los traduce en vez de seguir de largo:
  - 400: parámetros inválidos;
  - 401: falta el token o no sirve;
  - 403: el token no tiene permiso;
  - 404: no existe, o es privado y el token no lo ve;
  - 408: la API tardó demasiado;
  - 422: el pedido no se pudo procesar;
  - 429: se pasó el límite, y espera hasta `X-RateLimit-Reset`.

## 10.5. Lo que se corrige de la propuesta recibida

- **Los paquetes MCP que nombra no existen.** `arena-mcp` (PyPI) y `@modelcontextprotocol/server-arena` (npm) responden 404. El servidor de Are.na es otro: `@aredotna/mcp`, alojado en `https://mcp.are.na/mcp` (camino A).
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
