# Instala ggplot2 si no está instalado
# install.packages("ggplot2")

# Carga la biblioteca ggplot2
library(ggplot2)

# Configura la semilla para reproducibilidad
set.seed(123)

# Genera datos aleatorios crecientes para el primer conjunto
n1 <- 8
x1 <- seq(10, 40, length.out = n1)
y1 <- sort(runif(n1, -6505, -3632.15))

# Genera datos aleatorios crecientes para el segundo conjunto
n2 <- 8
x2 <- seq(10, 40, length.out = n2)
y2 <- sort(runif(n2, -6613.2, -5412.3))

# Combina ambos conjuntos de datos en un único marco de datos
datos <- data.frame(
  x = c(x1, x2),
  y = c(y1, y2),
  grupo = rep(c("cantidad de población", "cantidad de generaciones"), c(n1, n2))
)

# Crea la gráfica utilizando ggplot2
ggplot(datos, aes(x, y, color = grupo)) +
  geom_line() +
  labs(
    title = "Rendimiento por parámetro",
    x = "Eje X",
    y = "-sd"
  ) +
  scale_color_manual(values = c("cantidad de población" = "blue", "cantidad de generaciones" = "red"))

