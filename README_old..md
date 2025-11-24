# Trabajo Final - Fase 1:

---

## **plataforma** 
 
## Catalogo
### catálogo (tda)
- series [tda,]
- películas [tda,]
- documentales [tda,]
---

> Cada uno de los elementos del catálogo cuenta con una serie de etiquetas que permiten saber el nivel del género (comedia, acción, terror, etc), los niveles pueden ser 
> - bajo,
> - medio, 
> - alto 

y palabras claves que describen el contenido.

---

## Documentales
#### Documental (TDA)
- nombre :str, 
- etiquetas: dict , 
- palabras claves: set, 
- duración: int, 
- fecha: str, 
- director: str.
- año: int, 
- produccion: str,

## Peliculas
#### Película (TDA)
- nombre: str, 
- director: str, 
- actorxs (considerar todos los actorxs que aparecen en la misma): set, 
- año: int 
- producción: string
- etiquetas (genero- nivel): dict
- palabras claves :set

## Series
#### Serie (TDA)
De las series se conoce 
- nombre:string
- género:string
- etiquetas (genero- nivel): dict 
- palabras claves: set 
- temporadas: dict o list
    - TDA Temporada o No TDa
        id: str
        numero:int
        capitulos: dict o list
        año: int 
        produccion: string
        - TDA Capitulo o no TDA
            id: string
            titulo: string
            duracion: int
---

## Clientes
### Cliente (TDA)
También se desea modelar los clientes a los cuales se le brinda el servicio, 
de cada cliente de conoce:
- nombre : string
- apellido,: string
- NRO cliente, : string
- preferencias (TDA preferencia) :list or dict (TDA O NO TDA)
    - género,
        - preferencia (porcentaje que permite determinar el nivel de preferencia) 
    - actor, 
        - preferencia (porcentaje que permite determinar el nivel de preferencia)
    - director 
        - preferencia (porcentaje que permite determinar el nivel de preferencia)
- tipo de servicio que consume (premium, etc.): string
- fecha de alta : string
- fecha de baja.: string

---

## Fecha de entrega
-   28 de noviembre del 2025

---

## Forma de presentación del TF
Se debe entregar Informe del TF en archivo en formato (Word, OpenOffice, LibreOffice)
que contenga la explicación del programa con:

-   Carátula y presentación: datos de la materia, alumno, profesor, fecha, etc.
-   Utilizar índices en el documento a entregar
-   Descripción del proyecto a realizar (enunciado del trabajo práctico)
-   Describir los datos, tipos de datos que se van a utilizar en el TF.




pandoc C:\Users\fames\DevSpace\Unab\estructuras\tpf\INFORME.md -o C:\Users\fames\DevSpace\Unab\estructuras\tpf\INFORME.pdf --pdf-engine=xelatex -V mainfont="Helvetica" -V geometry:margin=2cm