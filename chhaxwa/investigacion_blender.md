# Investigación: modelar las pruebas en Blender

27 de noviembre de 2026. El autor pidió investigar antes de modelar en Blender. Le interesaban los repositorios de GitHub y la manera de lograr materiales procedurales realistas, una iluminación realista y lo demás que haga falta para modelar las pruebas de forma hiperrealista, en la forma y en la materia. Este documento reúne lo que se encontró, lo que se probó en el entorno de trabajo y lo que se propone.

## 1. Lo que el autor tiene que decidir antes

Las reglas del proyecto (`LEEME.md`) dicen que el modelo en el computador sirve para medir y planificar, y que lo que se muestra es la maqueta (regla 3). Un render hiperrealista cambia eso, y además trae un riesgo: puede pasar por la foto de algo que no se construyó. La regla 5 no está en juego, porque un render de Blender no es una imagen hecha con IA. Lo calcula el programa a partir de la geometría, los materiales y la luz que se le dan. Pero mientras más realista sea, más fácil es confundirlo.

**La propuesta es tratar cada render como una predicción.** Muestra cómo se espera que quede la maqueta o la obra. Cuando se construya, la foto se pone a su lado, y la diferencia entre las dos es un resultado. Es el contraste que hace Chandler entre el trabajo de certeza, que se decide antes, y el de riesgo, que se decide en la mano (Chandler, 2017: 216). Para que no haya confusión:

- cada imagen se llama `render_…` y su pie dice «Render de Blender, no es una foto»;
- no se publica un render como registro de una prueba;
- la regla 3 se reescribe así, si el autor está de acuerdo: «El modelo en el computador sirve para medir, planificar y predecir. Sus renders se muestran como predicciones, siempre rotulados, y se comparan con las fotos de las maquetas».

## 2. Lo que se encontró

### 2.1 Proyectos de código abierto

