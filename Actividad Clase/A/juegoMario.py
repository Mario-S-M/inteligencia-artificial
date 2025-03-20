import pygame
from queue import PriorityQueue
import pygame.display

# Configuraciones iniciales - Modificación de tamaños de ventana
pygame.init()
ANCHO_VENTANA = 1000  # Aumentado para tener espacio para las listas a la derecha
ALTO_VENTANA = 600
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Visualización de A* - Con Enumeración Secuencial")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)
AZUL_CLARO = (200, 220, 255)  # Fondo para área de listas

# Inicializar fuente para mostrar cálculos - Ajuste de tamaños para cuadrícula más grande
pygame.font.init()
FUENTE_PEQUENA = pygame.font.SysFont('Arial', 10)  # Aumentado
FUENTE_NORMAL = pygame.font.SysFont('Arial', 12)   # Aumentado
FUENTE_LISTA = pygame.font.SysFont('Arial', 14)   # Mantenido para listas

class Nodo:
    def __init__(self, fila, col, ancho, total_filas, numero_secuencial):
        self.fila = fila
        self.col = col
        self.x = col * ancho
        self.y = fila * ancho
        self.ancho = ancho
        self.total_filas = total_filas
        self.numero_secuencial = numero_secuencial
        self.vecinos = []
        self.es_muro = False
        self.es_nodo_inicio = False
        self.es_nodo_fin = False
        self.visitado = False
        self.en_camino = False
        self.nodo_origen = None
        # Valores para A*
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        
    def get_pos(self):
        return self.fila, self.col
        
    def get_id(self):
        return str(self.numero_secuencial)

    def restablecer(self):
        self.es_muro = False
        self.es_nodo_inicio = False
        self.es_nodo_fin = False
        self.visitado = False
        self.en_camino = False
        self.nodo_origen = None
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

    def hacer_inicio(self):
        self.es_nodo_inicio = True

    def hacer_fin(self):
        self.es_nodo_fin = True

    def hacer_muro(self):
        self.es_muro = True
        
    def marcar_visitado(self):
        self.visitado = True
        
    def marcar_camino(self):
        self.en_camino = True

    def dibujar(self, ventana):
        # Dibujar fondo de la celda
        if self.es_muro:
            pygame.draw.rect(ventana, NEGRO, (self.x, self.y, self.ancho, self.ancho))
        else:
            pygame.draw.rect(ventana, BLANCO, (self.x, self.y, self.ancho, self.ancho))
            
            # Mostrar número secuencial más pequeño en la esquina
            if not self.es_nodo_inicio and not self.es_nodo_fin:
                id_texto = FUENTE_PEQUENA.render(self.get_id(), True, NEGRO)
                ventana.blit(id_texto, (self.x + 2, self.y + 2))
            
            # Mostrar valores de g, h, f de manera más compacta
            if self.f != float("inf") and not self.es_nodo_inicio and not self.es_nodo_fin:
                # Formato compacto para valores
                g_texto = FUENTE_PEQUENA.render(f"g:{int(self.g)}", True, NEGRO)
                h_texto = FUENTE_PEQUENA.render(f"h:{int(self.h)}", True, NEGRO)
                f_texto = FUENTE_PEQUENA.render(f"f:{int(self.f)}", True, NEGRO)
                
                # Ubicaciones ajustadas para mejor visibilidad con cuadrícula más grande
                ventana.blit(g_texto, (self.x + 5, self.y + self.ancho//2 - 15))
                ventana.blit(h_texto, (self.x + 5, self.y + self.ancho//2))
                ventana.blit(f_texto, (self.x + 5, self.y + self.ancho//2 + 15))
            
            # Marcar nodos visitados con "*" más visible
            if self.visitado and not self.es_nodo_inicio and not self.es_nodo_fin:
                visitado_texto = FUENTE_NORMAL.render("*", True, NEGRO)
                ventana.blit(visitado_texto, (self.x + self.ancho - 12, self.y + 3))
            
            # Marcar nodos de inicio y fin
            if self.es_nodo_inicio:
                inicio_texto = FUENTE_NORMAL.render("INICIO", True, NEGRO)
                ventana.blit(inicio_texto, (self.x + (self.ancho - inicio_texto.get_width()) // 2, 
                                           self.y + (self.ancho - inicio_texto.get_height()) // 2))
            
            if self.es_nodo_fin:
                fin_texto = FUENTE_NORMAL.render("FIN", True, NEGRO)
                ventana.blit(fin_texto, (self.x + (self.ancho - fin_texto.get_width()) // 2, 
                                        self.y + (self.ancho - fin_texto.get_height()) // 2))
            
            # Dibujar borde rojo si es parte del camino final
            if self.en_camino:
                pygame.draw.rect(ventana, ROJO, (self.x, self.y, self.ancho, self.ancho), 3)
        
    def actualizar_vecinos(self, grid):
        self.vecinos = []
        
        # Abajo
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_muro:
            self.vecinos.append((grid[self.fila + 1][self.col], 10, "abajo"))
            
        # Arriba
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_muro:
            self.vecinos.append((grid[self.fila - 1][self.col], 10, "arriba"))
            
        # Derecha
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_muro:
            self.vecinos.append((grid[self.fila][self.col + 1], 10, "derecha"))
            
        # Izquierda
        if self.col > 0 and not grid[self.fila][self.col - 1].es_muro:
            self.vecinos.append((grid[self.fila][self.col - 1], 10, "izquierda"))
            
        # Diagonales (costo 14)
        # Diagonal abajo-derecha
        if (self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and 
            not grid[self.fila + 1][self.col + 1].es_muro and 
            not grid[self.fila + 1][self.col].es_muro and 
            not grid[self.fila][self.col + 1].es_muro):
            self.vecinos.append((grid[self.fila + 1][self.col + 1], 14, "diagonal-dr"))
            
        # Diagonal abajo-izquierda
        if (self.fila < self.total_filas - 1 and self.col > 0 and 
            not grid[self.fila + 1][self.col - 1].es_muro and 
            not grid[self.fila + 1][self.col].es_muro and 
            not grid[self.fila][self.col - 1].es_muro):
            self.vecinos.append((grid[self.fila + 1][self.col - 1], 14, "diagonal-di"))
            
        # Diagonal arriba-derecha
        if (self.fila > 0 and self.col < self.total_filas - 1 and 
            not grid[self.fila - 1][self.col + 1].es_muro and 
            not grid[self.fila - 1][self.col].es_muro and 
            not grid[self.fila][self.col + 1].es_muro):
            self.vecinos.append((grid[self.fila - 1][self.col + 1], 14, "diagonal-ar"))
            
        # Diagonal arriba-izquierda
        if (self.fila > 0 and self.col > 0 and 
            not grid[self.fila - 1][self.col - 1].es_muro and 
            not grid[self.fila - 1][self.col].es_muro and 
            not grid[self.fila][self.col - 1].es_muro):
            self.vecinos.append((grid[self.fila - 1][self.col - 1], 14, "diagonal-ai"))
    
    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        return self.f < other.f

def h(p1, p2):
    """Heurística: distancia Manhattan * 10 para coordinar con los costos"""
    x1, y1 = p1
    x2, y2 = p2
    return 10 * (abs(x1 - x2) + abs(y1 - y2))

def reconstruir_camino(came_from, actual, dibujar, lista_abierta, lista_cerrada):
    nodos_camino = set()
    
    while actual in came_from:
        actual.marcar_camino()
        nodos_camino.add(actual)
        actual = came_from[actual]
    
    actual.marcar_camino()
    nodos_camino.add(actual)
    
    dibujar(lista_abierta, lista_cerrada, nodos_camino)

def algoritmo_a_star(dibujar, grid, inicio, fin, filas, ancho_grid):
    contador = 0
    conjunto_abierto = PriorityQueue()
    conjunto_abierto.put((0, contador, inicio))
    came_from = {}
    
    lista_abierta = {inicio}
    lista_cerrada = set()
    
    inicio.g = 0
    inicio.h = h(inicio.get_pos(), fin.get_pos())
    inicio.f = inicio.h
    
    while not conjunto_abierto.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
                
        actual = conjunto_abierto.get()[2]
        lista_abierta.remove(actual)
        lista_cerrada.add(actual)
        
        if actual != inicio and actual != fin:
            actual.marcar_visitado()
        
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar, lista_abierta, lista_cerrada)
            fin.marcar_camino()
            inicio.marcar_camino()
            
            nodos_camino = set()
            actual = fin
            while actual in came_from:
                nodos_camino.add(actual)
                actual = came_from[actual]
            nodos_camino.add(inicio)
            
            dibujar(lista_abierta, lista_cerrada, nodos_camino)
            
            mostrar_resultado = True
            while mostrar_resultado:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return True
                        mostrar_resultado = False
                        break
                
                dibujar(lista_abierta, lista_cerrada, nodos_camino)
                pygame.time.delay(100)
            
            return True
            
        for vecino, costo, direccion in actual.vecinos:
            if vecino in lista_cerrada:
                continue
                
            temp_g = actual.g + costo
            
            if temp_g < vecino.g:
                came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = h(vecino.get_pos(), fin.get_pos())
                vecino.f = vecino.g + vecino.h
                
                vecino.nodo_origen = actual
                
                if vecino not in lista_abierta:
                    contador += 1
                    conjunto_abierto.put((vecino.f, contador, vecino))
                    lista_abierta.add(vecino)
        
        dibujar(lista_abierta, lista_cerrada, set())
            
    return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    numero = 1
    
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas, numero)
            grid[i].append(nodo)
            numero += 1
            
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo), 2)  # Líneas horizontales más gruesas
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho), 2)  # Líneas verticales más gruesas

def dibujar_listas(ventana, lista_abierta, lista_cerrada, nodos_camino, ancho_grid, alto_ventana):
    # Área dedicada para las listas (a la derecha)
    area_listas = pygame.Rect(ancho_grid + 10, 0, ANCHO_VENTANA - ancho_grid - 10, alto_ventana)
    pygame.draw.rect(ventana, AZUL_CLARO, area_listas)
    pygame.draw.rect(ventana, NEGRO, area_listas, 2)  # Borde
    
    # Título de lista abierta
    titulo_abierta = FUENTE_LISTA.render("Lista Abierta:", True, NEGRO)
    ventana.blit(titulo_abierta, (ancho_grid + 20, 20))
    
    # Mostrar lista abierta con IDs
    lista_abierta_ordenada = sorted(lista_abierta, key=lambda x: (x.f, -x.g))
    ids_abierta = [nodo.get_id() for nodo in lista_abierta_ordenada if nodo.f != float("inf")]
    
    # Mostrar IDs en columnas para mejor visualización
    x_pos = ancho_grid + 20
    y_pos = 50
    max_width = ANCHO_VENTANA - ancho_grid - 40  # Margen para columnas
    
    # Renderizar "Lista Abierta: ["
    texto_inicio = FUENTE_LISTA.render("Lista Abierta: [", True, NEGRO)
    ventana.blit(texto_inicio, (x_pos, y_pos))
    x_pos += texto_inicio.get_width()
    
    # Renderizar cada ID de la lista abierta
    for i, id_str in enumerate(ids_abierta):
        if i > 0:  # Añadir coma si no es el primer elemento
            coma = FUENTE_LISTA.render(", ", True, NEGRO)
            ventana.blit(coma, (x_pos, y_pos))
            x_pos += coma.get_width()
        
        id_texto = FUENTE_LISTA.render(id_str, True, ROJO if any(nodo.numero_secuencial == int(id_str) and nodo in nodos_camino for nodo in lista_abierta) else NEGRO)
        
        # Si se excede el ancho, pasar a la siguiente línea
        if x_pos + id_texto.get_width() > ancho_grid + max_width:
            y_pos += 25
            x_pos = ancho_grid + 40  # Con indentación
        
        ventana.blit(id_texto, (x_pos, y_pos))
        x_pos += id_texto.get_width()
    
    # Cerrar lista abierta
    cierre = FUENTE_LISTA.render("]", True, NEGRO)
    ventana.blit(cierre, (x_pos, y_pos))
    
    # Título de lista cerrada (dejar espacio adecuado)
    y_pos += 50
    titulo_cerrada = FUENTE_LISTA.render("Lista Cerrada:", True, NEGRO)
    ventana.blit(titulo_cerrada, (ancho_grid + 20, y_pos))
    y_pos += 30
    
    # Mostrar lista cerrada
    x_pos = ancho_grid + 20
    texto_inicio = FUENTE_LISTA.render("Lista Cerrada: [", True, NEGRO)
    ventana.blit(texto_inicio, (x_pos, y_pos))
    x_pos += texto_inicio.get_width()
    
    # Renderizar cada ID de la lista cerrada con tachado
    lista_cerrada_ordenada = sorted(lista_cerrada, key=lambda x: x.numero_secuencial)
    
    for i, nodo in enumerate(lista_cerrada_ordenada):
        if nodo.f == float("inf"):
            continue
            
        if i > 0:  # Añadir coma si no es el primer elemento
            coma = FUENTE_LISTA.render(", ", True, NEGRO)
            ventana.blit(coma, (x_pos, y_pos))
            x_pos += coma.get_width()
        
        # Color rojo para nodos en el camino final
        color = ROJO if nodo in nodos_camino else NEGRO
        
        id_texto = FUENTE_LISTA.render(nodo.get_id(), True, color)
        
        # Si se excede el ancho, pasar a la siguiente línea
        if x_pos + id_texto.get_width() > ancho_grid + max_width:
            y_pos += 25
            x_pos = ancho_grid + 40  # Con indentación
        
        ventana.blit(id_texto, (x_pos, y_pos))
        
        # Dibujar línea de tachado
        pygame.draw.line(ventana, color, 
                         (x_pos, y_pos + id_texto.get_height()//2), 
                         (x_pos + id_texto.get_width(), y_pos + id_texto.get_height()//2), 
                         1)
        
        x_pos += id_texto.get_width()
    
    # Cerrar lista cerrada
    cierre = FUENTE_LISTA.render("]", True, NEGRO)
    ventana.blit(cierre, (x_pos, y_pos))

def dibujar(ventana, grid, filas, ancho_grid, lista_abierta=None, lista_cerrada=None, nodos_camino=None):
    # Limpiar ventana
    ventana.fill(BLANCO)
    
    # Dibujar nodos de la cuadrícula
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    # Dibujar líneas de la cuadrícula
    dibujar_grid(ventana, filas, ancho_grid)
    
    # Dibujar listas a la derecha si están disponibles
    if lista_abierta is not None and lista_cerrada is not None:
        if nodos_camino is None:
            nodos_camino = set()
        dibujar_listas(ventana, lista_abierta, lista_cerrada, nodos_camino, ancho_grid, ALTO_VENTANA)
    
    # Añadir instrucciones en la parte inferior
    instrucciones_texto = "ESC: Salir | ESPACIO: Iniciar algoritmo | C: Limpiar todo"
    instrucciones = FUENTE_LISTA.render(instrucciones_texto, True, NEGRO)
    ventana.blit(instrucciones, (10, ALTO_VENTANA - 30))
    
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    x, y = pos
    col = x // ancho_nodo
    fila = y // ancho_nodo
    return fila, col

def main(ventana, ancho, alto):
    # Configurar para cuadrícula cuadrada que ocupe la altura de la ventana
    ancho_grid = alto  # La cuadrícula será cuadrada con el tamaño de la altura
    
    # Número de filas - Cambiado a 10x10 como solicitado
    FILAS = 10
    grid = crear_grid(FILAS, ancho_grid)

    inicio = None
    fin = None

    corriendo = True
    iniciado = False

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False
                
            # Si el algoritmo ya está corriendo, no permitir cambios
            if iniciado:
                continue
                
            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                if pos[0] < ancho_grid:  # Solo dentro de la cuadrícula
                    fila, col = obtener_click_pos(pos, FILAS, ancho_grid)
                    if fila < FILAS and col < FILAS:
                        nodo = grid[fila][col]
                        
                        if not inicio and nodo != fin:
                            inicio = nodo
                            inicio.hacer_inicio()

                        elif not fin and nodo != inicio:
                            fin = nodo
                            fin.hacer_fin()

                        elif nodo != fin and nodo != inicio:
                            nodo.hacer_muro()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                if pos[0] < ancho_grid:  # Solo dentro de la cuadrícula
                    fila, col = obtener_click_pos(pos, FILAS, ancho_grid)
                    if fila < FILAS and col < FILAS:
                        nodo = grid[fila][col]
                        nodo.restablecer()
                        if nodo == inicio:
                            inicio = None
                        elif nodo == fin:
                            fin = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not iniciado and inicio and fin:
                    # Reiniciar valores
                    for fila in grid:
                        for nodo in fila:
                            if not (nodo.es_muro or nodo.es_nodo_inicio or nodo.es_nodo_fin):
                                nodo.restablecer()
                    
                    # Actualizar vecinos
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    
                    # Iniciar algoritmo
                    iniciado = True
                    algoritmo_a_star(
                        lambda lista_a=None, lista_c=None, nodos_p=None: dibujar(ventana, grid, FILAS, ancho_grid, 
                                                            lista_a if lista_a is not None else set(), 
                                                            lista_c if lista_c is not None else set(),
                                                            nodos_p if nodos_p is not None else set()),
                        grid, inicio, fin, FILAS, ancho_grid
                    )
                    iniciado = False
                    
                if event.key == pygame.K_c:
                    # Limpiar todo
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho_grid)

    pygame.quit()

if __name__ == "__main__":
    main(VENTANA, ANCHO_VENTANA, ALTO_VENTANA)