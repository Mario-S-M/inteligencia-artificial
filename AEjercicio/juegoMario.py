import pygame
from queue import PriorityQueue

# Configuraciones iniciales
ANCHO_VENTANA = 800
ALTO_VENTANA = 1000  # Para mostrar las listas
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Visualización de A* - Con Enumeración Secuencial")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)

# Inicializar fuente para mostrar cálculos
pygame.font.init()
FUENTE_PEQUENA = pygame.font.SysFont('Arial', 10)
FUENTE_NORMAL = pygame.font.SysFont('Arial', 14)
FUENTE_LISTA = pygame.font.SysFont('Arial', 16)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas, numero_secuencial):
        self.fila = fila
        self.col = col
        self.x = col * ancho
        self.y = fila * ancho
        self.ancho = ancho
        self.total_filas = total_filas
        self.numero_secuencial = numero_secuencial  # Número secuencial (1, 2, 3...)
        self.vecinos = []
        self.es_muro = False
        self.es_nodo_inicio = False
        self.es_nodo_fin = False
        self.visitado = False  # Para marcar con "*"
        self.en_camino = False  # Para marcar como parte del camino final
        self.nodo_origen = None  # Para saber de qué nodo se calculó
        # Valores para A*
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        
    def get_pos(self):
        return self.fila, self.col
        
    def get_id(self):
        return str(self.numero_secuencial)  # Usar número secuencial como ID

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
        # Dibujar fondo de la celda (blanco o negro para paredes)
        if self.es_muro:
            pygame.draw.rect(ventana, NEGRO, (self.x, self.y, self.ancho, self.ancho))
        else:
            pygame.draw.rect(ventana, BLANCO, (self.x, self.y, self.ancho, self.ancho))
            
            # Mostrar número secuencial en la esquina superior izquierda
            # PERO NO para los nodos de inicio y fin
            if not self.es_nodo_inicio and not self.es_nodo_fin:
                id_texto = FUENTE_PEQUENA.render(self.get_id(), True, NEGRO)
                ventana.blit(id_texto, (self.x + 2, self.y + 2))
            
            # Mostrar valores de g, h, f en el centro (en ese orden)
            # también evitamos en nodos inicio/fin
            if self.f != float("inf") and not self.es_nodo_inicio and not self.es_nodo_fin:
                g_texto = FUENTE_NORMAL.render(f"g:{int(self.g)}", True, NEGRO)
                h_texto = FUENTE_NORMAL.render(f"h:{int(self.h)}", True, NEGRO)
                f_texto = FUENTE_NORMAL.render(f"f:{int(self.f)}", True, NEGRO)
                
                # Centrar los textos - cambiando el orden: G, H, F
                ventana.blit(g_texto, (self.x + (self.ancho - g_texto.get_width()) // 2, 
                                       self.y + (self.ancho // 2) - 25))
                ventana.blit(h_texto, (self.x + (self.ancho - h_texto.get_width()) // 2, 
                                       self.y + (self.ancho // 2) - 5))
                ventana.blit(f_texto, (self.x + (self.ancho - f_texto.get_width()) // 2, 
                                       self.y + (self.ancho // 2) + 15))
            
            # Marcar nodos visitados con "*"
            if self.visitado and not self.es_nodo_inicio and not self.es_nodo_fin:
                visitado_texto = FUENTE_NORMAL.render("*", True, NEGRO)
                ventana.blit(visitado_texto, (self.x + self.ancho - 15, self.y + 5))
            
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
                pygame.draw.rect(ventana, ROJO, (self.x, self.y, self.ancho, self.ancho), 3)  # Borde rojo
        
    def actualizar_vecinos(self, grid):
        self.vecinos = []
        
        # Abajo
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_muro:
            self.vecinos.append((grid[self.fila + 1][self.col], 10, "abajo"))  # Costo 10 para vertical
            
        # Arriba
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_muro:
            self.vecinos.append((grid[self.fila - 1][self.col], 10, "arriba"))  # Costo 10 para vertical
            
        # Derecha
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_muro:
            self.vecinos.append((grid[self.fila][self.col + 1], 10, "derecha"))  # Costo 10 para horizontal
            
        # Izquierda
        if self.col > 0 and not grid[self.fila][self.col - 1].es_muro:
            self.vecinos.append((grid[self.fila][self.col - 1], 10, "izquierda"))  # Costo 10 para horizontal
            
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
        # Modificado para usar f como principal factor de comparación (A* puro, sin componente voraz)
        if self.f == other.f:
            return self.g > other.g  # Si f es igual, prefiere nodo con mayor g
        return self.f < other.f

def h(p1, p2):
    """Heurística: distancia Manhattan * 10 para coordinar con los costos"""
    x1, y1 = p1
    x2, y2 = p2
    return 10 * (abs(x1 - x2) + abs(y1 - y2))

def reconstruir_camino(came_from, actual, dibujar):
    # Marcar todos los nodos del camino final
    while actual in came_from:
        actual.marcar_camino()
        actual = came_from[actual]
    
    # También marcar el nodo de inicio
    actual.marcar_camino()
    dibujar()

def algoritmo_a_star(dibujar, grid, inicio, fin):
    contador = 0
    conjunto_abierto = PriorityQueue()
    conjunto_abierto.put((0, contador, inicio))
    came_from = {}
    
    # Lista para seguimiento de nodos abiertos y cerrados
    lista_abierta = {inicio}
    lista_cerrada = set()
    
    inicio.g = 0
    inicio.h = h(inicio.get_pos(), fin.get_pos())
    inicio.f = inicio.h
    
    while not conjunto_abierto.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        actual = conjunto_abierto.get()[2]
        lista_abierta.remove(actual)
        lista_cerrada.add(actual)
        
        # Marcar nodo como visitado
        if actual != inicio and actual != fin:
            actual.marcar_visitado()
        
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.marcar_camino()  # Asegurar que el nodo final esté marcado
            inicio.marcar_camino()  # Asegurar que el nodo inicial esté marcado
            # Dibujar una última vez para mostrar las listas finales
            dibujar(lista_abierta, lista_cerrada)
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
                
                # Almacenar el nodo origen
                vecino.nodo_origen = actual
                
                if vecino not in lista_abierta:
                    contador += 1
                    conjunto_abierto.put((vecino.f, contador, vecino))
                    lista_abierta.add(vecino)
        
        # Asegurarse de llamar a dibujar con los parámetros correctos
        dibujar(lista_abierta, lista_cerrada)
            
    return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    numero = 1  # Comenzamos a numerar desde 1
    
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            # Cambiamos el orden de los índices para que la numeración sea por columnas
            nodo = Nodo(i, j, ancho_nodo, filas, numero)
            grid[i].append(nodo)
            numero += 1  # Incrementamos el número secuencial
            
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar_listas(ventana, lista_abierta, lista_cerrada, ancho, altura_grid):
    # Limpiar el área de las listas primero
    pygame.draw.rect(ventana, BLANCO, (0, altura_grid, ancho, ALTO_VENTANA - altura_grid))
    
    # Dibujar línea divisoria
    pygame.draw.line(ventana, NEGRO, (0, altura_grid), (ancho, altura_grid), 3)
    
    # Título de lista abierta
    titulo_abierta = FUENTE_LISTA.render("Lista Abierta:", True, NEGRO)
    ventana.blit(titulo_abierta, (20, altura_grid + 10))
    
    # Elementos de lista abierta
    y_pos = altura_grid + 40
    x_pos = 20
    max_y = ALTO_VENTANA - 30
    
    # Ordenar lista abierta por valor f
    lista_abierta_ordenada = sorted(lista_abierta, key=lambda x: (x.f, -x.g))
    
    for nodo in lista_abierta_ordenada:
        if nodo.f != float("inf"):  # Solo mostrar nodos con valores válidos
            texto = FUENTE_LISTA.render(
                f"Nodo {nodo.get_id()}: g={int(nodo.g)}, h={int(nodo.h)}, f={int(nodo.f)}", 
                True, NEGRO
            )
            ventana.blit(texto, (x_pos, y_pos))
            y_pos += 25
            # Pasar a la siguiente columna si llegamos al final
            if y_pos > max_y:
                y_pos = altura_grid + 40
                x_pos += 250
                # Si nos salimos del ancho de la ventana, parar
                if x_pos > ancho // 2 - 20:
                    break
    
    # Título de lista cerrada
    titulo_cerrada = FUENTE_LISTA.render("Lista Cerrada:", True, NEGRO)
    ventana.blit(titulo_cerrada, (ancho // 2 + 20, altura_grid + 10))
    
    # Elementos de lista cerrada
    y_pos = altura_grid + 40
    x_pos = ancho // 2 + 20
    
    # Ordenar lista cerrada por orden de exploración (no importa tanto)
    for nodo in lista_cerrada:
        if nodo.f != float("inf"):  # Solo mostrar nodos con valores válidos
            texto = FUENTE_LISTA.render(
                f"Nodo {nodo.get_id()}: g={int(nodo.g)}, h={int(nodo.h)}, f={int(nodo.f)}", 
                True, NEGRO
            )
            ventana.blit(texto, (x_pos, y_pos))
            y_pos += 25
            # Pasar a la siguiente columna si llegamos al final
            if y_pos > max_y:
                y_pos = altura_grid + 40
                x_pos += 250
                # Si nos salimos del ancho de la ventana, parar
                if x_pos > ancho - 20:
                    break

def dibujar(ventana, grid, filas, ancho, lista_abierta=None, lista_cerrada=None):
    # Dibujar solo la cuadrícula primero
    ventana.fill(BLANCO)
    
    # Dibujar nodos de la cuadrícula
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    # Dibujar líneas de la cuadrícula
    dibujar_grid(ventana, filas, ancho)
    
    # Dibujar listas si están disponibles
    if lista_abierta is not None and lista_cerrada is not None:
        dibujar_listas(ventana, lista_abierta, lista_cerrada, ancho, ancho)
    
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    x, y = pos
    col = x // ancho_nodo
    fila = y // ancho_nodo
    return fila, col

def main(ventana, ancho, alto):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True
    iniciado = False

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                
            # Si el algoritmo ya está corriendo, no permitir cambios
            if iniciado:
                continue
                
            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                if pos[1] < ancho:  # Asegurarse de que el clic es en la cuadrícula
                    fila, col = obtener_click_pos(pos, FILAS, ancho)
                    if fila < FILAS and col < FILAS:  # Verificar que está dentro de la cuadrícula
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
                if pos[1] < ancho:  # Asegurarse de que el clic es en la cuadrícula
                    fila, col = obtener_click_pos(pos, FILAS, ancho)
                    if fila < FILAS and col < FILAS:  # Verificar que está dentro de la cuadrícula
                        nodo = grid[fila][col]
                        nodo.restablecer()
                        if nodo == inicio:
                            inicio = None
                        elif nodo == fin:
                            fin = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not iniciado and inicio and fin:
                    # Reiniciar valores para nodos que no son muros, inicio o fin
                    for fila in grid:
                        for nodo in fila:
                            if not (nodo.es_muro or nodo.es_nodo_inicio or nodo.es_nodo_fin):
                                nodo.restablecer()
                    
                    # Actualizar vecinos
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    
                    # Iniciar algoritmo - USANDO LAMBDA BIEN CONFIGURADO
                    iniciado = True
                    algoritmo_a_star(
                        lambda lista_abierta=None, lista_cerrada=None: dibujar(ventana, grid, FILAS, ancho, lista_abierta, lista_cerrada),
                        grid, inicio, fin
                    )
                    iniciado = False
                    
                if event.key == pygame.K_c:
                    # Limpiar todo
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA, ALTO_VENTANA)