| Proyecto | Qué hace | Para qué sirve aquí |
|---|---|---|
| [Infinigen](https://github.com/princeton-vl/infinigen), del laboratorio de visión de Princeton | Genera escenas naturales fotorrealistas sobre Blender, todo con código: terreno, rocas, plantas y sus materiales. Convierte árboles de nodos en Python | Es el mejor ejemplo de materiales procedurales escritos como código. Se puede estudiar cómo arma la roca, el suelo y el pasto |
| [BlenderProc](https://github.com/DLR-RM/BlenderProc), del Centro Aeroespacial Alemán (GPL-3.0) | Una cadena de render fotorrealista con guiones. Carga texturas libres de ambientCG y cielos de Poly Haven | Es un modelo de cómo organizar el trabajo: escenas armadas por código, reproducibles |
| [Bullet Constraints Builder](https://github.com/KaiKostack/bullet-constraints-builder), de Kai Kostack | Un complemento de Blender que simula el colapso de estructuras con el motor físico Bullet. Se usó para predecir derrumbes de la Gran Muralla (Du et al., 2022) | Para la prueba 2 (sacar el relleno hasta que el muro cae) y la 3 (cuánto vuela una hilada) |
| [Meshroom](https://github.com/alicevision/meshroom), de AliceVision | Fotogrametría libre: reconstruye un objeto en 3D a partir de fotos. Desde 2025 tiene estéreo fotométrico, que separa el relieve fino de la luz | Para escanear las piedras, la champa y las maquetas reales, y usar su textura verdadera |
| [AgX](https://github.com/EaryChow/AgX), de Eary Chow | La transformación de color que Blender usa desde la versión 4.0. Da 16,5 pasos de rango dinámico y trata mejor los colores saturados que Filmic | Para que la luz del altiplano, muy contrastada, no queme los blancos |

Las herramientas que mejor resuelven pircas y techos de paja son pagadas: el generador de pircas PRIAPOS, el de muros Rampart y varios generadores de techos de paja. No se usan, para que el proyecto se pueda reproducir sin comprar nada. Los generadores de este proyecto están escritos aquí (`blender/comun.py`).

### 2.2 Materiales

- **Procedurales.** Se arman con ruido, Voronoi y ondas en nodos de Blender. Lo que más ayuda al realismo es oscurecer las juntas y cavidades (oclusión ambiental), variar el color de piedra en piedra y añadir un relieve fino que no está en la geometría.
- **Los colores tienen que ser físicamente posibles.** El color base de un material es su albedo, la fracción de luz que devuelve. Las tablas que circulan son aproximadas: roca de 0,3 a 0,4, suelo seco de 0,17 a 0,45, pasto alto de 0,16 a 0,25. Pasarse de esos valores hace que un material «brille» y delata el render.
- **Texturas escaneadas libres.** Poly Haven publica texturas fotografiadas con licencia CC0 y tiene una API pública. Hoy, 27 de noviembre, su catálogo tiene, entre otras, un techo de paja (`thatch_roof_angled`), techos de junco (`reed_roof_03`, `reed_roof_04`), pasto seco (`withered_grass`), barro seco (`brown_mud_dry`), suelo agrietado (`cracked_red_ground`), revoque de barro (`clay_plaster`), muro de bloques de tierra (`clay_block_wall`), arpillera (`hessian_230` y `hessian_380`, que sirve para la huella del costal en la *p'ira*) y piedras (`namaqualand_stones_01`). ambientCG publica otras con la misma licencia. No se suben al repositorio por su tamaño: si se usan, un guion las descarga.
- **Lo más fiel es escanear el material real.** Fotografiar la piedra, la tierra y el ichu del lugar donde se hagan las pruebas y reconstruirlos con Meshroom da la textura verdadera, y es coherente con la regla del material real.
- **El ichu.** *Jarava ichu* (sinónimo *Stipa ichu*) crece en matas densas, con cañas de 25 a 150 cm y hojas angostas, de 0,2 a 2 mm, planas, plegadas o enrolladas. Se usó para techar. Se modela con briznas curvas agrupadas en matas, un poco translúcidas, y con el color de la paja seca.

### 2.3 Luz

- **El cielo.** Blender 5.0 trae un cielo físico de dispersión múltiple, más exacto que el anterior (llamado Nishita, que queda como «dispersión simple»). Se le dan la altura del sol sobre el horizonte, su giro y la altitud de la cámara sobre el mar.
- **El sol de La Paz.** Se comprobó con un render de prueba que el giro del sol en Blender es el mismo acimut de la tabla de la prueba 5, si +y es el norte y +x el este. La tabla entra directamente: 21 de junio a las 10, altura 35,1° y acimut 44,3°. La altitud se pone en 3.850 m.
- **El complemento Sun Position** de Blender calcula lo mismo a partir de la latitud, la longitud, la fecha y la hora. No hace falta, porque el proyecto usa las fórmulas de la NOAA (`blender/comun.py`).
- **La exposición.** El cielo físico es muy brillante y el manual de Blender recomienda bajar la exposición. Con AgX, −5 pasos dio valores creíbles en el exterior.
- **La perspectiva aérea.** El cielo de Blender no vela los cerros lejanos. El aire del altiplano es claro, pero algo de velo hace falta. El prototipo lo resuelve en el material de los cerros, mezclándolo con el color del cielo según la distancia.
- **El estudio de las maquetas.** Fondo curvo gris claro, mesa de terciado sobre caballetes, una luz grande de ventana a un lado y un rebote suave, como en las fotos de referencia.

### 2.4 Simulación: lo que la maqueta no puede

- **Cuerpos rígidos.** El motor Bullet de Blender sirve para predecir cómo cae una mampostería de piedra seca, sin pretender exactitud de ingeniería. La literatura lo valida para predicciones cualitativas y advierte que no siempre coincide con las soluciones analíticas (Andrews et al., 2025) y que se le escapan las fisuras (Di Giosaffatte et al., 2025). En un montón, el ángulo del talud depende sobre todo del roce entre las piedras y de su forma.
- **Humo.** Mantaflow, el simulador de fluidos de Blender, puede llenar de humo la *chujlla* a tamaño real. La maqueta 1:10 no puede, porque el humo no se escala (prueba 5). La simulación es lenta y su render también.

## 3. Lo que se probó aquí

- **Blender 5.0.1 como módulo de Python**, instalado desde PyPI (`pip install bpy==5.0.1`; es la versión más nueva para Python 3.11). Funcionan Cycles en la CPU, el eliminador de ruido OpenImageDenoise, la transformación AgX y Freestyle, que dibuja líneas sobre el render.
- **Un prototipo en el paisaje** (`blender/prototipo_pirca_paisaje.py`): una pirca de 5 m con unas 460 piedras procedurales, piedrecilla regada, 2.260 matas de ichu, suelo de puna, cerros lejanos, el cielo de dispersión múltiple a 3.850 m y el sol del 21 de junio a las 10. A 1.280 × 800 píxeles y 64 muestras tardó 4 minutos y 18 segundos en cuatro núcleos (`renders/render_prototipo_pirca_paisaje.jpg`). Le falta mucho para ser hiperrealista. Las piedras todavía se ven ordenadas en hiladas parejas, el suelo es liso, los líquenes parecen pintados y los cerros casi no se ven.
- **Las quince maquetas de forma** de `exploracion_formal.md`, en el estudio, con `blender/renderizar.py`. Cada una tarda unos 7 segundos en la versión rápida y unos 3 minutos en la final.
- **Los cuerpos rígidos funcionan sin pantalla**, pero la primera prueba del montón no sirve todavía. Se llenó un tubo de piedras, se levantó despacio y el montón quedó casi plano, con 3 a 5° de talud, con roces de 0,4 a 1,0. Eso indica un problema del ensayo (piedras chicas y livianas, margen de colisión, amortiguación) y no un dato. Hay que calibrarlo con piedras a tamaño real antes de usarlo.

## 4. Lo que se propone

1. **Un modelo por forma y tres salidas.** De cada modelo salen el render de la maqueta en el estudio, que es la foto prevista, el render de la obra a tamaño real en el altiplano y las cuatro axonometrías del proceso en línea, con Freestyle, que reemplazan los dibujos planeados en `analisis/42` (§6).
2. **Subir el realismo por pasos.** Primero las piedras, con más cortes y suciedad en las juntas, y la paja con su translucidez. Después las texturas escaneadas por el autor o, mientras tanto, las de Poly Haven. Al final, la cámara: lente, profundidad de campo y la altura de los ojos en cuclillas en la prueba 5.
3. **Simular lo que la maqueta no puede.** El montón y el derrumbe con cuerpos rígidos, una vez calibrados. El humo de la *chujlla* a tamaño real.
4. **Comparar.** Cuando haya maquetas, se fotografían como dice la ficha y se ponen junto a su render.

## Fuentes

- Andrews, S. et al. (2025). Estudios sobre el balanceo de bloques de mampostería con motores físicos. École de technologie supérieure, Montreal. https://espace2.etsmtl.ca/31237/1/Andrews-S-2025-31237.pdf
- Blender (2025). *Blender 5.0: Rendering* (notas de la versión: el cielo de dispersión múltiple). https://developer.blender.org/docs/release_notes/5.0/rendering/
- Blender. *Sky Texture Node* y *Color Management*, manual de Blender. https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/sky.html
- Blender. *Sun Position*, manual de Blender. https://docs.blender.org/manual/en/4.1/addons/lighting/sun_position.html
- Blender. *Blender as a Python Module*. https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html
- Chandler, Alan (2017). En Radić (2017): 213 y ss.
- Di Giosaffatte, M. et al. (2025). *Alternative approaches in computational mechanics* (Blender para edificios históricos). Universidad Politécnica de las Marcas. https://iris.univpm.it/retrieve/92a5b173-8205-41a9-b807-e659a51be5ec/Di%20Giosafatte_Alternative-approaches-computational-mechanics_2025.pdf
- Du, Y. et al. (2022). Predicción de colapsos en la Gran Muralla Ming con Blender. *Buildings*. https://doaj.org/article/efaad77af159483f8605c9c924067b0c
- *Jarava ichu*: GrassBase y la clave DELTA de géneros de gramíneas. https://www.delta-intkey.com/grass/www/jarava.htm
- Poly Haven: catálogo y API (consultados el 27 de noviembre de 2026). https://polyhaven.com y https://api.polyhaven.com
- Radić, Smiljan (2017). *Obra gruesa*. Santiago de Chile: Ediciones Puro Chile y Fundación Antenna.
- Raistrick, A. et al. (2023). «Infinite Photorealistic Worlds using Procedural Generation». CVPR. https://arxiv.org/abs/2306.09310
- Valores de albedo: tabla de la Universidad Estatal de Pensilvania (https://www.e-education.psu.edu/earth103/node/1002) y recopilación de valores para PBR (https://blog.csdn.net/cubesky/article/details/106095521), las dos aproximadas.
- Wang, Pulatsu, Andrews y Malomo (2025). PyBullet para mampostería de junta seca. https://pure.etsmtl.ca/en/publications/breaking-boundaries-discontinuum-failure-analysis-of-dry-joint-ma/
